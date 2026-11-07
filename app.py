"""Euro area dashboard: ECB + FRED public data, cached in Postgres (or memory)."""
import csv, io, json, os, time, threading, urllib.request, datetime as dt
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

ECB = "https://data-api.ecb.europa.eu/service/data/"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
START = "2015-01-01"
TTL = 6 * 3600
HERE = os.path.dirname(os.path.abspath(__file__))

SERIES = {
    "dfr":    ("ecb", "FM/B.U2.EUR.4F.KR.DFR.LEV", "monthly_last"),
    "mro":    ("ecb", "FM/B.U2.EUR.4F.KR.MRR_FR.LEV", "monthly_last"),
    "hicp":   ("ecb", "HICP/M.U2.N.000000.4D0.ANR", None),
    "core":   ("ecb", "HICP/M.U2.N.XEF000.4D0.ANR", None),
    "y_de":   ("ecb", "IRS/M.DE.L.L40.CI.0000.EUR.N.Z", None),
    "y_fr":   ("ecb", "IRS/M.FR.L.L40.CI.0000.EUR.N.Z", None),
    "y_it":   ("ecb", "IRS/M.IT.L.L40.CI.0000.EUR.N.Z", None),
    "y_es":   ("ecb", "IRS/M.ES.L.L40.CI.0000.EUR.N.Z", None),
    "eurusd": ("ecb", "EXR/M.USD.EUR.SP00.A", None),
    "eurusd_d": ("ecb", "EXR/D.USD.EUR.SP00.A", "last_only"),
    "fed":    ("fred", "DFEDTARU", "monthly_last"),
    "us_cpi": ("fred", "CPIAUCSL", "yoy"),
    "us_core": ("fred", "CPILFESL", "yoy"),
    "ust10":  ("fred", "GS10", None),
}

_mem = {}
_lock = threading.Lock()
DB = os.environ.get("DATABASE_URL")


def _db():
    import psycopg
    return psycopg.connect(DB, autocommit=True, connect_timeout=5)


def cache_get():
    if DB:
        try:
            with _db() as c:
                c.execute("CREATE TABLE IF NOT EXISTS cache (k text primary key, v jsonb, ts double precision)")
                r = c.execute("SELECT v, ts FROM cache WHERE k='data'").fetchone()
                return (r[0], r[1]) if r else (None, 0)
        except Exception as e:
            print("db read failed:", e)
    return _mem.get("data", (None, 0))


def cache_put(v):
    ts = time.time()
    _mem["data"] = (v, ts)
    if DB:
        try:
            with _db() as c:
                c.execute("CREATE TABLE IF NOT EXISTS cache (k text primary key, v jsonb, ts double precision)")
                c.execute("INSERT INTO cache VALUES ('data', %s, %s) ON CONFLICT (k) DO UPDATE SET v=EXCLUDED.v, ts=EXCLUDED.ts",
                          (json.dumps(v), ts))
        except Exception as e:
            print("db write failed:", e)


def get(url):
    # FRED rejects unfamiliar user agents, so present a plain curl one.
    last = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0", "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode()
        except Exception as e:
            last = e
            time.sleep(1)
    raise last


def fetch_ecb(key, mode):
    # Rate series only list change dates, so start early enough to have a value in force at START.
    start = "2013-01-01" if mode == "monthly_last" else START
    q = "lastNObservations=1&" if mode == "last_only" else f"startPeriod={start}&"
    rows = csv.DictReader(io.StringIO(get(f"{ECB}{key}?{q}format=csvdata")))
    return [(r["TIME_PERIOD"], float(r["OBS_VALUE"])) for r in rows if r["OBS_VALUE"]]


def fetch_fred(sid, mode):
    start = "2014-01-01" if mode == "yoy" else ("2013-01-01" if mode == "monthly_last" else START)
    rows = csv.reader(io.StringIO(get(f"{FRED}{sid}&cosd={start}")))
    next(rows)
    return [(d, float(v)) for d, v in rows if v not in ("", ".")]


def monthly_last(pts):
    """Last value per month, carried forward to the current month (rates are step series)."""
    out = {}
    for d, v in pts:
        out[d[:7]] = v
    if not out:
        return []
    keys = sorted(out)
    y, m = map(int, keys[0].split("-"))
    now = dt.date.today()
    res, cur = [], None
    while (y, m) <= (now.year, now.month):
        k = f"{y:04d}-{m:02d}"
        cur = out.get(k, cur)
        if k >= START[:7]:
            res.append((k, cur))
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return res


def yoy(pts):
    m = {d[:7]: v for d, v in pts}
    out = []
    for k, v in sorted(m.items()):
        y, mo = k.split("-")
        prev = f"{int(y)-1}-{mo}"
        if prev in m and k >= START[:7]:
            out.append((k, round((v / m[prev] - 1) * 100, 2)))
    return out


def one(name, src, key, mode):
    pts = fetch_ecb(key, mode) if src == "ecb" else fetch_fred(key, mode)
    if mode == "monthly_last":
        return monthly_last(pts)
    if mode == "yoy":
        return yoy(pts)
    return [(d[:10] if mode == "last_only" else d[:7], v) for d, v in pts]


def build():
    from concurrent.futures import ThreadPoolExecutor
    data, errors = {}, []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {n: ex.submit(one, n, *spec) for n, spec in SERIES.items()}
    for name, f in futs.items():
        try:
            data[name] = f.result()
        except Exception as e:
            errors.append(f"{name}: {e}")
    return {"series": data, "errors": errors, "updated": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}


def load():
    v, ts = cache_get()
    if v and time.time() - ts < TTL:
        return v
    with _lock:
        v2, ts2 = cache_get()
        if v2 and time.time() - ts2 < TTL:
            return v2
        fresh = build()
        if v and fresh["errors"]:  # keep old values for any series that failed
            for k, pts in v["series"].items():
                fresh["series"].setdefault(k, pts)
        if fresh["series"]:
            cache_put(fresh)
            return fresh
        return v or fresh


app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")


@app.get("/api/data")
def api_data():
    d = dict(load())
    d["meetings"] = json.load(open(os.path.join(HERE, "meetings.json")))
    return JSONResponse(d, headers={"Cache-Control": "public, max-age=600"})


@app.get("/healthz")
def health():
    return {"ok": True}


@app.get("/")
def index():
    return FileResponse(os.path.join(HERE, "static", "index.html"))
