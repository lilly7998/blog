"""US dollar dashboard: FRED public data, cached in Postgres (or memory)."""
import csv, io, json, os, time, threading, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
START = "2015-01-01"
TTL = 6 * 3600
KEY = "usd"
HERE = os.path.dirname(os.path.abspath(__file__))

# name: (FRED id, transform)
SERIES = {
    "dxy":      ("DTWEXBGS", "monthly_avg"),   # nominal broad dollar index
    "dxy_d":    ("DTWEXBGS", "last_only"),
    "cny":      ("EXCHUS", None),              # CNY per USD, monthly avg
    "jpy":      ("EXJPUS", None),              # JPY per USD, monthly avg
    "eur":      ("EXUSEU", None),              # USD per EUR, monthly avg
    "t2":       ("GS2", None),
    "t10":      ("GS10", None),
    "t30":      ("GS30", None),
    "t10_d":    ("DGS10", "last_only"),
    "t2_d":     ("DGS2", "last_only"),
    "curve":    ("T10Y2Y", "monthly_avg"),
    "fed_hi":   ("DFEDTARU", "monthly_last"),
    "fed_lo":   ("DFEDTARL", "monthly_last"),
    "effr":     ("FEDFUNDS", None),
    "nfp":      ("PAYEMS", "diff"),
    "unrate":   ("UNRATE", None),
    "cpi":      ("CPIAUCSL", "yoy"),
    "core_cpi": ("CPILFESL", "yoy"),
    "pce":      ("PCEPI", "yoy"),
    "core_pce": ("PCEPILFE", "yoy"),
    "retail":   ("RSAFS", "yoy"),
    "spend":    ("PCE", "yoy"),
    "sent":     ("UMCSENT", None),
    "gdp":      ("A191RL1Q225SBEA", "quarter"),
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
                r = c.execute("SELECT v, ts FROM cache WHERE k=%s", (KEY,)).fetchone()
                return (r[0], r[1]) if r else (None, 0)
        except Exception as e:
            print("db read failed:", e)
    return _mem.get(KEY, (None, 0))


def cache_put(v):
    ts = time.time()
    _mem[KEY] = (v, ts)
    if DB:
        try:
            with _db() as c:
                c.execute("CREATE TABLE IF NOT EXISTS cache (k text primary key, v jsonb, ts double precision)")
                c.execute("INSERT INTO cache VALUES (%s, %s, %s) ON CONFLICT (k) DO UPDATE SET v=EXCLUDED.v, ts=EXCLUDED.ts",
                          (KEY, json.dumps(v), ts))
        except Exception as e:
            print("db write failed:", e)


def get(url):
    # FRED rejects unfamiliar user agents, so present a plain curl one.
    last = None
    for _ in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0", "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode()
        except Exception as e:
            last = e
            time.sleep(1)
    raise last


def fetch(sid, mode):
    start = {"yoy": "2014-01-01", "diff": "2014-11-01", "monthly_last": "2013-01-01"}.get(mode, START)
    if mode == "last_only":
        start = (dt.date.today() - dt.timedelta(days=30)).isoformat()
    rows = csv.reader(io.StringIO(get(f"{FRED}{sid}&cosd={start}")))
    next(rows)
    return [(d, float(v)) for d, v in rows if v not in ("", ".")]


def months_until_now(first):
    y, m = map(int, first.split("-"))
    now = dt.date.today()
    while (y, m) <= (now.year, now.month):
        yield f"{y:04d}-{m:02d}"
        m += 1
        if m > 12:
            y, m = y + 1, 1


def transform(pts, mode):
    if mode == "last_only":
        return pts[-1:]
    if mode == "monthly_last":   # step series carried forward to this month
        out = {d[:7]: v for d, v in pts}
        if not out:
            return []
        res, cur = [], None
        for k in months_until_now(min(out)):
            cur = out.get(k, cur)
            if k >= START[:7]:
                res.append((k, cur))
        return res
    if mode == "monthly_avg":
        acc = {}
        for d, v in pts:
            acc.setdefault(d[:7], []).append(v)
        return [(k, round(sum(v) / len(v), 4)) for k, v in sorted(acc.items())]
    m = {d[:7]: v for d, v in pts}
    if mode == "yoy":
        out = []
        for k, v in sorted(m.items()):
            y, mo = k.split("-")
            p = m.get(f"{int(y)-1}-{mo}")
            if p and k >= START[:7]:
                out.append((k, round((v / p - 1) * 100, 2)))
        return out
    if mode == "diff":
        ks = sorted(m)
        return [(k, round(m[k] - m[ks[i - 1]], 1)) for i, k in enumerate(ks) if i and k >= START[:7]]
    if mode == "quarter":
        return [(f"{d[:4]}-Q{(int(d[5:7]) - 1) // 3 + 1}", v) for d, v in pts]
    return [(d[:7], v) for d, v in pts]


def build():
    data, errors = {}, []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {n: ex.submit(lambda s=s, md=md: transform(fetch(s, md), md)) for n, (s, md) in SERIES.items()}
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
        if v and fresh["errors"]:
            for k, pts in v["series"].items():
                fresh["series"].setdefault(k, pts)
        if fresh["series"]:
            cache_put(fresh)
            return fresh
        return v or fresh


app = FastAPI(docs_url=None, redoc_url=None)
# The blog homepage (wyz.name) reads /api/data for its data strip.
app.add_middleware(CORSMiddleware, allow_origins=["https://wyz.name", "https://www.wyz.name", "http://localhost:1313"], allow_methods=["GET"])
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
