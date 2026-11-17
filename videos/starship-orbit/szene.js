const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(42);
const { RoomEnvironment } = await import("three/addons/environments/RoomEnvironment.js");
const pm = new THREE.PMREMGenerator(E.R); const env = pm.fromScene(new RoomEnvironment(), 0.04).texture;
const steel = new THREE.MeshStandardMaterial({ color: 0xa9afb8, metalness: 0.8, roughness: 0.38, envMap: env, envMapIntensity: 0.5 });
const tile = new THREE.MeshStandardMaterial({ color: 0x15161a, metalness: 0.1, roughness: 0.85, envMap: env, envMapIntensity: 0.3 });
const dark = new THREE.MeshStandardMaterial({ color: 0x2a2d33, metalness: 0.7, roughness: 0.55, envMap: env, envMapIntensity: 0.6 });
const flameMat = (c) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false });
// ---------- Starship (obere Stufe, 52 m) ----------
function makeShip() { const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 4.5, 38, 64), steel); body.position.y = 19; g.add(body);
  const hs = new THREE.Mesh(new THREE.CylinderGeometry(4.56, 4.56, 38, 64, 1, true, Math.PI * 0.5, Math.PI), tile); hs.position.y = 19; g.add(hs);
  const pts = []; for (let i = 0; i <= 24; i++) { const u = i / 24; pts.push(new THREE.Vector2(4.5 * Math.sqrt(1 - u * u * 0.96), u * 14)); }
  const nose = new THREE.Mesh(new THREE.LatheGeometry(pts, 64), steel); nose.position.y = 38; g.add(nose);
  const nh = new THREE.Mesh(new THREE.LatheGeometry(pts.map((p) => new THREE.Vector2(p.x + 0.06, p.y)), 64, Math.PI * 0.5, Math.PI), tile); nh.position.y = 38; g.add(nh);
  const fl = (y, w, h, s) => { const f = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.5), tile); f.position.set(s * (4.5 + w / 2 - 0.3), y, 0); g.add(f); };
  fl(6, 4.5, 10, 1); fl(6, 4.5, 10, -1); fl(43, 2.6, 6.5, 1); fl(43, 2.6, 6.5, -1);
  const eng = new THREE.Group(); g.add(eng); const fA = new THREE.Mesh(new THREE.ConeGeometry(3.2, 26, 32, 1, true), flameMat(0xffb070)); fA.rotation.x = Math.PI; fA.position.y = -13; eng.add(fA);
  const fB = new THREE.Mesh(new THREE.ConeGeometry(1.8, 16, 32, 1, true), flameMat(0xbfe0ff)); fB.rotation.x = Math.PI; fB.position.y = -8; eng.add(fB); const eg = K.sprite(eng, K.glowTex("rgba(255,180,90,.9)"), 40, V(0, -3, 0), 0.9);
  return { g, eng, flames: [fA, fB, eg] }; }
// ---------- Booster (71 m) ----------
function makeBooster() { const g = new THREE.Group(); const b = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 4.5, 71, 64), steel); b.position.y = 35.5; g.add(b);
  for (let i = 0; i < 4; i++) { const f = new THREE.Mesh(new THREE.BoxGeometry(5, 0.6, 3.6), dark); const a = (i * Math.PI) / 2 + Math.PI / 4; f.position.set(Math.cos(a) * 6.5, 68, Math.sin(a) * 6.5); f.rotation.y = -a; g.add(f); }
  const ring = new THREE.Mesh(new THREE.TorusGeometry(4.55, 0.25, 8, 64), dark); ring.rotation.x = Math.PI / 2; ring.position.y = 60; g.add(ring); return g; }

// ================= Startplatz (Nacht) =================
const scP = new THREE.Scene(); K.stars(scP, 6000, 0.02, 3000, 1.5).material.opacity = 0.7;
scP.add(new THREE.AmbientLight(0x3a4458, 0.9)); const moonL = new THREE.DirectionalLight(0xbcd0ff, 1.2); moonL.position.set(-200, 300, 200); scP.add(moonL);
const ground = new THREE.Mesh(new THREE.CircleGeometry(5000, 64), new THREE.MeshStandardMaterial({ color: 0x0b0d10, roughness: 0.95 })); ground.rotation.x = -Math.PI / 2; scP.add(ground);
K.sprite(scP, K.glowTex("rgba(255,150,80,.45)"), 2400, V(-600, -100, -2400), 0.45); K.sprite(scP, K.glowTex("rgba(90,120,200,.35)"), 3000, V(900, 0, -2600), 0.4);
// Turm ("Mechazilla")
const TX = -16, TH = 146; const tower = new THREE.Group(); tower.position.set(TX, 0, 0); scP.add(tower);
{ const bars = []; const S = 5.5; for (const [x, z] of [[-S, -S], [S, -S], [-S, S], [S, S]]) bars.push([x, TH / 2, z, 1.2, TH, 1.2]);
  for (let y = 4; y < TH; y += 6) { bars.push([0, y, -S, 2 * S, 0.6, 0.6], [0, y, S, 2 * S, 0.6, 0.6], [-S, y, 0, 0.6, 0.6, 2 * S], [S, y, 0, 0.6, 0.6, 2 * S]); }
  const im = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), dark, bars.length); const m4 = new THREE.Matrix4(); bars.forEach(([x, y, z, a, b, c], i) => { m4.compose(V(x, y, z), new THREE.Quaternion(), V(a, b, c)); im.setMatrixAt(i, m4); }); tower.add(im);
  // Diagonalen
  const dg = []; for (let y = 4; y < TH - 6; y += 6) for (const s of [-1, 1]) { dg.push([0, y + 3, s * S, s]); }
  const dm = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), dark, dg.length); dg.forEach(([x, y, z, s], i) => { m4.compose(V(x, y, z), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, Math.atan2(6, 2 * S) * (i % 2 ? 1 : -1))), V(Math.hypot(6, 2 * S), 0.4, 0.4)); dm.setMatrixAt(i, m4); }); tower.add(dm);
  for (let k = 0; k < 6; k++) K.sprite(tower, K.glowTex("rgba(255,235,200,.95)"), 7, V(S + 0.8, 20 + k * 22, (k % 2 ? 1 : -1) * S), 0.9); }
const AY = 100; const arms = [1, -1].map((s) => { const piv = new THREE.Group(); piv.position.set(TX + 6, AY, s * 5.6); scP.add(piv); const a = new THREE.Mesh(new THREE.BoxGeometry(32, 3.2, 1.6), dark); a.position.x = 16; piv.add(a); const rail = new THREE.Mesh(new THREE.BoxGeometry(32, 0.6, 0.4), steel); rail.position.set(16, -1.4, -s * 0.9); piv.add(rail); return { piv, s }; });
const carriage = new THREE.Mesh(new THREE.BoxGeometry(4, 8, 14), dark); carriage.position.set(TX + 6, AY, 0); scP.add(carriage);
const mount = new THREE.Mesh(new THREE.CylinderGeometry(9, 11, 20, 8), dark); mount.position.y = 10; scP.add(mount);
const SH = makeShip(); scP.add(SH.g); const BO = makeBooster(); scP.add(BO);
// Höhen-Vergleich
const mkLine = (y, col, op) => { const l = new THREE.Mesh(new THREE.PlaneGeometry(70, 0.5), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op, depthWrite: false, toneMapped: false })); l.position.set(18, y, 0); scP.add(l); return l; };
const l123 = mkLine(123, 0xffffff, 0), l93 = mkLine(93, 0xffd23f, 0); const o123 = new THREE.Object3D(); o123.position.set(42, 123, 0); scP.add(o123); const o93 = new THREE.Object3D(); o93.position.set(42, 93, 0); scP.add(o93);
// Meer + Booster-Explosion (weit weg)
const SEA = V(4000, 0, 0); const sea = new THREE.Mesh(new THREE.CircleGeometry(1500, 64), new THREE.MeshStandardMaterial({ color: 0x040a12, metalness: 0.2, roughness: 0.55 })); sea.rotation.x = -Math.PI / 2; sea.position.copy(SEA).add(V(0, 0.5, 0)); scP.add(sea);
const BO2 = makeBooster(); BO2.position.copy(SEA); scP.add(BO2); const boom = [K.sprite(scP, K.glowTex("rgba(255,200,120,1)"), 60, SEA, 0), K.sprite(scP, K.glowTex("rgba(255,110,40,.8)"), 120, SEA, 0), K.sprite(scP, K.glowTex("rgba(255,80,20,.5)"), 260, SEA, 0)];
const boomL = new THREE.PointLight(0xff9050, 0, 0, 0); scP.add(boomL);

// ================= Weltraum =================
const scE = new THREE.Scene(); K.stars(scE, 9000, -1, 30000, 1.7).material.opacity = 0.65;
scE.add(new THREE.AmbientLight(0x30303a, 0.5)); const sunD = new THREE.DirectionalLight(0xfff4e6, 2.6); sunD.position.set(600, 200, 400); scE.add(sunD);
const RE = 120; const EA = K.earth(scE, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(600, 200, 400).normalize();
const SS = makeShip(); SS.g.scale.setScalar(0.06); scE.add(SS.g); SS.flames.forEach((f) => (f.visible = false));
const orbitR = RE + 24; const orbitL = new THREE.Mesh(new THREE.TorusGeometry(orbitR, 0.12, 6, 256), new THREE.MeshBasicMaterial({ color: 0x9fd0ff, transparent: true, opacity: 0, depthWrite: false })); orbitL.rotation.x = Math.PI / 2 - 0.35; scE.add(orbitL);
const sats = []; for (let i = 0; i < 26; i++) { const s = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.012, 0.12), new THREE.MeshStandardMaterial({ color: 0x1b2a55, metalness: 0.6, roughness: 0.3, envMap: env })); s.visible = false; scE.add(s); sats.push(s); }
// Plasma beim Wiedereintritt
const plasma = [K.sprite(scE, K.glowTex("rgba(255,150,90,.95)"), 3, V(0, 0, 0), 0), K.sprite(scE, K.glowTex("rgba(255,90,170,.6)"), 7, V(0, 0, 0), 0)];
const trail = new THREE.Mesh(new THREE.ConeGeometry(1.2, 14, 32, 1, true), flameMat(0xff8a50)); trail.material.opacity = 0; scE.add(trail);
const moon = new THREE.Mesh(new THREE.SphereGeometry(32, 96, 64), new THREE.MeshStandardMaterial({ map: await tex("moon.jpg"), roughness: 1 })); moon.position.set(520, 140, -900); scE.add(moon);

// ===== Zeiten =====
const tAm = W("am"), tZum = W("zum"), tDie = W("die", 14), tHoe = W("höher"), tWas = W("was", 19.5), tDie2 = W("die", 25.2), tDabei = W("dabei"), tDann = W("dann", 36), tMit = W("mit", 39.2), tIhr = W("ihr", 43.9), tUnd = W("und", 47), tAber = W("aber", 52), tWarum = W("warum"), tUnd2 = W("und", 65.2);
label("Ship 42", SS.g, 2, { t0: tAm + 0.6, t1: tZum - 0.1, size: 56, gap: 20 });
label("Freiheitsstatue<small>93 m</small>", o93, 0, { t0: tHoe, t1: tWas - 0.1, size: 52, gap: 10 }); label("Starship<small>≈ 123 m</small>", o123, 0, { t0: tDie + 0.8, t1: tWas - 0.1, size: 52, gap: 10 });
label("Mond", moon, 32, { t0: tUnd2 + 1.2, t1: 71, size: 56, gap: 20 });

const placeOrbit = (obj, ang, tilt = 0.35) => { const p = V(Math.cos(ang) * orbitR, 0, Math.sin(ang) * orbitR).applyAxisAngle(V(1, 0, 0), -tilt); obj.position.copy(p); const v = V(-Math.sin(ang), 0, Math.cos(ang)).applyAxisAngle(V(1, 0, 0), -tilt); return { p, v }; };
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.28, 0.9);
  let scene = scP, pos, look, fov = 40;
  // Standard Startplatz
  SH.g.visible = true; BO.visible = false; mount.visible = false; SH.eng.visible = false; arms.forEach((a) => (a.piv.rotation.y = a.s * 0.65)); l123.material.opacity = 0; l93.material.opacity = 0; BO2.visible = false; boom.forEach((b) => (b.material.opacity = 0)); boomL.intensity = 0;
  SH.g.position.set(0, AY - 40, 0); SH.g.rotation.set(0, 0, 0);
  const catchAt = (t0, d) => { // Schiff sinkt, Arme schließen
    const f = K.eout(prog(t, t0, d * 0.75)); SH.g.position.y = lerp(AY + 160, AY - 40, f); SH.eng.visible = f < 0.995; SH.flames.forEach((x) => (x.scale.setScalar(1 + 0.08 * Math.sin(t * 40)))); const c = K.eio(prog(t, t0 + d * 0.62, d * 0.3)); arms.forEach((a) => (a.piv.rotation.y = a.s * lerp(0.65, 0.0, c))); };
  if (t < tAm - 0.05) { catchAt(0.2, tAm - 0.2); const f = prog(t, 0, tAm); pos = V(lerp(150, 120, f), lerp(60, 85, f), lerp(170, 150, f)); look = V(-5, lerp(140, 110, K.eio(f)), 0); }
  else if (t < tDie - 0.05) { scene = scE; SS.g.visible = true; const ang = 0.4 + (t - tAm) * 0.03; const { p, v } = placeOrbit(SS.g, ang); SS.g.quaternion.setFromUnitVectors(V(0, 1, 0), v.clone().normalize());
    const f = K.eio(prog(t, tAm, 3)); pos = p.clone().add(p.clone().normalize().multiplyScalar(lerp(40, 3, f))).add(v.clone().multiplyScalar(lerp(-60, -7, f))).add(p.clone().normalize().cross(v).normalize().multiplyScalar(lerp(10, 2.5, f))); look = p.clone().multiplyScalar(lerp(0.6, 1, f)); }
  else if (t < tWas - 0.05) { BO.visible = true; mount.visible = true; SH.g.position.set(0, 20 + 71, 0); BO.position.set(0, 20, 0);
    const f = K.eio(prog(t, tDie, 2)); l123.material.opacity = 0.6 * cl((t - tDie - 0.6) / 0.6); l93.material.opacity = 0.8 * cl((t - tHoe + 0.1) / 0.5); pos = V(lerp(60, 190, f), lerp(40, 80, f), lerp(120, 240, f)); look = V(0, lerp(60, 72, f), 0); }
  else if (t < tDie2 - 0.05) { BO.visible = true; mount.visible = true; SH.g.position.set(0, 91, 0); BO.position.set(0, 20, 0); const a = 0.6 + (t - tWas) * 0.07; pos = V(Math.sin(a) * 230, 50, Math.cos(a) * 230); look = V(0, 85, 0); E.look([1, 1, 1], [0, 0, 0], 0.35, 0.82); }
  else if (t < tDann - 0.05) { scene = scE; const ang = 1.0 + (t - tDie2) * 0.35; const { p, v } = placeOrbit(SS.g, ang); SS.g.quaternion.setFromUnitVectors(V(0, 1, 0), v.clone().normalize());
    if (t < tDabei - 0.05) { orbitL.material.opacity = 0.45 * cl((t - tDie2) / 0.8); const f = K.eio(prog(t, tDie2, 2.5)); pos = V(lerp(0, 120, f), lerp(60, 420, f), lerp(300, 330, f)); look = V(0, 0, 0); }
    else { orbitL.material.opacity = 0; sats.forEach((s, i) => { const td = tDabei + 0.3 + i * 0.12; s.visible = t > td; const d = Math.max(0, t - td); const side = p.clone().normalize().cross(v).normalize(); s.position.copy(p).add(side.clone().multiplyScalar(0.6 + d * 0.55)).add(v.clone().multiplyScalar(-d * 0.25 + (i % 5) * 0.02)).add(p.clone().normalize().multiplyScalar(((i % 3) - 1) * 0.08)); s.rotation.set(d * 0.5 + i, d * 0.7, i); });
      pos = p.clone().add(p.clone().normalize().multiplyScalar(2.5)).add(v.clone().multiplyScalar(-3.5)).add(p.clone().normalize().cross(v).normalize().multiplyScalar(6.5)); look = p.clone().add(p.clone().normalize().cross(v).normalize().multiplyScalar(1.2)); } }
  else if (t < tUnd - 0.05) { scene = scE; // Wiedereintritt über dem Erdrand
    const f = prog(t, tDann, tUnd - tDann); const ang = 1.45 + f * 0.25; const rr = lerp(RE + 14, RE + 9, f); const p = V(Math.cos(ang) * rr, 0, Math.sin(ang) * rr); const v = V(-Math.sin(ang), -0.08, Math.cos(ang)).normalize(); SS.g.position.copy(p);
    SS.g.up.copy(p.clone().normalize()); SS.g.lookAt(p.clone().add(v)); SS.g.rotateY(Math.PI / 2); SS.g.rotateZ(Math.PI / 2 - 0.3);
    const heat = cl((t - tMit + 0.5) / 2) * (0.75 + 0.25 * Math.sin(t * 23)); plasma.forEach((s, i) => { s.position.copy(p).add(v.clone().multiplyScalar(2)); s.scale.setScalar(i ? 18 : 8); s.material.opacity = heat * (i ? 0.7 : 1); });
    trail.scale.setScalar(1.2); trail.position.copy(p).add(v.clone().multiplyScalar(-9)); trail.quaternion.setFromUnitVectors(V(0, 1, 0), v); trail.material.opacity = 0.35 * heat;
    SS.g.scale.setScalar(0.15); pos = p.clone().add(p.clone().normalize().multiplyScalar(22)).add(v.clone().multiplyScalar(lerp(-34, -28, f))).add(p.clone().normalize().cross(v).normalize().multiplyScalar(-14)); look = p.clone().add(v.clone().multiplyScalar(6)).add(p.clone().normalize().multiplyScalar(-3)); E.look([1, 1, 1], [0, 0, 0], 0.55, 0.75);
    if (t >= tIhr - 0.05) E.look([1, 1, 1], [0.03, 0.01, 0], 0.7, 0.7); }
  else if (t < tAber - 0.05) { catchAt(tUnd - 0.6, 4.2); const f = prog(t, tUnd, tAber - tUnd); pos = V(lerp(120, 105, f), lerp(125, 115, f), lerp(170, 150, f)); look = V(-6, AY + 2, 0); }
  else if (t < tWarum - 0.05) { BO2.visible = true; const f = prog(t, tAber, tWarum - tAber); const fall = K.eio(cl(f / 0.55)); BO2.position.set(SEA.x, lerp(420, 15, fall), SEA.z); BO2.rotation.z = lerp(0.1, 0.9, fall);
    const fb = prog(t, tAber + (tWarum - tAber) * 0.55, 1.6); if (fb > 0) { BO2.visible = fb < 0.15; boom.forEach((b, i) => { b.material.opacity = 0.8 * Math.sin(Math.PI * Math.min(1, fb * (1 + i * 0.2))) * (1 - i * 0.25); b.position.copy(SEA).add(V(0, 30 + i * 20, 0)); b.scale.setScalar((22 + i * 26) * (0.4 + fb)); }); boomL.position.copy(SEA).add(V(0, 60, 0)); boomL.intensity = 12 * Math.sin(Math.PI * Math.min(1, fb)); E.grade.uniforms.flash.value = fb < 0.08 ? 0.25 : 0; }
    pos = SEA.clone().add(V(-420, 110, 680)); look = SEA.clone().add(V(0, lerp(250, 80, fall), 0)); SH.g.visible = false; E.look([1, 1, 1], [0, 0, 0], 0.15, 0.95); }
  else if (t < tUnd2 - 0.05) { arms.forEach((a) => (a.piv.rotation.y = 0)); const a = 2.2 + (t - tWarum) * 0.08; pos = V(Math.sin(a) * 120, 70, Math.cos(a) * 120); look = V(-6, 85, 0); E.look([1, 1, 1], [0, 0, 0], 0.4, 0.8); }
  else { scene = scE; const f = prog(t, tUnd2, 6); const p = V(lerp(160, 470, K.eio(f)), lerp(40, 125, K.eio(f)), lerp(-60, -820, K.eio(f))); SS.g.position.copy(p); const v = moon.position.clone().sub(p).normalize(); SS.g.quaternion.setFromUnitVectors(V(0, 1, 0), v); SS.eng.visible = true; SS.g.scale.setScalar(0.25);
    pos = p.clone().add(v.clone().multiplyScalar(-45)).add(V(5, 5, 4)); look = p.clone().add(v.clone().multiplyScalar(140)).add(V(0, 8, 0)); }
  if (scene === scE) { SS.g.scale.setScalar(t >= tUnd2 - 0.05 ? 0.25 : t >= tDann - 0.05 && t < tUnd - 0.05 ? 0.15 : 0.06); SS.eng.visible = t >= tUnd2 - 0.05; } else { sats.forEach((s) => (s.visible = false)); }
  if (!(t >= tDabei - 0.05 && t < tDann - 0.05)) sats.forEach((s) => (s.visible = false)); if (!(t >= tDann - 0.05 && t < tUnd - 0.05)) { plasma.forEach((s) => (s.material.opacity = 0)); trail.material.opacity = 0; }
  if (!(t >= tDie2 - 0.05 && t < tDabei - 0.05)) orbitL.material.opacity = 0;
  EA.group.rotation.y = t * 0.01; moon.rotation.y = t * 0.02;
  cam.fov = fov; cam.near = scene === scE ? 0.02 : 0.5; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tZum + 0.2, tDie - 0.1, "Erster Fang<div class='sub'>aus dem All · 14.11.2026</div>");
  seg(W("zweiundzwanzig") - 0.1, tDabei - 0.1, "≈ 22 Stunden<div class='sub'>≈ 14 Runden um die Erde</div>");
  seg(W("sechsundzwanzig") - 0.1, tDann - 0.1, "26 Starlink-Satelliten");
  seg(W("siebenundzwanzigtausend") - 0.1, tIhr - 0.1, "≈ 27.000 km/h"); seg(tIhr, tUnd - 0.1, "Hitzeschild: > 1.000 °C");
  seg(W("hielten") - 0.2, tAber - 0.1, "gefangen ✓");
  seg(W("untere") - 0.1, tWarum - 0.1, "Booster verloren<div class='sub'>33 Triebwerke</div>");
  seg(W("wenn") - 0.1, tUnd2 - 0.1, "wiederverwendbar<div class='sub'>= Raumfahrt viel billiger</div>");
  word(wh, wa); cap(t);
};
