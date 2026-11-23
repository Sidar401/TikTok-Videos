#!/usr/bin/env python3
"""Bild-Bogen mit N Gegenständen in EINER Reihe ausschneiden (Trennung an den leersten Spalten).
Aufruf: python3 hundewissen/reihe_schneiden.py <bogen.png> <zielordner> name1 name2 ..."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

src, ziel, names = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
ziel.mkdir(parents=True, exist_ok=True)
im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(int)
weiss = (a.min(axis=2) > 236) & (a.max(axis=2) - a.min(axis=2) < 18)
lab, _ = nd.label(weiss)
rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(rand)); fg = ~bg
spalte = fg.sum(axis=0).astype(float); W = len(spalte); n = len(names)
cuts = [0]
for k in range(1, n):  # Schnitt nahe k*W/n an der leersten Spalte
    lo, hi = int(W * (k - 0.45) / n), int(W * (k + 0.45) / n)
    lo = max(lo, cuts[-1] + 20)
    cuts.append(lo + int(np.argmin(spalte[lo:hi])))
cuts.append(W)
for (x0, x1), name in zip(zip(cuts, cuts[1:]), names):
    m = np.zeros_like(fg); m[:, x0:x1] = fg[:, x0:x1]
    alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.copy(); rgba.putalpha(alpha)
    t = rgba.crop(rgba.getbbox()); t.save(ziel / f"{name}.png"); print(name, t.size)
