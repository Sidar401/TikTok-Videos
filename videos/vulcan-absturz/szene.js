const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(15);
// ================= Weltraum mit Erde =================
const scS = new THREE.Scene(); K.stars(scS, 9000, -1, 30000, 1.7).material.opacity = 0.65; scS.add(new THREE.AmbientLight(0x30303a, 0.5));
const RE = 100; const EA = K.earth(scS, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-0.5, 0.35, 0.8).normalize();
// 40 Satelliten als Zug (Hook)
const train = []; for (let i = 0; i < 40; i++) train.push(K.sprite(scS, K.glowTex("rgba(255,215,110,1)"), 2.2, V(0, 0, 0), 0));
// Schwarm: 400 gold (oben) + 2800 grau (fehlen noch)
const shell = (n, col, size) => { const p = []; for (let i = 0; i < n; i++) { const u = K.rnd() * 2 - 1, a = K.rnd() * 6.283, r = RE * (1.08 + K.rnd() * 0.03), s = Math.sqrt(1 - u * u); p.push(Math.cos(a) * s * r, u * r * 0.9, Math.sin(a) * s * r); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); const pts = new THREE.Points(g, new THREE.PointsMaterial({ color: col, size, sizeAttenuation: false, transparent: true, opacity: 0, depthWrite: false })); scS.add(pts); return pts; };
const gold400 = shell(400, 0xffd23f, 3.2), grey = shell(2800, 0x8890a0, 2.0);
// Ziel-Bahn (gold) + echte Bahn (rot)
const tilt = new THREE.Group(); tilt.rotation.set(0.35, 0, -0.25); scS.add(tilt);
const ring = new THREE.Line(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 200 }, (_, i) => { const a = (i / 199) * Math.PI * 2; return V(Math.cos(a) * 118, 0, Math.sin(a) * 118); })), new THREE.LineBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); tilt.add(ring);
const pathPts = Array.from({ length: 120 }, (_, i) => { const f = i / 119; const a = 2.2 - f * 1.9; const r = RE + 1 + 15 * Math.sin(Math.PI * Math.min(1, f * 1.05)) * (f < 0.55 ? 1 : 1 - (f - 0.55) * 0.9); return V(Math.cos(a) * r, 0, Math.sin(a) * r); });
const redGeo = new THREE.BufferGeometry().setFromPoints(pathPts); const red = new THREE.Line(redGeo, new THREE.LineBasicMaterial({ color: 0xff4d5e, transparent: true, opacity: 0, toneMapped: false })); tilt.add(red);
const upDot = K.sprite(tilt, K.glowTex("rgba(255,120,100,1)"), 5, V(0, 0, 0), 0);
const ringO = new THREE.Object3D(); ringO.position.set(Math.cos(1.3) * 118, 0, Math.sin(1.3) * 118); tilt.add(ringO);
const crash = K.sprite(tilt, K.glowTex("rgba(255,90,70,1)"), 10, pathPts[119], 0);
// @fotos
await fotosInit({ v1: "assets/foto/v1.jpg", v2: "assets/foto/v2.jpg", v3: "assets/foto/v3.jpg", v4: "assets/foto/v4.jpg", v5: "assets/foto/v5.jpg", v6: "assets/foto/v6.jpg", v7: "assets/foto/v7.jpg" });

// ===== Zeiten =====
const tAm = W("am", 3.4), tAn = W("an", 7.4), tVier = W("vierzig", 8), tDoch = W("doch"), tSchief = W("schief"), tKamen = W("kamen"), tFolg = W("folg"), tDie = W("die", 17.3), tDah = W("dahinter"), tAnf = W("am", 22.4), tAber = W("aber", 24.4), tSie = W("sie", 28.9), tTrenn = W("trennte"), tObere = W("die", 32.3), tFehl = W("fehlende"), tFur = W("für", 37.4), tBaut = W("amazon", 43), tDafur = W("dafür"), tOben = W("oben", 50.8), tUnd = W("und", 53), tJetzt = W("jetzt"), tDer = W("der", 62.3), tAri = W("ariane"), tFrueh = W("frühestens"), tSechs = W("sechsunddreißig"), END = 72.0;
label("Ziel-Bahn", ringO, 2, { t0: tObere + 0.4, t1: tFur - 0.1, size: 48, gap: 18 });
const SY = "FOTO: NASA · VULCAN-START 2024 (SYMBOLBILD)";
const SHOTS = [
  [0, tAm, "v1", { z0: 1.0, z1: 1.12, cr: SY }],
  [tAm, tVier - 0.2, "v2", { z0: 1.05, z1: 1.2, y0: 40, y1: -20, cr: SY }],
  [tVier - 0.2, tDoch, "v3", { z0: 1.1, z1: 1.25, pos: "50% 30%", cr: SY }],
  [tDoch, tKamen, "v2", { z0: 1.5, z1: 1.9, y0: 0, y1: 80, cr: SY }],
  [tDie, tAnf, "v4", { z0: 1.05, z1: 1.18, pos: "60% 40%", cr: SY }],
  [tAnf, tObere, "v5", { z0: 1.6, z1: 1.25, pos: "50% 75%", y0: -200, y1: 0, cr: SY }],
  [tFur, tBaut, "v3", { z0: 1.3, z1: 1.1, pos: "50% 25%", cr: SY }],
  [tUnd, tJetzt, "v6", { z0: 1.05, z1: 1.15, dim: 0.35, cr: SY }],
  [tJetzt, tDer, "v4", { z0: 1.5, z1: 1.3, pos: "70% 20%", cr: SY }],
  [tDer, END + 1, "v7", { z0: 1.05, z1: 1.18, cr: "FOTO: NASA / ISS" }],
];
const grid38 = `<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:8px 12px;width:640px;margin:0 auto 18px;font-size:52px;line-height:1">${Array.from({ length: 38 }, (_, i) => `<span style="position:relative;${i ? "" : "filter:grayscale(1) brightness(.6)"}">🚀${i ? "" : "<b style='position:absolute;left:0;right:0;top:-6px;color:#ff4d5e;font-size:64px'>✕</b>"}</span>`).join("")}</div>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.35, 0.85);
  let pos = V(0, 0, 300), look = V(0, 0, 0), fov = 40;
  train.forEach((s) => (s.material.opacity = 0)); gold400.material.opacity = 0; grey.material.opacity = 0; ring.material.opacity = 0; red.material.opacity = 0; upDot.material.opacity = 0; crash.material.opacity = 0;
  EA.group.rotation.y = 1.2 + t * 0.012; EA.clouds.rotation.y = t * 0.004;
  if (t < tObere - 0.05) { // Satelliten verschwinden (nach „kamen nie oben an“)
    const f = prog(t, tKamen, tAnf - tKamen); for (let i = 0; i < 40; i++) { const a = -0.55 + i * 0.022; train[i].position.set(Math.sin(a) * 112, 38 - i * 0.3, Math.cos(a) * 112 - 10); train[i].material.opacity = 1 - cl((t - tKamen - 1.0 - i * 0.04) / 0.2); }
    pos = V(lerp(-40, -10, f), 70, 190); look = V(-20, 30, 70); fov = 42; }
  else if (t < tFur - 0.05) { // Bahn zu niedrig
    ring.material.opacity = cl((t - tObere) / 0.6) * 0.9; const f = prog(t, tObere + 0.4, tFur - tObere - 1.4); const n = Math.max(2, Math.floor(f * 119)); redGeo.setDrawRange(0, n); red.material.opacity = 0.95;
    upDot.position.copy(pathPts[n - 1]); upDot.material.opacity = f < 1 ? 1 : 0; crash.material.opacity = f >= 1 ? 0.9 * (0.6 + 0.4 * Math.sin(t * 8)) : 0;
    const g = prog(t, tObere, tFur - tObere); tilt.updateMatrixWorld(true); const nrm = V(0, 1, 0).applyQuaternion(tilt.quaternion); const side = V(Math.cos(1.25), 0, Math.sin(1.25)).applyQuaternion(tilt.quaternion); pos = nrm.multiplyScalar(lerp(560, 520, g)).add(side.multiplyScalar(lerp(220, 180, g))); look = side.clone().multiplyScalar(0.3); fov = 40; }
  else { gold400.material.opacity = cl((t - tBaut) / 0.8); grey.material.opacity = 0.55 * cl((t - tDafur) / 1.2); if (t > tOben) { grey.material.opacity *= 0.7; gold400.material.opacity = 0.75 + 0.25 * Math.sin(t * 6); }
    gold400.rotation.y = t * 0.03; grey.rotation.y = t * 0.03; const f = prog(t, tBaut, tUnd - tBaut); pos = V(Math.sin(f * 0.6) * lerp(360, 330, f), 80, Math.cos(f * 0.6) * lerp(360, 330, f)); look = V(0, 0, 0); fov = 40; }
  cam.fov = fov; cam.near = 0.5; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scS, t); updLabels(t); fotos(t, SHOTS);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tAm, tVier - 0.3, "15. November<div class='sub'>Start in Florida 🇺🇸</div>");
  seg(tVier - 0.2, tDoch - 0.1, "<div style='display:inline-block;background:#fff;border-radius:22px;padding:18px 30px 6px;margin-bottom:16px'><img src='assets/logos/amazon.svg' style='height:72px;display:block'></div><br>40 Satelliten");
  const T = Math.min(600, 596 + (t - tDoch) * 1.6); const mm = Math.floor(T / 60), ss = Math.floor(T % 60);
  seg(tDoch, tKamen - 0.1, `<span style="font-variant-numeric:tabular-nums">T+ ${String(mm).padStart(2, "0")}:${String(ss).padStart(2, "0")}</span>`);
  seg(tKamen - 0.1, tFolg - 0.1, "<span style='color:#ff6b78'>nie oben angekommen</span>");
  seg(tDie, tDah - 0.1, "ULA<div class='sub'>United Launch Alliance</div>"); seg(tDah, tAnf - 0.1, "Boeing + Lockheed Martin");
  seg(tAber, tSie - 0.1, "1. Stufe: zu wenig Kraft"); seg(tSie, tObere - 0.1, "zu lange gebrannt<div class='sub'>zu spät getrennt</div>");
  seg(tObere, tFehl - 0.1, "Obere Stufe gibt alles"); seg(tFehl, tFur - 0.1, "<span style='color:#ff6b78'>zu niedrig</span>");
  seg(tFur + 0.3, tBaut - 0.1, "größte Ladung<div class='sub'>40 auf einmal</div>");
  seg(tBaut, tDafur - 0.1, "Internet aus dem All<div class='sub'>wie Starlink</div>"); seg(tDafur, tOben - 0.1, "3.200+ nötig");
  seg(tOben, tUnd - 0.1, "<span class='y'>erst ≈ 400 oben</span>");
  seg(tUnd, tJetzt - 0.1, grid38 + "38 Flüge gebucht<div class='sub'>das war der erste</div>");
  seg(tJetzt, tDer - 0.1, "Untersuchung<div class='sub'>kann Monate dauern</div>");
  seg(tAri - 0.2, tFrueh - 0.1, "🇪🇺 Ariane 6"); seg(tFrueh, tSechs - 0.1, "frühestens 23. November"); seg(tSechs, END, "+36 Satelliten");
  WORDEL.style.top = (t >= tFolg - 0.1 && t < tDah) || (t >= tUnd && t < tJetzt) ? "300px" : "";
  word(wh, wa); cap(t);
};
