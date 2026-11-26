#!/usr/bin/env python3
"""Produkt-Bild (weißer Hintergrund, 1–6 Ansichten) in einzelne freigestellte PNGs schneiden.
Aufruf: python3 scripts/produkte_schneiden.py <bild> <zielordner> name1 [name2 ...]  (Reihenfolge: Zeile für Zeile, links→rechts)"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

src, ziel, names = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
ziel.mkdir(parents=True, exist_ok=True)
im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(int)
weiss = (a.min(axis=2) > 232) & (a.max(axis=2) - a.min(axis=2) < 20)
lab, _ = nd.label(weiss)
rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
fg = ~np.isin(lab, list(rand))
grp, n = nd.label(nd.binary_dilation(fg, iterations=12))
size = nd.sum(fg, grp, range(1, n + 1))
best = [k + 1 for k in np.argsort(size)[::-1][:len(names)]]
objs = nd.find_objects(grp)
boxes = sorted(best, key=lambda k: (round(objs[k - 1][0].start / (a.shape[0] / 3)), objs[k - 1][1].start))
for k, name in zip(boxes, names):
    ys, xs = objs[k - 1]
    alpha = Image.fromarray(((fg & (grp == k)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.copy(); rgba.putalpha(alpha)
    t = rgba.crop((xs.start, ys.start, xs.stop, ys.stop)); t = t.crop(t.getbbox())
    t.save(ziel / f"{name}.png"); print(name, t.size)
