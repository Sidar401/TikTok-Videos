// Baukasten für den Wissens-Kanal (Neon-Stil, dunkler Hintergrund).
// Alles ist rein von der Zeit t abhängig (kein Zufall, keine Uhr).
(function () {
  const K = {};
  K.cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  K.lerp = (a, b, f) => a + (b - a) * f;
  K.eio = (f) => (f < 0.5 ? 4 * f * f * f : 1 - Math.pow(-2 * f + 2, 3) / 2);
  K.eout = (f) => 1 - Math.pow(1 - f, 3);
  K.ein = (f) => f * f * f;
  K.back = (f) => { const c = 1.9; return 1 + (c + 1) * Math.pow(f - 1, 3) + c * Math.pow(f - 1, 2); };
  K.prog = (t, a, d) => K.cl((t - a) / d);
  K.rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  K.de = (n, d = 0) => Number(n).toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d });
  K.C = { mint: "#5ef2c2", gold: "#ffc94d", pink: "#ff5f8f", red: "#ff4d5e", orange: "#ff9a3c", amber: "#ffb347", icon: "#8fe9ff", purple: "#b99cff", white: "#ffffff" };

  K.init = function (id) { const c = document.getElementById(id); K.g = c.getContext("2d"); return K.g; };
  const STARS = Array.from({ length: 170 }, (_, i) => [K.rnd(i) * 1080, K.rnd(i + 500) * 1920, 0.6 + K.rnd(i + 900) * 2.2, K.rnd(i + 1300)]);

  K.bg = function (t, o = {}) {
    const g = K.g;
    const gr = g.createLinearGradient(0, 0, 0, 1920);
    gr.addColorStop(0, o.top || "#1b1232"); gr.addColorStop(0.55, o.mid || "#0f0b1d"); gr.addColorStop(1, "#05040a");
    g.fillStyle = gr; g.fillRect(0, 0, 1080, 1920);
    const sa = o.stars == null ? 0.6 : o.stars;
    if (sa > 0) STARS.forEach((s, i) => { g.fillStyle = "rgba(255,255,255," + sa * (0.25 + 0.6 * s[3]) * (0.75 + 0.25 * Math.sin(t * 2.5 + i)) + ")"; g.fillRect(s[0], s[1], s[2], s[2]); });
    if (o.red > 0) {
      const rg = g.createRadialGradient(540, 960, 400, 540, 960, 1150);
      rg.addColorStop(0, "rgba(255,40,60,0)"); rg.addColorStop(1, "rgba(255,40,60," + o.red + ")");
      g.fillStyle = rg; g.fillRect(0, 0, 1080, 1920);
    }
    if (o.glow) {
      const rg = g.createRadialGradient(540, 950, 50, 540, 950, 750);
      rg.addColorStop(0, o.glow); rg.addColorStop(1, "rgba(0,0,0,0)");
      g.fillStyle = rg; g.fillRect(0, 0, 1080, 1920);
    }
  };

  K.label = function (txt, x, y, size, col = "#fff", align = "center", weight = 800) {
    const g = K.g;
    g.font = weight + " " + size + "px Montserrat, sans-serif"; g.textAlign = align; g.textBaseline = "middle";
    g.lineJoin = "round"; if (col !== "#1a0f24") { g.lineWidth = Math.max(5, size * 0.18); g.strokeStyle = "rgba(10,7,20,0.9)"; g.strokeText(txt, x, y); }
    g.fillStyle = col; g.fillText(txt, x, y);
  };
  K.mono = function (txt, x, y, size, col = "#fff", glow) {
    const g = K.g;
    g.font = "800 " + size + "px 'JetBrains Mono', monospace"; g.textAlign = "center"; g.textBaseline = "middle";
    if (glow) { g.shadowColor = glow; g.shadowBlur = 30; }
    g.fillStyle = col; g.fillText(txt, x, y); g.shadowBlur = 0;
  };
  K.glowLine = function (x1, y1, x2, y2, col, w, a = 1, dash) {
    const g = K.g; g.save(); g.globalAlpha *= a; g.strokeStyle = col; g.lineWidth = w; g.lineCap = "round";
    if (dash) g.setLineDash(dash);
    g.shadowColor = col; g.shadowBlur = 18; g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); g.restore();
  };
  K.ground = function (y, col = "#ffb347") {
    const g = K.g; g.fillStyle = "#0e0a16"; g.fillRect(0, y, 1080, 1920 - y);
    K.glowLine(-20, y, 1100, y, col, 6, 0.95);
  };
  K.bar = function (x, y, w, f, col, h = 22) {
    const g = K.g; g.save();
    g.fillStyle = "rgba(255,255,255,0.13)"; g.beginPath(); g.roundRect(x, y, w, h, h / 2); g.fill();
    if (f > 0) { g.fillStyle = col; g.shadowColor = col; g.shadowBlur = 16; g.beginPath(); g.roundRect(x, y, Math.max(h, w * K.cl(f)), h, h / 2); g.fill(); }
    g.restore();
  };
  K.ring = function (x, y, r, col, w, a = 1) {
    const g = K.g; g.save(); g.globalAlpha *= a; g.strokeStyle = col; g.lineWidth = w; g.shadowColor = col; g.shadowBlur = 24;
    g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.stroke(); g.restore();
  };
  K.dot = function (x, y, r, col, blur = 24) {
    const g = K.g; g.save(); g.fillStyle = col; g.shadowColor = col; g.shadowBlur = blur; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); g.restore();
  };
  K.boom = function (x, y, d, size, col = "255,160,60") {
    const g = K.g; if (d < 0 || d > 0.9) return;
    const al = 1 - d / 0.9, r = size * (0.3 + K.eout(K.cl(d / 0.5)));
    const rg = g.createRadialGradient(x, y, 0, x, y, r);
    rg.addColorStop(0, "rgba(255,250,225," + al + ")"); rg.addColorStop(0.45, "rgba(" + col + "," + al * 0.8 + ")"); rg.addColorStop(1, "rgba(" + col + ",0)");
    g.fillStyle = rg; g.fillRect(x - r, y - r, 2 * r, 2 * r);
  };

  // Gefüllte Felsform (Asteroid, Komet-Kern)
  const ROCK = Array.from({ length: 30 }, (_, i) => 1 + 0.13 * (K.rnd(i + 70) - 0.5) + 0.07 * Math.sin(i * 1.7));
  const CRAT = Array.from({ length: 7 }, (_, i) => [(K.rnd(i + 200) - 0.5) * 1.1, (K.rnd(i + 300) - 0.5) * 1.1, 0.08 + K.rnd(i + 400) * 0.14]);
  K.rock = function (x, y, r, rot = 0, heat = 0, tint) {
    const g = K.g; g.save(); g.translate(x, y); g.rotate(rot);
    if (heat > 0) { g.shadowColor = "rgba(255,140,60," + heat + ")"; g.shadowBlur = 50 * heat; }
    g.beginPath();
    ROCK.forEach((k, i) => { const a = (i / ROCK.length) * Math.PI * 2; i ? g.lineTo(Math.cos(a) * r * k, Math.sin(a) * r * k) : g.moveTo(Math.cos(a) * r * k, Math.sin(a) * r * k); });
    g.closePath();
    const gr = g.createRadialGradient(-r * 0.35, -r * 0.35, r * 0.1, 0, 0, r * 1.1);
    const c = tint || ["#9b8c80", "#5e5149", "#2e2622"];
    gr.addColorStop(0, c[0]); gr.addColorStop(0.6, c[1]); gr.addColorStop(1, c[2]);
    g.fillStyle = gr; g.fill(); g.shadowBlur = 0;
    g.save(); g.clip();
    CRAT.forEach((cc) => { g.fillStyle = "rgba(30,22,18,0.45)"; g.beginPath(); g.arc(cc[0] * r, cc[1] * r, cc[2] * r, 0, Math.PI * 2); g.fill(); });
    g.restore(); g.restore();
  };
  K.planet = function (x, y, r, c1, c2, glow) {
    const g = K.g; g.save();
    if (glow) { g.shadowColor = glow; g.shadowBlur = Math.min(60, r * 0.6 + 10); }
    const gr = g.createRadialGradient(x - r * 0.3, y - r * 0.35, r * 0.1, x, y, r);
    gr.addColorStop(0, c1); gr.addColorStop(1, c2);
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, Math.max(0.5, r), 0, Math.PI * 2); g.fill(); g.restore();
  };
  K.earth = function (x, y, r) {
    const g = K.g; K.planet(x, y, r, "#4a9cf0", "#123a7a", "#5fb8ff");
    if (r < 3) return;
    g.save(); g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.clip(); g.fillStyle = "rgba(63,190,130,0.85)";
    [[-0.4, -0.3, 0.32], [0.35, -0.1, 0.25], [-0.1, 0.45, 0.28], [0.5, 0.5, 0.18]].forEach((c) => { g.beginPath(); g.ellipse(x + c[0] * r, y + c[1] * r, c[2] * r, c[2] * r * 0.7, 0.5, 0, Math.PI * 2); g.fill(); });
    g.restore();
  };
  K.moon = function (x, y, r) {
    const g = K.g; K.planet(x, y, r, "#f1edfb", "#a59fc0", "#e8e2ff");
    if (r < 4) return;
    g.save(); g.fillStyle = "rgba(140,130,170,0.55)";
    [[-0.3, -0.25, 0.2], [0.3, 0.1, 0.26], [0.0, 0.45, 0.13], [0.4, -0.45, 0.1]].forEach((c) => { g.beginPath(); g.arc(x + c[0] * r, y + c[1] * r, c[2] * r, 0, Math.PI * 2); g.fill(); });
    g.restore();
  };

  // Linien-Symbole (Fuß auf x,y; h = Höhe in px). Pfad wird nur gebaut.
  K.iconPath = function (kind, x, y, h) {
    const g = K.g; g.beginPath();
    const M = (a, b) => g.moveTo(x + a * h, y - b * h), L = (a, b) => g.lineTo(x + a * h, y - b * h);
    switch (kind) {
      case "you":
        g.arc(x, y - h * 0.9, h * 0.1, 0, Math.PI * 2); M(0, 0.8); L(0, 0.42); M(-0.13, 0); L(0, 0.42); L(0.13, 0); M(-0.2, 0.55); L(0, 0.72); L(0.2, 0.55); break;
      case "house":
        M(-0.55, 0); L(-0.55, 0.55); L(0, 1); L(0.55, 0.55); L(0.55, 0); g.closePath(); g.rect(x - h * 0.12, y - h * 0.33, h * 0.24, h * 0.33); break;
      case "car":
        M(-0.9, 0.12); L(-0.9, 0.45); L(-0.5, 0.5); L(-0.3, 0.85); L(0.35, 0.85); L(0.55, 0.5); L(0.9, 0.42); L(0.9, 0.12); g.closePath();
        g.moveTo(x - h * 0.45 + h * 0.17, y - h * 0.12); g.arc(x - h * 0.45, y - h * 0.12, h * 0.17, 0, Math.PI * 2);
        g.moveTo(x + h * 0.5 + h * 0.17, y - h * 0.12); g.arc(x + h * 0.5, y - h * 0.12, h * 0.17, 0, Math.PI * 2); break;
      case "plane":
        M(-1, 0.55); L(0.85, 0.55); L(1, 0.45); L(0.85, 0.35); L(-0.9, 0.35); L(-1.05, 0.85); L(-0.85, 0.85); L(-0.7, 0.55); M(-0.1, 0.45); L(-0.4, 0.05); L(-0.2, 0.05); L(0.25, 0.45); break;
      case "rocket":
        M(0, 1); L(0.13, 0.7); L(0.13, 0.15); L(0.28, 0); L(-0.28, 0); L(-0.13, 0.15); L(-0.13, 0.7); g.closePath(); g.moveTo(x + h * 0.06, y - h * 0.62); g.arc(x, y - h * 0.62, h * 0.06, 0, Math.PI * 2); break;
      case "bullet":
        M(-0.6, 0.35); L(0.25, 0.35); L(0.6, 0.5); L(0.25, 0.65); L(-0.6, 0.65); g.closePath(); break;
      case "iss":
        g.rect(x - h * 0.08, y - h * 0.58, h * 0.16, h * 0.16); g.rect(x - h * 0.7, y - h * 0.75, h * 0.5, h * 0.5); g.rect(x + h * 0.2, y - h * 0.75, h * 0.5, h * 0.5); break;
      case "cheetah":
        M(-0.7, 0.45); L(0.3, 0.5); L(0.55, 0.62); L(0.7, 0.55); L(0.5, 0.4); M(-0.5, 0.45); L(-0.75, 0.05); M(-0.35, 0.45); L(-0.2, 0.05); M(0.15, 0.48); L(-0.05, 0.05); M(0.28, 0.48); L(0.45, 0.05); M(-0.7, 0.47); L(-1.0, 0.7); break;
      case "door":
        g.rect(x - h * 0.33, y - h, h * 0.66, h); g.moveTo(x + h * 0.22, y - h * 0.5); g.arc(x + h * 0.2, y - h * 0.5, h * 0.03, 0, Math.PI * 2); break;
      case "goat":
        M(-0.45, 0.35); L(0.3, 0.38); L(0.45, 0.6); L(0.62, 0.72); L(0.58, 0.55); L(0.4, 0.42); M(0.45, 0.6); L(0.38, 0.82); M(0.52, 0.66); L(0.6, 0.85);
        M(-0.38, 0.36); L(-0.42, 0); M(-0.2, 0.37); L(-0.18, 0); M(0.1, 0.38); L(0.08, 0); M(0.25, 0.38); L(0.28, 0); M(-0.45, 0.4); L(-0.55, 0.55); M(0.6, 0.62); L(0.55, 0.45); break;
      case "trophy":
        M(-0.35, 1); L(0.35, 1); L(0.28, 0.55); L(0.08, 0.42); L(0.08, 0.2); L(0.25, 0.08); L(0.25, 0); L(-0.25, 0); L(-0.25, 0.08); L(-0.08, 0.2); L(-0.08, 0.42); L(-0.28, 0.55); g.closePath(); break;
      default: g.rect(x - h / 2, y - h, h, h);
    }
  };
  K.icon = function (kind, x, y, h, a = 1, col = "#8fe9ff", fill = "rgba(120,200,255,0.10)") {
    const g = K.g; if (a <= 0) return; g.save(); g.globalAlpha *= a;
    g.strokeStyle = col; g.fillStyle = fill; g.lineWidth = Math.max(3, Math.min(6, h * 0.04)); g.lineJoin = "round"; g.lineCap = "round";
    g.shadowColor = col; g.shadowBlur = 14; K.iconPath(kind, x, y, h); g.fill(); g.stroke(); g.restore();
  };

  // Wackeln/Blitz: hits = [[zeit, stärke], ...]
  K.shake = function (t, hits) {
    let s = 0; hits.forEach(([ti, a]) => { const d = t - ti; if (d > 0 && d < 0.6) s += a * Math.exp(-d * 7) * Math.sin(d * 75); }); return s;
  };
  K.flash = function (t, hits) {
    const g = K.g; hits.forEach(([ti, a]) => { const d = t - ti; if (d > 0 && d < 0.3) { g.fillStyle = "rgba(255,248,235," + a * (1 - d / 0.3) + ")"; g.fillRect(0, 0, 1080, 1920); } });
  };

  // GSAP-Helfer für Texte
  K.texts = function (tl) {
    return {
      pop(id, at, dur) { tl.from("#" + id, { opacity: 0, y: 30, scale: 0.85, duration: 0.25, ease: "back.out(2.4)" }, at); if (dur) tl.to("#" + id, { opacity: 0, duration: 0.15 }, at + dur - 0.17); },
      slam(id, at, dur) { tl.from("#" + id, { opacity: 0, scale: 1.7, duration: 0.22, ease: "power3.out" }, at); if (dur) tl.to("#" + id, { opacity: 0, duration: 0.15 }, at + dur - 0.17); },
      pulse(id, at, n = 3) { tl.to("#" + id, { scale: 1.07, duration: 0.25, yoyo: true, repeat: n, ease: "sine.inOut" }, at); },
    };
  };
  window.K = K;
})();
