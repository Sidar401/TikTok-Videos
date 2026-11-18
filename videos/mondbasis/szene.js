const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(21);
E.R.shadowMap.enabled = true; E.R.shadowMap.type = THREE.PCFSoftShadowMap;
const moonTex = await tex("moon.jpg");
const { RoomEnvironment } = await import("three/addons/environments/RoomEnvironment.js");
const pm = new THREE.PMREMGenerator(E.R); const env = pm.fromScene(new RoomEnvironment(), 0.04).texture;
// ================= Mond als Kugel =================
const scM = new THREE.Scene(); K.stars(scM, 9000, -1, 30000, 1.7).material.opacity = 0.65; scM.add(new THREE.AmbientLight(0x3a3a44, 0.35));
const sunM = new THREE.DirectionalLight(0xfff4e6, 3.0); sunM.position.set(-260, 40, 500); scM.add(sunM);
const RM = 100; const moon = new THREE.Mesh(new THREE.SphereGeometry(RM, 192, 128), new THREE.MeshStandardMaterial({ map: moonTex, roughness: 1, metalness: 0 })); scM.add(moon);
const poleO = new THREE.Object3D(); poleO.position.set(0, -RM * 1.0, 0); moon.add(poleO);
K.reseed(3); const mIP = [], mIceG = []; for (let k = 0; k < 900; k++) { const la = (-84 - Math.pow(K.rnd(), 0.7) * 5.8) * Math.PI / 180, lo = K.rnd() * 6.283; const r = RM * 1.002; mIP.push(Math.cos(la) * Math.cos(lo) * r, Math.sin(la) * r, Math.cos(la) * Math.sin(lo) * r); }
const mIGeo = new THREE.BufferGeometry(); mIGeo.setAttribute("position", new THREE.Float32BufferAttribute(mIP, 3)); const mIce = new THREE.Points(mIGeo, new THREE.PointsMaterial({ color: 0xa8ddff, size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); moon.add(mIce);
for (let k = 0; k < 6; k++) { const la = (-86 - K.rnd() * 3) * Math.PI / 180, lo = K.rnd() * 6.283; mIceG.push(K.sprite(moon, K.glowTex("rgba(120,190,255,.6)"), 2.5 + K.rnd() * 2, V(Math.cos(la) * Math.cos(lo) * RM, Math.sin(la) * RM, Math.cos(la) * Math.sin(lo) * RM), 0)); }
mIceG.forEach((g) => { g.material.depthTest = false; g.material.depthWrite = false; }); const iceM = new THREE.Object3D(); iceM.position.set(0, -RM, 0); moon.add(iceM);
const poleDot = K.sprite(moon, K.glowTex("rgba(255,215,110,1)"), 8, V(0, -RM * 1.01, 0), 0);
const EAF = K.earth(scM, { day, night, topo }, 36); EAF.group.children[EAF.group.children.length - 1].scale.setScalar(0.93); EAF.group.position.set(700, 200, -1800); EAF.U.sun.value = V(-1, 0.1, 0.6).normalize();
// ================= Erde (USA) =================
const scE = new THREE.Scene(); K.stars(scE, 9000, -1, 30000, 1.7).material.opacity = 0.6; scE.add(new THREE.AmbientLight(0x30303a, 0.5));
const RE = 100; const EA = K.earth(scE, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(0.3, 0.3, 1).normalize();
const usaDot = K.sprite(scE, K.glowTex("rgba(255,215,110,1)"), 7, V(0, 0, 0), 0);
// ================= Mondoberfläche am Südpol =================
const scS = new THREE.Scene(); K.reseed(4); K.stars(scS, 9000, 0.0, 30000, 1.6).material.opacity = 0.8;
scS.add(new THREE.AmbientLight(0x4a5060, 0.22)); scS.add(new THREE.HemisphereLight(0x8090b0, 0x202020, 0.12));
const sun = new THREE.DirectionalLight(0xfff2e0, 3.2); sun.position.set(-1600, 120, -700); sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096);
Object.assign(sun.shadow.camera, { left: -1100, right: 1100, top: 1100, bottom: -1100, near: 10, far: 4500 }); sun.shadow.bias = -0.0008; scS.add(sun); scS.add(sun.target);
const CR = { x: 520, z: -620, r: 330, d: 70 }; // großer dunkler Krater
const craters = [[CR.x, CR.z, CR.r, CR.d]]; for (let i = 0; i < 90; i++) craters.push([(K.rnd() - 0.5) * 3000, (K.rnd() - 0.5) * 3000, 8 + Math.pow(K.rnd(), 3) * 140, 0]);
const hN = (x, z) => 6 * Math.sin(x * 0.004 + 1) * Math.cos(z * 0.0035) + 3 * Math.sin(x * 0.013 + z * 0.011) + 1.2 * Math.sin(x * 0.05 - z * 0.04);
const height = (x, z) => { let h = hN(x, z); for (const [cx, cz, r, dd] of craters) { const d = Math.hypot(x - cx, z - cz) / r; const depth = dd || r * 0.28; if (d < 1) h -= depth * (1 - d * d) * 0.9; else if (d < 1.5) h += depth * 0.22 * Math.pow(1 - (d - 1) / 0.5, 2); } return h; };
{ const N = 420, S = 9000; const g = new THREE.PlaneGeometry(S, S, N, N); g.rotateX(-Math.PI / 2); const pa = g.attributes.position; const col = []; const nC = K.noiseCanvas(512, 512, 8, 6, 0.5, 0.7); const nd = nC.getContext("2d").getImageData(0, 0, 512, 512).data;
  for (let i = 0; i < pa.count; i++) { const x = pa.getX(i), z = pa.getZ(i); const edge = 1 - cl((Math.max(Math.abs(x), Math.abs(z)) - 2600) / 1500); pa.setY(i, height(x, z) * edge); const u = Math.floor(((x / S + 0.5) * 2048) % 512), v = Math.floor(((z / S + 0.5) * 2048) % 512); const n = nd[(v * 512 + u) * 4] / 255; const c = 0.42 + n * 0.22; col.push(c, c, c * 1.02); }
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3)); g.computeVertexNormals();
  const ground = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 1, metalness: 0 })); ground.receiveShadow = true; ground.castShadow = true; scS.add(ground); }
// Eis im Krater (glitzernde Punkte)
const NI = 1600; const ip = []; for (let i = 0; i < NI; i++) { const a = K.rnd() * 6.283, r = Math.sqrt(K.rnd()) * CR.r * 0.62; const x = CR.x + Math.cos(a) * r, z = CR.z + Math.sin(a) * r; ip.push(x, height(x, z) + 0.6, z); }
const iGeo = new THREE.BufferGeometry(); iGeo.setAttribute("position", new THREE.Float32BufferAttribute(ip, 3));
const ice = new THREE.Points(iGeo, new THREE.PointsMaterial({ color: 0x9fd8ff, size: 2.6, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); scS.add(ice);
const iceGlow = K.sprite(scS, K.glowTex("rgba(120,190,255,.35)"), CR.r * 1.3, V(CR.x, height(CR.x, CR.z) + 4, CR.z), 0);
const iceO = new THREE.Object3D(); iceO.position.set(CR.x, height(CR.x, CR.z) + 5, CR.z); scS.add(iceO);
// Basis
const white = new THREE.MeshStandardMaterial({ color: 0xe9ebee, metalness: 0.1, roughness: 0.55, envMap: env, envMapIntensity: 0.4 });
const gold = new THREE.MeshStandardMaterial({ color: 0xc89b3c, metalness: 0.9, roughness: 0.35, envMap: env, envMapIntensity: 0.7 });
const dark = new THREE.MeshStandardMaterial({ color: 0x2a2d33, metalness: 0.5, roughness: 0.5, envMap: env, envMapIntensity: 0.4 });
const panelM = new THREE.MeshStandardMaterial({ color: 0x14244a, metalness: 0.6, roughness: 0.25, envMap: env, envMapIntensity: 0.8, side: THREE.DoubleSide });
const base = new THREE.Group(); scS.add(base); const BX = -60, BZ = 40; base.position.set(BX, height(BX, BZ), BZ);
const cast = (m) => { m.castShadow = true; m.receiveShadow = true; return m; };
const hab = (x, z, ry, L = 22) => { const g = new THREE.Group(); const c = cast(new THREE.Mesh(new THREE.CylinderGeometry(4.2, 4.2, L, 40), white)); c.rotation.z = Math.PI / 2; g.add(c);
  for (const s of [-1, 1]) { const e = cast(new THREE.Mesh(new THREE.SphereGeometry(4.2, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), white)); e.rotation.z = (s * -Math.PI) / 2; e.position.x = (s * L) / 2; g.add(e); }
  const band = new THREE.Mesh(new THREE.CylinderGeometry(4.3, 4.3, 1.2, 40), gold); band.rotation.z = Math.PI / 2; g.add(band); for (const s of [-1, 1]) { const leg = cast(new THREE.Mesh(new THREE.BoxGeometry(1, 3, 6), dark)); leg.position.set(s * L * 0.3, -4.4, 0); g.add(leg); }
  g.position.set(x, 5.6, z); g.rotation.y = ry; base.add(g); return g; };
hab(0, 0, 0); hab(10, 18, Math.PI / 2, 16); hab(-26, 6, 0.3, 18);
{ const dome = cast(new THREE.Mesh(new THREE.SphereGeometry(10, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), white)); dome.position.set(24, 0, -10); base.add(dome); const r = new THREE.Mesh(new THREE.TorusGeometry(10, 0.5, 12, 48), gold); r.rotation.x = Math.PI / 2; r.position.copy(dome.position); base.add(r); }
const panels = []; for (let i = 0; i < 4; i++) { const g = new THREE.Group(); const mast = cast(new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.7, 34, 12), dark)); mast.position.y = 17; g.add(mast);
  const p = cast(new THREE.Mesh(new THREE.BoxGeometry(10, 22, 0.4), panelM)); p.position.y = 24; g.add(p); g.position.set(-100 + i * 14, 0, 22); g.lookAt(V(-1600, 0, -700).add(g.position)); base.add(g); panels.push(g); }
const lights = []; [[0, 10, 0], [10, 10, 18], [-26, 10, 6], [24, 11, -10]].forEach((p) => lights.push(K.sprite(base, K.glowTex("rgba(255,220,160,1)"), 2.4, V(...p), 0.9)));
// Atomkraftwerk (klein, etwas abseits)
const reactor = new THREE.Group(); scS.add(reactor); const RX = -190, RZ = 150; reactor.position.set(RX, height(RX, RZ), RZ);
{ const core = cast(new THREE.Mesh(new THREE.CylinderGeometry(3.2, 3.6, 10, 32), white)); core.position.y = 5; reactor.add(core); const top = cast(new THREE.Mesh(new THREE.ConeGeometry(3.2, 4, 32), gold)); top.position.y = 12; reactor.add(top);
  for (let i = 0; i < 4; i++) { const f = cast(new THREE.Mesh(new THREE.BoxGeometry(0.3, 9, 12), new THREE.MeshStandardMaterial({ color: 0x9aa0aa, metalness: 0.6, roughness: 0.4, envMap: env, envMapIntensity: 0.5 }))); const a = (i / 4) * Math.PI * 2 + 0.4; f.position.set(Math.cos(a) * 9, 7, Math.sin(a) * 9); f.rotation.y = -a; reactor.add(f); } }
const rGlow = K.sprite(reactor, K.glowTex("rgba(120,200,255,.8)"), 10, V(0, 6, 0), 0);
const cable = new THREE.Line(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 40 }, (_, i) => { const f = i / 39; const x = lerp(RX, BX - 20, f), z = lerp(RZ, BZ + 6, f); return V(x, height(x, z) + 0.6, z); })), new THREE.LineBasicMaterial({ color: 0x7fd0ff, transparent: true, opacity: 0, toneMapped: false })); scS.add(cable);
// Erde knapp über dem Horizont
const EAH = K.earth(scS, { day, night, topo }, 60); EAH.group.children[EAH.group.children.length - 1].scale.setScalar(0.93); EAH.group.position.set(500, 90, 2600); EAH.U.sun.value = V(-1, 0.05, -0.4).normalize();

// ===== Zeiten =====
const tAm = W("am", 5.3), tMit = W("mitmachen"), tFolg = W("folg"), tTeams = W("teams"), tDenn = W("denn"), tDort = W("dort"), tAber = W("aber", 38.7), tDen = W("den", 45.2), tErst = W("erst"), tBis = W("bis", 53.5), tIns = W("insgesamt"), tAnm = W("anmelden"), tViel = W("vielleicht");
label("Südpol", poleO, 6, { t0: tDenn + 0.6, t1: tDort - 0.1, size: 56, gap: 24 });
label("Eis", iceM, 3, { t0: W("eis") - 0.1, t1: tAber - 0.1, size: 56, gap: 10 });
label("Atomkraftwerk", reactor, 16, { t0: W("atomkraftwerk") - 0.2, t1: tIns - 0.1, size: 50, gap: 16 });
label("Basis", base, 22, { t0: W("basis", 28.8) - 0.1, t1: tDenn + 0.3, size: 52, gap: 16 });
const usaO = new THREE.Object3D(); scE.add(usaO); label("USA", usaO, 3, { t0: W("nur", 12.2) - 0.1, t1: tFolg + 0.4, size: 56, gap: 16 });
const items = [["strom", "⚡ Strom"], ["bauen", "🏗️ Bauen"], ["luft", "💧 Luft & Wasser"], ["fahrzeuge", "🚙 Fahrzeuge"], ["funk", "📡 Funk"], ["sicherheit", "🧑‍🚀 Sicherheit"]].map(([k, h]) => [W(k, 19), h]);

renderAt = (t) => {
  sun.position.set(-1600, 120, -700);
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.35, 0.85);
  mIce && (mIce.material.opacity = 0); mIceG.forEach((g) => (g.material.opacity = 0));
  let scene = scM, pos = V(0, 0, 300), look = V(0, 0, 0), fov = 40; poleDot.material.opacity = 0; usaDot.material.opacity = 0; ice.material.opacity = 0; iceGlow.material.opacity = 0; rGlow.material.opacity = 0; cable.material.opacity = 0;
  moon.rotation.y = t * 0.01; EAH.group.rotation.y = 2.0 + t * 0.01;
  if (t < tAm - 0.05) { const f = K.eio(prog(t, 0, tAm)); pos = V(lerp(90, 120, f), lerp(-60, -20, f), lerp(170, 300, f)); look = V(lerp(-10, 0, f), lerp(-50, 0, f), 0); fov = 40; }
  else if (t < tMit - 0.05) { const f = K.eio(prog(t, tAm, tMit - tAm)); pos = V(lerp(120, 40, f), lerp(-20, 30, f), lerp(300, 340, f)); look = V(0, lerp(0, 40, f), 0); }
  else if (t < tFolg - 0.05) { scene = scE; const us = EA.ll(39, -98, RE * 1.01); usaO.position.copy(us); usaDot.position.copy(us); usaDot.material.opacity = cl((t - W("nur", 12.2)) / 0.4); const c = EA.ll(30, -95, RE).normalize(); const f = K.eio(prog(t, tMit, tFolg - tMit)); pos = c.multiplyScalar(lerp(420, 360, f)); look = V(0, 0, 0); }
  else if (t < tTeams - 0.05 + 1.2) { const a = (t - tFolg) * 0.05; pos = V(Math.sin(a) * 330, 40, Math.cos(a) * 330); look = V(0, 20, 0); }
  else if (t < tDenn - 0.05) { scene = scS; const f = prog(t, tTeams + 1.2, tDenn - tTeams - 1.2); const a = -0.9 + f * 1.1; const c = base.position.clone(); pos = c.clone().add(V(Math.sin(a) * lerp(150, 110, f), lerp(60, 34, f), Math.cos(a) * lerp(150, 110, f))); look = c.clone().add(V(0, 6, 0)); fov = 42;
    const hot = items.findIndex((it, i) => t >= it[0] - 0.1 && (i === 5 || t < items[i + 1][0] - 0.1)); if (hot === 0) rGlow.material.opacity = 0.7; }
  else if (t < tDort - 0.05) { const f = K.eio(prog(t, tDenn, tDort - tDenn)); poleDot.material.opacity = cl((t - tDenn - 0.5) / 0.5) * (0.8 + 0.2 * Math.sin(t * 6)); pos = V(lerp(40, 60, f), lerp(-160, -250, f), lerp(300, 150, f)); look = V(0, lerp(-30, -80, f), 0); fov = 40; }
  else if (t < tDen - 0.05) { const iOn = cl((t - W("eis") + 0.2) / 0.8); mIce.material.opacity = 0.95 * iOn * (0.85 + 0.15 * Math.sin(t * 7)); mIceG.forEach((g) => (g.material.opacity = 0.5 * iOn)); moon.rotation.y = tDort * 0.01; const f = K.eio(prog(t, tDort, tDen - tDort));
    pos = V(lerp(70, 30, f), lerp(-200, -150, f), lerp(140, 70, f)); look = V(0, -RM * 0.92, 0); fov = 36; if (t > tAber) E.look([0.86, 0.95, 1.12], [0, 0, 0], 0.35, 0.85); }
  else if (t < tIns - 0.05) { scene = scS; const on = cl((t - W("atomkraftwerk") + 0.2) / 0.8); rGlow.material.opacity = on * (0.7 + 0.3 * Math.sin(t * 4)); cable.material.opacity = on * 0.8; const f = prog(t, tDen, tIns - tDen); const c = reactor.position.clone().lerp(base.position, 0.35);
    const rp = reactor.position.clone(); const a = 0.5 + f * 0.5; pos = rp.clone().add(V(Math.sin(a) * lerp(55, 80, f), lerp(16, 26, f), Math.cos(a) * lerp(55, 80, f))); look = rp.clone().add(V(0, 7, 0)); fov = 42; }
  else if (t < tAnm - 0.05) { poleDot.material.opacity = 0.9; const f = K.eio(prog(t, tIns, tAnm - tIns)); pos = V(lerp(60, 200, f), lerp(-250, -120, f), lerp(150, 260, f)); look = V(0, lerp(-80, -20, f), 0); }
  else { scene = scS; const f = K.eio(prog(t, tAnm, 69 - tAnm)); const c = base.position.clone(); const dir = c.clone().sub(EAH.group.position).setY(0).normalize(); pos = c.clone().add(dir.multiplyScalar(lerp(110, 150, f))).add(V(0, lerp(30, 24, f), 0)); look = c.clone().add(V(0, 10, 0)).lerp(EAH.group.position, lerp(0.03, 0.06, f)); fov = 44; }
  if (scene === scS) pos.y = Math.max(pos.y, height(pos.x, pos.z) + 10);
  cam.fov = fov; cam.near = 0.5; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tAm, tMit - 0.1, "<img src='assets/logos/nasa.svg' style='height:150px;display:block;margin:0 auto 14px'>Wettbewerb<div class='sub'>seit 8. November</div>");
  seg(tMit, W("nur", 12.2) - 0.1, "🎓 Schüler & Studenten"); seg(W("nur", 12.2) - 0.1, tFolg - 0.1, "nur aus den USA");
  seg(tTeams, items[0][0] - 0.1, "Teams: 2–5 Leute<div class='sub'>6 Probleme</div>");
  items.forEach((it, i) => seg(it[0] - 0.1, i < 5 ? items[i + 1][0] - 0.1 : tDenn - 0.1, `${it[1]}<div class='sub'>${i + 1} / 6</div>`));
  seg(W("echte") - 0.1, tDort - 0.1, "Basis am Südpol");
  seg(W("wasser", 34.5) - 0.1, W("atemluft") - 0.1, "💧 Wasser"); seg(W("atemluft") - 0.1, W("raketentreibstoff") - 0.1, "🫁 Atemluft"); seg(W("raketentreibstoff") - 0.1, tAber - 0.1, "🚀 Treibstoff");
  seg(W("minus") - 0.4, tDen - 0.1, `<span style="color:#9fd8ff">${Math.round(lerp(-20, -230, K.eio(cl((t - W("minus") + 0.4) / 1.6))))} °C</span>`);
  seg(W("isaacman") - 0.6, tBis - 0.1, "NASA-Chef<div class='sub'>Jared Isaacman</div>"); seg(tBis, tIns - 0.1, "⚛️ bis Ende des Jahrzehnts");
  seg(W("zwanzig", 58) - 0.2, tAnm - 0.1, "≈ 20 Mrd. $");
  seg(tAnm, tViel - 0.1, "Anmeldung bis<div class='sub'>25. Januar 2027</div>"); seg(tViel, 69, "💡 Idee von einem Schüler?");
  word(wh, wa); cap(t);
};
