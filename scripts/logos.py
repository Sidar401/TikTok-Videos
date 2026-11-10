#!/usr/bin/env python3
"""Echte Firmen-/Institutions-Logos holen (Nutzer 10.11.: „immer die echten Logos, professioneller“).

  python3 scripts/logos.py ezb nvidia …            → brand/logos/<name>.svg|png (Cache, einmal laden reicht)
  python3 scripts/logos.py --datei <name> <Commons-Dateiname>   (neues Logo hinzufügen)
Quelle: Wikimedia Commons (Special:FilePath, keine API → kein Rate-Limit). Nur redaktionell zeigen,
nie so, als wären die Firmen Partner/Sponsoren. Im Video: `logo_img("assets/logos/ezb.svg", …)` aus glow_teile
bzw. die Datei nach videos/<name>/assets/logos/ kopieren.
"""
import json
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIEL = ROOT / "brand/logos"
LISTE = ZIEL / "quellen.json"
BEKANNT = {
    "ezb": "Logo_European_Central_Bank.svg",
    "nvidia": "Nvidia_logo.svg",
    "amd": "AMD_Logo.svg",
    "microsoft": "Microsoft_logo_(2012).svg",
    "apple": "Apple_logo_black.svg",
    "openai": "OpenAI_Logo.svg",
    "oracle": "Oracle_logo.svg",
    "tesla": "Tesla_Motors.svg",
    "amazon": "Amazon_logo.svg",
    "google": "Google_2015_logo.svg",
    "meta": "Meta_Platforms_Inc._logo.svg",
    "klarna": "Klarna_Payment_Badge.svg",
    "paypal": "PayPal.svg",
    "bundesbank": "Deutsche_Bundesbank_logo.svg",
    "dax": "DAX_Logo.svg",
    "spacex": "SpaceX-Logo.svg",
}


def hole(name, datei=None):
    quellen = json.loads(LISTE.read_text()) if LISTE.exists() else {}
    datei = datei or quellen.get(name) or BEKANNT.get(name)
    if not datei:
        raise SystemExit(f"Unbekannt: {name} – mit --datei <name> <Commons-Dateiname> hinzufügen")
    endung = Path(datei).suffix.lower()
    ziel = ZIEL / f"{name}{endung}"
    if ziel.exists():
        return ziel
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(datei)
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    daten = urllib.request.urlopen(r, timeout=60).read()
    if daten[:200].lower().find(b"<html") >= 0:
        raise SystemExit(f"Nicht gefunden auf Commons: {datei}")
    ZIEL.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(daten)
    quellen[name] = datei
    LISTE.write_text(json.dumps(quellen, indent=1, ensure_ascii=False))
    return ziel


def kopiere(namen, video_ordner):
    z = Path(video_ordner) / "assets/logos"
    z.mkdir(parents=True, exist_ok=True)
    return {n: f"assets/logos/{shutil.copy(hole(n), z / hole(n).name) and hole(n).name}" for n in namen}


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--datei":
        print(hole(a[1], a[2]))
    else:
        for n in a:
            try:
                print(n, "→", hole(n))
            except SystemExit as e:
                print(n, "FEHLER", e)
