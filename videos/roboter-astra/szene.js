const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(11);
const { RoomEnvironment } = await import("three/addons/environments/RoomEnvironment.js");
const pm = new THREE.PMREMGenerator(E.R); const env = pm.fromScene(new RoomEnvironment(), 0.04).texture;
const M = (color, metal = 0.2, rough = 0.5, ei = 0.5, o = {}) => { const c = new THREE.Color(color); if (c.r + c.g + c.b > 2.4) c.multiplyScalar(0.75); return new THREE.MeshStandardMaterial({ color: c, metalness: metal, roughness: rough, envMap: env, envMapIntensity: ei * 0.5, ...o }); };
const alu = M(0xc9ccd2, 0.85, 0.3, 1), strutM = M(0xe6e6e6, 0.1, 0.35, 0.8), darkM = M(0x2a2d33, 0.5, 0.45), goldM = M(0xd9a441, 0.95, 0.3, 1.2);
const glowStrut = new THREE.MeshBasicMaterial({ color: 0xffd23f, toneMapped: false }), ghostM = new THREE.MeshBasicMaterial({ color: 0x9fb4d0, transparent: true, opacity: 0.22, depthWrite: false });
const strut = (a, b, r, mat) => { const d = b.clone().sub(a); const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, d.length(), 10), mat); m.position.copy(a).add(b).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); return m; };
// Ring aus N Teilstücken (Fachwerk)
function ringBays(N, R, h, r, y = 0) { const bays = []; for (let i = 0; i < N; i++) { const g = new THREE.Group(); const a0 = (i / N) * Math.PI * 2, a1 = ((i + 1) / N) * Math.PI * 2;
    const p0 = V(Math.cos(a0) * R, y, Math.sin(a0) * R), p1 = V(Math.cos(a1) * R, y, Math.sin(a1) * R), q0 = p0.clone().setY(y + h), q1 = p1.clone().setY(y + h);
    const parts = [[p0, q0], [p0, p1], [q0, q1], [p0, q1], [p1, q1]].map(([a, b]) => strut(a, b, r, strutM)); parts.forEach((m) => g.add(m));
    [p0, p1, q0, q1].forEach((p) => { const j = new THREE.Mesh(new THREE.SphereGeometry(r * 2.2, 12, 8), alu); j.position.copy(p); g.add(j); });
    g.userData.parts = parts; bays.push(g); } return bays; }
const setMat = (bay, mat) => bay.userData.parts.forEach((m) => (m.material = mat));
// ================= Weltraum mit Erde (Bahn) =================
const scO = new THREE.Scene(); K.stars(scO, 9000, -1, 30000, 1.7).material.opacity = 0.65; scO.add(new THREE.AmbientLight(0x30303a, 0.6)); const sunO = new THREE.DirectionalLight(0xfff2e0, 2.2); sunO.position.set(-300, 200, 500); scO.add(sunO);
const RE = 100; const EA = K.earth(scO, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-0.5, 0.35, 0.8).normalize();
function mkSat(s = 1) { const g = new THREE.Group(); const b = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), goldM); g.add(b); const top = new THREE.Mesh(new THREE.BoxGeometry(2.05, 0.15, 2.05), alu); top.position.y = 1.05; g.add(top);
  for (const sx of [-1, 1]) { const p = new THREE.Mesh(new THREE.BoxGeometry(4, 0.08, 1.6), M(0x16264d, 0.6, 0.25, 1)); p.position.set(sx * 3.2, 0, 0); g.add(p); }
  const rg = ringBays(11, 1.8, 0.5, 0.04, 1.1); rg.slice(0, 3).forEach((x) => g.add(x)); g.scale.setScalar(s); return g; }
const sat = mkSat(1.4); scO.add(sat);
const link = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(0, 0, 1)]), new THREE.LineDashedMaterial({ color: 0x7fd0ff, dashSize: 3, gapSize: 2, transparent: true, opacity: 0, toneMapped: false })); scO.add(link);
const gsDot = K.sprite(scO, K.glowTex("rgba(255,215,110,1)"), 7, V(0, 0, 0), 0); const gsO = new THREE.Object3D(); scO.add(gsO);
const pulse = K.sprite(scO, K.glowTex("rgba(127,208,255,1)"), 4, V(0, 0, 0), 0);
// ================= Astra-Kiste (Meter) =================
const scB = new THREE.Scene(); K.reseed(4); K.stars(scB, 7000, -1, 20000, 1.6).material.opacity = 0.75; scB.add(new THREE.AmbientLight(0x50586a, 0.6)); scB.add(new THREE.HemisphereLight(0x8090b0, 0x202020, 0.3));
const sunB = new THREE.DirectionalLight(0xfff2e0, 2.4); sunB.position.set(-4, 5, 6); scB.add(sunB);
const EB = K.earth(scB, { day, night, topo }, 60); EB.group.children[EB.group.children.length - 1].scale.setScalar(0.93); EB.group.position.set(0, -95, -70); EB.U.sun.value = V(-0.4, 0.6, 0.7).normalize();
const box = new THREE.Group(); scB.add(box);
{ const c = [-0.5, 0.5]; for (const x of c) for (const z of c) box.add(strut(V(x, -0.5, z), V(x, 0.5, z), 0.02, darkM)); for (const y of c) for (const z of c) box.add(strut(V(-0.5, y, z), V(0.5, y, z), 0.02, darkM)); for (const y of c) for (const x of c) box.add(strut(V(x, y, -0.5), V(x, y, 0.5), 0.02, darkM));
  const back = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), M(0xd9a441, 0.95, 0.35, 1.2, { side: THREE.DoubleSide })); back.position.z = -0.5; box.add(back);
  const floor = new THREE.Mesh(new THREE.BoxGeometry(1, 0.03, 1), alu); floor.position.y = -0.5; box.add(floor);
  const plate = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.03, 40), M(0x3b4250, 0.6, 0.4)); plate.position.set(0.15, -0.3, 0); box.add(plate); }
// Fächer mit Stangen + Gelenken (links)
const rack = new THREE.Group(); rack.position.set(-0.36, -0.48, 0); box.add(rack);
for (let i = 0; i < 7; i++) rack.add(strut(V(-0.06 + (i % 2) * 0.05, 0.02 + i * 0.045, -0.3), V(-0.06 + (i % 2) * 0.05, 0.02 + i * 0.045, 0.3), 0.012, strutM));
for (let i = 0; i < 10; i++) { const j = new THREE.Mesh(new THREE.SphereGeometry(0.022, 12, 8), alu); j.position.set(0.06, 0.03 + (i % 5) * 0.05, -0.2 + Math.floor(i / 5) * 0.4); rack.add(j); }
// Portal-Arm (fährt in x/z, Stange in y)
const railM = alu; box.add(strut(V(-0.48, 0.45, -0.4), V(0.48, 0.45, -0.4), 0.018, railM)); box.add(strut(V(-0.48, 0.45, 0.4), V(0.48, 0.45, 0.4), 0.018, railM));
const bridge = new THREE.Group(); box.add(bridge); bridge.add(strut(V(0, 0.45, -0.42), V(0, 0.45, 0.42), 0.022, M(0x8a8f99, 0.7, 0.35)));
const carr = new THREE.Group(); bridge.add(carr); carr.add(new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.07, 0.09), darkM)); carr.children[0].position.y = 0.45;
const rod = new THREE.Group(); carr.add(rod); const rodM = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.6, 10), alu); rodM.position.y = 0.15; rod.add(rodM);
const grip = new THREE.Group(); grip.position.y = -0.15; rod.add(grip); for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.06, 0.03), darkM); f.position.set(s * 0.025, -0.03, 0); grip.add(f); }
const held = strut(V(-0.12, 0, 0), V(0.12, 0, 0), 0.012, strutM); grip.add(held); held.position.y = -0.07;
const armO = new THREE.Object3D(); grip.add(armO); const rackO = new THREE.Object3D(); rackO.position.set(0, 0.25, 0); rack.add(rackO);
const setArm = (x, y, z) => { bridge.position.x = x; carr.position.z = z; rod.position.y = y; };
// Antenne: Ring 11 Teile, Ø 1,4 m, oben um die Kiste
const RB = ringBays(11, 0.7, 0.22, 0.017, 0.52); RB.forEach((b) => box.add(b));
const ghost = ringBays(11, 0.7, 0.22, 0.009, 0.52); ghost.forEach((b) => { setMat(b, ghostM); b.children.forEach((m) => (m.material = ghostM)); box.add(b); });
const ringO = new THREE.Object3D(); ringO.position.set(0, 0.85, 0); box.add(ringO);
const dimA = new THREE.Object3D(); dimA.position.set(0, -0.5, 0.55); box.add(dimA); const dimB = new THREE.Object3D(); dimB.position.set(0.55, 0, 0.55); box.add(dimB); const dimC = new THREE.Object3D(); dimC.position.set(0.55, -0.5, 0); box.add(dimC);
// Zukunft: riesiges Teleskop/Antenne (eigene Szene-Gruppe im gleichen Raum, weit weg)
const big = new THREE.Group(); big.position.set(0, 0, -400); scB.add(big);
ringBays(48, 60, 6, 0.35).forEach((b) => big.add(b));
const dish = new THREE.Mesh(new THREE.SphereGeometry(140, 64, 16, 0, Math.PI * 2, 0, 0.45), M(0xd9b061, 0.95, 0.25, 1.3, { side: THREE.DoubleSide, transparent: true, opacity: 0.85 })); dish.position.y = -125; big.add(dish);
const bots = []; for (let i = 0; i < 6; i++) { const b = mkSat(1.3); big.add(b); bots.push(b); }
const sparks = []; for (let i = 0; i < 6; i++) sparks.push(K.sprite(big, K.glowTex("rgba(255,215,110,1)"), 10, V(0, 0, 0), 0));
// Falcon-9-artige Rakete
const scR = new THREE.Scene(); K.reseed(6); const stR = K.stars(scR, 7000, -1, 20000, 1.6); const skyR = K.sky(scR, 0x02040a, 0x0a1a3a, 0x24406e, 15000);
scR.add(new THREE.AmbientLight(0x404858, 0.5)); const sunR = new THREE.DirectionalLight(0xfff2e0, 1.6); sunR.position.set(300, 200, 400); scR.add(sunR);
const F9 = new THREE.Group(); scR.add(F9); { const c = new THREE.Mesh(new THREE.CylinderGeometry(1.85, 1.85, 42, 40), M(0xf2f2f2, 0.05, 0.45)); c.position.y = 21; F9.add(c); const is = new THREE.Mesh(new THREE.CylinderGeometry(1.86, 1.86, 4, 40), M(0x15161a, 0.3, 0.5)); is.position.y = 44; F9.add(is);
  const s2 = new THREE.Mesh(new THREE.CylinderGeometry(1.85, 1.85, 10, 40), M(0xf2f2f2, 0.05, 0.45)); s2.position.y = 51; F9.add(s2); const fa = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 1.85, 3, 40), M(0xf7f7f7, 0.05, 0.4)); fa.position.y = 57.5; F9.add(fa);
  const fb = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 2.6, 7, 40), M(0xf7f7f7, 0.05, 0.4)); fb.position.y = 62.5; F9.add(fb); const ft = new THREE.Mesh(new THREE.SphereGeometry(2.6, 40, 20, 0, Math.PI * 2, 0, Math.PI / 2), M(0xf7f7f7, 0.05, 0.4)); ft.scale.y = 2.1; ft.position.y = 66; F9.add(ft); }
const fireTex = K.glowTex("rgba(255,190,110,1)"), smokeTex = K.glowTex("rgba(200,200,210,.55)");
const flames = []; for (let i = 0; i < 22; i++) flames.push(K.sprite(scR, fireTex, 10, V(0, 0, 0), 0));
const smoke = []; for (let i = 0; i < 40; i++) smoke.push(K.sprite(scR, smokeTex, 20, V(0, 0, 0), 0)); smoke.forEach((s) => (s.material.blending = THREE.NormalBlending));
const fl = new THREE.PointLight(0xffaa55, 0, 300); scR.add(fl);
function fire(t) { flames.forEach((s, i) => { const k = i / flames.length; s.position.set(Math.sin(t * 40 + i) * 0.4, -1.5 - k * 26, Math.cos(t * 33 + i) * 0.4); s.scale.setScalar(11 - k * 6); s.material.opacity = (1 - k) * 0.95; }); fl.position.set(0, -5, 6); fl.intensity = 350;
  smoke.forEach((s, i) => { const k = ((i / smoke.length) + t * 0.35) % 1; s.position.set(Math.sin(i * 7.3) * (2 + k * 14), -20 - k * 160, Math.cos(i * 3.1) * (2 + k * 14)); s.scale.setScalar(10 + k * 45); s.material.opacity = 0.35 * (1 - k); }); }

// ===== Zeiten =====
const tZum = W("zum"), tOhne = W("ohne"), tUnd = W("und", 11), tFolg = W("folg"), tDer = W("der", 16.4), tGeb = W("gebaut"), tBez = W("bezahlt"), tIm = W("im", 25), tAstra = W("astra", 28), tDarin = W("darin"), tFach = W("fächer"), tArm = W("der", 36.5), tStueck = W("stück"), tDas = W("das", 41.8), tEins = W("eins"), tElf = W("elf"), tZwei = W("zwei", 47), tDritte = W("das", 49.8), tGanz = W("ganz", 52.5), tDrei = W("drei", 54.3), tKontakt = W("kontakt"), tFertig = W("fertig"), tDez = W("im", 63.2), tWarum = W("warum"), tRiesig = W("riesige"), tIn = W("in", 70.2), END = 74.9;
label("1 m", dimA, 0.02, { t0: tAstra + 0.8, t1: tDarin - 0.1, size: 46, gap: 14 }); label("1 m", dimB, 0.02, { t0: tAstra + 1.6, t1: tDarin - 0.1, size: 46, gap: 14 }); label("1 m", dimC, 0.02, { t0: W("tief") - 0.2, t1: tDarin - 0.1, size: 46, gap: 14 });
label("Greifarm", armO, 0.05, { t0: W("greifarm") - 0.1, t1: tFach - 0.1, size: 48, gap: 20 }); label("Stangen & Gelenke", rackO, 0.05, { t0: tFach - 0.1, t1: tArm - 0.1, size: 44, gap: 20 });
const satO = new THREE.Object3D(); sat.add(satO); label("Astra", satO, 3, { t0: tDer + 0.4, t1: tGeb - 0.1, size: 54, gap: 22 });
label("Bodenstation", gsO, 3, { t0: tDrei, t1: tFertig - 0.1, size: 44, gap: 18 });
const logo = (f, h = 110, bg = false) => bg ? `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>` : `<img src='assets/logos/${f}' style='height:${h}px;display:block;margin:0 auto 18px;filter:drop-shadow(0 6px 24px rgba(0,0,0,.8))'>`;
const WORDEL = document.getElementById("word");
// Bauablauf: Stange vom Fach zum Ring (Teil Nr. 3)
const target = V(Math.cos(2.5 / 11 * Math.PI * 2) * 0.7, 0.62, Math.sin(2.5 / 11 * Math.PI * 2) * 0.7);
function build(f) { // f 0..1
  const p0 = V(-0.36, -0.2, 0), up = V(-0.1, 0.2, 0.1), p1 = V(Math.max(-0.45, Math.min(0.45, target.x)), 0.1, Math.max(-0.4, Math.min(0.4, target.z)));
  let p; if (f < 0.35) p = p0.clone().lerp(up, K.eio(f / 0.35)); else p = up.clone().lerp(p1, K.eio((f - 0.35) / 0.65)); setArm(p.x, p.y, p.z); held.visible = true; }

renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.35, 0.85);
  let scene = scB, pos = V(2, 1, 3), look = V(0, 0, 0), fov = 40;
  EA.group.rotation.y = 1.9 + t * 0.012; EA.clouds.rotation.y = t * 0.004; EB.group.rotation.y = t * 0.01; EB.group.visible = !(t >= tDas - 0.05 && t < tWarum - 0.05); box.rotation.y = 0; big.visible = false;
  link.material.opacity = 0; gsDot.material.opacity = 0; pulse.material.opacity = 0; sparks.forEach((s) => (s.material.opacity = 0)); flames.forEach((s) => (s.material.opacity = 0)); smoke.forEach((s) => (s.material.opacity = 0));
  // Ring-Zustand: 2 Teile (Erde) + Teil 3 im All
  RB.forEach((b, i) => { b.visible = i < 3; setMat(b, strutM); }); ghost.forEach((b) => (b.visible = false)); held.visible = false; setArm(Math.sin(t * 0.9) * 0.25, 0.1 + Math.sin(t * 1.3) * 0.08, Math.cos(t * 0.7) * 0.2);
  // Satellit auf der Bahn
  const oa = 0.9 + t * 0.02; sat.position.set(Math.cos(oa) * 116, 30, Math.sin(oa) * 116); sat.rotation.set(0.3, -oa, 0.1);
  if (t < tZum - 0.05) { const f = prog(t, 0, tZum); const a = 0.7 - f * 0.4; pos = V(Math.sin(a) * lerp(5.2, 4.4, f), lerp(2.2, 1.7, f), Math.cos(a) * lerp(5.2, 4.4, f)); look = V(0, 0.2, 0); }
  else if (t < tUnd - 0.05) { const f = prog(t, tZum, 8.6 - tZum); build(f); if (f > 0.97) { RB[2].visible = true; held.visible = false; } else RB[2].visible = false; const a = 0.2 + f * 0.5; pos = V(Math.sin(a) * 2.9, 1.5, Math.cos(a) * 2.9); look = V(0, 0.2, 0); fov = 42; }
  else if (t < tFolg - 0.05) { big.visible = true; const f = prog(t, tUnd, tFolg - tUnd);
    bots.forEach((b, i) => { const a = (i / 6) * 6.283 + t * 0.12; b.position.set(Math.cos(a) * 64, 12 + Math.sin(t + i) * 3, Math.sin(a) * 64); b.rotation.y = -a; sparks[i].position.copy(b.position).add(V(0, -5, 0)); sparks[i].material.opacity = 0.5 + 0.5 * Math.sin(t * 9 + i * 2); });
    pos = V(lerp(-60, 40, f), lerp(130, 90, f), -400 + lerp(260, 230, f)); look = V(0, -10, -400); fov = 50; }
  else if (t < tIm - 0.05) { scene = scO; const f = prog(t, tFolg, tIm - tFolg); const sp = sat.position.clone(); const out = sp.clone().normalize(); const tg = V(-Math.sin(oa), 0, Math.cos(oa)); pos = sp.clone().add(tg.clone().multiplyScalar(lerp(-34, -28, f))).add(out.clone().multiplyScalar(lerp(10, 7, f))).add(V(0, 4, 0)); look = sp.clone().add(tg.multiplyScalar(6)).add(out.multiplyScalar(-4)); fov = 42; }
  else if (t < tAstra - 0.05) { scene = scR; const f = prog(t, tIm, tAstra - tIm); fire(t); const k = cl(f); skyR.material.uniforms.m.value.setRGB(lerp(0.04, 0.01, k), lerp(0.1, 0.02, k), lerp(0.23, 0.06, k)); const a = 0.4 + f * 0.4; pos = V(Math.sin(a) * 105, lerp(-10, 15, f), Math.cos(a) * 105); look = V(0, 30, 0); fov = 44; }
  else if (t < tArm - 0.05) { const f = prog(t, tAstra, tArm - tAstra); RB.forEach((b) => (b.visible = false)); const a = 0.55 - f * 0.3; pos = V(Math.sin(a) * lerp(3.4, 2.9, f), lerp(1.2, 0.9, f), Math.cos(a) * lerp(3.4, 2.9, f)); look = V(0, -0.05, 0); fov = 40; if (t > tFach) look = V(-0.15, -0.15, 0); }
  else if (t < tDas - 0.05) { RB[2].visible = false; const f = prog(t, tArm, tDas - tArm - 0.6); build(f); if (f >= 1) { RB[2].visible = true; setMat(RB[2], glowStrut); held.visible = false; } const a = 0.3 + f * 0.25; pos = V(Math.sin(a) * 2.6, 1.3, Math.cos(a) * 2.6); look = V(0, 0.2, 0); fov = 42; }
  else if (t < tZwei - 0.05) { ghost.forEach((b) => (b.visible = true)); RB.forEach((b) => (b.visible = false)); const n = t >= tElf ? 11 : 0; ghost.forEach((b, i) => { if (t >= tElf && t > tElf + i * 0.08) { setMat(b, glowStrut); b.children.forEach((m) => { if (!b.userData.parts.includes(m)) m.material = alu; }); } else { b.children.forEach((m) => (m.material = ghostM)); } });
    box.rotation.y = t * 0.15; const f = prog(t, tDas, tZwei - tDas); pos = V(0, lerp(3.6, 3.2, f), lerp(2.6, 2.3, f)); look = V(0, 0.2, 0); fov = 44; }
  else if (t < tGanz - 0.05) { ghost.forEach((b, i) => { b.visible = i >= 3; b.children.forEach((m) => (m.material = ghostM)); }); RB.forEach((b, i) => (b.visible = i < 2 || (i === 2 && t > tDritte + 0.5)));
    if (t > tDritte + 0.5) setMat(RB[2], glowStrut); box.rotation.y = 0.4 + (t - tZwei) * 0.06; const f = prog(t, tZwei, tGanz - tZwei); pos = V(lerp(0.9, 0.3, f), lerp(2.8, 2.5, f), lerp(2.6, 2.3, f)); look = V(0, 0.35, 0); fov = 42; }
  else if (t < tFertig - 0.05) { scene = scO; EA.group.rotation.y = 1.9 + tGanz * 0.012; const gs = EA.ll(34.1, -118.1, RE * 1.005); { const n0 = gs.clone().normalize(); const sd = V(0, 1, 0).cross(n0).normalize(); sat.position.copy(n0.clone().multiplyScalar(122).add(sd.multiplyScalar(30))); } gsDot.position.copy(gs); gsO.position.copy(gs); gsDot.material.opacity = cl((t - tGanz) / 0.5); const sp = sat.position;
    link.geometry.setFromPoints([gs, sp.clone()]); link.computeLineDistances(); const on = t > tKontakt ? (Math.sin(t * 2.2) > -0.2 ? 1 : 0) : 1; link.material.opacity = 0.85 * cl((t - tGanz - 0.6) / 0.5) * on;
    const k = ((t * 0.7) % 1); pulse.position.copy(gs.clone().lerp(sp, t > tDrei + 1.5 && Math.floor(t * 0.7) % 2 ? 1 - k : k)); pulse.material.opacity = link.material.opacity;
    const f = prog(t, tGanz, tFertig - tGanz); const mid = gs.clone().lerp(sp, 0.5); const n = mid.clone().normalize(); pos = n.clone().multiplyScalar(lerp(430, 400, f)).add(V(0, lerp(30, 50, f), 0)); look = mid.clone().multiplyScalar(0.55); fov = 40; }
  else if (t < tWarum - 0.05) { ghost.forEach((b, i) => { b.visible = i >= 3; b.children.forEach((m) => (m.material = ghostM)); }); RB.forEach((b, i) => (b.visible = i < 3)); box.rotation.y = 0.8 + (t - tFertig) * 0.1; if (t > tDez) E.look([0.9, 0.92, 1.05], [0, 0, 0], 0.35, 0.85);
    const f = prog(t, tFertig, tWarum - tFertig); pos = V(0, lerp(3.2, 3.6, f), lerp(2.4, 2.8, f)); look = V(0, 0.2, 0); fov = 42; }
  else { big.visible = true; bots.forEach((b, i) => { const a = (i / 6) * 6.283 + t * 0.12; b.position.set(Math.cos(a) * 64, 12 + Math.sin(t + i) * 3, Math.sin(a) * 64); b.rotation.y = -a; sparks[i].position.copy(b.position).add(V(0, -5, 0)); sparks[i].material.opacity = t > tIn ? 0.5 + 0.5 * Math.sin(t * 9 + i * 2) : 0; });
    const f = prog(t, tWarum, END - tWarum); const a = -0.5 + f * 0.8; pos = V(Math.sin(a) * lerp(300, 240, f), lerp(160, 110, f), -400 + Math.cos(a) * lerp(300, 240, f)); look = V(0, -20, -400); fov = 48; }
  cam.fov = fov; cam.near = 0.05; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tZum + 0.2, tOhne - 0.1, "Zum ersten Mal"); seg(tOhne - 0.1, 8.6, "🧑‍🚀 ohne Astronauten");
  seg(tUnd + 0.2, tFolg - 0.1, "🏗️ Bauen im All");
  seg(tDer, tGeb - 0.1, "🤖 Astra"); seg(tGeb, tBez - 0.1, logo("caltech.svg", 70, true) + "<div class='sub'>Uni in Kalifornien</div>"); seg(tBez, tIm - 0.1, "<span style='font-size:120px;letter-spacing:8px'>DARPA</span><div class='sub'>Forschung des US-Militärs</div>");
  seg(tIm, tAstra - 0.1, logo("spacex.svg", 50, true) + "März 2026");
  seg(tAstra + 0.5, tDarin - 0.1, "📦 etwa 1 × 1 × 1 m"); seg(tArm, tDas - 0.1, "Stück für Stück");
  seg(tDas, tElf - 0.1, "📡 Antenne<div class='sub'>Ø 1,4 m</div>"); seg(tElf, tZwei - 0.1, "11 Teilstücke");
  seg(tZwei, tDritte - 0.1, "2 auf der Erde gebaut"); seg(tDritte, tGanz - 0.1, "<span class='y'>Nr. 3 im All ✓</span>");
  seg(tDrei, tKontakt - 0.1, "👨‍🔬 3 Forscher<div class='sub'>Befehle & Fotos</div>"); seg(tKontakt, tFertig - 0.1, "📡 ein paar Mal am Tag<div class='sub'>je ≈ 15 Minuten</div>");
  seg(tFertig, tWarum - 0.1, "nicht fertig<div class='sub'>Mission endet im Dezember</div>");
  seg(tRiesig, tIn - 0.1, "zu groß für jede Rakete"); seg(tIn, END, "🤖 Roboter bauen oben");
  WORDEL.style.top = t >= 15.3 && t < 20.8 ? "300px" : "";
  word(wh, wa); cap(t);
};
