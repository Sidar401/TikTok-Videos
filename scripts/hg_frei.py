"""Freie (CC0/gemeinfrei) Hintergründe von Wikimedia Commons holen. Aufruf: hg_frei.py key=suchbegriff …"""
import json, time, sys, urllib.request, urllib.parse
UA = {"User-Agent": "HundeFinanzTv-Video/1.0 (editorial use)"}
API = "https://commons.wikimedia.org/w/api.php?"
Z = "/home/user/TikTok-Videos/brand/hintergruende/"
Q = json.load(open(Z + "quellen.json"))
def get(p):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(p), headers=UA), timeout=60))
        except Exception as e: print("warte", e, flush=True); time.sleep(25 * (i + 1))
benutzt = {v["datei"] for v in Q.values()}
for a in sys.argv[1:]:
    key, q = a.split("=", 1); key = "frei-" + key
    if key + ".jpg" in Q: continue
    ok = False
    for such in (q + " unsplash", q):
        d = get({"action": "query", "generator": "search", "gsrnamespace": 6, "gsrsearch": such + " filetype:bitmap", "gsrlimit": 8, "prop": "imageinfo",
                 "iiprop": "url|extmetadata|size", "iiurlwidth": 1280, "format": "json"})
        time.sleep(40)
        if not d or "query" not in d: continue
        for p in sorted(d["query"]["pages"].values(), key=lambda x: x.get("index", 99)):
            ii = p["imageinfo"][0]; lic = ii["extmetadata"].get("LicenseShortName", {}).get("value", "")
            if not (lic.startswith("CC0") or lic.lower().startswith("public domain")) or ii["width"] < 1200 or p["title"] in benutzt: continue
            try:
                img = urllib.request.urlopen(urllib.request.Request(ii.get("thumburl") or ii["url"], headers=UA), timeout=120).read()
                import io; from PIL import Image
                im = Image.open(io.BytesIO(img)).convert("RGB"); im.thumbnail((1600, 1600)); b = io.BytesIO(); im.save(b, "JPEG", quality=88); img = b.getvalue()
            except Exception as e: print("bild", e, flush=True); time.sleep(90); continue
            open(Z + key + ".jpg", "wb").write(img); benutzt.add(p["title"])
            Q[key + ".jpg"] = {"datei": p["title"], "lizenz": lic, "urheber": "", "einblenden": "", "frei": True}
            json.dump(Q, open(Z + "quellen.json", "w"), ensure_ascii=False, indent=1)
            print(key, "→", p["title"], lic, flush=True); ok = True; break
        if ok: break
    if not ok: print("NICHTS", key, flush=True)
    time.sleep(60)
