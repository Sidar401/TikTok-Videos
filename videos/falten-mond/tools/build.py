"""Falt-Zeiten, Meilensteine, Ton. Schreibt assets/data.js + assets/sfx.wav"""
import json, os, subprocess, wave, math
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = os.path.join(ROOT, "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx")
P = 1e-4  # Papierdicke 0,1 mm
LY = 9.4607e15

# Faltzeiten
T = [None]
t = 2.3
for k in range(1, 43):
    T.append(round(t, 4)); t += 0.44 - 0.16 * (k - 1) / 41
T42 = T[42]
t = 20.6
for k in range(43, 104):
    T.append(round(t, 4)); t += 0.16 - 0.11 * (k - 43) / 60
print("Falte 42 bei", T42, " Falte 103 bei", T[103])

def de(x, d=0):
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s
def fmt(m):
    if m < 0.01: return de(m * 1000, 1) + " mm"
    if m < 1: return de(m * 100, 1 if m < 0.1 else 0) + " cm"
    if m < 1000: return de(m, 1 if m < 10 else 0) + " m"
    if m < 1e9: return de(m / 1000, 1 if m < 1e4 else 0) + " km"
    if m < 1e15: return de(m / 1e9, 0 if m >= 1e10 else 1) + " Mio. km"
    ly = m / LY
    if ly < 1e6: return de(ly, 1 if ly < 10 else 0) + " Lichtjahre"
    if ly < 1e9: return de(ly / 1e6, 1) + " Mio. Lichtjahre"
    return de(ly / 1e9, 0) + " Mrd. Lichtjahre"
labels = [fmt(P * 2 ** n) for n in range(0, 104)]

# Vergleiche: (art, name, höhe in m, Spruch)
objs = [
 ("dice", "Würfel", 0.016, ""),
 ("mug", "Tasse", 0.095, ""),
 ("cat", "Katze", 0.30, "Schon größer als eine Katze!"),
 ("you", "Du", 1.75, "Jetzt größer als DU!"),
 ("giraffe", "Giraffe", 5.5, ""),
 ("house", "Haus", 10, ""),
 ("pisa", "Turm von Pisa", 57, ""),
 ("eiffel", "Eiffelturm", 330, ""),
 ("burj", "Burj Khalifa", 828, "Höher als der Burj Khalifa!"),
 ("everest", "Mount Everest", 8849, "Über dem Mount Everest!"),
 ("space", "Weltall", 100000, "Hallo, Weltall!"),
 ("iss", "Raumstation", 420000, ""),
 ("earth", "Erde", 12742000, "Dicker als die ganze Erde!"),
]
OBJ = []
for kind, name, h, quip in objs:
    n = math.ceil(math.log2(h / P))  # erste Faltung über dem Objekt
    OBJ.append(dict(kind=kind, name=name, h=h, hl=fmt(h), n=n, t=T[n], quip=quip))
    print(f"{name:14s} {fmt(h):>14s} überholt bei Falte {n} ({fmt(P*2**n)}) t={T[n]}")
far = [
 ("sun", "Sonne", 1.496e11), ("star", "Nächster Stern", 4.24 * LY),
 ("milky", "Milchstraße", 1e5 * LY), ("andro", "Andromeda", 2.5e6 * LY), ("uni", "Universum", 93e9 * LY),
]
FAR = []
for kind, name, h in far:
    n = math.ceil(math.log2(h / P))
    FAR.append(dict(kind=kind, name=name, h=h, hl=fmt(h), n=n, t=T[n]))
    print(f"{name:14s} {fmt(h):>20s} Falte {n} t={T[n]}")

with open(os.path.join(ROOT, "assets", "data.js"), "w") as f:
    f.write("window.FALT = " + json.dumps(dict(T=T, labels=labels, objs=OBJ, far=FAR, P=P, moon=384400000, T42=T42), ensure_ascii=False) + ";\n")

# ---------- Ton ----------
SR, DUR = 44100, 30.0
def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SFX, name), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()
cache = {}
def snd(name):
    if name not in cache: cache[name] = load(name)
    return cache[name]
def pitch(a, semis):
    r = 2 ** (semis / 12)
    idx = np.arange(0, len(a) - 1, r)
    return np.interp(idx, np.arange(len(a)), a)
buf = np.zeros(int(SR * (DUR + 12)))
def put(a, t, vol=1.0):
    i = int(t * SR); buf[i:i + len(a)] += a * vol

# Einstieg
put(snd("whoosh-short.mp3"), 0.0, 0.6)
for i, tt in enumerate([0.55, 0.95, 1.35]): put(pitch(snd("pop.mp3"), i * 3), tt, 0.8)
# Faltungen: aufsteigende Tonleiter
pent = [0, 2, 4, 7, 9]
for k in range(1, 104):
    deg = k - 1
    semis = pent[deg % 5] + 12 * ((deg // 5) % 2) - 4
    if k <= 42:
        put(pitch(snd("pop.mp3"), semis), T[k] + 0.02, 0.55)
    else:
        put(pitch(snd("click-soft.mp3"), semis + 5), T[k] + 0.02, 0.35)
# Meilensteine: kleiner Glanz
for o in OBJ:
    if o["quip"]: put(snd("sparkle.mp3"), o["t"] + 0.05, 0.25)
# Mond
put(snd("riser.mp3")[int(6.5 * SR):], T42 - 3.5, 0.45)
put(snd("impact-bass-1.mp3"), T42 + 0.03, 1.0)
put(snd("chime.mp3"), T42 + 0.1, 0.35)
# Warp
put(snd("whoosh-cinematic.mp3"), 20.4, 0.7)
put(snd("riser.mp3")[int(3.5 * SR):], T[103] - 6.5, 0.4)
put(snd("impact-bass-2.mp3"), T[103] + 0.03, 1.0)
put(snd("glitch-1.mp3")[: int(0.6 * SR)], T[103] + 0.05, 0.25)
put(snd("pop.mp3"), 28.1, 0.7)
buf = buf[: int(SR * DUR)]
fade = int(0.3 * SR); buf[-fade:] *= np.linspace(1, 0, fade)
buf = buf / np.max(np.abs(buf)) * 0.89
with wave.open(os.path.join(ROOT, "assets", "sfx.wav"), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype(np.int16).tobytes())
print("Ton ok")
