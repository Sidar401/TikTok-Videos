const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(31);
// @modelle
// ================= Tiefer Raum: Sonde, Sonne, Asteroiden =================
const sc = new THREE.Scene(); K.stars(sc, 11000, -1, 40000, 1.7).material.opacity = 0.8; sc.add(new THREE.AmbientLight(0x2c3040, 0.8)); sc.add(new THREE.HemisphereLight(0x8090b0, 0x101010, 0.3));
const sun = new THREE.DirectionalLight(0xfff2e0, 2.0); sun.position.set(-600, 250, 400); sc.add(sun); const sunS = K.sprite(sc, K.glowTex("rgba(255,225,170,1)"), 900, V(-6000, 2500, 4000), 0.9);
const HB = MO.hayabusa2(); sc.add(HB.g); const hbO = new THREE.Object3D(); HB.g.add(hbO); hbO.position.set(0, 1.2, 0);
const sparks = []; for (let i = 0; i < 6; i++) sparks.push(K.sprite(HB.g, K.glowTex("rgba(190,220,255,1)"), 0.35, V(-1.0, 0, 0), 0));
const engGlow = HB.engines.map((e) => { const s = K.sprite(e, K.glowTex("rgba(120,170,255,1)"), 0.7, V(-0.08, 0, 0), 0); return s; });
const RY = MO.asteroid({ r: 40, seed: 11, top: true, craters: 30 }); sc.add(RY); RY.position.set(0, 0, -2000); const ryO = new THREE.Object3D(); RY.add(ryO); ryO.position.set(0, 1.25, 0);
const TF = new THREE.Group(); sc.add(TF); TF.position.set(0, 0, 2000); { const a = MO.asteroid({ r: 14, seed: 5, craters: 20 }); a.position.x = -9; const b = MO.asteroid({ r: 10, seed: 9, craters: 14 }); b.position.x = 8; TF.add(a, b); } const tfO = new THREE.Object3D(); TF.add(tfO); tfO.position.set(0, 20, 0);
const KY = MO.asteroid({ r: 4, seed: 41, craters: 8 }); sc.add(KY); KY.position.set(3000, 0, 0);
const NB = MO.asteroid({ r: 22, seed: 77, craters: 22, stretch: V(1.5, 0.8, 1) }); sc.add(NB); NB.position.set(-3000, 0, 0);
const cross = []; for (const s of [-1, 1]) { const m = new THREE.Mesh(new THREE.BoxGeometry(22, 1.6, 0.5), new THREE.MeshBasicMaterial({ color: 0xff3b30, transparent: true, opacity: 0, toneMapped: false })); m.rotation.z = s * 0.785; m.position.copy(KY.position).add(V(0, 0, 12)); sc.add(m); cross.push(m); }
// Erde + Kapsel (2020)
const scE = new THREE.Scene(); K.stars(scE, 8000, -1, 30000, 1.6).material.opacity = 0.7; scE.add(new THREE.AmbientLight(0x30343e, 0.6)); const sunE = new THREE.DirectionalLight(0xfff2e0, 1.4); sunE.position.set(-500, 300, 600); scE.add(sunE);
const RE = 100; const EA = K.earth(scE, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-0.5, 0.3, 0.8).normalize();
const capF = MO.exhaust(30, 1.6, [1, 0.95, 0.8], [1, 0.45, 0.12]); scE.add(capF); const capG = K.sprite(scE, K.glowTex("rgba(255,170,80,1)"), 10, V(0, 0, 0), 0);
const capM = new THREE.Mesh(new THREE.SphereGeometry(0.8, 24, 16), MO.plain(0x6b5b48, 0.4, 0.6)); scE.add(capM);
// Bahnlinie (gepunktet)
const path = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(1, 0, 0)]), new THREE.LineDashedMaterial({ color: 0x7fd0ff, dashSize: 2, gapSize: 1.5, transparent: true, opacity: 0, toneMapped: false })); sc.add(path);
// ===== Zeiten =====
const tDie = W("die", 4), tSeit = W("seit"), tJetzt = W("jetzt"), tFolg = W("folg"), tHB = W("hayabusa", 13), tSie = W("sie", 15), tBr = W("brachte"), tGut = W("gut"), tDanach = W("danach"), tJuli = W("im", 23.5), tVier = W("die", 28), tSchieb = W("sie", 30.8), tDoch = W("doch"), tStrom = W("die", 38), tTrick = W("der", 40), tTeile = W("teile"), tSo = W("so", 45.4), tAber = W("aber", 48.3), tFunk = W("immer"), tAlt = W("das", 54.6), tNeu = W("neues"), tApr = W("im", 61.8), tLand = W("landen"), tRent = W("ein", 69.4), END = 73.2;
label("Hayabusa2", hbO, 1, { t0: tDie + 0.3, t1: tJetzt - 0.1, size: 54, gap: 22 }); label("Ryugu", ryO, 40, { t0: tSie + 0.4, t1: tBr - 0.1, size: 56, gap: 24 }); label("Torifune", tfO, 4, { t0: tJuli + 0.8, t1: tVier - 0.1, size: 54, gap: 22 });
const WORDEL = document.getElementById("word");
const engines = (on, t, flick = 0) => HB.engines.forEach((e, i) => { const p = typeof on === "function" ? on(i) : on; const fl = flick ? (Math.sin(t * 37 + i * 3) > 0.2 ? 1 : 0.15) : 1; const k = p * fl;
  e.userData.ex.visible = k > 0.02; e.userData.ex.userData.mat.uniforms.t.value = t; e.userData.ex.userData.mat.uniforms.power.value = k; engGlow[i].material.opacity = 0.9 * k; e.userData.grid.material.color.setRGB(0.1 + 0.4 * k, 0.16 + 0.55 * k, 0.33 + 0.67 * k); });
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.32, 0.86);
  let scene = sc, pos = V(6, 2, 8), look = V(0, 0, 0), fov = 40; HB.g.position.set(0, 0, 0); HB.g.rotation.set(0.15, 0.6 + t * 0.03, 0.05); HB.g.scale.setScalar(1);
  sparks.forEach((s) => (s.material.opacity = 0)); cross.forEach((c) => (c.material.opacity = 0)); path.material.opacity = 0; engines(0, t);
  RY.rotation.y = t * 0.05; TF.rotation.y = t * 0.03; KY.rotation.set(t * 0.4, t * 0.3, 0); NB.rotation.y = t * 0.08;
  const spark = (n, amp) => sparks.slice(0, n).forEach((s, i) => { const on = Math.sin(t * 23 + i * 7.1) > 0.55; s.position.set(-0.95, -0.1 + Math.sin(i * 2.3) * 0.25, Math.cos(i * 3.7) * 0.25); s.material.opacity = on ? amp : 0; s.scale.setScalar(0.2 + 0.3 * Math.abs(Math.sin(t * 11 + i))); });
  if (t < tDie - 0.05) { const f = prog(t, 0, tDie); engines(f < 0.45 ? 1 : 0, t, f > 0.25 ? 1 : 0); spark(6, f > 0.3 ? 1 : 0); HB.g.rotation.set(0, 0, 0); pos = V(-4.2, lerp(1.2, 0.6, f), lerp(1.4, 0.6, f)); look = V(-0.7, 0, 0); fov = 42; }
  else if (t < tFolg - 0.05) { const f = prog(t, tDie, tFolg - tDie); engines(1, t); HB.g.rotation.y = 2.2 + t * 0.02; const a = 1.0 + f * 0.9; const d = lerp(9, 11, f); pos = V(Math.sin(a) * d, lerp(3, 1.5, f), Math.cos(a) * d); look = V(0, 0, 0); fov = 42; }
  else if (t < tSie - 0.05) { engines(1, t); HB.g.rotation.y = 2.6 + t * 0.02; const f = prog(t, tFolg, tSie - tFolg); const a = 0.3 + f * 0.5; pos = V(Math.sin(a) * 8, 2, Math.cos(a) * 8); fov = 42; }
  else if (t < tBr - 0.05) { const f = prog(t, tSie, tBr - tSie); HB.g.position.copy(RY.position).add(V(6, lerp(58, 41.8, K.eio(cl(f * 1.4))), 4)); HB.g.rotation.set(0, 0.5, 0); const a = 0.7 - f * 0.3; pos = RY.position.clone().add(V(Math.sin(a) * 120, 60, Math.cos(a) * 120)); look = RY.position.clone().add(V(0, 15, 0)); fov = 40; }
  else if (t < tDanach - 0.05) { scene = scE; const f = prog(t, tBr, tDanach - tBr); EA.group.rotation.y = 2.4 + t * 0.01; const p0 = V(-40, 60, 130), p1 = V(-12, 20, 99); const cp = p0.clone().lerp(p1, K.eio(f)); capM.position.copy(cp);
    capF.position.copy(cp); capF.lookAt(p0); capF.rotateX(Math.PI / 2); capF.userData.mat.uniforms.t.value = t; capF.userData.mat.uniforms.power.value = cl(f * 3) * (1 - cl((f - 0.9) * 10)); capG.position.copy(cp); capG.material.opacity = capF.userData.mat.uniforms.power.value;
    pos = V(-10, 70, 300); look = V(-20, 30, 80); fov = 40; }
  else if (t < tVier - 0.05) { const f = prog(t, tDanach, tVier - tDanach); engines(0.6, t); HB.g.position.copy(TF.position).add(V(lerp(-70, 70, f), 22, 18)); HB.g.rotation.set(0, Math.PI, 0); pos = TF.position.clone().add(V(lerp(-40, 40, f) * 0.5, 30, 110)); look = TF.position.clone().add(V(0, 8, 0)); fov = 42; }
  else if (t < tDoch - 0.05) { engines(1, t); HB.g.rotation.set(0, 0, 0); const f = prog(t, tVier, tDoch - tVier); pos = V(-3.6, 0.7, lerp(-0.9, 0.9, f)); look = V(-0.9, -0.05, 0); fov = 40; }
  else if (t < tTrick - 0.05) { HB.g.rotation.set(0, 0, 0); const f = prog(t, tDoch, tTrick - tDoch); engines((i) => (i === 3 ? (t < W("fiel") + 0.4 ? 1 : 0) : 0), t, t > W("fiel") - 0.3 ? 1 : 0); if (t > tStrom) spark(4, 1);
    if (t > tStrom) E.look([1.05, 0.95, 0.95], [0, 0, 0], 0.32, 0.86); pos = V(-3.0, 0.5, lerp(0.8, -0.4, f)); look = V(-0.9, -0.05, 0); fov = 40; }
  else if (t < tAber - 0.05) { HB.g.rotation.set(0, 0, 0); const f = prog(t, tTrick, tAber - tTrick); engines((i) => (t > tTeile + 0.6 ? (i === 0 || i === 3 ? 0.5 + 0.5 * cl((t - tTeile - 0.6) / 1.5) : 0) : 0), t);
    if (t > tTeile && t < tSo) { path.material.opacity = 0.9; const a = HB.engines[0].getWorldPosition(V(0, 0, 0)), b = HB.engines[3].getWorldPosition(V(0, 0, 0)); path.geometry.setFromPoints([a, b]); path.computeLineDistances(); path.material.dashSize = 0.08; path.material.gapSize = 0.05; }
    pos = V(-2.9, 0.4, lerp(-0.6, 0.6, f)); look = V(-0.9, -0.05, 0); fov = 40; }
  else if (t < tAlt - 0.05) { HB.g.rotation.set(0, 0, 0); engines((i) => (i === 0 || i === 3 ? 0.8 : 0), t, 1); spark(6, 1); const f = prog(t, tAber, tAlt - tAber); pos = V(-3.3, 0.8, lerp(0.7, -0.7, f)); look = V(-0.9, -0.05, 0); fov = 40; }
  else if (t < tNeu - 0.05) { const f = prog(t, tAlt, tNeu - tAlt); cross.forEach((c) => (c.material.opacity = 0.95 * cl((t - W("ist", 59.2) + 0.2) / 0.3))); const a = f * 0.6; pos = KY.position.clone().add(V(Math.sin(a) * 30, 6, Math.cos(a) * 30 + 10)); look = KY.position.clone(); fov = 42; }
  else if (t < tRent - 0.05) { const f = prog(t, tNeu, tRent - tNeu); HB.g.position.copy(NB.position).add(V(lerp(-160, 160, cl((t - tApr) / (tRent - tApr))), 30, 30)); HB.g.rotation.set(0, Math.PI, 0); engines(0, t);
    path.material.opacity = 0.6; path.geometry.setFromPoints([NB.position.clone().add(V(-200, 30, 30)), NB.position.clone().add(V(200, 30, 30))]); path.computeLineDistances(); path.material.dashSize = 4; path.material.gapSize = 3;
    const a = -0.4 + f * 0.5; pos = NB.position.clone().add(V(Math.sin(a) * 170, 60, Math.cos(a) * 170)); look = NB.position.clone().add(V(0, 15, 0)); fov = 44; }
  else { const f = prog(t, tRent, END - tRent); HB.g.rotation.y = 1.2 + t * 0.05; const d = lerp(7, 16, K.eio(f)); const a = 0.8 + f * 0.5; pos = V(Math.sin(a) * d, lerp(1.5, 4, f), Math.cos(a) * d); look = V(0, 0, 0); fov = 42; }
  cam.fov = fov; cam.near = 0.05; cam.far = 80000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(tSeit - 0.1, tJetzt - 0.1, "🇯🇵 seit fast 12 Jahren" + sub("Start: Dezember 2014")); seg(tJetzt, tFolg - 0.1, "🎯 Ziel geändert!");
  seg(tBr, tGut - 0.1, "2020 → 🌍"); seg(tGut, tDanach - 0.1, "🪨 gut 5 Gramm");
  seg(tVier + 0.2, tSchieb - 0.1, "4 Ionen-Triebwerke"); seg(tSchieb, tDoch - 0.1, "sanft – aber jahrelang");
  seg(tDoch, tStrom - 0.1, "August: letztes fällt aus"); seg(tStrom, tTrick - 0.1, "⚡ Stromversorgung kaputt");
  seg(tTeile - 0.2, tSo - 0.1, "2 kaputte → 1 neues"); seg(tSo, tAber - 0.1, "Trick der 1. Hayabusa" + sub("Heimkehr 2010"));
  seg(tFunk - 0.1, tAlt - 0.1, "⚡ Funken – kein Schub");
  seg(tAlt, tNeu - 0.1, "Ziel 2031 gestrichen ❌"); seg(tApr - 0.1, tLand - 0.1, "📅 April 2028" + sub("schneller Vorbeiflug")); seg(tLand, tRent - 0.1, "keine Landung mehr");
  seg(tRent + 0.3, END, "👴 Rentner im All");
  word(wh, wa); cap(t);
};
