"""Build cached dashboard data for the blog (run by GitHub Actions before hugo).

Pulls the same ECB/FRED series the euro and dollar dashboards use, by calling
their build() functions directly, so the blog never depends on the dashboards
being awake. A series that fails keeps its value from the copy already live on
wyz.name, so visitors always see the last good data.
"""
import importlib.util, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "data")
LIVE = "https://wyz.name/data/{}.json"
APPS = {"euro": "dashboard", "usd": "usd"}


def load_app(name, folder):
    spec = importlib.util.spec_from_file_location(f"{name}_app", os.path.join(ROOT, folder, "app.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def previous(name):
    try:
        req = urllib.request.Request(LIVE.format(name), headers={"User-Agent": "curl/8.5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print(f"{name}: no previous copy ({e})")
        return None


def main():
    os.environ.pop("DATABASE_URL", None)
    os.makedirs(OUT, exist_ok=True)
    ok = 0
    for name, folder in APPS.items():
        old = previous(name)
        try:
            mod = load_app(name, folder)
            d = mod.build()
            d["meetings"] = json.load(open(os.path.join(ROOT, folder, "meetings.json")))
        except Exception as e:
            print(f"{name}: build failed: {e}")
            d = None
        if d and old:
            for k, pts in old.get("series", {}).items():
                if not d["series"].get(k):
                    d["series"][k] = pts
        if not d or not d.get("series"):
            d = old
        if not d:
            print(f"{name}: nothing to write")
            continue
        with open(os.path.join(OUT, f"{name}.json"), "w") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
        ok += 1
        print(f"{name}: {len(d['series'])} series, updated {d.get('updated')}, errors {d.get('errors')}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
