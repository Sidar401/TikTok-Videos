const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(51);
// @modelle
const sunT = await tex("sun.jpg");
const star = (sc, r, col, glow, gs = 3) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(...col), toneMapped: false, transparent: true })); sc.add(m); m.userData.glow = K.sprite(sc, K.glowTex(glow), r * gs, V(0, 0, 0), 0.6); return m; };
// ================= Sternpaar (Einheit: 1 Sonnenradius / 10) =================
const sc = new THREE.Scene(); K.stars(sc, 9000, -1, 60000, 1.7).material.opacity = 0.7;
const BIG = star(sc, 60, [1.35, 0.5, 0.3], "rgba(255,90,40,.55)", 3.2); const LIT = star(sc, 4, [1.4, 1.15, 0.8], "rgba(255,220,150,1)", 6);
const SUN = star(sc, 3.5, [1.3, 1.0, 0.72], "rgba(255,170,70,.6)", 4); SUN.visible = false;
const trail = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0xffe2a0, transparent: true, opacity: 0, toneMapped: false })); sc.add(trail);
// Gas-Hülle beim Ausbruch
const gas = []; { K.reseed(9); for (let i = 0; i < 220; i++) { const m = new THREE.SpriteMaterial({ map: K.glowTex(i % 3 ? "rgba(255,140,70,1)" : "rgba(255,210,160,1)"), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }); const s = new THREE.Sprite(m); const d = V(K.rnd() - 0.5, (K.rnd() - 0.5) * 0.6, K.rnd() - 0.5).normalize(); s.userData = { d, v: 0.6 + K.rnd() * 0.8, sz: 10 + K.rnd() * 30 }; sc.add(s); gas.push(s); } }
const flash = K.sprite(sc, K.glowTex("rgba(255,245,230,1)"), 600, V(0, 0, 20), 0);
const bigO = new THREE.Object3D(); sc.add(bigO); bigO.position.set(0, 60, 0); const litO = new THREE.Object3D(); sc.add(litO); const sunO = new THREE.Object3D(); sc.add(sunO);
// ================= Andromeda =================
const sg = new THREE.Scene(); { K.reseed(33); const p = [], c = []; for (let i = 0; i < 80000; i++) { const core = K.rnd() < 0.18; let r, a, y; if (core) { r = Math.pow(K.rnd(), 2) * 12; a = K.rnd() * 6.283; y = (K.rnd() - 0.5) * 4; } else { const arm = i % 2; r = Math.pow(K.rnd(), 0.7) * 76; a = arm * Math.PI + Math.log(r / 76 * 12 + 1) * 2.4 + (K.rnd() - 0.5) * 0.7; y = (K.rnd() - 0.5) * 1.5; }
    p.push(Math.cos(a) * r, y, Math.sin(a) * r); const col = new THREE.Color(1, 0.9, 0.78).lerp(new THREE.Color(0.65, 0.75, 1), core ? 0 : Math.min(1, r / 76 + 0.2)); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const pts = new THREE.Points(g, new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false })); const G = new THREE.Group(); G.add(pts); K.sprite(G, K.glowTex("rgba(255,225,180,.7)"), 30, V(0, 0, 0), 0.4); G.rotation.set(1.25, 0, 0.6); sg.add(G); K.stars(sg, 5000, -1, 60000, 1.5).material.opacity = 0.5; }
const mark = K.sprite(sg, K.glowTex("rgba(255,120,60,1)"), 5, V(28, 0, -10), 0); const markO = new THREE.Object3D(); markO.position.copy(mark.position); sg.add(markO);
const ringM = new THREE.Mesh(new THREE.TorusGeometry(5, 0.25, 8, 64), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); ringM.position.copy(mark.position); sg.add(ringM);
// ================= James Webb =================
const sj = new THREE.Scene(); K.stars(sj, 9000, -1, 60000, 1.7).material.opacity = 0.8; sj.add(new THREE.AmbientLight(0x30343e, 0.7)); const lj = new THREE.DirectionalLight(0xfff2e0, 2.2); lj.position.set(-3, 5, 4); sj.add(lj);
const JW = MO.jwst(); sj.add(JW.g); const jwO = new THREE.Object3D(); JW.g.add(jwO); jwO.position.set(0, 7, 0);
// ===== Zeiten =====
const tFor = W("forscher"), tUnd = W("und", 9), tPass = W("passiert"), tNen = W("die", 18.3), tBig = W("big", 22.3), tLit = W("little", 29.4), tKr = W("die", 33.2), tDann = W("dann", 40), tIm = W("im", 45.5), tDab = W("dabei"), tNur = W("nur", 53.6), tSo = W("so", 57.2), tUebr = W("übrig", 61.6), END = 67.4, KARTE = 13.0;
label("Big Bao", bigO, 0, { t0: tNen + 1.6, t1: tKr - 0.1, size: 56, gap: 20 }); label("Little Bao", litO, 4, { t0: W("little", 21) - 0.1, t1: tKr - 0.1, size: 50, gap: 18 }); label("Sonne", sunO, 3.5, { t0: tBig + 1.5, t1: tKr - 0.1, size: 46, gap: 14 });
label("James Webb", jwO, 2, { t0: tUnd + 0.6, t1: tPass - 0.1, size: 52, gap: 18 }); label("Bao", bigO, 0, { t0: tUebr + 1.2, t1: END, size: 60, gap: 20 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.32, 0.86);
  let scene = sc, pos = V(0, 60, 420), look = V(0, 0, 0), fov = 40; BIG.rotation.y = t * 0.03; LIT.rotation.y = t * 0.2; BIG.material.opacity = 1; BIG.scale.setScalar(1); BIG.userData.glow.material.opacity = 0.6;
  LIT.visible = true; LIT.userData.glow.visible = true; SUN.visible = false; SUN.userData.glow.visible = false; trail.material.opacity = 0; flash.material.opacity = 0; gas.forEach((s) => (s.material.opacity = 0)); BIG.position.set(0, 0, 0); BIG.userData.glow.position.set(0, 0, -10);
  const orbitAt = (k, R) => { const a = k; const p = V(Math.cos(a) * R, Math.sin(a) * R * 0.18, Math.sin(a) * R); LIT.position.copy(p); LIT.userData.glow.position.copy(p); litO.position.copy(p); return p; };
  const spiralTrail = (k0, k1, R0, R1) => { const pts = []; for (let i = 0; i <= 200; i++) { const f = i / 200; const k = lerp(k0, k1, f); const R = lerp(R0, R1, f); pts.push(V(Math.cos(k) * R, Math.sin(k) * R * 0.18, Math.sin(k) * R)); } trail.geometry.setFromPoints(pts); };
  if (t < tFor - 0.05) { const f = prog(t, 0, tFor); const k = f * 9; const R = lerp(110, 50, f * f); orbitAt(k, R); spiralTrail(Math.max(0, k - 3), k, lerp(110, 50, Math.max(0, f - 0.3) ** 2), R); trail.material.opacity = 0.6; if (f > 0.85) { LIT.visible = false; LIT.userData.glow.visible = false; flash.material.opacity = (f - 0.85) * 4; } pos = V(0, 120, 300); look = V(0, 0, 0); fov = 44; }
  else if (t < tUnd - 0.05) { const f = prog(t, tFor, tUnd - tFor); const k = 1 + f * 4; orbitAt(k, lerp(105, 80, f)); spiralTrail(k - 2.5, k, lerp(115, 105, f), lerp(105, 80, f)); trail.material.opacity = 0.5; const a = 0.4 + f * 0.4; pos = V(Math.sin(a) * 330, 70, Math.cos(a) * 330); look = V(10, 0, 0); fov = 42; }
  else if (t < tPass - 0.05) { scene = sj; const f = prog(t, tUnd, tPass - tUnd); JW.g.rotation.set(0.2, 0.5 + f * 0.5, 0); const a = 0.6 + f * 0.6; pos = V(Math.sin(a) * 26, 8, Math.cos(a) * 26); look = V(0, 1.5, 0); fov = 42; }
  else if (t < tNen - 0.05) { scene = sg; const f = prog(t, tPass, tNen - tPass); const d = lerpLog(420, 60, K.eio(cl(f * 1.2))); const tgt = mark.position.clone().multiplyScalar(K.eio(cl(f * 1.2))); pos = tgt.clone().add(V(0, d * 0.55, d)); look = tgt; fov = 44; mark.material.opacity = cl((t - tPass - 1.2) / 0.5); ringM.material.opacity = mark.material.opacity; ringM.lookAt(pos); }
  else if (t < tBig - 0.05) { const f = prog(t, tNen, tBig - tNen); orbitAt(1.2 + f * 1.5, 105); pos = V(20, 40, 360); look = V(30, 0, 0); fov = 42; }
  else if (t < tLit - 0.05) { const f = prog(t, tBig, tLit - tBig); orbitAt(2.5 + f * 0.6, 105); SUN.visible = true; SUN.userData.glow.visible = true; SUN.position.set(-90, -40, 40); SUN.userData.glow.position.copy(SUN.position); sunO.position.copy(SUN.position); pos = V(-10, 20, 330); look = V(-10, 0, 0); fov = 44; }
  else if (t < tKr - 0.05) { const f = prog(t, tLit, tKr - tLit); const p = orbitAt(3.1 + f * 0.4, 105); SUN.visible = true; SUN.userData.glow.visible = true; SUN.position.copy(p).add(V(14, 0, 0)); SUN.userData.glow.position.copy(SUN.position); sunO.position.copy(SUN.position); pos = p.clone().add(V(4, 6, 60)); look = p.clone().add(V(6, 0, 0)); fov = 42; }
  else if (t < tDann - 0.05) { const f = prog(t, tKr, tDann - tKr); const k = 3 + f * 9; const R = lerp(105, 66, f); orbitAt(k, R); spiralTrail(k - 4, k, lerp(110, 105, f), R); trail.material.opacity = 0.55; const glowUp = W("schon", 36) ; BIG.userData.glow.material.opacity = 0.6 + 0.4 * cl((t - glowUp) / 3); pos = V(0, 170, 300); look = V(0, 0, 0); fov = 44; }
  else if (t < tIm - 0.05) { const f = prog(t, tDann, tIm - tDann); BIG.material.opacity = 0.55; const k = 12 + f * 10; const R = lerp(64, 4, Math.pow(f, 0.8)); orbitAt(k, R); spiralTrail(k - 6, k, lerp(66, 64, f), R); trail.material.opacity = 0.8; pos = V(0, 140, 230); look = V(0, 0, 0); fov = 44; }
  else if (t < tNur - 0.05) { LIT.visible = false; LIT.userData.glow.visible = false; const f = prog(t, W("ausbruch") - 0.6, 6); const k = cl(f); flash.material.opacity = Math.max(0, 1 - k * 2.5) * (t > W("ausbruch") - 0.6 ? 1 : 0); E.grade.uniforms.flash.value = Math.max(0, 0.35 - k * 1.5) * (k > 0 ? 1 : 0);
    gas.forEach((s) => { const r = 60 + k * 260 * s.userData.v; s.position.copy(s.userData.d).multiplyScalar(r); s.scale.setScalar(s.userData.sz * (1 + k * 2)); s.material.opacity = k > 0 ? 0.2 * (1 - k * 0.6) : 0; });
    const a = 0.2 + prog(t, tIm, tNur - tIm) * 0.5; pos = V(Math.sin(a) * 560, 120, Math.cos(a) * 560); look = V(0, 0, 0); fov = 44; }
  else if (t < tSo - 0.05) { scene = sj; const f = prog(t, tNur, tSo - tNur); JW.g.rotation.set(0.15, 2.6 + f * 0.4, 0); pos = V(-18, 6, 16); look = V(0, 2, 0); fov = 42; }
  else { LIT.visible = false; LIT.userData.glow.visible = false; const k = 1; gas.forEach((s) => { const r = 60 + 260 * s.userData.v + (t - tSo) * 8; s.position.copy(s.userData.d).multiplyScalar(r); s.scale.setScalar(s.userData.sz * 3); s.material.opacity = 0.08; });
    BIG.scale.setScalar(0.8); const f = prog(t, tSo, END - tSo); const a = 0.8 + f * 0.6; const d = lerp(700, 380, K.eio(f)); pos = V(Math.sin(a) * d, 90, Math.cos(a) * d); look = V(0, 0, 0); fov = 44; }
  cam.fov = fov; cam.near = 0.1; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(tFor, tUnd - 0.1, "👀 zum ersten Mal live"); seg(W("james", 10) - 0.1, KARTE - 0.1, logo("nasa.svg", 80) + "📸 James Webb");
  seg(W("andromeda") - 0.1, W("zweieinhalb") - 0.1, "🌌 Andromeda-Galaxie"); seg(W("zweieinhalb") - 0.1, tNen - 0.1, "2,5 Mio. Lichtjahre");
  seg(W("siebenmal") - 0.2, W("und", 26.4) - 0.1, "7× so schwer wie die Sonne"); seg(W("und", 26.4), tLit - 0.1, "> 350× so breit"); seg(W("nicht", 31.2) - 0.1, tKr - 0.1, "< 1 Sonne schwer");
  seg(W("immer", 35) - 0.1, W("schon", 36) - 0.1, "🌀 immer enger"); seg(W("schon", 36), tDann - 0.1, "💡 seit ≈ 2018 heller"); seg(W("raste") - 0.1, tIm - 0.1, "bis in den Kern 🎯");
  seg(tIm, tDab - 0.1, "💥 Oktober 2025"); seg(tDab, tNur - 0.1, "Gas: ≈ 1/10 Sonne"); seg(tNur, tSo - 0.1, "📸 47 Tage später"); seg(tSo, tUebr - 0.1, "🔭 extrem selten"); seg(tUebr, END, "1 Stern übrig ⭐");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
