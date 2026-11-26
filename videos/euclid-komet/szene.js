const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(227);
// @modelle
const sunT = await tex("sun.jpg"), jupT = await tex("jupiter.jpg"), satT = await tex("saturn.jpg"), ringT = await tex("saturn_ring.png");
// ===== Komet: Kern + Koma + Schweif =====
function comet(parent, n = 1400) { const g = new THREE.Group(); parent.add(g); const nuc = MO.asteroid({ r: 1, seed: 11, craters: 30 }); const N = nuc.g || nuc; N.scale.setScalar(1); g.add(N);
  const coma = K.sprite(g, K.glowTex("rgba(170,225,255,.7)"), 6, V(0, 0, 0), 0.5), coma2 = K.sprite(g, K.glowTex("rgba(120,200,255,.35)"), 14, V(0, 0, 0), 0.35);
  const pos = new Float32Array(n * 3), seed = []; K.reseed(3001); for (let i = 0; i < n; i++) { seed.push([K.rnd(), K.rnd() - 0.5, K.rnd() - 0.5]); }
  const tg = new THREE.BufferGeometry(); tg.setAttribute("position", new THREE.BufferAttribute(pos, 3)); const tail = new THREE.Points(tg, new THREE.PointsMaterial({ color: 0xa8dcff, size: 3, sizeAttenuation: false, transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending, depthWrite: false })); tail.frustumCulled = false; parent.add(tail);
  const upd = (dir, len, act) => { const c = g.position; for (let i = 0; i < n; i++) { const [k, a, b] = seed[i]; const L = len * Math.pow(k, 1.3); const sp = 0.2 + L * 0.1; pos[i * 3] = c.x + dir.x * L + a * sp; pos[i * 3 + 1] = c.y + dir.y * L + b * sp; pos[i * 3 + 2] = c.z + dir.z * L + (a - b) * sp * 0.5; }
    tg.attributes.position.needsUpdate = true; tail.material.opacity = 0.6 * act; tail.visible = act > 0.01; coma.material.opacity = 0.15 + 0.5 * act; coma2.material.opacity = 0.1 + 0.3 * act; };
  return { g, N, tail, upd, coma, coma2 }; }
// ===== Euclid-Teleskop =====
function euclid() { const g = new THREE.Group(); const hex = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.2, 1.4, 6), MO.mliM()); g.add(hex);
  const plat = new THREE.Mesh(new THREE.CylinderGeometry(2.0, 2.0, 0.3, 32), MO.plain(0x6e737a, 0.4, 0.5)); plat.position.y = 0.85; g.add(plat);
  const tube = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.25, 3.4, 40, 1, true), MO.plain(0x2a2c31, 0.6, 0.4, 0.4, { side: THREE.DoubleSide })); tube.position.set(0, 2.7, 0.3); g.add(tube);
  const lip = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.06, 8, 48), MO.plain(0x80858c, 0.5, 0.4)); lip.rotation.x = Math.PI / 2; lip.position.set(0, 4.4, 0.3); g.add(lip);
  const shield = new THREE.Group(); shield.position.set(0, 2.4, -1.4); shield.rotation.x = 0.12; g.add(shield);
  const sh = new THREE.Mesh(new THREE.BoxGeometry(4.6, 6.2, 0.12), MO.plain(0xd9dbde, 0.5, 0.35)); shield.add(sh); const cells = new THREE.Mesh(new THREE.BoxGeometry(4.3, 5.9, 0.05), MO.cellM()); cells.position.z = -0.09; shield.add(cells);
  for (const s of [-1, 1]) { const a = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.6, 8), MO.plain(0x8a8f96, 0.7, 0.3)); a.rotation.x = Math.PI / 2; a.position.set(s * 1.4, 1.2, -0.7); g.add(a); }
  const dish = new THREE.Mesh(new THREE.SphereGeometry(0.5, 24, 8, 0, Math.PI * 2, 0, 0.8), MO.plain(0xe6e6e8, 0.3, 0.4, 0.4, { side: THREE.DoubleSide })); dish.rotation.x = Math.PI; dish.position.set(1.2, -0.9, 0.8); g.add(dish);
  return g; }
// ================= Komet im All (Hook / Ende) =================
const sc = new THREE.Scene(); K.stars(sc, 10000, -1, 60000, 1.7).material.opacity = 0.7; sc.add(new THREE.AmbientLight(0x30343e, 0.8)); const lc = new THREE.DirectionalLight(0xfff2e0, 2.4); lc.position.set(-1, 0.2, 0.3); sc.add(lc);
const C1 = comet(sc, 4000); const sunFar = K.sprite(sc, K.glowTex("rgba(255,230,180,1)"), 3000, V(-30000, 4000, 9000), 0.9); const anti = V(1, -0.13, -0.3).normalize();
// ================= Euclid =================
const se = new THREE.Scene(); K.stars(se, 9000, -1, 60000, 1.7).material.opacity = 0.8; se.add(new THREE.AmbientLight(0x30343e, 0.8)); const le = new THREE.DirectionalLight(0xfff2e0, 2.2); le.position.set(-3, 4, -5); le.intensity = 1.5; se.add(le); const le2 = new THREE.DirectionalLight(0x9fb4ff, 0.25); le2.position.set(4, 1, 5); se.add(le2);
const EU = euclid(); se.add(EU); const euO = new THREE.Object3D(); EU.add(euO); euO.position.set(0, 5.6, 0);
// ================= Galaxien + dunkle Materie =================
const sg = new THREE.Scene(); const gals = []; { K.reseed(51); for (let i = 0; i < 700; i++) { const col = K.rnd() < 0.5 ? "rgba(255,210,170,.9)" : "rgba(170,200,255,.9)"; const s = K.sprite(sg, K.glowTex(col), 6 + K.rnd() * 18, V((K.rnd() - 0.5) * 1600, (K.rnd() - 0.5) * 2800, -K.rnd() * 1200), 0.55); s.material.rotation = K.rnd() * 3; s.scale.set(s.scale.x, s.scale.y * (0.35 + K.rnd() * 0.65), 1); gals.push(s); } }
const webP = []; { K.reseed(61); const nodes = []; for (let i = 0; i < 40; i++) nodes.push(V((K.rnd() - 0.5) * 1600, (K.rnd() - 0.5) * 2800, -K.rnd() * 1200));
  for (let i = 0; i < 40; i++) { const a = nodes[i], b = nodes[(i * 7 + 3) % 40]; for (let k = 0; k < 400; k++) { const f = K.rnd(); const p = a.clone().lerp(b, f); webP.push(p.x + (K.rnd() - 0.5) * 40, p.y + (K.rnd() - 0.5) * 40, p.z + (K.rnd() - 0.5) * 40); } } }
const webG = new THREE.BufferGeometry(); webG.setAttribute("position", new THREE.Float32BufferAttribute(webP, 3)); const WEB = new THREE.Points(webG, new THREE.PointsMaterial({ color: 0x6d8cff, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); sg.add(WEB);
// ================= Bildfeld mit wanderndem Punkt =================
const sf = new THREE.Scene(); { K.reseed(88); const p = [], c = []; for (let i = 0; i < 50000; i++) { p.push((K.rnd() - 0.5) * 3000, (K.rnd() - 0.5) * 5400, -K.rnd() * 300); const col = new THREE.Color(1, 0.92, 0.85).lerp(new THREE.Color(0.6, 0.72, 1), K.rnd()); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3)); sf.add(new THREE.Points(g, new THREE.PointsMaterial({ size: 1.8, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false }))); }
const dot = K.sprite(sf, K.glowTex("rgba(190,235,255,1)"), 7, V(0, 0, 0), 1); const dRing = new THREE.Mesh(new THREE.TorusGeometry(12, 0.7, 8, 64), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); sf.add(dRing);
const trailP = new Float32Array(6 * 3); const trG = new THREE.BufferGeometry(); trG.setAttribute("position", new THREE.BufferAttribute(trailP, 3)); const TR = new THREE.Points(trG, new THREE.PointsMaterial({ color: 0x9fd8ff, size: 5, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); sf.add(TR);
// ================= Sonnensystem =================
const ss = new THREE.Scene(); K.stars(ss, 9000, -1, 60000, 1.7).material.opacity = 0.7; ss.add(new THREE.AmbientLight(0x404650, 0.6)); const lss = new THREE.PointLight(0xfff2e0, 3, 0, 0); ss.add(lss);
const SUN = new THREE.Mesh(new THREE.SphereGeometry(6, 64, 48), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(1.4, 1.05, 0.7), toneMapped: false })); ss.add(SUN); const sunG = K.sprite(ss, K.glowTex("rgba(255,190,90,.9)"), 40, V(0, 0, 0), 0.9);
const orbit = (r, col, op) => { const pts = []; for (let i = 0; i <= 256; i++) { const a = i / 256 * 6.2832; pts.push(V(Math.cos(a) * r, 0, Math.sin(a) * r)); } const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: op, toneMapped: false })); ss.add(l); return l; };
const dayT = new THREE.Texture(day); dayT.needsUpdate = true; dayT.colorSpace = THREE.SRGBColorSpace;
const planet = (r, map, d, a) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 64, 48), new THREE.MeshStandardMaterial({ map, roughness: 0.9 })); m.position.set(Math.cos(a) * d, 0, Math.sin(a) * d); ss.add(m); return m; };
const RE_ = 22, RJ = 75, RS = 120; orbit(RE_, 0x7ab8ff, 0.5); orbit(RJ, 0xffffff, 0.3); orbit(RS, 0xffffff, 0.3);
const EAR = planet(1.6, dayT, RE_, 0.9), JUP = planet(5, jupT, RJ, 0.3), SAT = planet(4.2, satT, RS, 0.6);
const ring = new THREE.Mesh(new THREE.RingGeometry(5.5, 9.5, 96), new THREE.MeshBasicMaterial({ map: ringT, transparent: true, side: THREE.DoubleSide, opacity: 0.9 })); { const p = ring.geometry.attributes.position, uv = ring.geometry.attributes.uv; for (let i = 0; i < p.count; i++) { const v = V(p.getX(i), p.getY(i), 0); uv.setXY(i, (v.length() - 5.5) / 4, 0.5); } } ring.rotation.x = -Math.PI / 2 + 0.45; SAT.add(ring);
const KD = K.sprite(ss, K.glowTex("rgba(190,235,255,1)"), 4, V(Math.cos(0.42) * 98, 2, Math.sin(0.42) * 98), 0); const kdO = new THREE.Object3D(); kdO.position.copy(KD.position); ss.add(kdO);
const dLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints([EAR.position, KD.position]), new THREE.LineDashedMaterial({ color: 0xffd23f, dashSize: 2, gapSize: 1.5, transparent: true, opacity: 0, toneMapped: false })); dLine.computeLineDistances(); ss.add(dLine);
const C2 = comet(ss, 1200); C2.g.scale.setScalar(0.6); C2.g.visible = false;
const path = []; for (let i = 0; i <= 200; i++) { const u = i / 200; const a = lerp(1.9, -0.4, u); const r = lerp(260, 12, Math.pow(u, 0.8)); path.push(V(Math.cos(a) * r, lerp(30, 0, u), Math.sin(a) * r)); }
const PL = new THREE.Line(new THREE.BufferGeometry().setFromPoints(path), new THREE.LineBasicMaterial({ color: 0x9fd8ff, transparent: true, opacity: 0, toneMapped: false })); ss.add(PL);
// ================= Komet weit draußen / nah an der Sonne =================
const sk = new THREE.Scene(); K.stars(sk, 9000, -1, 60000, 1.7).material.opacity = 0.75; sk.add(new THREE.AmbientLight(0x30343e, 0.6)); const lk = new THREE.DirectionalLight(0xfff2e0, 1.0); lk.position.set(-1, 0.1, 0.2); sk.add(lk);
const C3 = comet(sk, 3500); const sunK = K.sprite(sk, K.glowTex("rgba(255,220,150,1)"), 28, V(-60, 5, 10), 0);
// ================= Comet Interceptor =================
const si = new THREE.Scene(); K.stars(si, 9000, -1, 60000, 1.7).material.opacity = 0.8; si.add(new THREE.AmbientLight(0x30343e, 0.8)); const li = new THREE.DirectionalLight(0xfff2e0, 2.2); li.position.set(-3, 3, 4); si.add(li);
const CI = MO.hera(); const CIg = CI.g || CI; si.add(CIg); CIg.traverse((o) => { if (o.isMesh && o.material && o.material.color && o.material.color.getHex() === 0xb9b6ad) o.material = MO.mliM(); }); const ciO = new THREE.Object3D(); CIg.add(ciO); ciO.position.set(0, 2, 0);
const C4 = comet(si, 1500); C4.g.position.set(-25, 40, -150);
const eaSmall = K.earth(si, { day, night, topo }, 40); eaSmall.group.position.set(120, -90, -300); eaSmall.U.sun.value = V(-1, 0.3, 0.4).normalize();
// ===== Zeiten =====
const tUnd = W("und", 4), tEig = W("eigentlich"), tDie = W("die", 9.6), tDaf = W("dafür"), tDoch = W("doch"), tEnt = W("entdeckt", 21), tEs = W("es", 23.9), tDer = W("der", 27.3), tEr = W("er", 30.3), tDasB = W("das", 36.9), tSein = W("sein", 40.8), tEuc = W("euclid", 43.2), tGen = W("genau"), tDiese = W("diese", 50.3), tJe = W("und", 55.5), tWas = W("was", 58.7), END = 63.0, KARTE = 12.89;
label("Euclid", euO, 1, { t0: tUnd + 0.4, t1: tEig - 0.1, size: 64, gap: 22 }); label("C/2026 S1 (Euclid)", C2.g, 1, { t0: 99, t1: 99 }); const lbK = label("C/2026 S1", kdO, 1, { t0: 99, t1: 99, size: 44, gap: 14 });
const lbN = label("C/2026 S1<small>Euclid</small>", C3.g, 1.4, { t0: tEs + 0.4, t1: tEr - 0.1, size: 60, gap: 24 }); label("Jupiter", JUP, 5, { t0: W("jupiter") - 0.1, t1: tDasB - 0.1, size: 44, gap: 10 }); label("Saturn", SAT, 4.2, { t0: W("saturn") - 0.1, t1: tDasB - 0.1, size: 44, gap: 10 }); label("Erde", EAR, 1.6, { t0: tEr + 0.3, t1: tDasB - 0.1, size: 40, gap: 8 });
label("Comet Interceptor", ciO, 1, { t0: W("comet") - 0.1, t1: tJe - 0.1, size: 54, gap: 22 });
lbK.t0 = W("zwischen", 33) - 0.1; lbK.t1 = tDasB - 0.1;
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sc, pos = V(0, 0, 40), look = V(0, 0, 0), fov = 42; [C1, C3, C4].forEach((c) => c.N.rotation.set(t * 0.15, t * 0.25, 0));
  if (t < tUnd - 0.05) { const f = prog(t, 0, tUnd); C1.g.position.set(lerp(-30, 10, f), lerp(4, -1, f), 0); C1.upd(anti, 70, 1); pos = C1.g.position.clone().add(V(-5, 3, 16)); look = C1.g.position.clone().add(V(3, -0.8, -1)); fov = 50; }
  else if (t < tDie - 0.05) { scene = se; const f = prog(t, tUnd, tDie - tUnd); EU.rotation.set(0.1, 0.6 + f * 1.0, 0.05); const d = lerp(17, 14, f); pos = V(Math.sin(0.4 + f * 0.3) * d, lerp(5, 3, f), Math.cos(0.4 + f * 0.3) * d); look = V(0, 2.2, 0); fov = 44; }
  else if (t < tDoch - 0.05) { scene = sg; const f = prog(t, tDie, tDoch - tDie); WEB.material.opacity = 0.55 * cl((t - tDie) / 0.6) * (1 - cl((t - tDaf - 0.3) / 0.8)); const z = lerp(900, 2600, K.eio(f)); pos = V(0, 0, z); look = V(0, 0, -400); fov = 50; }
  else if (t < tEs - 0.05) { scene = sf; const f = prog(t, tDoch, tEs - tDoch); const k = cl((t - W("winzigen") + 0.3) / 3.0); dot.position.set(30 + k * 26, -40 + k * 14, 5); dRing.position.copy(dot.position); dRing.material.opacity = cl((t - W("stillhielt") - 0.3) / 0.4);
    for (let i = 0; i < 6; i++) { const kk = Math.max(0, k - i * 0.12); trailP[i * 3] = 30 + kk * 26; trailP[i * 3 + 1] = -40 + kk * 14; trailP[i * 3 + 2] = 4; } trG.attributes.position.needsUpdate = true; TR.material.opacity = 0.35 * (k > 0 ? 1 : 0);
    const z = lerpLog(2200, 180, K.eio(cl(f * 1.6))); pos = V(lerp(0, 43, cl(f * 1.6)), lerp(0, -33, cl(f * 1.6)), z); look = V(pos.x, pos.y, -100); fov = 50; }
  else if (t < tEr - 0.05) { scene = sk; const f = prog(t, tEs, tEr - tEs); C3.g.position.set(0, 0, 0); C3.upd(V(1, 0, -0.2).normalize(), 4, 0.25); sunK.material.opacity = 0; const a = 0.3 + f * 0.8; pos = V(Math.sin(a) * 7, 2, Math.cos(a) * 7); look = V(0, 0.2, 0); fov = 42; }
  else if (t < tDasB - 0.05) { scene = ss; const f = prog(t, tEr, tDasB - tEr); KD.material.opacity = 1; KD.scale.setScalar(4 + Math.sin(t * 5)); dLine.material.opacity = 0.9 * cl((t - tEr - 0.5) / 0.6); pos = V(55 + f * 10, lerp(250, 280, f), 210); look = V(52, 0, 40); fov = 44; }
  else if (t < tEuc - 0.05) { scene = sk; const near = t > tSein - 0.1; const f = prog(t, tDasB, tEuc - tDasB); C3.g.position.set(0, 0, 0);
    if (!near) { C3.upd(V(1, 0, -0.2).normalize(), 2, 0.12); sunK.material.opacity = 0; lk.intensity = 0.35; pos = V(4, 1.2, 9); look = V(0, 0, 0); }
    else { const k = cl((t - tSein) / 2); C3.upd(V(0.15, -1, -0.1).normalize(), lerp(6, 55, K.eout(k)), 1); sunK.position.set(-3, 30, -10); sunK.material.opacity = 0.95; lk.position.set(-0.1, 1, 0.1); lk.intensity = 2.4; pos = V(6, -8, 70); look = V(0, -10, 0); } fov = 50; }
  else if (t < tGen - 0.05) { scene = se; const f = prog(t, tEuc, tGen - tEuc); EU.rotation.set(0.15, 2.2 + f * 0.6, 0); pos = V(Math.sin(2.6 + f * 0.3) * 12 + 2, 6, Math.cos(2.6 + f * 0.3) * 12); look = V(0, 2.5, 0); fov = 44; }
  else if (t < tJe - 0.05) { scene = si; const f = prog(t, tGen, tJe - tGen); const go = cl((t - W("abfangen") + 1.2) / 3); C4.upd(V(-0.6, 0.6, -0.3).normalize(), 70, 1); CIg.position.copy(V(0, 0, 0).lerp(C4.g.position.clone().multiplyScalar(0.85), K.eio(go) * 0.35)); CIg.rotation.set(0.2, 0.6 + t * 0.08, 0);
    pos = CIg.position.clone().add(V(lerp(3, 5, f), -3, lerp(13, 16, f))); look = CIg.position.clone().add(V(-1.5, 4, -10)); fov = 50; }
  else if (t < tWas - 0.05) { scene = ss; const f = prog(t, tJe, tWas - tJe); KD.material.opacity = 0; PL.material.opacity = 0.6; C2.g.visible = true; const u = K.eio(f) * 0.85; const idx = Math.floor(u * 200); C2.g.position.copy(path[idx]); C2.upd(C2.g.position.clone().normalize(), lerp(2, 40, u * u), cl(u * 1.5)); const a = 0.8 + f * 0.4; pos = V(Math.cos(a) * 200, 240, Math.sin(a) * 200 + 80); look = V(20, 0, 20); fov = 46; }
  else { const f = prog(t, tWas, END - tWas); C1.g.position.set(lerp(-8, 4, f), 0, 0); C1.upd(anti, 70, 1); const a = -0.3 + f * 0.5; pos = C1.g.position.clone().add(V(-4 + f * 2, 3.5, 17)); look = C1.g.position.clone().add(V(1.8, -0.8, -1)); fov = 50; }
  if (scene !== ss) { C2.g.visible = false; C2.tail.visible = false; PL.material.opacity = 0; } if (scene === ss && t < tJe - 0.05) { C2.g.visible = false; C2.tail.visible = false; PL.material.opacity = 0; }
  cam.fov = fov; cam.near = 0.05; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("europäische") - 0.2, tEig - 0.1, logo("esa.svg", 70) + "🔭 Euclid"); seg(W("helsinki") - 0.3, tEs - 0.1, "🇫🇮 Helsinki"); seg(W("eins", 31) - 0.1, W("irgendwo") - 0.1, "1,3 Mrd. km");
  seg(W("esa", 45) - 0.2, tDiese - 0.1, logo("esa.svg", 70) + "☄️ Comet Interceptor");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
