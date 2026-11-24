const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(62);
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
const tUm = W("um", 5), tDer = W("der", 10.5), tIm = W("im", 18), tEs = W("es", 25.5), tUnd = W("und", 30.5), tAber = W("aber", 37), tDie = W("die", 47), tIhre = W("ihre"), tJetzt = W("jetzt", 56), tWas = W("was", 60.5), END = 64.3, KARTE = 17.9;
label("Dimorphos", dimO, 8, { t0: W("dimorphos") - 0.1, t1: tIm - 0.1, size: 52, gap: 16 }); label("Didymos", didO, 4, { t0: W("didymos") - 0.1, t1: tAber - 0.1, size: 52, gap: 18 }); label("Hera", heO, 1, { t0: W("hera") - 0.1, t1: tIhre - 0.1, size: 54, gap: 18 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sc, pos = V(0, 60, 300), look = V(0, 0, 0), fov = 40; DID.rotation.y = t * 0.12; DIM.rotation.y = t * 0.3; DIM.scale.set(1, 1, 1);
  const dimAt = (a, R) => { const p = V(Math.cos(a) * R, 0, Math.sin(a) * R); DIM.position.copy(p); dimO.position.copy(p); return p; };
  oOld.material.opacity = 0; oNew.material.opacity = 0; flash.material.opacity = 0; ej.forEach((s) => (s.material.opacity = 0)); HE.g.visible = false; DA.g.visible = false; daGlow.material.opacity = 0; CS.forEach((c) => (c.g.visible = false));
  const impact = (k, p) => { flash.position.copy(p); flash.material.opacity = Math.max(0, 1 - k * 3); ej.forEach((s) => { const r = 8 + k * 70 * s.userData.v; s.position.copy(p).add(s.userData.d.clone().multiplyScalar(r)); s.scale.setScalar(1 + k * 3.5); s.material.opacity = k > 0 ? 0.4 * (1 - k) : 0; }); };
  const dart = (t0, tHit, p) => { flash.scale.setScalar(40); DA.g.visible = t < tHit; const from = p.clone().add(V(-30, 45, -10)); const k0 = cl((t - t0) / (tHit - t0)); DA.g.position.copy(from.clone().lerp(p, Math.pow(k0, 1.5))); DA.g.lookAt(p); daGlow.position.copy(DA.g.position); daGlow.material.opacity = DA.g.visible ? 0.35 : 0; if (!DA.g.visible) impact(cl((t - tHit) / 1.4), p); };
  if (t < tUm - 0.05) { const p = dimAt(0.6, ROld); dart(0, W("angerichtet") + 0.2, p); pos = p.clone().add(V(30, 8, 45)); look = p.clone().add(V(-8, 12, 0)); fov = 50; }
  else if (t < tDer - 0.05) { const f = prog(t, tUm, tDer - tUm); dimAt(0.6 + f * 0.4, ROld); HE.g.visible = true; HE.g.position.set(lerp(240, 150, K.eio(f)), 40, lerp(140, 110, f)); HE.g.rotation.set(0, -0.9 + f * 0.5, 0.1); pos = HE.g.position.clone().add(V(10, 7, 26)); look = HE.g.position.clone().add(V(-2, 0, 0)); fov = 46; }
  else if (t < tIm - 0.05) { const f = prog(t, tDer, tIm - tDer); const p = dimAt(1.0 + f * 0.3, ROld); const n = p.clone().normalize(); const sd = V(-n.z, 0, n.x); pos = p.clone().add(n.multiplyScalar(lerp(30, 22, f))).add(sd.multiplyScalar(lerp(-8, 8, f))).add(V(0, 6, 0)); look = p; fov = 40; }
  else if (t < tEs - 0.05) { const p = dimAt(0.3, ROld); dart(tIm, W("hineingekracht") + 0.3, p); pos = p.clone().add(V(30, 8, 45)); look = p.clone().add(V(-8, 12, 0)); fov = 52; }
  else if (t < tUnd - 0.05) { scene = se; const f = prog(t, tEs, tUnd - tEs); EA.group.rotation.y = t * 0.02; const A = V(-260, 30, -200), B = V(0, 0, 0); pathA.geometry.setFromPoints([A, B]); pathA.computeLineDistances(); pathA.material.opacity = 0.9;
    const k = K.eio(f); rock.position.copy(A.clone().lerp(V(0, 120, 0), k)); pathB.geometry.setFromPoints([A, V(-130, 75, -100), V(260, 160, 200)]); pathB.computeLineDistances(); pathB.material.opacity = cl((t - W("ablenken") + 0.3) / 0.5); pos = V(60, 120, 330); look = V(-40, 40, 0); fov = 46; }
  else if (t < tAber - 0.05) { const tS = W("seitdem"); dimAt(t * 0.9, t > tS ? lerp(ROld, RNew, cl((t - tS) / 2)) : ROld); oOld.material.opacity = 0.45; oNew.material.opacity = 0.9 * cl((t - tS - 0.5) / 0.8); pos = V(0, 240, 120); look = V(0, 0, 0); fov = 44; }
  else if (t < tDie - 0.05) { const f = prog(t, tAber, tDie - tAber); const p = dimAt(0.9, RNew); const kv = cl((t - W("verformt") + 0.2) / 1.2); DIM.scale.set(lerp(1, 1.18, kv), lerp(1, 0.78, kv), lerp(1, 1.06, kv)); const n = p.clone().normalize(); const sd = V(-n.z, 0, n.x); pos = p.clone().add(n.multiplyScalar(lerp(26, 20, f))).add(sd.multiplyScalar(lerp(10, -6, f))).add(V(0, 5, 0)); look = p; fov = 40; }
  else if (t < tIhre - 0.05) { const f = prog(t, tDie, tIhre - tDie); const p = dimAt(1.0, RNew); HE.g.visible = true; HE.g.position.copy(p).add(V(60, 25, 50)); HE.g.rotation.set(0, -0.8, 0); CS.forEach((c, i) => { c.g.visible = true; c.g.position.copy(HE.g.position.clone().lerp(p, K.eio(f) * (0.55 + i * 0.15))).add(V(i ? 6 : -6, i ? -4 : 4, 0)); c.g.rotation.set(t * 0.2, i + t * 0.3, 0); });
    pos = HE.g.position.clone().add(V(20, 10, 40)); look = HE.g.position.clone().lerp(p, 0.5); fov = 46; }
  else if (t < tJetzt - 0.05) { const f = prog(t, tIhre, tJetzt - tIhre); const p = dimAt(1.0, RNew); pos = p.clone().add(V(lerp(24, 20, f), 4, lerp(-12, -9, f))); look = p; fov = 40; }
  else { const f = prog(t, tJetzt, END - tJetzt); const p = dimAt(1.0, RNew); HE.g.visible = t < tWas; HE.g.position.copy(p).add(V(lerp(70, 40, f), 18, lerp(60, 34, f))); HE.g.rotation.set(0, -0.8, 0); const n = p.clone().normalize(); const sd = V(-n.z, 0, n.x); const d = lerp(60, 22, K.eio(f)); pos = p.clone().add(n.multiplyScalar(d)).add(sd.multiplyScalar(lerp(14, 4, f))).add(V(0, 6, 0)); look = p; fov = 42; }
  cam.fov = fov; cam.near = 0.1; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("nasa") - 0.1, tUm - 0.1, logo("nasa.svg", 80)); seg(W("europäische") - 0.1, tDer - 0.1, logo("esa.svg", 70) + "🔴 heute 19:45 Uhr live");
  seg(W("hundertfünfzig") - 0.1, tIm - 0.1, "📏 ≈ 150 Meter"); seg(W("sechzig") - 0.1, tJetzt - 0.1, "📸 aus 60 km"); seg(W("heute", 57.5) - 0.1, END, "🕗 heute Abend: Details!");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
