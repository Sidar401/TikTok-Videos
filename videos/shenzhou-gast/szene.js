const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(21);
// @modelle
// ================= Orbit: Erde + Tiangong (nicht maßstäblich) =================
const scO = new THREE.Scene(); K.stars(scO, 9000, -1, 40000, 1.7).material.opacity = 0.7; scO.add(new THREE.AmbientLight(0x30343e, 0.7)); scO.add(new THREE.HemisphereLight(0x8090b0, 0x101010, 0.25));
const sunO = new THREE.DirectionalLight(0xfff2e0, 1.6); sunO.position.set(-500, 300, 600); scO.add(sunO);
const RE = 2000; const EA = K.earth(scO, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-0.5, 0.3, 0.8).normalize(); EA.group.position.set(0, -RE * 1.13, 0);
const TG = MO.tiangong(); scO.add(TG.g); TG.g.rotation.y = 0.3;
const SZ = MO.shenzhou(); scO.add(SZ.g); const SZ2 = MO.shenzhou(); scO.add(SZ2.g);
const ISS = MO.iss(); scO.add(ISS.g); ISS.g.scale.setScalar(0.9);
const plasma = MO.exhaust(70, 6, [1, 0.9, 0.7], [1, 0.4, 0.1]); scO.add(plasma); const pglow = K.sprite(scO, K.glowTex("rgba(255,150,60,1)"), 60, V(0, 0, 0), 0);
const capGlow = K.sprite(scO, K.glowTex("rgba(255,160,70,1)"), 8, V(0, 0, 0), 0);
const altLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(0, -60, 0)]), new THREE.LineDashedMaterial({ color: 0xffd23f, dashSize: 3, gapSize: 2, transparent: true, opacity: 0, toneMapped: false })); altLine.computeLineDistances(); scO.add(altLine);
const tgO = new THREE.Object3D(); TG.g.add(tgO); tgO.position.set(2, 6, 0); const altO = new THREE.Object3D(); altO.position.set(8, -130, 0); scO.add(altO);
const issO = new THREE.Object3D(); ISS.g.add(issO); issO.position.set(0, 12, 0); const szO = new THREE.Object3D(); SZ.g.add(szO); szO.position.set(0, 2.2, 0);
// ================= Boden: Wüste Gobi + Rakete =================
const scG = new THREE.Scene(); K.reseed(5); const stG = K.stars(scG, 5000, -1, 20000, 1.5); stG.material.opacity = 0.5; const skyG = K.sky(scG, 0x050a1c, 0x2a3c66, 0xe08a4a, 15000);
scG.add(new THREE.AmbientLight(0x4a4f63, 0.7)); scG.add(new THREE.HemisphereLight(0x9fb0d8, 0x5a3a20, 0.45)); const sunG = new THREE.DirectionalLight(0xffc58a, 1.5); sunG.position.set(-400, 120, 300); scG.add(sunG);
const sandT = (() => { const c = document.createElement("canvas"); c.width = c.height = 512; const g = c.getContext("2d"); g.fillStyle = "#a07a52"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 9000; i++) { const v = K.rnd(); g.fillStyle = `rgba(${v < 0.5 ? 60 : 210},${v < 0.5 ? 40 : 170},${v < 0.5 ? 25 : 120},${0.08 * K.rnd()})`; g.beginPath(); g.arc(K.rnd() * 512, K.rnd() * 512, 1 + K.rnd() * 6, 0, 7); g.fill(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(60, 60); t.colorSpace = THREE.SRGBColorSpace; return t; })();
const ground = new THREE.Mesh(new THREE.PlaneGeometry(8000, 8000), new THREE.MeshStandardMaterial({ map: sandT, roughness: 1 })); ground.rotation.x = -Math.PI / 2; scG.add(ground);
// Hügel am Horizont
for (let i = 0; i < 26; i++) { const a = (i / 26) * 6.283; const h = new THREE.Mesh(new THREE.ConeGeometry(120 + K.rnd() * 220, 40 + K.rnd() * 90, 7), new THREE.MeshStandardMaterial({ color: 0x7a5636, roughness: 1, flatShading: true })); h.position.set(Math.cos(a) * 2600, 15, Math.sin(a) * 2600); scG.add(h); }
const LM = MO.longMarch2F(); const rollG = new THREE.Group(); scG.add(rollG); rollG.add(LM.g); LM.g.position.y = 6;
const plat = new THREE.Mesh(MO.RBox(16, 6, 16, 2, 0.3), MO.plain(0x8a8f99, 0.4, 0.6)); plat.position.y = 3; rollG.add(plat);
const umb = MO.pad(); umb.scale.setScalar(1); umb.position.set(0, 6, 0); rollG.add(umb);
for (const z of [-5, 5]) { const rail = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.4, 1500), MO.plain(0x55585e, 0.8, 0.4)); rail.position.set(0, 0.2, -700); rail.rotation.y = Math.PI / 2; rail.position.set(-700, 0.2, z); scG.add(rail); }
const vab = new THREE.Mesh(new THREE.BoxGeometry(60, 105, 50), MO.mat(MO.panelTex({ base: "#cfd3d8", mottle: 0.03, vseams: 10, w: 512, h: 512 }), { rough: 0.6 })); vab.position.set(-1500, 52, 0); scG.add(vab);
const lamps = []; for (const [x, z] of [[60, -60], [-60, -60], [60, 60], [-60, 60]]) { const tw = new THREE.Mesh(new THREE.BoxGeometry(1.5, 90, 1.5), MO.plain(0x6a6e76, 0.6, 0.5)); tw.position.set(x, 45, z); scG.add(tw); lamps.push(K.sprite(scG, K.glowTex("rgba(255,240,210,1)"), 14, V(x, 90, z), 0.8)); }
const lmTop = new THREE.Object3D(); lmTop.position.y = 64; LM.g.add(lmTop);
// ===== Zeiten =====
const tBis = W("bisher"), tJetzt = W("jetzt"), tUnd = W("und", 10.5), tFolg = W("folg"), tDie = W("die", 14.4), tHeisst = W("heißt"), tDas = W("das", 16.5), tSie = W("sie", 19), tDiese = W("diese", 22), tLanger = W("langer"), tMitten = W("mitten"), tErw = W("erwartet"), tDen = W("den", 32.8), tAn = W("an", 36.2), tZwei = W("zwei", 40.5), tMuh = W("muhammad"), tWer = W("wer"), tGast = W("der", 49.5), tEr = W("er", 51.8), tKap = W("fliegt", 53.3), tWarum = W("warum"), tIss = W("die", 58), tDann = W("dann", 61.8), tViele = W("viele", 65), END = 67.6;
label("Tiangong", tgO, 8, { t0: tHeisst - 0.1, t1: tSie - 0.1, size: 56, gap: 24 }); label("≈ 400 km", altO, 0, { t0: tSie + 0.6, t1: tDiese - 0.1, size: 52, gap: 0 });
label("Langer Marsch 2F", lmTop, 2, { t0: tLanger - 0.1, t1: tErw - 0.1, size: 50, gap: 20 }); label("Shenzhou", szO, 1, { t0: tAn + 0.2, t1: tZwei - 0.1, size: 50, gap: 18 }); label("ISS", issO, 3, { t0: tIss + 0.2, t1: tDann - 0.1, size: 56, gap: 22 });
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = scO, pos = V(40, 10, 60), look = V(0, 0, 0), fov = 40;
  EA.group.rotation.y = 2.2 + t * 0.004; EA.clouds.rotation.y = t * 0.002; TG.g.rotation.y = 0.3 + t * 0.01;
  SZ.g.visible = false; SZ2.g.visible = false; ISS.g.visible = false; plasma.visible = false; pglow.material.opacity = 0; capGlow.material.opacity = 0; altLine.material.opacity = 0; TG.g.visible = true;
  const port = TG.port.getWorldPosition(V(0, 0, 0)); const portDir = V(1, 0, 0).applyQuaternion(TG.g.quaternion);
  const dockAt = (sz, gap) => { sz.g.visible = true; sz.g.quaternion.copy(TG.g.quaternion); sz.g.rotateY(Math.PI); sz.g.position.copy(port).add(portDir.clone().multiplyScalar(4.4 + gap)); };
  if (t < tBis - 0.05) { const f = prog(t, 0, tBis); dockAt(SZ, lerp(30, 6, K.eio(f))); const a = 0.9 - f * 0.35; pos = V(Math.sin(a) * 70, lerp(18, 12, f), Math.cos(a) * 70); look = V(4, 0, 0); fov = 42; }
  else if (t < tUnd - 0.05) { const f = prog(t, tBis, tUnd - tBis); dockAt(SZ, 0); const a = -0.6 + f * 0.5; pos = V(Math.sin(a) * 55, lerp(-6, 4, f), Math.cos(a) * 55); look = V(2, 2, 0); fov = 44; }
  else if (t < tDie - 0.05) { scene = scG; rollG.position.x = 0; const f = prog(t, tUnd, tDie - tUnd); const a = 0.6 + f * 0.3; pos = V(Math.sin(a) * 120, lerp(8, 20, f), Math.cos(a) * 120); look = V(0, 34, 0); fov = 44; }
  else if (t < tDiese - 0.05) { const f = prog(t, tDie, tDiese - tDie); dockAt(SZ, 0);
    if (t > tSie) { altLine.material.opacity = 0.9 * cl((t - tSie - 0.2) / 0.5); altLine.geometry.setFromPoints([V(0, -4, 0), V(0, -RE * 0.13 + 2, 0)]); altLine.computeLineDistances(); }
    const a = 0.3 + f * 0.6; const d = lerp(110, t > tSie ? 380 : 140, K.eio(f)); pos = V(Math.sin(a) * d, lerp(30, -40, f), Math.cos(a) * d); look = V(0, t > tSie ? -150 : 0, 0); fov = 42; }
  else if (t < tErw - 0.05) { scene = scG; const f = prog(t, tDiese, tErw - tDiese); rollG.position.x = lerp(-260, 0, K.eio(cl(f * 1.15))); const a = 1.2 - f * 0.5; pos = V(rollG.position.x * 0.4 + Math.sin(a) * 210, lerp(30, 60, f), Math.cos(a) * 210); look = V(rollG.position.x * 0.6, 30, 0); fov = 46;
    if (t > tMitten) { const g2 = prog(t, tMitten, tErw - tMitten); pos = V(lerp(500, 700, g2), lerp(120, 200, g2), lerp(600, 900, g2)); look = V(-200, 20, 0); fov = 50; } }
  else if (t < tAn - 0.05) { scene = scG; rollG.position.x = 0; const f = prog(t, tErw, tAn - tErw); const a = -0.3 + f * 0.6; pos = V(Math.sin(a) * 45, 2.5, Math.cos(a) * 45); look = V(0, 40, 0); fov = 58; }
  else if (t < tGast - 0.05) { const f = prog(t, tAn, tGast - tAn); TG.g.visible = false; SZ.g.visible = true; SZ.g.position.set(0, 0, 0); SZ.g.rotation.set(0.1, 0.4 + t * 0.06, 0); const a = 0.5 + f * 0.8; const d = lerp(18, 14, f); pos = V(Math.sin(a) * d, lerp(4, 2, f), Math.cos(a) * d); look = V(0, 0, 0); fov = 40; }
  else if (t < tWarum - 0.05) { const f = prog(t, tGast, tWarum - tGast); if (t < tKap) dockAt(SZ, 0); else { dockAt(SZ2, 0); const g2 = prog(t, tKap, tWarum - tKap); SZ.g.visible = true; SZ.g.quaternion.copy(TG.g.quaternion); SZ.g.rotateZ(-Math.PI / 2); SZ.g.position.copy(port).add(portDir.clone().multiplyScalar(lerp(8, 30, g2))).add(V(0, -lerp(0, 50, g2 * g2), 0)); }
    const a = 0.8 + f * 0.4; pos = V(Math.sin(a) * 90, lerp(20, 4, f), Math.cos(a) * 90); look = V(6, -6, 0); fov = 42; }
  else if (t < tDann - 0.05) { TG.g.visible = false; ISS.g.visible = true; const f = prog(t, tIss, tDann - tIss); const k = cl(f); ISS.g.position.set(lerp(-60, 60, k), lerp(0, -45, k * k), 0); ISS.g.rotation.set(0.15 + k * 0.4, 0.2, -0.1 - k * 0.3);
    if (t > tIss + 0.6) { plasma.visible = true; const p = cl((t - tIss - 0.6) / 1); plasma.userData.mat.uniforms.t.value = t; plasma.userData.mat.uniforms.power.value = p; plasma.position.copy(ISS.g.position).add(V(-4, 6, 0)); plasma.rotation.z = Math.PI / 2 + 0.6; pglow.position.copy(ISS.g.position); pglow.material.opacity = 0.6 * p; E.look([1.05, 0.98, 0.92], [0, 0, 0], 0.35, 0.82); }
    pos = V(ISS.g.position.x * 0.4 - 40, 20, 170); look = V(ISS.g.position.x * 0.6, ISS.g.position.y * 0.7, 0); fov = 46; }
  else { const f = prog(t, tDann, END - tDann); dockAt(SZ, 0); const a = 1.4 + f * 0.8; const d = lerp(80, 260, K.eio(f)); pos = V(Math.sin(a) * d, lerp(10, 70, f), Math.cos(a) * d); look = V(0, lerp(0, -30, f), 0); fov = 42; }
  if (scene === scG) { lamps.forEach((l) => (l.material.opacity = 0.8)); }
  cam.fov = fov; cam.near = 0.1; cam.far = 80000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(tBis + 0.1, tJetzt - 0.1, "🇨🇳 bisher nur China"); seg(tJetzt, tUnd - 0.1, "🇨🇳 + 🇵🇰"); seg(tUnd + 0.1, tFolg - 0.1, "🚀 Start: nächste Woche?");
  seg(tDas, tSie - 0.1, "„Himmelspalast“"); seg(tMitten, tErw - 0.1, "🏜️ Wüste Gobi");
  seg(W("vierundzwanzigsten") - 0.1, tDen - 0.1, "📅 24. oder 25. November"); seg(tDen, tAn - 0.1, "🤫 Termin kommt kurz vorher");
  seg(tAn + 0.2, tZwei - 0.1, "🇨🇳 🇨🇳 🇵🇰"); seg(tZwei, tMuh - 0.1, "🇵🇰 2 trainiert"); seg(tMuh, tWer - 0.1, "Muhammad Zeeshan Ali" + sub("oder Khurram Daud")); seg(tWer, tGast - 0.1, "Wer fliegt? ❓");
  seg(W("etwa", 50) - 0.2, tEr - 0.1, "⏱️ ≈ 1 Woche"); seg(tEr, tKap - 0.1, "🔬 Experimente"); seg(tKap, tWarum - 0.1, "🏠 zurück mit anderer Kapsel");
  seg(W("soll", 58.5), tDann - 0.1, "🌊 ≈ 2030 ins Meer"); seg(tDann, tViele - 0.1, "eine der letzten Stationen"); seg(tViele, END, "🌍 viele Länder wollen mit");
  word(wh, wa); cap(t);
};
