# bootstrap_requests.py — run once: python bootstrap_requests.py
import io, json, os, urllib.request, zipfile

PKGS = ["requests", "urllib3", "certifi", "charset-normalizer", "idna"]
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
os.makedirs(DEST, exist_ok=True)

def wheel_url(pkg):
    with urllib.request.urlopen(f"https://pypi.org/pypi/{pkg}/json") as r:
        data = json.load(r)
    # prefer a pure-python (py3-none-any) wheel; fall back to first wheel
    urls = data["urls"]
    for u in urls:
        if u["packagetype"] == "bdist_wheel" and "py3-none-any" in u["filename"]:
            return u["url"]
    for u in urls:
        if u["packagetype"] == "bdist_wheel":
            return u["url"]
    raise RuntimeError(f"no wheel for {pkg}")

for pkg in PKGS:
    url = wheel_url(pkg)
    print("fetching", url.split("/")[-1])
    with urllib.request.urlopen(url) as r:
        buf = io.BytesIO(r.read())
    with zipfile.ZipFile(buf) as z:
        for name in z.namelist():
            # skip the .dist-info metadata dirs, keep the package code
            if ".dist-info/" in name:
                continue
            z.extract(name, DEST)

print("done ->", DEST)
