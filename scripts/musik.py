"""Synthetischer Beat für Videos ohne Stimme (lizenzfrei, lokal erzeugt).

  from musik import beat
  m = beat(30.0, pausen=[(20, 22)])   # numpy-Array, 44,1 kHz mono
Am–F–C–G, 120 BPM: Kick, Clap, Hi-Hats, Bass, Pad, Pluck-Arpeggio, Riser vor jedem Drop, Crash beim Drop.
In den Pausen (Breakdown) laufen nur Pad + Riser.
"""
import numpy as np
from scipy.signal import butter, lfilter, sawtooth

SR = 44100
AKKORDE = [(110.0, [220.0, 261.63, 329.63]), (87.31, [174.61, 220.0, 261.63]),
           (65.41, [261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66])]


def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def _filt(x, f, art="low"):
    b, a = butter(2, f / (SR / 2), art)
    return lfilter(b, a, x)


def _add(out, s, t):
    i = int(t * SR)
    if i >= len(out):
        return
    out[i: i + len(s)] += s[: len(out) - i]


def beat(dauer, bpm=120, pausen=(), seed=3):
    rng = np.random.default_rng(seed)
    n = int(dauer * SR)
    drums, bass, pad, arp, fx = (np.zeros(n) for _ in range(5))
    sb = 60 / bpm
    leise = lambda t: any(a <= t < b for a, b in pausen)  # noqa: E731

    kick = np.sin(2 * np.pi * np.cumsum(np.geomspace(160, 42, int(0.35 * SR))) / SR) * _env(int(0.35 * SR), 0.002, 0.16)
    clap = _filt(rng.standard_normal(int(0.2 * SR)), 1500, "high") * _env(int(0.2 * SR), 0.002, 0.06)
    hat = _filt(rng.standard_normal(int(0.05 * SR)), 7000, "high") * _env(int(0.05 * SR), 0.001, 0.015)

    duck = np.ones(n)  # Sidechain: nach jeder Kick kurz leiser
    k = 0
    while k * sb < dauer:
        t = k * sb
        if not leise(t):
            _add(drums, kick, t)
            if k % 2 == 1:
                _add(drums, 0.45 * clap, t)
            _add(drums, 0.22 * hat, t + sb / 2)
            if k % 4 == 3:
                _add(drums, 0.15 * hat, t + sb * 0.75)
            i = int(t * SR)
            m = min(int(0.25 * SR), n - i)
            duck[i: i + m] = np.minimum(duck[i: i + m], 1 - 0.65 * np.exp(-np.arange(m) / SR / 0.08))
        k += 1

    takt = 4 * sb
    for j in range(int(np.ceil(dauer / takt))):
        root, akk = AKKORDE[j % 4]
        t0 = j * takt
        L = min(int(takt * SR), n - int(t0 * SR))
        if L <= 0:
            break
        tt = np.arange(L) / SR
        p = sum(sawtooth(2 * np.pi * f * d * tt) for f in akk for d in (0.997, 1.003)) / 6
        p *= np.minimum(1, tt / 0.15) * np.minimum(1, (takt - tt) / 0.1)
        _add(pad, _filt(p, 1400), t0)
        for e in range(8):  # Bass in Achteln
            te = t0 + e * sb / 2
            if leise(te):
                continue
            L2 = int(sb / 2 * SR * 0.9)
            t2 = np.arange(L2) / SR
            b = np.sin(2 * np.pi * root * t2) + 0.35 * sawtooth(2 * np.pi * root * t2)
            _add(bass, _filt(b, 600) * _env(L2, 0.005, 0.18), te)
        tonfolge = [akk[0] * 2, akk[1] * 2, akk[2] * 2, akk[1] * 2]
        for e in range(16):  # Pluck in Sechzehnteln
            te = t0 + e * sb / 4
            if leise(te):
                continue
            L3 = int(0.18 * SR)
            t3 = np.arange(L3) / SR
            f = tonfolge[e % 4]
            s = sawtooth(2 * np.pi * f * t3, 0.5) * _env(L3, 0.002, 0.07)
            _add(arp, s * (1.0 if e % 4 == 0 else 0.6), te)

    for a, b in pausen:  # Riser in der Pause, Crash beim Drop
        L = int((b - a) * SR)
        r = rng.standard_normal(L)
        fr = np.linspace(400, 9000, L)
        y = np.zeros(L)
        for s0 in range(0, L, 2048):  # Filter-Sweep blockweise
            y[s0: s0 + 2048] = _filt(r[s0: s0 + 2048], fr[s0], "high")
        _add(fx, 0.35 * y * np.linspace(0, 1, L) ** 2, a)
        cr = _filt(rng.standard_normal(int(1.6 * SR)), 4000, "high") * _env(int(1.6 * SR), 0.002, 0.5)
        _add(fx, 0.4 * cr, b)
        _add(drums, 1.2 * kick, b)

    out = 0.9 * drums + 0.55 * bass * duck + 0.22 * pad * (0.5 + 0.5 * duck) + 0.12 * _filt(arp, 3000) * duck + fx
    fade = np.minimum(1, (n - np.arange(n)) / (1.2 * SR))
    out *= fade
    return out / (np.abs(out).max() + 1e-9) * 0.9
