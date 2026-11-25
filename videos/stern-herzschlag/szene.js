const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(61);
// @modelle
const sunT = await tex("sun.jpg");
const star = (sc, r, col, glow, gs = 3) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(...col), toneMapped: false })); sc.add(m); m.userData.glow = K.sprite(sc, K.glowTex(glow), r * gs, V(0, 0, 0), 0.6); m.userData.gs = r * gs; return m; };
const shellMat = (col) => new THREE.ShaderMaterial({ uniforms: { op: { value: 0 }, col: { value: new THREE.Color(...col) } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  vertexShader: `varying vec3 vN;varying vec3 vV;varying vec3 vP;void main(){vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-mv.xyz);vP=position;gl_Position=projectionMatrix*mv;}`,
  fragmentShader: `uniform float op;uniform vec3 col;varying vec3 vN;varying vec3 vV;varying vec3 vP;void main(){float f=1.-abs(dot(vN,vV));float a=pow(f,3.2);float n=.7+.3*sin(vP.x*9.+vP.y*7.)*sin(vP.z*8.-vP.y*5.);gl_FragColor=vec4(col*a*op*n,a*op);}` });
// ================= Sterbender Riese =================
const sc = new THREE.Scene(); K.stars(sc, 10000, -1, 60000, 1.7).material.opacity = 0.7;
const GI = star(sc, 10, [1.4, 0.55, 0.3], "rgba(255,100,50,.6)", 3.4);
const SH = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), shellMat([1, 0.55, 0.3])); sc.add(SH);
const SH2 = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), shellMat([1, 0.7, 0.45])); sc.add(SH2);
const flash = K.sprite(sc, K.glowTex("rgba(255,235,210,1)"), 80, V(0, 0, 0), 0);
const marker = K.sprite(sc, K.glowTex("rgba(255,150,90,1)"), 10, V(0, 0, 0), 0);
// Sanduhr-Wolke (zwei Blasen aus Gas)
const HG = new THREE.Group(); sc.add(HG); { K.reseed(23); const p = [], c = []; const L = 70, R = 30; for (let i = 0; i < 16000; i++) { const s = i % 2 ? 1 : -1; const k = Math.pow(K.rnd(), 0.8); const r = R * Math.pow(Math.sin(Math.PI * Math.min(0.98, k)), 0.75) + 2.5; const th = K.rnd() * 6.283; const j = 1 + (K.rnd() - 0.5) * 0.12; p.push(Math.cos(th) * r * j, s * k * L, Math.sin(th) * r * j);
    const col = new THREE.Color(1, 0.45, 0.4).lerp(new THREE.Color(0.45, 0.6, 1), Math.min(1, k * 1.1)); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  HG.userData.m = new THREE.PointsMaterial({ size: 2.2, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }); HG.add(new THREE.Points(g, HG.userData.m)); }
// unsichtbarer Begleiter
const CO = star(sc, 1.6, [0.55, 0.8, 1.7], "rgba(150,190,255,.9)", 6); const coO = new THREE.Object3D(); sc.add(coO);
const giO = new THREE.Object3D(); sc.add(giO);
// ================= Unsere Sonne =================
const ss = new THREE.Scene(); K.stars(ss, 9000, -1, 60000, 1.7).material.opacity = 0.7;
const SUN = star(ss, 4, [1.35, 1.0, 0.65], "rgba(255,180,80,.6)", 3.6); const sunO = new THREE.Object3D(); ss.add(sunO);
const SSH = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), shellMat([1, 0.75, 0.4])); ss.add(SSH);
// ===== Zeiten =====
const tUnd = W("und", 5.5), tEnt = W("entdeckt"), tDer = W("der", 12.8), tEr = W("er", 16.3), tIn = W("in", 20.7), tBei = W("bei", 27.2), tGen = W("genau"), tBis = W("bisher"), tUnd2 = W("und", 42.6), tWahr = W("wahrscheinlich"), tUnd3 = W("und", 56.8), tUns = W("unsere", 60.8), tWas = W("was", 64.4), END = 69.3, KARTE = 13.0;
const beats = [W("stirbt") + 0.1, W("herzschlag") + 0.15, W("zuckt") + 0.1, W("heftig") + 0.1, W("zusammen") + 0.15, W("herz", 24.9) + 0.1, W("schlägt") + 0.15, W("schlag", 27.8) + 0.1];
const bump = (t) => beats.reduce((a, b) => a + Math.exp(-Math.pow((t - b) / 0.11, 2)), 0);
label("Sonne", sunO, 4, { t0: tUnd + 0.8, t1: tEnt - 0.1, size: 52, gap: 18 }); label("Sonne", sunO, 4, { t0: tUns + 0.6, t1: tWas - 0.1, size: 52, gap: 18 });
label("zweiter Stern?", coO, 1.6, { t0: W("zweiter") + 0.2, t1: tUnd3 - 0.1, size: 46, gap: 14 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.32, 0.86);
  let scene = sc, pos = V(0, 10, 80), look = V(0, 0, 0), fov = 40;
  const b = bump(t); GI.rotation.y = t * 0.04; GI.scale.setScalar(1 + 0.1 * b); GI.userData.glow.scale.setScalar(GI.userData.gs * (1 + 0.5 * b)); GI.userData.glow.material.opacity = 0.6 + 0.35 * b; GI.visible = GI.userData.glow.visible = true;
  flash.material.opacity = 0.5 * b; E.grade.uniforms.flash.value = 0.12 * b; marker.material.opacity = 0;
  SH.material.uniforms.op.value = 0; SH2.material.uniforms.op.value = 0; HG.userData.m.opacity = 0; CO.visible = CO.userData.glow.visible = false; SSH.material.uniforms.op.value = 0;
  const shellAt = (S, t0, rMax, op = 1, dur = 3.5) => { if (t < t0) return; const k = cl((t - t0) / dur); S.scale.setScalar(lerp(10, rMax, 1 - Math.pow(1 - k, 2.5))); S.material.uniforms.op.value = op * Math.min(1, (t - t0) * 4); };
  const hourglass = (g) => { HG.userData.m.opacity = 0.9 * cl(g * 3); HG.scale.set(lerp(0.15, 1, g), lerp(0.05, 1, g), lerp(0.15, 1, g)); HG.rotation.y = t * 0.05; };
  const comp = () => { CO.visible = CO.userData.glow.visible = true; const a = t * 0.5; const p = V(Math.cos(a) * 15, Math.sin(a) * 3, Math.sin(a) * 15); CO.position.copy(p); CO.userData.glow.position.copy(p); coO.position.copy(p); };
  if (t < tUnd - 0.05) { const f = prog(t, 0, tUnd); shellAt(SH, beats[1], 45, 1, 2.5); const a = 0.2 + f * 0.35; pos = V(Math.sin(a) * 95, 12, Math.cos(a) * 95); look = V(0, 13, 0); }
  else if (t < tEnt - 0.05) { scene = ss; const f = prog(t, tUnd, tEnt - tUnd); SUN.rotation.y = t * 0.05; pos = V(Math.sin(f * 0.4 - 0.2) * 32, 4, Math.cos(f * 0.4 - 0.2) * 32); }
  else if (t < tDer - 0.05) { const f = prog(t, tEnt, tDer - tEnt); const a = -0.4 + f * 0.4; pos = V(Math.sin(a) * 110, lerp(30, 8, f), Math.cos(a) * 110); }
  else if (t < tEr - 0.05) { const f = K.eio(prog(t, tDer, tEr - tDer)); const d = lerpLog(30000, 110, f); marker.material.opacity = 1 - cl((f - 0.7) / 0.25); marker.scale.setScalar(d * 0.03); pos = V(d * 0.15, d * 0.08, d); }
  else if (t < tIn - 0.05) { const f = prog(t, tEr, tIn - tEr); const g = lerp(0.18, 1, K.eio(cl((t - W("riesen") + 1.2) / 1.8))); GI.scale.setScalar(g); GI.userData.glow.scale.setScalar(GI.userData.gs * g); GI.material.color.setRGB(lerp(1.35, 1.4, g), lerp(1.0, 0.55, g), lerp(0.65, 0.3, g)); pos = V(Math.sin(f * 0.5) * 85, 8, Math.cos(f * 0.5) * 85); }
  else if (t < tBei - 0.05) { const f = prog(t, tIn, tBei - tIn); pos = V(Math.sin(-0.3 + f * 0.3) * lerp(78, 64, f), 6, Math.cos(-0.3 + f * 0.3) * lerp(78, 64, f)); }
  else if (t < tGen - 0.05) { const f = prog(t, tBei, tGen - tBei); shellAt(SH, beats[7], 120, 1, 3.6); const d = lerp(80, 420, K.eio(f)); pos = V(d * 0.2, d * 0.12, d); }
  else if (t < tBis - 0.05) { const f = prog(t, tGen, tBis - tGen); SH.scale.setScalar(120); SH.material.uniforms.op.value = 1; shellAt(SH2, tGen, 70, 0.5, 6); const a = 0.2 + f * 0.6; pos = V(Math.sin(a) * 520, lerp(60, 140, f), Math.cos(a) * 520); }
  else if (t < tUnd2 - 0.05) { const f = prog(t, tBis, tUnd2 - tBis); SH.scale.setScalar(120 + f * 4); SH.material.uniforms.op.value = 0.9; SH2.scale.setScalar(70); SH2.material.uniforms.op.value = 0.45; const a = 0.8 + f * 0.4; pos = V(Math.sin(a) * 480, 120, Math.cos(a) * 480); }
  else if (t < tWahr - 0.05) { const f = prog(t, tUnd2, tWahr - tUnd2); SH.scale.setScalar(125); SH.material.uniforms.op.value = lerp(0.9, 0.35, f); const g = K.eio(cl((t - W("formt") + 0.3) / 5)); hourglass(g); GI.scale.setScalar(0.6); GI.userData.glow.scale.setScalar(GI.userData.gs * 0.7); const a = 0.4 - f * 0.5; pos = V(Math.sin(a) * lerp(300, 240, f), 20, Math.cos(a) * lerp(300, 240, f)); }
  else if (t < tUnd3 - 0.05) { const f = prog(t, tWahr, tUnd3 - tWahr); SH.scale.setScalar(125); SH.material.uniforms.op.value = 0.3; hourglass(1); HG.userData.m.opacity = 0.35; GI.scale.setScalar(0.6); GI.userData.glow.scale.setScalar(GI.userData.gs * 0.7); comp(); pos = V(Math.sin(0.3 + f * 0.3) * 125, 22, Math.cos(0.3 + f * 0.3) * 125); }
  else if (t < tUns - 0.05) { const f = prog(t, tUnd3, tUns - tUnd3); SH.scale.setScalar(125); SH.material.uniforms.op.value = 0.5; hourglass(1); GI.scale.setScalar(0.6); GI.userData.glow.scale.setScalar(GI.userData.gs * 0.7); comp(); const a = -0.2 + f * 0.5; const d = lerp(260, 330, f); pos = V(Math.sin(a) * d, lerp(40, 90, f), Math.cos(a) * d); }
  else { scene = ss; const f = prog(t, tUns, END - tUns); SUN.rotation.y = t * 0.05; const tb = W("herzschlag", 66) + 0.15; const bb = Math.exp(-Math.pow((t - tb) / 0.12, 2)); const g = 1 + 0.6 * K.eio(cl((t - W("milliarden") + 0.3) / 2.2)); SUN.scale.setScalar(g * (1 + 0.1 * bb)); SUN.userData.glow.scale.setScalar(SUN.userData.gs * g * (1 + 0.5 * bb)); SUN.material.color.setRGB(1.35, lerp(1.0, 0.75, (g - 1) / 0.6), lerp(0.65, 0.45, (g - 1) / 0.6)); E.grade.uniforms.flash.value = 0.12 * bb;
    if (t > tb) { const k = cl((t - tb) / 3); SSH.scale.setScalar(lerp(6, 30, 1 - Math.pow(1 - k, 2.5))); SSH.material.uniforms.op.value = Math.min(1, (t - tb) * 4); }
    const d = lerp(40, 58, f); pos = V(Math.sin(0.3 - f * 0.4) * d, 5, Math.cos(0.3 - f * 0.4) * d); }
  if (scene === sc) { GI.userData.glow.position.set(0, 0, 0); giO.position.set(0, 0, 0); }
  cam.fov = fov; cam.near = 0.1; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("nasa") - 0.3, tDer - 0.1, logo("nasa.svg", 80)); seg(W("zwölftausend") - 0.1, tEr - 0.1, "📍 12.000 Lichtjahre");
  seg(W("halbes") - 0.2, tBis - 0.1, "⭕ ½ Lichtjahr groß"); seg(W("siebenhundert") - 0.1, tWahr - 0.1, "⏳ nur 700 Jahre");
  seg(W("fünf", 62) - 0.1, tWas - 0.1, "☀️ in ca. 5 Mrd. Jahren");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
