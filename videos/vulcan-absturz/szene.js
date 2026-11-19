const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(15);
const { RoomEnvironment } = await import("three/addons/environments/RoomEnvironment.js");
const pm = new THREE.PMREMGenerator(E.R); const env = pm.fromScene(new RoomEnvironment(), 0.04).texture;
const M = (color, metal = 0.2, rough = 0.5, ei = 0.5) => { const c = new THREE.Color(color); const l = c.r + c.g + c.b; if (l > 2.4) c.multiplyScalar(0.72); return new THREE.MeshStandardMaterial({ color: c, metalness: metal, roughness: rough, envMap: env, envMapIntensity: ei * 0.45 }); };
const fireTex = K.glowTex("rgba(255,190,110,1)"), smokeTex = K.glowTex("rgba(200,200,210,.55)");
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
// ================= Raketen-Szene =================
const scR = new THREE.Scene(); K.reseed(5); const st = K.stars(scR, 7000, -1, 20000, 1.6); const skyM = K.sky(scR, 0x02040a, 0x0a1a3a, 0x24406e, 15000);
scR.add(new THREE.AmbientLight(0x404858, 0.5)); const sunR = new THREE.DirectionalLight(0xfff2e0, 1.7); sunR.position.set(300, 200, 400); scR.add(sunR);
const flameLight = new THREE.PointLight(0xffaa55, 0, 300); scR.add(flameLight);
function mkVulcan() {
  const g = new THREE.Group(); const boost = new THREE.Group(), up = new THREE.Group(); g.add(boost); g.add(up);
  const b = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 33, 48), M(0xc77a3e, 0.1, 0.75, 0.3)); b.position.y = 16.5; boost.add(b);
  const ist = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 3, 48), M(0x1d1f24, 0.4, 0.5)); ist.position.y = 34.5; boost.add(ist);
  for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2; const s = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 20, 24), M(0xeef0f2, 0.1, 0.5)); s.position.set(Math.cos(a) * 3.5, 10, Math.sin(a) * 3.5); boost.add(s);
    const c = new THREE.Mesh(new THREE.ConeGeometry(0.8, 2.2, 24), M(0xeef0f2, 0.1, 0.5)); c.position.set(Math.cos(a) * 3.5, 21.1, Math.sin(a) * 3.5); boost.add(c); }
  for (const s of [-1, 1]) { const n = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 1.2, 2.4, 24, 1, true), M(0x2a2a2e, 0.7, 0.4)); n.position.set(s * 1.2, -1.1, 0); boost.add(n); }
  const cen = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 12, 48), M(0xf1f2f4, 0.1, 0.45)); cen.position.y = 42; up.add(cen);
  const fair = new THREE.Group(); fair.position.y = 48; up.add(fair);
  const halves = [0, 1].map((k) => { const h = new THREE.Group(); const cyl = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 10, 48, 1, true, k * Math.PI, Math.PI), M(0xf7f7f8, 0.05, 0.4)); cyl.position.y = 5; h.add(cyl);
    const top = new THREE.Mesh(new THREE.SphereGeometry(2.7, 48, 24, k * Math.PI, Math.PI, 0, Math.PI / 2), M(0xf7f7f8, 0.05, 0.4)); top.scale.y = 2.0; top.position.y = 10; h.add(top); fair.add(h); return h; });
  const sats = new THREE.Group(); fair.add(sats); for (let lv = 0; lv < 10; lv++) for (let s = 0; s < 4; s++) { const a = (s / 4) * Math.PI * 2 + 0.785; const m = new THREE.Mesh(new THREE.BoxGeometry(1.25, 1.05, 0.45), M(lv % 2 ? 0x2b3140 : 0x343a4a, 0.6, 0.35, 0.8)); m.position.set(Math.cos(a) * 1.75, 0.6 + lv * 1.2, Math.sin(a) * 1.75); m.rotation.y = -a; sats.add(m);
    const gp = new THREE.Mesh(new THREE.BoxGeometry(1.27, 0.12, 0.47), M(0xc89b3c, 0.9, 0.35, 0.8)); gp.position.copy(m.position).add(V(0, 0.45, 0)); gp.rotation.y = -a; sats.add(gp); }
  sats.visible = false; return { g, boost, up, halves, sats };
}
function mkAriane() {
  const g = new THREE.Group(); const c = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 30, 48), M(0xf3f4f6, 0.05, 0.5)); c.position.y = 15; g.add(c);
  const band = new THREE.Mesh(new THREE.CylinderGeometry(2.72, 2.72, 1.2, 48), M(0x1f2430, 0.3, 0.5)); band.position.y = 30.5; g.add(band);
  const u = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 6, 48), M(0xf3f4f6, 0.05, 0.5)); u.position.y = 34; g.add(u);
  const f = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 10, 48), M(0xfafafa, 0.05, 0.4)); f.position.y = 42; g.add(f); const ft = new THREE.Mesh(new THREE.SphereGeometry(2.7, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), M(0xfafafa, 0.05, 0.4)); ft.scale.y = 2; ft.position.y = 47; g.add(ft);
  for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2 + 0.78; const s = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 15, 32), M(0xd8dbe0, 0.1, 0.5)); s.position.set(Math.cos(a) * 4.2, 7.5, Math.sin(a) * 4.2); g.add(s); const k = new THREE.Mesh(new THREE.ConeGeometry(1.5, 4, 32), M(0xd8dbe0, 0.1, 0.5)); k.position.set(Math.cos(a) * 4.2, 17, Math.sin(a) * 4.2); g.add(k); }
  return { g };
}
const VU = mkVulcan(); scR.add(VU.g); const AR = mkAriane(); scR.add(AR.g); AR.g.visible = false;
const flames = []; for (let i = 0; i < 22; i++) flames.push(K.sprite(scR, fireTex, 10, V(0, 0, 0), 0));
const smoke = []; for (let i = 0; i < 40; i++) smoke.push(K.sprite(scR, smokeTex, 20, V(0, 0, 0), 0)); smoke.forEach((s) => (s.material.blending = THREE.NormalBlending));
function fire(base, power, t, len = 1) { flames.forEach((s, i) => { const k = i / flames.length; s.position.set(base.x + Math.sin(t * 40 + i) * 0.4, base.y - 1.5 - k * 28 * len * (0.5 + power * 0.5), base.z + Math.cos(t * 33 + i) * 0.4); s.scale.setScalar((13 - k * 8) * (0.5 + power * 0.6)); s.material.opacity = power * (1 - k) * 0.95; });
  flameLight.position.copy(base).add(V(0, -5, 6)); flameLight.intensity = power * 350; }
function trail(base, a, t) { smoke.forEach((s, i) => { const k = ((i / smoke.length) + t * 0.35) % 1; s.position.set(base.x + Math.sin(i * 7.3) * (2 + k * 14), base.y - 20 - k * 160, base.z + Math.cos(i * 3.1) * (2 + k * 14)); s.scale.setScalar(10 + k * 45); s.material.opacity = a * 0.35 * (1 - k); }); }
const boostO = new THREE.Object3D(); boostO.position.set(0, 16, 0); VU.boost.add(boostO);
const upO = new THREE.Object3D(); upO.position.set(0, 44, 0); VU.up.add(upO);

// ===== Zeiten =====
const tAm = W("am", 3.4), tAn = W("an", 7.4), tVier = W("vierzig", 8), tDoch = W("doch"), tSchief = W("schief"), tKamen = W("kamen"), tFolg = W("folg"), tDie = W("die", 20.3), tDah = W("dahinter"), tAnf = W("am", 25.5), tAber = W("aber", 27.4), tSie = W("sie", 31.9), tTrenn = W("trennte"), tObere = W("die", 35.3), tFehl = W("fehlende"), tFur = W("für", 40.4), tBaut = W("amazon", 46), tDafur = W("dafür"), tOben = W("oben", 53.8), tUnd = W("und", 56), tJetzt = W("jetzt"), tDer = W("der", 65.3), tAri = W("ariane"), tFrueh = W("frühestens"), tSechs = W("sechsunddreißig"), END = 74.9;
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
  flames.forEach((s) => (s.material.opacity = 0)); smoke.forEach((s) => (s.material.opacity = 0)); flameLight.intensity = 0;
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
    if (t < tSchief) { fire(V(0, 34, 0), 0.75, t, 0.6); VU.boost.visible = false; } else { fire(V(0, 34, 0), 0.75 * (1 - bad) * (Math.sin(t * 50) > 0 ? 1 : 0.3), t, 0.6); VU.boost.visible = false; }
    VU.g.rotation.z = fall * 1.6; VU.g.position.y = -fall * fall * 40; if (t > tSchief && t < tSchief + 0.35) E.grade.uniforms.flash.value = 0.25 * (1 - (t - tSchief) / 0.35);
    if (t > tSchief) E.look([1.12, 0.86, 0.84], [0.02, 0, 0], 0.35, 0.85);
    const f = prog(t, tDoch, tFolg - tDoch); pos = V(lerp(70, 85, f), lerp(50, 30, f), lerp(40, 60, f)); look = V(0, lerp(42, 30, f), 0); fov = 40; }
  else if (t < tAnf - 0.05) { scene = scR; space(); VU.boost.visible = true; const a = (t - tFolg) * 0.12 + 0.3; pos = V(Math.sin(a) * 90, 22, Math.cos(a) * 90); look = V(0, 26, 0); fov = 44; }
  else if (t < tObere - 0.05) { scene = scR; VU.boost.visible = true; const k = cl((t - tAnf) / 6); skyM.material.uniforms.m.value.setRGB(0.01, 0.02 * (1 - k), 0.07 * (1 - k * 0.6)); skyM.material.uniforms.h.value.setRGB(0.03, 0.07 * (1 - k * 0.5), 0.18 * (1 - k * 0.5));
    const weak = t > tAber ? 0.55 + 0.25 * Math.sin(t * 9) : 1; const sep = cl((t - tTrenn - 0.4) / 2.5);
    if (sep <= 0) { fire(V(0, -1, 0), weak, t); trail(V(0, -1, 0), weak, t); } else { VU.boost.position.y = -sep * sep * 50; VU.boost.rotation.z = sep * 0.5; fire(V(0, 34, 0), 0.8 * cl((sep - 0.15) * 4), t, 0.6); }
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
    fire(V(0, -1, 0), 1, t, 1.1); trail(V(0, -1, 0), 1, t); const f = prog(t, tDer, END - tDer); const a = -0.6 + f * 0.6; pos = V(Math.sin(a) * lerp(100, 125, f), lerp(-15, 10, f), Math.cos(a) * lerp(100, 125, f)); look = V(0, 24, 0); fov = 44; }
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
  WORDEL.style.top = (t >= 19.1 && t < 24.7) || (t >= tUnd && t < tJetzt) ? "300px" : "";
  word(wh, wa); cap(t);
};
