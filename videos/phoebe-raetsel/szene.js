const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(441);
// @modelle
const moonT = await tex("moon.jpg"), jupT = await tex("jupiter.jpg");
// ===== Unsichtbares Objekt: nur ein schwacher Rand =====
const ghostMat = () => new THREE.ShaderMaterial({ uniforms: { op: { value: 1 }, time: { value: 0 } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec3 vN;varying vec3 vV;void main(){vec4 w=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-w.xyz);gl_Position=projectionMatrix*w;}`,
  fragmentShader: `uniform float op,time;varying vec3 vN;varying vec3 vV;void main(){float f=pow(1.-max(dot(vN,vV),0.),3.);float w=.8+.2*sin(time*2.);gl_FragColor=vec4(vec3(.62,.55,1.)*f*1.6*w*op,f*op);}` });
const ghost = (parent, r) => { const g = new THREE.Group(); const m = new THREE.Mesh(new THREE.SphereGeometry(r, 64, 48), ghostMat()); g.add(m); const inner = new THREE.Mesh(new THREE.SphereGeometry(r * 0.98, 48, 32), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.55, depthWrite: false })); g.add(inner); parent.add(g); return { g, m }; };
// ================= Stern + Phoebe (Linse) =================
const sl = new THREE.Scene(); K.stars(sl, 10000, -1, 60000, 1.7).material.opacity = 0.75;
const STAR = K.sprite(sl, K.glowTex("rgba(255,235,210,1)"), 14, V(0, 0, -300), 1); const STAR2 = K.sprite(sl, K.glowTex("rgba(255,200,150,.6)"), 40, V(0, 0, -300), 0.4);
const G1 = ghost(sl, 6); const ph = new THREE.Object3D(); G1.g.add(ph); ph.position.set(0, 6, 0);
// Lichtstrahlen (Seitenansicht): Stern oben, Phoebe Mitte, Erde unten
const rays = []; const rayM = new THREE.LineBasicMaterial({ color: 0xffe2a8, transparent: true, opacity: 0, toneMapped: false });
const RG = new THREE.Group(); sl.add(RG); RG.position.set(0, 0, 200); const rStar = K.sprite(RG, K.glowTex("rgba(255,235,210,1)"), 10, V(0, 90, 0), 1); const G2 = ghost(RG, 4);
const EAR = new THREE.Mesh(new THREE.SphereGeometry(3, 48, 32), new THREE.MeshStandardMaterial({ map: (() => { const t = new THREE.Texture(day); t.needsUpdate = true; t.colorSpace = THREE.SRGBColorSpace; return t; })(), roughness: 0.8 })); EAR.position.set(0, -75, 0); RG.add(EAR); sl.add(new THREE.AmbientLight(0x404858, 0.6)); const lE = new THREE.DirectionalLight(0xfff2e0, 2); lE.position.set(-1, 1, 1); sl.add(lE);
for (let i = -4; i <= 4; i++) { if (!i) continue; const o = i * 3.2 + Math.sign(i) * 3; const c = new THREE.QuadraticBezierCurve3(V(0, 90, 0), V(o * 2, 0, 0), V(0, -72, 0)); const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(c.getPoints(60)), rayM); RG.add(l); rays.push(l); }
const eO = new THREE.Object3D(); RG.add(eO); eO.position.set(0, -75, 0);
// ================= Altes Bildfeld =================
const sf = new THREE.Scene(); { K.reseed(88); const p = [], c = []; for (let i = 0; i < 50000; i++) { p.push((K.rnd() - 0.5) * 3000, (K.rnd() - 0.5) * 5400, -K.rnd() * 300); const col = new THREE.Color(1, 0.92, 0.85).lerp(new THREE.Color(0.6, 0.72, 1), K.rnd()); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3)); sf.add(new THREE.Points(g, new THREE.PointsMaterial({ size: 1.8, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false }))); }
const fStar = K.sprite(sf, K.glowTex("rgba(255,235,210,1)"), 8, V(-40, 60, 5), 1); const frame = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(30, 30)), new THREE.LineBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); frame.position.set(-40, 60, 6); sf.add(frame);
// ================= Milchstraße + Nachbargalaxie =================
const galaxy = (parent, R, n, seed, tilt, irr = false) => { K.reseed(seed); const p = [], c = []; for (let i = 0; i < n; i++) { let x, y, z; if (irr) { const r = Math.pow(K.rnd(), 0.6) * R; const a = K.rnd() * 6.283; x = Math.cos(a) * r * 1.5 + (K.rnd() - 0.5) * R * 0.3; y = (K.rnd() - 0.5) * R * 0.15; z = Math.sin(a) * r * 0.8; }
    else { const core = K.rnd() < 0.15; let r, a; if (core) { r = Math.pow(K.rnd(), 2) * R * 0.16; a = K.rnd() * 6.283; y = (K.rnd() - 0.5) * R * 0.05; } else { const arm = i % 2; r = Math.pow(K.rnd(), 0.7) * R; a = arm * Math.PI + Math.log(r / R * 12 + 1) * 2.4 + (K.rnd() - 0.5) * 0.7; y = (K.rnd() - 0.5) * R * 0.02; } x = Math.cos(a) * r; z = Math.sin(a) * r; }
    p.push(x, y, z); const col = new THREE.Color(1, 0.9, 0.78).lerp(new THREE.Color(0.65, 0.75, 1), K.rnd() * 0.8); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const m = new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false }); const G = new THREE.Group(); G.add(new THREE.Points(g, m)); G.rotation.set(tilt, 0, 0.3); parent.add(G); G.userData.m = m; return G; };
const sg = new THREE.Scene(); K.stars(sg, 6000, -1, 60000, 1.5).material.opacity = 0.5; const MW = galaxy(sg, 300, 90000, 41, 0.9); const LMC = galaxy(sg, 60, 20000, 52, 0.5, true); LMC.position.set(260, -230, 120);
const lmcO = new THREE.Object3D(); LMC.add(lmcO); const mwO = new THREE.Object3D(); MW.add(mwO); mwO.position.set(0, 0, 0);
const lStar = K.sprite(sg, K.glowTex("rgba(255,240,220,1)"), 4, V(270, -228, 125), 0);
const halo = []; { K.reseed(61); for (let i = 0; i < 30000; i++) { const r = 120 + Math.pow(K.rnd(), 0.5) * 380; const u = K.rnd() * 2 - 1, a = K.rnd() * 6.283; halo.push(Math.sqrt(1 - u * u) * Math.cos(a) * r, u * r * 0.8, Math.sqrt(1 - u * u) * Math.sin(a) * r); } }
const hG = new THREE.BufferGeometry(); hG.setAttribute("position", new THREE.Float32BufferAttribute(halo, 3)); const HALO = new THREE.Points(hG, new THREE.PointsMaterial({ color: 0x6d8cff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); sg.add(HALO);
const phG = ghost(sg, 5); phG.g.position.set(150, -120, 60); phG.g.visible = false;
// ================= Mond-Vergleich =================
const sm = new THREE.Scene(); K.stars(sm, 6000, -1, 60000, 1.5).material.opacity = 0.6; sm.add(new THREE.AmbientLight(0x404858, 0.5)); const lm = new THREE.DirectionalLight(0xfff2e0, 2.4); lm.position.set(-1, 0.4, 0.8); sm.add(lm);
const moons = [-1, 0, 1].map((k) => { const m = new THREE.Mesh(new THREE.SphereGeometry(3, 64, 48), new THREE.MeshStandardMaterial({ map: moonT, roughness: 1 })); m.position.set(k * 7, 6, 0); sm.add(m); return m; }); const G3 = ghost(sm, 2); G3.g.position.set(0, -6, 0);
// ================= Urknall + uraltes Schwarzes Loch =================
const sb = new THREE.Scene(); K.stars(sb, 7000, -1, 60000, 1.6).material.opacity = 0.6; const bang = K.sprite(sb, K.glowTex("rgba(255,240,220,1)"), 10, V(0, 0, 0), 0); const bang2 = K.sprite(sb, K.glowTex("rgba(255,150,90,.7)"), 10, V(0, 0, 0), 0);
const BH = new THREE.Group(); sb.add(BH); BH.add(new THREE.Mesh(new THREE.SphereGeometry(2, 64, 48), new THREE.MeshBasicMaterial({ color: 0x000000 })));
const pring = new THREE.Mesh(new THREE.TorusGeometry(2.15, 0.06, 12, 128), new THREE.MeshBasicMaterial({ color: 0xffd9a8, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); BH.add(pring);
const diskM = new THREE.ShaderMaterial({ uniforms: { time: { value: 0 } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec2 vP;void main(){vP=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float time;varying vec2 vP;void main(){float r=length(vP);float a=atan(vP.y,vP.x);float k=(r-2.4)/5.6;float sw=.6+.4*sin(a*6.-r*2.+time*3.);vec3 c=mix(vec3(1.,.95,.85),vec3(1.,.45,.15),smoothstep(0.,.7,k));float al=(1.-smoothstep(0.,1.,k))*sw*smoothstep(0.,.05,k);gl_FragColor=vec4(c*al*1.3,al);}` });
const DISK = new THREE.Mesh(new THREE.RingGeometry(2.4, 8, 128, 2), diskM); DISK.rotation.x = -1.3; BH.add(DISK); const bhG = K.sprite(BH, K.glowTex("rgba(255,190,120,.5)"), 26, V(0, 0, 0), 0.4); BH.scale.setScalar(0.001);
// ================= Einsamer Planet =================
const sr = new THREE.Scene(); K.stars(sr, 9000, -1, 60000, 1.7).material.opacity = 0.75; sr.add(new THREE.AmbientLight(0x1a2030, 0.4)); const lr = new THREE.DirectionalLight(0x9fb4ff, 1.8); lr.position.set(1, 0.3, -0.5); sr.add(lr);
const ROG = new THREE.Mesh(new THREE.SphereGeometry(6, 96, 64), new THREE.MeshStandardMaterial({ map: jupT, color: 0x6a7488, roughness: 0.9 })); sr.add(ROG); const rogO = new THREE.Object3D(); ROG.add(rogO);
const LMC2 = galaxy(sr, 120, 20000, 52, 0.5, true); LMC2.position.set(-60, 150, -600); LMC2.userData.m.opacity = 0;
// ===== Zeiten =====
const tFor = W("forscher"), tEin = W("ein", 8.2), tDer = W("der", 13.2), tDies = W("dieses"), tEs = W("es", 24), tUnd = W("und", 26.7), tViel = W("vielleicht"), tSol = W("solche"), tOder = W("oder"), tLieg = W("liegt"), tDoch = W("doch"), tDas = W("das", 60), END = 65.9, KARTE = 13.3;
label("Phoebe", ph, 0.5, { t0: W("phoebe") - 0.1, t1: tEs - 0.1, size: 64, gap: 20 }); label("Erde", eO, 3, { t0: tDer + 0.3, t1: tDies - 0.1, size: 44, gap: 10 }); label("Nachbargalaxie", lmcO, 12, { t0: W("nachbargalaxie") - 0.2, t1: tDer - 0.1, size: 46, gap: 14 }); label("Milchstraße", mwO, 30, { t0: W("nachbargalaxie") - 0.2, t1: tDer - 0.1, size: 46, gap: 14 });
label("Planet ohne Sonne", rogO, 6, { t0: W("einsamer") - 0.1, t1: tLieg - 0.1, size: 52, gap: 20 });
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sl, pos = V(0, 0, 60), look = V(0, 0, 0), fov = 42; [G1, G2, G3, phG].forEach((q) => (q.m.material.uniforms.time.value = t)); rayM.opacity = 0; RG.visible = false; G1.g.visible = true; STAR.scale.setScalar(14); STAR.material.opacity = 1; STAR2.scale.setScalar(40); STAR2.material.opacity = 0.4; diskM.uniforms.time.value = t; pring.quaternion.copy(cam.quaternion);
  const passBy = (x) => { G1.g.position.set(x, 0.6, 0); const b = 1 / (1 + Math.pow(x / 5, 2)); STAR.scale.setScalar(14 + 46 * b); STAR2.material.opacity = 0.4 + 0.6 * b; STAR2.scale.setScalar(40 + 50 * b); };
  if (t < tFor - 0.05) { const f = prog(t, 0, tFor); passBy(lerp(-26, 14, f)); pos = V(0, 0, 70); fov = 40; }
  else if (t < tEin - 0.05) { scene = sf; const f = K.eio(prog(t, tFor, tEin - tFor)); frame.material.opacity = cl((t - tFor - 2) / 0.5); const z = lerpLog(2400, 140, f); pos = V(lerp(0, -40, f), lerp(0, 60, f), z); look = V(pos.x, pos.y, -100); fov = 50; fStar.scale.setScalar(8); }
  else if (t < tDer - 0.05) { scene = sg; MW.userData.m.opacity = 0.8; LMC.userData.m.opacity = 0.8; const f = prog(t, tEin, tDer - tEin); const k = 0.45 * K.eio(cl(f * 1.3)); pos = V(lerp(150, 290, k), lerp(500, -150, k), lerp(900, 260, k)); look = V(lerp(60, 265, k), lerp(-60, -228, k), lerp(30, 120, k)); fov = 44;
    const fl = cl((t - W("heller") + 0.2) / 0.5) * (1 - cl((t - W("stunde") - 0.8) / 0.6)); lStar.material.opacity = 0.6 + fl; lStar.scale.setScalar(4 + 14 * fl); }
  else if (t < tDies - 0.05) { const f = prog(t, tDer, tDies - tDer); G1.g.visible = false; RG.visible = true; rayM.opacity = 0.85 * cl((t - W("etwas", 14) - 0.6) / 1.2); STAR.material.opacity = 0; STAR2.material.opacity = 0; pos = V(lerp(-30, -10, f), 0, 200 + 260); look = V(0, 4, 200); fov = 44; }
  else if (t < tEs - 0.05) { const f = prog(t, tDies, tEs - tDies); passBy(lerp(-5, 3, f)); G1.g.position.z = 30; pos = V(lerp(8, -6, f), 3, 30 + 46); look = V(0, 0, 30); fov = 40; }
  else if (t < tUnd - 0.05) { scene = sm; const f = prog(t, tEs, tUnd - tEs); moons.forEach((m, i) => (m.rotation.y = t * 0.1 + i)); pos = V(0, 0, lerp(50, 56, f)); fov = 44; }
  else if (t < tViel - 0.05) { const f = prog(t, tUnd, tViel - tUnd); passBy(0); G1.g.position.z = 30; G1.g.rotation.y = t; const a = f * 0.8; pos = V(Math.sin(a) * 40, 2, 30 + Math.cos(a) * 40); look = V(0, 0, 30); fov = 40; }
  else if (t < tSol - 0.05) { scene = sb; const f = prog(t, tViel, tSol - tViel); const kb = cl((t - tViel - 0.1) / 1.8); bang.material.opacity = kb > 0 ? (1 - kb) : 0; bang.scale.setScalar(10 + kb * 400); bang2.material.opacity = kb > 0 ? 0.8 * (1 - kb) : 0; bang2.scale.setScalar(20 + kb * 700); E.grade.uniforms.flash.value = kb > 0 ? Math.max(0, 0.5 - kb) : 0;
    const kh = K.eout(cl((t - tViel - 1.0) / 2)); BH.scale.setScalar(Math.max(0.001, kh)); const a = 0.2 + f * 0.6; pos = V(Math.sin(a) * 36, 6, Math.cos(a) * 36); fov = 42; }
  else if (t < tOder - 0.05) { scene = sg; const f = prog(t, tSol, tOder - tSol); MW.userData.m.opacity = 0.3; LMC.userData.m.opacity = 0.3; HALO.material.opacity = 0.45 * cl((t - tSol - 0.3) / 1); phG.g.visible = false; const a = 0.4 + f * 0.4; const d = lerp(1300, 1100, f); pos = V(Math.sin(a) * d, d * 0.35, Math.cos(a) * d); look = V(0, 0, 0); fov = 44; }
  else if (t < tDoch - 0.05) { scene = sr; const f = prog(t, tOder, tDoch - tOder); ROG.rotation.y = t * 0.06; ROG.position.set(lerp(-3, 3, f), 0, 0); LMC2.userData.m.opacity = 0.45 * cl((t - tLieg) / 1); const a = -0.2 + f * 0.4; pos = V(Math.sin(a) * 30, 4, Math.cos(a) * 30); look = V(ROG.position.x, t > tLieg ? 4 : 0, 0); fov = t > tLieg ? 48 : 40; }
  else if (t < tDas - 0.05) { const f = prog(t, tDoch, tDas - tDoch); G1.g.visible = false; const fl = Math.max(0, Math.sin(t * 11) * Math.sin(t * 4.3)) * cl((t - W("geflackert") + 1.2) / 0.5); STAR.scale.setScalar(6 + 22 * fl); STAR2.scale.setScalar(25); STAR2.material.opacity = 0.3 + 0.5 * fl; pos = V(0, 0, lerp(80, 60, f)); look = V(0, 0, -300); fov = 40; }
  else { const f = prog(t, tDas, END - tDas); passBy(lerp(-3, 3, f)); G1.g.position.z = 20; const d = lerp(40, 70, K.eio(f)); pos = V(-8, 3, 20 + d); look = V(0, 0, 0); fov = 40; }
  cam.fov = fov; cam.near = 0.05; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("alten") - 0.2, tEin - 0.1, "🗓️ Bilder von 2019"); seg(W("stunde") - 0.2, tDer - 0.1, "⏱️ nur 1 Stunde"); seg(tEs, tUnd - 0.1, "⚖️ ≈ 3 × Mond");
  seg(W("ersten", 33) - 0.3, tSol - 0.1, "🌑 älter als alle Sterne?"); seg(W("geflackert") - 0.3, tDas - 0.1, "✨ nur Flackern?");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
