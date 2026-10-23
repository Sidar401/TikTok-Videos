"""Untertitel-Text aus dem Sprechtext: deutsche Zahlwörter -> Ziffern ("dreihundert Euro" -> "300 €").

Kleine Zahlen (< 13) bleiben als Wort, außer vor Euro/Prozent ("zehn Euro" -> "10 €", aber "drei Jahre" bleibt).
Aufruf: python3 scripts/zahlen.py videos/<name>/skript.json  -> setzt "text" jedes Satzes neu.
"""
import json
import re
import sys

EINER = {"ein": 1, "eins": 1, "eine": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9}
TEENS = {"zehn": 10, "elf": 11, "zwölf": 12, "dreizehn": 13, "vierzehn": 14, "fünfzehn": 15, "sechzehn": 16, "siebzehn": 17,
         "achtzehn": 18, "neunzehn": 19}
ZEHNER = {"zwanzig": 20, "dreißig": 30, "vierzig": 40, "fünfzig": 50, "sechzig": 60, "siebzig": 70, "achtzig": 80, "neunzig": 90}


def _unter100(w):
    if w in TEENS:
        return TEENS[w]
    if w in ZEHNER:
        return ZEHNER[w]
    if w in EINER and w != "eine":
        return EINER[w]
    if "und" in w:
        a, _, b = w.partition("und")
        if a in EINER and b in ZEHNER:
            return EINER[a] + ZEHNER[b]
    return None


def _unter1000(w):
    if "hundert" in w:
        a, _, b = w.partition("hundert")
        h = 1 if a in ("", "ein") else _unter100(a)
        r = 0 if b == "" else _unter100(b)
        return None if h is None or r is None or h > 9 and a not in TEENS else h * 100 + r
    return _unter100(w)


def wert(wort):
    """Zahlwort -> int, sonst None. Versteht z. B. 'dreiundzwanzigtausendvierhundert', 'zweieinhalbtausend'."""
    w = wort.lower()
    if w.startswith("zweieinhalbtausend") and w == "zweieinhalbtausend":
        return 2500
    if "tausend" in w:
        a, _, b = w.partition("tausend")
        t = 1 if a in ("", "ein") else _unter1000(a)
        r = 0 if b == "" else _unter1000(b)
        return None if t is None or r is None else t * 1000 + r
    return _unter1000(w)


def fmt(n):
    return f"{n:,}".replace(",", ".")


EINHEIT = {"Euro": " €", "Prozent": " %"}


def ziffern(text):
    tok = re.split(r"(\s+)", text)
    worte = [(i, t) for i, t in enumerate(tok) if t.strip()]
    out = list(tok)
    for k, (i, t) in enumerate(worte):
        m = re.match(r"^([A-Za-zäöüß]+?)(-?)([.,:;!?]*)$", t)
        if not m:
            continue
        n = wert(m.group(1))
        if n is None:
            continue
        nxt = re.sub(r"[.,:;!?]", "", worte[k + 1][1]) if k + 1 < len(worte) else ""
        prev = worte[k - 1][1].lower() if k else ""
        # "zwei- bis viertausend Euro" / "zehn bis zwanzig Prozent": Einheit hinter dem Bereich
        bereich_einheit = None
        if nxt == "bis" and k + 3 <= len(worte) and k + 2 < len(worte):
            n2 = wert(re.sub(r"[.,:;!?]", "", worte[k + 2][1]))
            unit = re.sub(r"[.,:;!?]", "", worte[k + 3][1]) if k + 3 < len(worte) else ""
            if n2 is not None and unit in EINHEIT:
                bereich_einheit = unit
                if m.group(2) == "-" and "tausend" in worte[k + 2][1]:
                    n *= 1000
        if prev in ("mehrere", "paar", "einige", "ein", "einem"):
            continue
        if nxt in EINHEIT or bereich_einheit or n >= 13:
            out[i] = fmt(n) + m.group(3)
    s = "".join(out)
    s = re.sub(r"(\d) (Euro|Prozent)\b", lambda x: x.group(1) + EINHEIT[x.group(2)], s)
    return re.sub(r"[.!]$", "", s)


if __name__ == "__main__":
    p = sys.argv[1]
    d = json.load(open(p))
    for s in d["saetze"]:
        s["text"] = ziffern(s["sprechtext"])
        print(s["id"], s["text"])
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
