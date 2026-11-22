const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(61);
// @modelle
// ================= Doppel-Asteroid (nicht maßstäblich) =================
const sc = new THREE.Scene(); K.stars(sc, 10000, -1, 60000, 1.7).material.opacity = 0.75; sc.add(new THREE.AmbientLight(0x2a2e3a, 0.35));
const sun = new THREE.DirectionalLight(0xfff2e0, 2.6); sun.position.set(-1, 0.3, 0.2); sc.add(sun); K.sprite(sc, K.glowTex("rgba(255,235,200,1)"), 2600, V(-12000, 3600, 2400), 0.9);
const DID = MO.asteroid({ r: 40, seed: 21, top: true, craters: 35 }); sc.add(DID); const didO = new THREE.Object3D(); sc.add(didO); didO.position.set(0, 36, 0);
const DIM = MO.asteroid({ r: 8, seed: 77, craters: 12, stretch: V(1.3, 0.85, 1) }); sc.add(DIM); const dimO = new THREE.Object3D(); sc.add(dimO);
const ROld = 95, RNew = 88; const orbit = (R, col) => { const m = new THREE.Mesh(new THREE.TorusGeometry(R, 0.35, 8, 256), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, toneMapped: false })); m.rotation.x = Math.PI / 2; sc.add(m); return m; };
const oOld = orbit(ROld, 0xffffff), oNew = orbit(RNew, 0xffd23f);
const HE = MO.hera(); sc.add(HE.g); HE.g.scale.setScalar(2.2); const heO = new THREE.Object3D(); HE.g.add(heO); heO.position.set(0, 2.2, 0);
const CS = [MO.cubesat(), MO.cubesat()]; CS.forEach((c) => { c.g.scale.setScalar(4); sc.add(c.g); });
const DA = MO.dart(); sc.add(DA.g); DA.g.scale.setScalar(1.6); const daGlow = K.sprite(sc, K.glowTex("rgba(255,230,180,1)"), 14, V(0, 0, 0), 0);
const flash = K.sprite(sc, K.glowTex("rgba(255,240,215,1)"), 120, V(0, 0, 0), 0);
const ej = []; { K.reseed(3); for (let i = 0; i < 160; i++) { const m = new THREE.SpriteMaterial({ map: K.glowTex("rgba(200,180,150,1)"), transparent: true, opacity: 0, depthWrite: false }); const s = new THREE.Sprite(m); const d = V((K.rnd() - 0.5) * 1.3, 1, (K.rnd() - 0.5) * 1.3).normalize(); s.userData = { d, v: 0.4 + K.rnd() }; sc.add(s); ej.push(s); } }
// ================= Erde + Asteroid weg-schubsen =================
const se = new THREE.Scene(); K.stars(se, 8000, -1, 60000, 1.6).material.opacity = 0.7; se.add(new THREE.AmbientLight(0x30343e, 0.5)); const le = new THREE.DirectionalLight(0xfff2e0, 1.5); le.position.set(-5, 2, 4); se.add(le);
const EA = K.earth(se, { day, night, topo }, 60); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-0.8, 0.3, 0.5).normalize();
const rock = MO.asteroid({ r: 6, seed: 9 }); se.add(rock); const pathA = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineDashedMaterial({ color: 0xff5a4a, dashSize: 6, gapSize: 4, transparent: true, opacity: 0, toneMapped: false })); se.add(pathA);
const pathB = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineDashedMaterial({ color: 0x7fd0ff, dashSize: 6, gapSize: 4, transparent: true, opacity: 0, toneMapped: false })); se.add(pathB);
// ===== Zeiten =====
const tJetzt = W("jetzt"), tIn = W("in", 9.5), tDie = W("die", 12.3), tIhr = W("ihr"), tDid = W("didymos", 19.5), tUnd = W("und", 22), tIm = W("im", 25.8), tDer = W("der", 33.6), tUnd2 = W("und", 38.8), tAber = W("aber", 45), tGen = W("genau"), tSie = W("sie", 53.6), tErst = W("die", 58.2), tAm = W("am", 63.8), END = 67.6, KARTE = 12.2;
label("Didymos", didO, 4, { t0: tDid - 0.1, t1: tIm - 0.1, size: 52, gap: 18 }); label("Dimorphos", dimO, 8, { t0: W("dimorphos", 23) - 0.1, t1: tIm - 0.1, size: 48, gap: 16 }); label("Hera", heO, 1, { t0: tDie + 0.6, t1: tIhr - 0.1, size: 54, gap: 18 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sc, pos = V(0, 60, 300), look = V(0, 0, 0), fov = 40; DID.rotation.y = t * 0.12; DIM.rotation.y = t * 0.3;
  const dimAt = (a, R) => { const p = V(Math.cos(a) * R, 0, Math.sin(a) * R); DIM.position.copy(p); dimO.position.copy(p); return p; };
  oOld.material.opacity = 0; oNew.material.opacity = 0; flash.material.opacity = 0; ej.forEach((s) => (s.material.opacity = 0)); HE.g.visible = false; DA.g.visible = false; daGlow.material.opacity = 0; CS.forEach((c) => (c.g.visible = false));
  const impact = (k, p) => { flash.position.copy(p); flash.material.opacity = Math.max(0, 1 - k * 3); ej.forEach((s) => { const r = 8 + k * 70 * s.userData.v; s.position.copy(p).add(s.userData.d.clone().multiplyScalar(r)); s.scale.setScalar(1 + k * 3.5); s.material.opacity = k > 0 ? 0.4 * (1 - k) : 0; }); };
  if (t < tJetzt - 0.05) { const f = prog(t, 0, tJetzt); const p = dimAt(0.6, ROld); DA.g.visible = f < 0.82; const from = p.clone().add(V(6, 95, 25)); DA.g.position.copy(from.clone().lerp(p, Math.min(1, f / 0.82))); DA.g.lookAt(p); if (f >= 0.82) impact((f - 0.82) / 0.18 * 0.5, p); daGlow.position.copy(DA.g.position); daGlow.material.opacity = DA.g.visible ? 0.8 : 0; pos = p.clone().add(V(0, 20, 140)); look = p.clone().add(V(0, 38, 0)); fov = 50; }
  else if (t < tDie - 0.05) { const f = prog(t, tJetzt, tDie - tJetzt); const p = dimAt(0.6 + f * 0.4, ROld); HE.g.visible = true; HE.g.position.set(lerp(240, 150, K.eio(f)), 40, lerp(140, 110, f)); HE.g.rotation.set(0, -0.9, 0.1); pos = HE.g.position.clone().add(V(10, 7, 26)); look = HE.g.position.clone().add(V(-2, 0, 0)); fov = 46; }
  else if (t < tIhr - 0.05) { const f = prog(t, tDie, tIhr - tDie); dimAt(1.1, ROld); HE.g.visible = true; HE.g.position.set(150, 40, 110); HE.g.rotation.set(0.2, -0.6 + f * 0.8, 0.1); pos = HE.g.position.clone().add(V(Math.sin(f * 1.2) * 14, 4, 14)); look = HE.g.position.clone(); fov = 42; }
  else if (t < tIm - 0.05) { const f = prog(t, tIhr, tIm - tIhr); const a = 1.2 + f * 1.6; dimAt(a, ROld); oOld.material.opacity = 0.35 * cl((t - tIhr - 0.5) / 0.8); const d = t < tUnd ? lerp(230, 170, f) : 150; pos = V(Math.sin(0.4) * d, d * 0.55, Math.cos(0.4) * d); look = t < tUnd ? V(0, 0, 0) : DIM.position.clone().multiplyScalar(0.5); fov = 44; }
  else if (t < tDer - 0.05) { const tHit = W("dimorphos", 32.5) + 0.05; const p = dimAt(0.3, ROld); DA.g.visible = t < tHit; const from = p.clone().add(V(6, 95, 25)); const k0 = cl((t - tIm) / (tHit - tIm)); DA.g.position.copy(from.clone().lerp(p, Math.pow(k0, 1.5))); DA.g.lookAt(p);
    daGlow.position.copy(DA.g.position); daGlow.material.opacity = DA.g.visible ? 0.7 : 0; if (!DA.g.visible) impact(cl((t - tHit) / 1.2), p); pos = p.clone().add(V(0, 20, 140)); look = p.clone().add(V(0, 38, 0)); fov = 52; }
  else if (t < tUnd2 - 0.05) { scene = se; const f = prog(t, tDer, tUnd2 - tDer); EA.group.rotation.y = t * 0.02; const A = V(-260, 30, -200), B = V(0, 0, 0), C = V(260, -30, 200); pathA.geometry.setFromPoints([A, B]); pathA.computeLineDistances(); pathA.material.opacity = 0.9;
    const k = K.eio(f); rock.position.copy(A.clone().lerp(V(0, 120, 0), k)); pathB.geometry.setFromPoints([A, V(-130, 75, -100), V(260, 160, 200)]); pathB.computeLineDistances(); pathB.material.opacity = cl((t - W("wegschubsen") + 0.3) / 0.5); pos = V(60, 120, 330); look = V(-40, 40, 0); fov = 46; }
  else if (t < tAber - 0.05) { const f = prog(t, tUnd2, tAber - tUnd2); dimAt(t * 0.9, t > W("seitdem") ? lerp(ROld, RNew, cl((t - W("seitdem")) / 2)) : ROld); oOld.material.opacity = 0.45; oNew.material.opacity = 0.9 * cl((t - W("seitdem") - 0.5) / 0.8); pos = V(0, 240, 120); look = V(0, 0, 0); fov = 44; }
  else if (t < tSie - 0.05) { const f = prog(t, tAber, tSie - tAber); const p = dimAt(0.9, RNew); const a = f * 1.4; pos = p.clone().add(V(Math.sin(a) * 30, 8, Math.cos(a) * 30)); look = p; fov = 40; }
  else if (t < tErst - 0.05) { const f = prog(t, tSie, tErst - tSie); const p = dimAt(1.0, RNew); HE.g.visible = true; HE.g.position.copy(p).add(V(60, 25, 50)); HE.g.rotation.set(0, -0.8, 0); CS.forEach((c, i) => { c.g.visible = true; c.g.position.copy(HE.g.position.clone().lerp(p, K.eio(f) * (0.55 + i * 0.15))).add(V(i ? 6 : -6, i ? -4 : 4, 0)); c.g.rotation.set(t * 0.2, i + t * 0.3, 0); });
    pos = HE.g.position.clone().add(V(20, 10, 40)); look = HE.g.position.clone().lerp(p, 0.5); fov = 46; }
  else { const f = prog(t, tErst, END - tErst); const p = dimAt(2.6, RNew); sun.intensity = 2.6; pos = V(Math.cos(2.6) * 220 + 40, 30, Math.sin(2.6) * 220 + 120); pos = p.clone().add(V(lerp(70, 50, f), 10, lerp(40, 30, f))); look = p.clone().add(V(-20, 0, -10)); fov = 44; }
  cam.fov = fov; cam.near = 0.1; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("nasa", 1) - 0.1, tJetzt - 0.1, logo("nasa.svg", 80)); seg(W("europäischen") - 0.1, tIhr - 0.1, logo("esa.svg", 70));
  seg(W("über", 30) - 0.1, tDer - 0.1, "💥 > 20.000 km/h"); seg(W("rund", 42.2) - 0.1, tAber - 0.1, "⏱️ 33 Minuten schneller"); seg(tAm, END, "📅 25. November");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
