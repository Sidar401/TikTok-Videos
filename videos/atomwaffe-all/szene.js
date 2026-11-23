const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(91);
// @modelle
// ================= Erde mit Satelliten =================
const so = new THREE.Scene(); K.stars(so, 9000, -1, 60000, 1.7).material.opacity = 0.7; so.add(new THREE.AmbientLight(0x30343e, 0.6)); const sunO = new THREE.DirectionalLight(0xfff2e0, 1.8); sunO.position.set(-1, 0.4, 0.6); so.add(sunO);
const RE = 100; const EA = K.earth(so, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-1, 0.4, 0.6).normalize();
// Satelliten-Punkte (je mit "tot"-Zeitpunkt)
const N = 3000; K.reseed(4); const pp = [], die = []; for (let i = 0; i < N; i++) { const v = V(K.rnd() - 0.5, (K.rnd() - 0.5) * 1.3, K.rnd() - 0.5).normalize().multiplyScalar(RE * (1.06 + K.rnd() * 0.08)); pp.push(v.x, v.y, v.z); die.push(K.rnd() < 0.34 ? K.rnd() : 9); }
const sg = new THREE.BufferGeometry(); sg.setAttribute("position", new THREE.Float32BufferAttribute(pp, 3)); const col = new Float32Array(N * 3); sg.setAttribute("color", new THREE.BufferAttribute(col, 3));
const satPts = new THREE.Points(sg, new THREE.PointsMaterial({ size: 2.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 1, blending: THREE.AdditiveBlending, depthWrite: false })); so.add(satPts);
const setSats = (k) => { for (let i = 0; i < N; i++) { const d = die[i] < 2 && k > die[i]; col[i * 3] = d ? 0.8 : 0.75; col[i * 3 + 1] = d ? 0.08 : 0.9; col[i * 3 + 2] = d ? 0.05 : 1; } sg.attributes.color.needsUpdate = true; };
// Strahlungsgürtel
const belt = new THREE.Group(); so.add(belt); for (let i = 0; i < 3; i++) { const m = new THREE.Mesh(new THREE.TorusGeometry(RE * (1.35 + i * 0.35), RE * (0.06 + i * 0.03), 24, 160), new THREE.MeshBasicMaterial({ color: i ? 0xff5a3c : 0xffb14a, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); m.rotation.x = Math.PI / 2; belt.add(m); }
const flash = K.sprite(so, K.glowTex("rgba(255,250,235,1)"), 200, V(0, 0, 0), 0); const shell = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshBasicMaterial({ color: 0xffc070, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.BackSide })); so.add(shell);
// Der Satellit (Konzept, keine echten Bilder bekannt)
const bomb = new THREE.Group(); so.add(bomb); { const b = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 3, 24), MO.plain(0x5a5e66, 0.7, 0.35)); bomb.add(b); const c = new THREE.Mesh(new THREE.ConeGeometry(0.9, 1.2, 24), MO.plain(0x3a3d44, 0.7, 0.35)); c.position.y = 2.1; bomb.add(c);
  for (const s of [-1, 1]) { const w = new THREE.Mesh(new THREE.BoxGeometry(5, 0.05, 1.6), [MO.plain(0x50545c), MO.plain(0x50545c), MO.cellM(), MO.cellM(), MO.plain(0x50545c), MO.plain(0x50545c)]); w.position.x = s * 3.4; bomb.add(w); }
  const sym = new THREE.Mesh(new THREE.CircleGeometry(0.45, 3), new THREE.MeshBasicMaterial({ color: 0xffd23f, toneMapped: false })); sym.position.set(0, 0.2, 0.92); bomb.add(sym); }
const bombO = new THREE.Object3D(); bomb.add(bombO); bombO.position.set(0, 3.2, 0);
// Hawaii-Lichter (1962)
const haw = []; { K.reseed(12); const base = EA.ll(20.8, -156.9, RE * 1.003); for (let i = 0; i < 26; i++) { const s = K.sprite(EA.group, K.glowTex("rgba(255,210,140,1)"), 3, base.clone().add(V((K.rnd() - 0.5) * 6, (K.rnd() - 0.5) * 4, (K.rnd() - 0.5) * 6)), 0); haw.push(s); } }
// ===== Zeiten =====
const tDas = W("das", 3.4), tRuss = W("russland", 7.7), tEin = W("ein", 9.8), tLaut = W("laut"), tWarum = W("warum"), tDie = W("die", 30.2), tNach = W("nach", 37.4), tDas2 = W("das", 46), tGab = W("das", 50.6), tSeit = W("seit"), tNennt = W("russland", 70.8), END = 74.0, KARTE = 9.7;
label("Sputnik-S?", bombO, 1, { t0: tLaut + 1.4, t1: tWarum - 0.1, size: 52, gap: 18 });
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let pos = V(0, 80, 360), look = V(0, 0, 0), fov = 42; EA.group.rotation.y = 2.4 + t * 0.008; EA.clouds.rotation.y = t * 0.004; EA.clouds.visible = true; flash.material.opacity = 0; shell.material.opacity = 0; belt.children.forEach((m) => (m.material.opacity = 0)); bomb.visible = false; bomb.scale.setScalar(1); haw.forEach((h) => (h.material.opacity = 0)); setSats(-1);
  const boom = (k, p, big = 1) => { flash.position.copy(p); flash.material.opacity = Math.max(0, 1 - k * 1.6); flash.scale.setScalar((80 + k * 260) * big); shell.position.copy(p); shell.scale.setScalar((4 + k * 120) * big); shell.material.opacity = 0.25 * (1 - k); E.grade.uniforms.flash.value = Math.max(0, 0.5 - k * 2); };
  const P0 = V(-45, 115, 115);
  if (t < tDas - 0.05) { const f = prog(t, 0, tDas); bomb.visible = f < 0.55; bomb.scale.setScalar(2); bomb.position.copy(P0); bomb.rotation.set(0.3, t * 0.4, 0.2); if (f > 0.55) boom((f - 0.55) / 0.45, P0, 0.6); pos = P0.clone().add(V(14, 10, 38)); look = P0.clone().add(V(-4, -12, -30)); fov = 50; }
  else if (t < tEin - 0.05) { const f = prog(t, tDas, tEin - tDas); const a = 0.3 + f * 0.4; pos = V(Math.sin(a) * 420, 90, Math.cos(a) * 420); look = V(0, 0, 0); fov = 42; }
  else if (t < tWarum - 0.05) { const f = prog(t, tEin, tWarum - tEin); bomb.visible = true; bomb.position.set(0, 0, 0); bomb.rotation.set(0.25, 0.4 + t * 0.15, 0.1); EA.group.position.set(0, -160, -260); const d = lerp(18, 12, f); pos = V(Math.sin(f) * d, 3, d); look = V(0, 0.5, 0); fov = 44; }
  else if (t < tNach - 0.05) { EA.group.position.set(0, 0, 0); const f = prog(t, tWarum, tNach - tWarum); const k = cl((t - W("atomexplosion") - 0.2) / 3); if (k > 0 && k < 1) boom(k, P0); if (t > tDie) belt.children.forEach((m, i) => (m.material.opacity = 0.03 * cl((t - tDie - i * 0.4) / 1.2))); setSats(t > tDie + 1 ? (t - tDie - 1) / 5 : -1); const a = 0.5 + f * 0.4; pos = V(Math.sin(a) * 440, 130, Math.cos(a) * 440); look = V(0, 0, 0); fov = 42; }
  else if (t < tGab - 0.05) { EA.group.position.set(0, 0, 0); const f = prog(t, tNach, tGab - tNach); belt.children.forEach((m) => (m.material.opacity = 0.025)); setSats(1); const a = 0.9 + f * 0.5; pos = V(Math.sin(a) * 300, 60, Math.cos(a) * 300); look = V(0, 0, 0); fov = 42; }
  else if (t < tSeit - 0.05) { EA.group.position.set(0, 0, 0); const f = prog(t, tGab, tSeit - tGab); EA.group.rotation.y = 0.9; EA.clouds.visible = false; const hp = EA.ll(16.7, -169.5, RE * 1.4); const hw = haw[0].getWorldPosition(V(0, 0, 0)); const kx = cl((t - W("zündeten") + 0.1) / 3); if (kx > 0 && kx < 1) boom(kx, hp, 0.5);
    const lightsOff = t > W("straßenlaternen") - 0.1; haw.forEach((h, i) => (h.material.opacity = lightsOff ? (Math.sin(i * 7 + t * 20) > 0.6 && t < W("straßenlaternen") + 0.6 ? 0.8 : 0) : 0.9)); const n = hw.clone().normalize(); pos = n.clone().multiplyScalar(lerp(380, 330, f)).add(V(0, 40, 0)); look = hw.clone().multiplyScalar(0.8); fov = 40; }
  else { EA.group.position.set(0, 0, 0); const f = prog(t, tSeit, END - tSeit); const a = 1.2 + f * 0.6; pos = V(Math.sin(a) * 430, 100, Math.cos(a) * 430); look = V(0, 0, 0); fov = 42; }
  cam.fov = fov; cam.near = 0.1; cam.far = 80000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(so, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("dezember") - 0.2, tWarum - 0.1, "📅 schon im Dezember?"); seg(W("rund", 39.6) - 0.1, tDas2 - 0.1, "≈ 1/3 aller Satelliten" + sub("in niedriger Umlaufbahn"));
  seg(W("neunzehnhundertzweiundsechzig") - 0.1, W("danach") - 0.1, "💥 1962 · Pazifik"); seg(tSeit - 0.1, tNennt - 0.1, "📜 1967: Atomwaffen im All verboten");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
