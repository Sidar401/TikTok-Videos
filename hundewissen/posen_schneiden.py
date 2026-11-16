#!/usr/bin/env python3
"""Posen-Bogen (6 Posen auf Weiß) in einzelne freigestellte PNGs schneiden.
Aufruf: python3 hundewissen/posen_schneiden.py <bogen.png> name1 name2 ... (Reihenfolge: Zeile für Zeile, links→rechts)"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

src, names = sys.argv[1], sys.argv[2:]
im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(int)
weiss = (a.min(axis=2) > 236) & (a.max(axis=2) - a.min(axis=2) < 18)
# Hintergrund = Weiß, das mit dem Rand verbunden ist (weißes Fell innen bleibt)
lab, _ = nd.label(weiss)
rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(rand))
fg = nd.binary_closing(~bg, iterations=2)
fg = nd.binary_fill_holes(fg) & ~bg | (~bg)
H = a.shape[0] // 2
boxen = []
for r in range(2):  # zwei Zeilen à 3 Posen
    zeile = np.zeros_like(fg); zeile[r * H:(r + 1) * H] = fg[r * H:(r + 1) * H]
    grp, n = nd.label(nd.binary_dilation(zeile, iterations=6))
    groesse = nd.sum(zeile, grp, range(1, n + 1))
    beste = np.argsort(groesse)[::-1][:3] + 1
    bx = [(nd.find_objects((grp == k).astype(int))[0], grp == k) for k in beste]
    boxen += sorted(bx, key=lambda b: b[0][1].start)
for ((ys, xs), maske), name in zip(boxen, names):
    alpha = Image.fromarray(((fg & maske) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.copy(); rgba.putalpha(alpha)
    teil = rgba.crop((xs.start, ys.start, xs.stop, ys.stop))
    teil = teil.crop(teil.getbbox())
    teil.save(f"brand/aussie/{name}.png"); print(name, teil.size)
