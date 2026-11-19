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
// @modelle
// ================= Raketen-Szene =================
const scR = new THREE.Scene(); K.reseed(5); const st = K.stars(scR, 7000, -1, 20000, 1.6); const skyM = K.sky(scR, 0x02040a, 0x0a1a3a, 0x24406e, 15000);
scR.add(new THREE.AmbientLight(0x404858, 0.22)); const sunR = new THREE.DirectionalLight(0xfff2e0, 1.25); sunR.position.set(300, 200, 400); scR.add(sunR);
const rimR = new THREE.DirectionalLight(0x8fb0ff, 0.9); rimR.position.set(-300, 120, -300); scR.add(rimR);
const flameLight = new THREE.PointLight(0xffaa55, 0, 120, 1.5); scR.add(flameLight);
const VU = MO.vulcan(); scR.add(VU.g); const AR = MO.ariane6(); scR.add(AR.g); AR.g.visible = false;
const coreX = [-1.2, 1.2].map((x) => { const e = MO.exhaust(30, 1.35); e.position.set(x, -3.2, 0); VU.boost.add(e); return e; });
const srbX = VU.srbs.map((s) => { const e = MO.exhaust(34, 0.8, [1, 0.97, 0.9], [1, 0.7, 0.35]); e.position.y = -1.1; s.add(e); return e; });
const upX = MO.exhaust(16, 0.8, [0.85, 0.9, 1], [0.45, 0.55, 1]); upX.position.y = 34.5; VU.up.add(upX);
const arX = [MO.exhaust(26, 1.2)]; arX[0].position.y = -2.4; AR.g.add(arX[0]); AR.boosters.forEach((b) => { const e = MO.exhaust(30, 1.0, [1, 0.97, 0.9], [1, 0.7, 0.35]); e.position.y = -1.8; b.add(e); arX.push(e); });
const glowS = K.sprite(scR, K.glowTex("rgba(255,200,140,1)"), 40, V(0, 0, 0), 0);
const smoke = MO.smoke(scR, 70);
const ALLX = [...coreX, ...srbX, upX, ...arX];
function fire(base, power, t, len = 1, which = "vu") { ALLX.forEach((e) => (e.visible = false));
  const list = which === "ar" ? arX : which === "up" ? [upX] : [...coreX, ...srbX];
  list.forEach((e) => { e.visible = power > 0.01; e.userData.mat.uniforms.t.value = t; e.userData.mat.uniforms.power.value = power; e.scale.set(1, len, 1); });
  glowS.position.copy(base).add(V(0, -3, 0)); glowS.material.opacity = power * 0.7; glowS.scale.setScalar(20 + power * 10);
  flameLight.position.copy(base).add(V(0, -6, 0)); flameLight.intensity = power * 160; }
function trail(base, a, t) { smoke.forEach((s, i) => { const k = ((i / smoke.length) + t * 0.3) % 1; s.position.set(base.x + Math.sin(i * 7.3) * (2 + k * 18), base.y - 22 - k * 190, base.z + Math.cos(i * 3.1) * (2 + k * 18)); s.scale.setScalar(12 + k * 60); s.material.opacity = a * 0.5 * (1 - k) * cl(k * 6); s.material.color.setRGB(0.55 + 0.4 * (1 - k), 0.5 + 0.4 * (1 - k), 0.5 + 0.38 * (1 - k)); }); }
const noFire = () => { ALLX.forEach((e) => (e.visible = false)); glowS.material.opacity = 0; flameLight.intensity = 0; smoke.forEach((s) => (s.material.opacity = 0)); };
const boostO = new THREE.Object3D(); boostO.position.set(0, 16, 0); VU.boost.add(boostO);
const upO = new THREE.Object3D(); upO.position.set(0, 44, 0); VU.up.add(upO);

// ===== Zeiten =====
const tAm = W("am", 3.4), tAn = W("an", 7.4), tVier = W("vierzig", 8), tDoch = W("doch"), tSchief = W("schief"), tKamen = W("kamen"), tFolg = W("folg"), tDie = W("die", 17.3), tDah = W("dahinter"), tAnf = W("am", 22.4), tAber = W("aber", 24.4), tSie = W("sie", 28.9), tTrenn = W("trennte"), tObere = W("die", 32.3), tFehl = W("fehlende"), tFur = W("für", 37.4), tBaut = W("amazon", 43), tDafur = W("dafür"), tOben = W("oben", 50.8), tUnd = W("und", 53), tJetzt = W("jetzt"), tDer = W("der", 62.3), tAri = W("ariane"), tFrueh = W("frühestens"), tSechs = W("sechsunddreißig"), END = 72.0;
label("Ziel-Bahn", ringO, 2, { t0: tObere + 0.4, t1: tFur - 0.1, size: 48, gap: 18 });
label("1. Stufe", boostO, 4, { t0: tAber + 0.2, t1: tObere - 0.1, size: 52, gap: 30 });
label("obere Stufe", upO, 4, { t0: tTrenn + 0.6, t1: tObere - 0.1, size: 46, gap: 30 });
const logo = (f, h = 120) => `<img src='assets/logos/${f}' style='height:${h}px;display:block;margin:0 auto 18px;filter:drop-shadow(0 6px 24px rgba(0,0,0,.8))'>`;
const grid38 = `<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:8px 12px;width:640px;margin:0 auto 18px;font-size:52px;line-height:1">${Array.from({ length: 38 }, (_, i) => `<span style="position:relative;${i ? "" : "filter:grayscale(1) brightness(.6)"}">🚀${i ? "" : "<b style='position:absolute;left:0;right:0;top:-6px;color:#ff4d5e;font-size:64px'>✕</b>"}</span>`).join("")}</div>`;

const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.35, 0.85);
  let scene = scS, pos = V(0, 0, 300), look = V(0, 0, 0), fov = 40;
  train.forEach((s) => (s.material.opacity = 0)); gold400.material.opacity = 0; grey.material.opacity = 0; ring.material.opacity = 0; red.material.opacity = 0; upDot.material.opacity = 0; crash.material.opacity = 0;
  noFire();
  VU.g.visible = true; AR.g.visible = false; VU.g.position.set(0, 0, 0); VU.g.rotation.set(0, 0, 0); VU.boost.position.set(0, 0, 0); VU.boost.rotation.set(0, 0, 0); VU.halves.forEach((h) => h.position.set(0, 0, 0)); VU.sats.visible = false;
  skyM.material.uniforms.t.value.set(0x02040a); skyM.material.uniforms.m.value.set(0x0a1a3a); skyM.material.uniforms.h.value.set(0x24406e); skyM.visible = true; st.material.opacity = 0.8;
  EA.group.rotation.y = 1.2 + t * 0.012; EA.clouds.rotation.y = t * 0.004;
  const space = () => { skyM.visible = false; st.material.opacity = 0.85; };
  if (t < tAm - 0.05) { // 40 Satelliten verschwinden
    const f = prog(t, 0, tAm); for (let i = 0; i < 40; i++) { const a = -0.55 + i * 0.022; train[i].position.set(Math.sin(a) * 112, 38 - i * 0.3, Math.cos(a) * 112 - 10); train[i].material.opacity = 1 - cl((t - 1.3 - i * 0.035) / 0.15); }
    pos = V(lerp(-40, -10, f), 70, 190); look = V(-20, 30, 70); fov = 42; }
  else if (t < tDoch - 0.05) { scene = scR; const f = prog(t, tAm, tDoch - tAm); const k = cl((t - tAm) / 7);
    skyM.material.uniforms.m.value.setRGB(lerp(0.04, 0.01, k), lerp(0.1, 0.02, k), lerp(0.23, 0.06, k)); skyM.material.uniforms.h.value.setRGB(lerp(0.14, 0.03, k), lerp(0.25, 0.06, k), lerp(0.43, 0.15, k));
    fire(V(0, -1, 0), 1, t); trail(V(0, -1, 0), 1, t); const a = 0.6 + f * 0.5; pos = V(Math.sin(a) * lerp(95, 120, f), lerp(-25, 10, f), Math.cos(a) * lerp(95, 120, f)); look = V(0, 25, 0); fov = 44; }
  else if (t < tFolg - 0.05) { scene = scR; space(); const bad = cl((t - tSchief) / 0.3), fall = cl((t - tSchief - 0.5) / 3);
    if (t < tSchief) { fire(V(0, 34, 0), 0.75, t, 0.6, "up"); VU.boost.visible = false; } else { fire(V(0, 34, 0), 0.75 * (1 - bad) * (Math.sin(t * 50) > 0 ? 1 : 0.3), t, 0.6, "up"); VU.boost.visible = false; }
    VU.g.rotation.z = fall * 1.6; VU.g.position.y = -fall * fall * 40; if (t > tSchief && t < tSchief + 0.35) E.grade.uniforms.flash.value = 0.25 * (1 - (t - tSchief) / 0.35);
    if (t > tSchief) E.look([1.12, 0.86, 0.84], [0.02, 0, 0], 0.35, 0.85);
    const f = prog(t, tDoch, tFolg - tDoch); pos = V(lerp(70, 85, f), lerp(50, 30, f), lerp(40, 60, f)); look = V(0, lerp(42, 30, f), 0); fov = 40; }
  else if (t < tAnf - 0.05) { scene = scR; space(); VU.boost.visible = true; const a = (t - tFolg) * 0.12 + 0.3; pos = V(Math.sin(a) * 90, 22, Math.cos(a) * 90); look = V(0, 26, 0); fov = 44; }
  else if (t < tObere - 0.05) { scene = scR; VU.boost.visible = true; const k = cl((t - tAnf) / 6); skyM.material.uniforms.m.value.setRGB(0.01, 0.02 * (1 - k), 0.07 * (1 - k * 0.6)); skyM.material.uniforms.h.value.setRGB(0.03, 0.07 * (1 - k * 0.5), 0.18 * (1 - k * 0.5));
    const weak = t > tAber ? 0.55 + 0.25 * Math.sin(t * 9) : 1; const sep = cl((t - tTrenn - 0.4) / 2.5);
    if (sep <= 0) { fire(V(0, -1, 0), weak, t); trail(V(0, -1, 0), weak, t); } else { VU.boost.position.y = -sep * sep * 50; VU.boost.rotation.z = sep * 0.5; fire(V(0, 34, 0), 0.8 * cl((sep - 0.15) * 4), t, 0.6, "up"); }
    if (t > tAber && t < tTrenn) E.look([1.08, 0.94, 0.86], [0, 0, 0], 0.35, 0.85);
    const f = prog(t, tAnf, tObere - tAnf); const a = -0.4 + f * 0.7; pos = V(Math.sin(a) * lerp(110, 130, f), lerp(5, 30, f), Math.cos(a) * lerp(110, 130, f)); look = V(0, lerp(18, 25, f), 0); fov = 44; }
  else if (t < tFur - 0.05) { // Bahn zu niedrig
    ring.material.opacity = cl((t - tObere) / 0.6) * 0.9; const f = prog(t, tObere + 0.4, tFur - tObere - 1.4); const n = Math.max(2, Math.floor(f * 119)); redGeo.setDrawRange(0, n); red.material.opacity = 0.95;
    upDot.position.copy(pathPts[n - 1]); upDot.material.opacity = f < 1 ? 1 : 0; crash.material.opacity = f >= 1 ? 0.9 * (0.6 + 0.4 * Math.sin(t * 8)) : 0;
    const g = prog(t, tObere, tFur - tObere); tilt.updateMatrixWorld(true); const nrm = V(0, 1, 0).applyQuaternion(tilt.quaternion); const side = V(Math.cos(1.25), 0, Math.sin(1.25)).applyQuaternion(tilt.quaternion); pos = nrm.multiplyScalar(lerp(560, 520, g)).add(side.multiplyScalar(lerp(220, 180, g))); look = side.clone().multiplyScalar(0.3); fov = 40; }
  else if (t < tBaut - 0.05) { scene = scR; space(); VU.sats.visible = true; const o = K.eio(cl((t - tFur - 0.3) / 1.5)); VU.halves[0].position.set(0, 0, -o * 9); VU.halves[1].position.set(0, 0, o * 9); VU.halves[0].rotation.x = -o * 0.3; VU.halves[1].rotation.x = o * 0.3;
    const f = prog(t, tFur, tBaut - tFur); const a = 1.3 + f * 0.5; pos = V(Math.sin(a) * lerp(34, 26, f), lerp(60, 55, f), Math.cos(a) * lerp(34, 26, f)); look = V(0, 54, 0); fov = 44; }
  else if (t < tUnd - 0.05) { gold400.material.opacity = cl((t - tBaut) / 0.8); grey.material.opacity = 0.55 * cl((t - tDafur) / 1.2); if (t > tOben) { grey.material.opacity *= 0.7; gold400.material.opacity = 0.75 + 0.25 * Math.sin(t * 6); }
    gold400.rotation.y = t * 0.03; grey.rotation.y = t * 0.03; const f = prog(t, tBaut, tUnd - tBaut); pos = V(Math.sin(f * 0.6) * lerp(360, 330, f), 80, Math.cos(f * 0.6) * lerp(360, 330, f)); look = V(0, 0, 0); fov = 40; }
  else if (t < tJetzt - 0.05) { scene = scR; space(); const a = (t - tUnd) * 0.1 - 0.4; pos = V(Math.sin(a) * 70, -30, Math.cos(a) * 70); look = V(0, 30, 0); fov = 46; }
  else if (t < tDer - 0.05) { scene = scR; space(); VU.up.visible = true; E.look([0.82, 0.88, 1.0], [0, 0, 0], 0.35, 0.85); const f = prog(t, tJetzt, tDer - tJetzt); VU.g.rotation.z = 0.25; pos = V(lerp(40, 30, f), lerp(5, 12, f), lerp(45, 35, f)); look = V(0, 8, 0); fov = 42; }
  else { scene = scR; VU.g.visible = false; AR.g.visible = true; const k = cl((t - tDer) / 9); skyM.material.uniforms.m.value.setRGB(lerp(0.05, 0.01, k), lerp(0.13, 0.03, k), lerp(0.3, 0.08, k)); skyM.material.uniforms.h.value.setRGB(lerp(0.2, 0.04, k), lerp(0.35, 0.08, k), lerp(0.55, 0.2, k));
    fire(V(0, -1, 0), 1, t, 1.1, "ar"); trail(V(0, -1, 0), 1, t); const f = prog(t, tDer, END - tDer); const a = -0.6 + f * 0.6; pos = V(Math.sin(a) * lerp(100, 125, f), lerp(-15, 10, f), Math.cos(a) * lerp(100, 125, f)); look = V(0, 24, 0); fov = 44; }
  if (!(t >= tDoch - 0.05 && t < tFolg - 0.05)) VU.boost.visible = true;
  cam.fov = fov; cam.near = 0.5; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tAm, tAn - 0.1, "🚀 15. November<div class='sub'>Start in Florida 🇺🇸</div>");
  seg(tVier - 0.2, 10.9, "<div style='display:inline-block;background:#fff;border-radius:22px;padding:18px 30px 6px;margin-bottom:16px'><img src='assets/logos/amazon.svg' style='height:72px;display:block'></div><br>40 Satelliten");
  const T = Math.min(600, 596 + (t - tDoch) * 1.6); const mm = Math.floor(T / 60), ss = Math.floor(T % 60);
  seg(tDoch, tKamen - 0.1, `<span style="font-variant-numeric:tabular-nums">⏱ T+ ${String(mm).padStart(2, "0")}:${String(ss).padStart(2, "0")}</span>`);
  seg(tKamen - 0.1, tFolg - 0.1, "<span style='color:#ff6b78'>❌ nie im All angekommen</span>");
  seg(tDie, tDah - 0.1, "<span style='font-size:130px;letter-spacing:6px'>ULA</span><div class='sub'>United Launch Alliance</div>"); seg(tDah, tAnf - 0.1, "Boeing + Lockheed Martin");
  seg(tAber, tSie - 0.1, "⚠️ zu wenig Kraft"); seg(tSie, tObere - 0.1, "⏱ zu lange gebrannt<div class='sub'>zu spät getrennt</div>");
  seg(tObere, tFehl - 0.1, "Obere Stufe gibt alles"); seg(tFehl, tFur - 0.1, "<span style='color:#ff6b78'>Kraft fehlt → zu niedrig</span>");
  seg(tFur + 0.3, tBaut - 0.1, "40 auf einmal<div class='sub'>größte Ladung für Amazon</div>");
  seg(tBaut, tDafur - 0.1, "🛰️ Internet aus dem All<div class='sub'>wie Starlink</div>"); seg(tDafur, tOben - 0.1, "3.200+ nötig");
  seg(tOben, tUnd - 0.1, "<span class='y'>erst ≈ 400 oben</span><div class='sub'>≈ 12 %</div>");
  seg(tUnd, tJetzt - 0.1, grid38 + "38 Flüge gebucht<div class='sub'>das war der erste</div>");
  seg(tJetzt, tDer - 0.1, "🔍 Untersuchung<div class='sub'>kann Monate dauern</div>");
  seg(tAri - 0.2, tFrueh - 0.1, "🇪🇺 Ariane 6"); seg(tFrueh, tSechs - 0.1, "frühestens 23. November"); seg(tSechs, END, "+36 Satelliten");
  WORDEL.style.top = (t >= 16.1 && t < 21.7) || (t >= tUnd && t < tJetzt) ? "300px" : "";
  word(wh, wa); cap(t);
};
