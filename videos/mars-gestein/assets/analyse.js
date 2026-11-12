// Novaro Analyse-Ebene (über dem 3D-Bild): Karten mit Karopapier, Logo-Karten, Klebezettel, Handschrift,
// Stempel, selbst zeichnende Pfeile/Kreise/Unterstriche, Balken, Zähler. Alles nur aus der Zeit t berechnet.
//   import { Ebene } from "./assets/analyse.js";  const A = new Ebene(document.getElementById("root"));
//   A.stempel("ERSTMALS", 540, 900, { t0: 12.3, t1: 15, rot: -8 });   …   in renderAt(t): A.update(t);
// Freie Fläche: y ≈ 480–1350 (oben Datum/Balken/Beschriftung, unten Untertitel ab 1380).
const cl = (x) => Math.max(0, Math.min(1, x));
const back = (x) => { const c = 1.9; x = cl(x); return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const eout = (x) => 1 - Math.pow(1 - cl(x), 3);
export const ORANGE = "#ff9a3c", GELB = "#ffd23f", ROT = "#ff4d5e", GRUEN = "#5ef2a2", BLAU = "#7fd0ff", WEISS = "#ffffff";

const CSS = `@font-face{font-family:Caveat;src:url(assets/caveat-700.woff2);font-weight:700}
.an{position:absolute;transform-origin:50% 50%;will-change:transform,opacity;z-index:5}
.an-card{border-radius:26px;background:rgba(12,14,22,.86);border:3px solid rgba(255,154,60,.55);box-shadow:0 20px 60px rgba(0,0,0,.55),0 0 40px rgba(255,154,60,.18);
  background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:30px 30px;overflow:hidden}
.an-card .tt{position:absolute;left:26px;top:18px;font:800 34px "Inter Display",sans-serif;color:#fff}
.an-card .st{position:absolute;left:26px;top:60px;font:600 24px "Inter",sans-serif;color:rgba(255,255,255,.6);letter-spacing:1px}
.an-logo{background:#fff;border-radius:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 50px rgba(255,154,60,.35),0 20px 40px rgba(0,0,0,.6)}
.an-logo img{width:100%;height:100%;object-fit:contain;display:block}
.an-hand{font-family:Caveat,cursive;font-weight:700;line-height:1;white-space:nowrap;text-shadow:0 3px 14px rgba(0,0,0,.85)}
.an-zettel{background:#ffd54a;color:#1a1408;font-family:Caveat,cursive;font-weight:700;line-height:1.05;padding:26px 30px;box-shadow:0 18px 40px rgba(0,0,0,.5);text-align:center}
.an-zettel::before{content:"";position:absolute;left:50%;top:-18px;width:120px;height:36px;margin-left:-60px;background:rgba(255,255,255,.45);transform:rotate(-3deg)}
.an-stempel{font:900 54px "Inter Display",sans-serif;letter-spacing:3px;padding:10px 26px;border:7px solid;border-radius:16px;text-transform:uppercase;white-space:nowrap;background:rgba(0,0,0,.25)}
.an-zahl{font:900 120px "Inter Display",sans-serif;letter-spacing:-2px;white-space:nowrap;text-shadow:0 0 40px currentColor,0 6px 24px rgba(0,0,0,.9)}
.an-zahl small{display:block;font:700 34px "Inter",sans-serif;color:#fff;letter-spacing:0;text-shadow:0 3px 12px rgba(0,0,0,.9)}
.an-svg{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;pointer-events:none;z-index:6}`;

export class Ebene {
  constructor(root) {
    if (!document.getElementById("an-css")) { const s = document.createElement("style"); s.id = "an-css"; s.textContent = CSS; document.head.appendChild(s); }
    this.box = document.createElement("div"); this.box.style.cssText = "position:absolute;inset:0;pointer-events:none;z-index:5";
    root.insertBefore(this.box, document.getElementById("cap"));
    this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); this.svg.setAttribute("viewBox", "0 0 1080 1920"); this.svg.setAttribute("class", "an-svg");
    this.box.appendChild(this.svg); this.items = [];
  }
  _el(html, x, y, o, anchor = "c") {
    const d = document.createElement("div"); d.className = "an"; d.innerHTML = html; d.style.left = x + "px"; d.style.top = y + "px";
    if (o.w) d.style.width = o.w + "px"; if (o.h) d.style.height = o.h + "px"; if (o.z) d.style.zIndex = o.z;
    this.box.appendChild(d); const it = { el: d, t0: o.t0 ?? 0, t1: o.t1 ?? 999, rot: o.rot ?? 0, kind: o.kind ?? "pop", anchor, upd: o.upd };
    this.items.push(it); return it;
  }
  karte(titel, x, y, w, h, o = {}) { return this._el(`<div class="tt">${titel}</div>${o.unter ? `<div class="st">${o.unter}</div>` : ""}${o.html ?? ""}`, x, y, { ...o, w, h }, "tl"), this._last("an-card"); }
  _last(cls) { const it = this.items[this.items.length - 1]; it.el.classList.add(cls); return it; }
  logo(src, x, y, w, h, o = {}) { this._el(`<img src="${src}" alt="">`, x, y, { ...o, w, h }, "tl"); const it = this._last("an-logo"); it.el.style.padding = `${h * 0.14}px ${w * 0.08}px`; it.el.style.boxSizing = "border-box"; return it; }
  hand(text, x, y, o = {}) { this._el(text, x, y, o, "c"); const it = this._last("an-hand"); it.el.style.fontSize = (o.size ?? 64) + "px"; it.el.style.color = o.farbe ?? GELB; return it; }
  zettel(text, x, y, o = {}) { this._el(text, x, y, { ...o, kind: o.kind ?? "pop" }, "c"); const it = this._last("an-zettel"); it.el.style.fontSize = (o.size ?? 60) + "px"; if (o.w) it.el.style.width = o.w + "px"; return it; }
  stempel(text, x, y, o = {}) { this._el(text, x, y, { ...o, kind: "stempel" }, "c"); const it = this._last("an-stempel"); const f = o.farbe ?? ROT; it.el.style.color = f; it.el.style.borderColor = f; return it; }
  zahl(x, y, o) { // o: {von, bis, t0, dauer, fmt, farbe, unter}
    const it = this._el("", x, y, o, "c"); it.el.classList.add("an-zahl"); it.el.style.color = o.farbe ?? GELB;
    const fmt = o.fmt ?? ((v) => Math.round(v).toLocaleString("de-DE"));
    it.upd = (t) => { const v = o.von + (o.bis - o.von) * eout((t - it.t0) / (o.dauer ?? 1.2)); const h = fmt(v) + (o.unter ? `<small>${o.unter}</small>` : ""); if (h !== it.last) { it.el.innerHTML = h; it.last = h; } };
    return it;
  }
  balken(x, y, w, hMax, werte, o = {}) { // werte: [{name, wert, farbe, text}]
    const max = o.max ?? Math.max(...werte.map((v) => v.wert)); const bw = (w - (werte.length - 1) * 30) / werte.length;
    const html = werte.map((v, i) => `<div class="b" style="position:absolute;left:${i * (bw + 30)}px;bottom:46px;width:${bw}px;height:0;border-radius:14px 14px 4px 4px;background:${v.farbe ?? ORANGE};box-shadow:0 0 30px ${v.farbe ?? ORANGE}66"></div>
      <div style="position:absolute;left:${i * (bw + 30)}px;bottom:0;width:${bw}px;text-align:center;font:700 28px Inter,sans-serif;color:rgba(255,255,255,.85)">${v.name}</div>
      <div class="v" style="position:absolute;left:${i * (bw + 30)}px;width:${bw}px;text-align:center;font:900 42px 'Inter Display',sans-serif;color:#fff;opacity:0">${v.text ?? v.wert}</div>`).join("");
    const it = this._el(html, x, y, { ...o, w, h: hMax + 46, kind: "fade" }, "tl");
    const bars = it.el.querySelectorAll(".b"), vals = it.el.querySelectorAll(".v");
    it.upd = (t) => werte.forEach((v, i) => { const p = eout((t - it.t0 - 0.2 - i * (o.versatz ?? 0.35)) / 0.8); const h = hMax * (v.wert / max) * p; bars[i].style.height = h + "px"; vals[i].style.bottom = 46 + h + 8 + "px"; vals[i].style.opacity = cl(p * 3 - 2); });
    return it;
  }
  _path(d, o, len) {
    const p = document.createElementNS("http://www.w3.org/2000/svg", "path"); p.setAttribute("d", d); p.setAttribute("fill", "none"); const f = o.farbe ?? ORANGE;
    p.setAttribute("stroke", f); p.setAttribute("stroke-width", o.breite ?? 9); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round");
    p.style.filter = `drop-shadow(0 0 10px ${f})`; this.svg.appendChild(p); const L = len ?? p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
    const it = { el: p, t0: o.t0 ?? 0, t1: o.t1 ?? 999, kind: "draw", L, dauer: o.dauer ?? 0.5 }; this.items.push(it); return it;
  }
  pfeil(x1, y1, x2, y2, o = {}) {
    const bogen = o.bogen ?? 0.25, mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1, cx = mx - dy * bogen, cy = my + dx * bogen;
    const w = Math.atan2(y2 - cy, x2 - cx), k = 36, a1 = [x2 - k * Math.cos(w - 0.5), y2 - k * Math.sin(w - 0.5)], a2 = [x2 - k * Math.cos(w + 0.5), y2 - k * Math.sin(w + 0.5)];
    return this._path(`M${x1},${y1} Q${cx},${cy} ${x2},${y2} M${a1[0]},${a1[1]} L${x2},${y2} L${a2[0]},${a2[1]}`, o);
  }
  kreis(cx, cy, rx, ry, o = {}) { // leicht ungleichmäßig, wie von Hand
    let d = ""; for (let i = 0; i <= 64; i++) { const a = -0.6 + (i / 64) * (Math.PI * 2 + 0.5), r = 1 + 0.04 * Math.sin(i * 0.7); d += (i ? "L" : "M") + (cx + Math.cos(a) * rx * r).toFixed(1) + "," + (cy + Math.sin(a) * ry * r).toFixed(1); }
    return this._path(d, { farbe: ROT, ...o });
  }
  strich(x1, y, x2, o = {}) { return this._path(`M${x1},${y} Q${(x1 + x2) / 2},${y + 10} ${x2},${y - 4}`, { farbe: GELB, ...o }); }
  update(t) {
    for (const it of this.items) {
      const vis = t >= it.t0 && t < it.t1 + 0.3; if (!vis) { if (it.kind === "draw") it.el.style.opacity = 0; else it.el.style.display = "none"; continue; }
      const out = 1 - cl((t - it.t1) / 0.25);
      if (it.kind === "draw") { it.el.style.opacity = out; it.el.style.strokeDashoffset = it.L * (1 - eout((t - it.t0) / it.dauer)); continue; }
      it.el.style.display = "block"; const p = (t - it.t0) / 0.32; let s = 1, op = cl(p * 2.5) * out;
      if (it.kind === "pop") s = 0.55 + 0.45 * back(p);
      if (it.kind === "stempel") { const q = cl((t - it.t0) / 0.18); s = 1.9 - 0.9 * q; op = cl(q * 3) * out; }
      if (it.kind === "fade") s = 1;
      const tr = it.anchor === "c" ? "translate(-50%,-50%) " : ""; it.el.style.transform = `${tr}rotate(${it.rot}deg) scale(${s})`; it.el.style.opacity = op;
      if (it.upd) it.upd(t);
    }
  }
}
// Zeitpunkt eines Wortes (erstes Vorkommen ab Sekunde ab)
export function wortZeit(words, wort, ab = 0) { const w = words.find((x) => x.s >= ab - 0.01 && x.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(wort.toLowerCase())); return w ? w.s : ab; }
