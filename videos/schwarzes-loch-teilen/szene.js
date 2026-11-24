const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(93);
// @modelle
// ================= Schwarzes Loch (Konzept-Darstellung) =================
const sc = new THREE.Scene(); K.stars(sc, 10000, -1, 30000, 1.7).material.opacity = 0.6;
const diskMat = (hot) => new THREE.ShaderMaterial({ uniforms: { time: { value: 0 }, bright: { value: 1 }, hot: { value: hot } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec2 vP;void main(){vP=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float time,bright,hot;varying vec2 vP;void main(){float r=length(vP);float a=atan(vP.y,vP.x);float k=(r-3.6)/9.4;
    float sw=.55+.45*sin(a*7.-r*1.7+time*2.2)*sin(a*3.+r*.9-time*1.3);vec3 c=mix(vec3(1.,.97,.92),mix(vec3(1.,.55,.2),vec3(.6,.75,1.),hot),smoothstep(0.,.45,k));c=mix(c,mix(vec3(.6,.12,.05),vec3(.25,.3,.8),hot),smoothstep(.45,1.,k));
    float al=(1.-smoothstep(.0,1.,k))*(.55+.45*sw)*smoothstep(0.,.04,k);gl_FragColor=vec4(c*al*bright*1.5,al);}` });
const blackM = new THREE.MeshBasicMaterial({ color: 0x000000 });
function hole(parent, s, hot) { const g = new THREE.Group(); const core = new THREE.Mesh(new THREE.SphereGeometry(3, 64, 48), blackM); g.add(core);
  const dm = diskMat(hot); const disk = new THREE.Mesh(new THREE.RingGeometry(3.6, 13, 160, 4), dm); disk.rotation.x = -1.35; g.add(disk);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(3.25, 0.12, 12, 128), new THREE.MeshBasicMaterial({ color: 0xffd9a8, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); g.add(ring);
  const halo = K.sprite(g, K.glowTex("rgba(255,170,90,.55)"), 34, V(0, 0, 0), 0.45); halo.material.depthTest = true; halo.renderOrder = -1; g.scale.setScalar(s); parent.add(g); return { g, core, disk, dm, ring, halo }; }
const B0 = hole(sc, 1, 0.0);
// Dehnung: drei schwarze Kugeln (Hüfte + zwei Beine)
const legL = new THREE.Mesh(new THREE.SphereGeometry(3, 64, 48), blackM), legR = legL.clone(), waist = new THREE.Mesh(new THREE.SphereGeometry(3, 64, 48), blackM), midL = legL.clone(), midR = legL.clone(); [legL, legR, waist, midL, midR].forEach((m) => sc.add(m));
const B1 = hole(sc, 0.72, 0.15), B2 = hole(sc, 0.72, 0.35);
const flash = K.sprite(sc, K.glowTex("rgba(255,250,235,1)"), 60, V(0, 0, 0), 0);
// einfallendes Gas/Licht
const NP = 700, pa = []; K.reseed(5); for (let i = 0; i < NP; i++) pa.push([K.rnd(), K.rnd() * 6.28, 0.6 + K.rnd() * 0.8]);
const pg = new THREE.BufferGeometry(); const parr = new Float32Array(NP * 3); pg.setAttribute("position", new THREE.BufferAttribute(parr, 3));
const pts = new THREE.Points(pg, new THREE.PointsMaterial({ color: 0xffd7a0, size: 2.6, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); sc.add(pts);
const fall = (t, sp) => { const c = Math.cos(-1.35), s = Math.sin(-1.35); for (let i = 0; i < NP; i++) { const [ph, a0, v] = pa[i]; const k = (ph + t * 0.12 * v * sp) % 1; const r = lerp(40, 3.2, Math.pow(k, 0.7)); const a = a0 + k * 9; const x = Math.cos(a) * r, y = Math.sin(a) * r; parr[i * 3] = x; parr[i * 3 + 1] = y * c; parr[i * 3 + 2] = y * s; } pg.attributes.position.needsUpdate = true; };
// ================= Kurz nach dem Urknall: viele winzige Schwarze Löcher =================
const su = new THREE.Scene(); K.sky(su, 0x1a0602, 0x4a1a08, 0x9a4a1c, 15000); K.reseed(17); K.stars(su, 4000, -1, 20000, 1.6).material.opacity = 0.35;
const tiny = []; for (let i = 0; i < 70; i++) { const h = hole(su, 0.18 + K.rnd() * 0.25, K.rnd()); h.g.position.set((K.rnd() - 0.5) * 120, (K.rnd() - 0.5) * 160, -K.rnd() * 140); h.g.rotation.set(K.rnd() * 3, K.rnd() * 3, 0); h.disk.rotation.x = -1.35 + (K.rnd() - 0.5); tiny.push(h); }
// ===== Zeiten =====
const tDas = W("das", 3.3), tEin = W("ein", 7.9), tWas = W("was", 14.8), tDoch = W("doch"), tDer = W("der", 26.3), tDann = W("dann", 34.5), tUnd = W("und", 41.8), tFast = W("fast", 46.5), tAm = W("am", 49.2), tAber = W("aber", 55.3), tWas2 = W("was", 60.8), END = 65.1, KARTE = 14.6;
const tLang = W("länge"), tHose = W("hose"), tReiss = W("reißt") + 0.3;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sc, pos = V(0, 8, 60), look = V(0, 0, 0), fov = 40;
  // Drehtempo der Scheibe (ab "Drehung" viel schneller, stetig)
  const spin = t + Math.max(0, t - tDer) * 3; [B0, B1, B2].forEach((b) => (b.dm.uniforms.time.value = spin)); tiny.forEach((h, i) => (h.dm.uniforms.time.value = t * (1 + (i % 5) * 0.3)));
  B0.g.visible = true; B0.core.visible = true; B0.g.scale.set(1, 1, 1); B0.g.position.set(0, 0, 0); B1.g.visible = B2.g.visible = false; [legL, legR, waist, midL, midR].forEach((m) => (m.visible = false)); waist.position.set(0, 0, 0); [B0, B1, B2].forEach((b) => b.ring.quaternion.copy(cam.quaternion)); flash.material.opacity = 0; pts.material.opacity = 0;
  const split = (k, d0, d1) => { // k: 0..1 Dehnung -> Trennung
    B0.core.visible = false; const d = lerp(d0, d1, k); legL.visible = legR.visible = waist.visible = true; legL.position.set(-d, 0, 0); legR.position.set(d, 0, 0); const sL = lerp(1, 0.74, k); legL.scale.setScalar(sL); legR.scale.setScalar(sL);
    waist.scale.set(Math.max(0.01, d / 3 + 0.4), lerp(0.95, 0.25, k), lerp(0.95, 0.25, k)); waist.visible = k < 0.98; B0.disk.scale.set(1 + d / 9, 1, 1); B0.ring.scale.set(1 + d / 3.2, 1 - k * 0.3, 1); };
  const two = (d, k = 1) => { B0.g.visible = false; B1.g.visible = B2.g.visible = true; B1.g.position.set(-d, 0, 0); B2.g.position.set(d, 0, 0); };
  if (t < tDas - 0.05) { const f = prog(t, 0, tDas); const tS = W("spalten") - 0.3; if (t < tS) { split(cl((t - 0.3) / (tS - 0.3)) * 0.9, 0, 3.4); } else { two(lerp(4, 9, cl((t - tS) / 1.2))); flash.position.set(0, 0, 0); flash.material.opacity = Math.max(0, 1 - (t - tS) * 1.6); E.grade.uniforms.flash.value = Math.max(0, 0.35 - (t - tS)); }
    pos = V(Math.sin(f * 0.4) * 50, 7, Math.cos(f * 0.4) * 50); fov = 40; }
  else if (t < tEin - 0.05) { const f = prog(t, tDas, tEin - tDas); const a = -0.5 + f * 0.8; const d = lerp(70, 52, f); pos = V(Math.sin(a) * d, 9, Math.cos(a) * d); fov = 40; }
  else if (t < tDoch - 0.05) { const f = prog(t, tEin, tDoch - tEin); pts.material.opacity = 0.85; fall(t, 1); const g = 1 + 0.35 * cl((t - W("wachsen") + 0.2) / 1.6); B0.g.scale.setScalar(g); const a = 0.3 + f * 0.9; const d = lerp(80, 60, f); pos = V(Math.sin(a) * d, 14 - f * 6, Math.cos(a) * d); fov = 40; B0.g.scale.setScalar(t > W("wachsen") - 0.3 ? g : 1); }
  else if (t < tDer - 0.05) { const f = prog(t, tDoch, tDer - tDoch); B0.g.scale.setScalar(1.35); B0.g.scale.setScalar(1); pos = V(lerp(-30, 30, f), lerp(40, 10, f), lerp(60, 70, f)); fov = 40; }
  else if (t < tDann - 0.05) { const f = prog(t, tDer, tDann - tDer); B0.g.scale.set(1.04, 0.9, 1.04); const a = f * 1.0; pos = V(Math.sin(a) * 46, lerp(6, 18, f), Math.cos(a) * 46); fov = 40; }
  else if (t < tUnd - 0.05) { const f = prog(t, tDann, tUnd - tDann); B0.g.rotation.y = 0; const k = cl((t - tLang + 0.3) / (tUnd - tLang)); split(K.eio(k) * 0.75, 0.4, 5.5); const hv = false; if (hv) { const d = 3 + K.eio(cl((t - tHose + 0.3) / 1.2)) * 2.5; waist.scale.set(1.7, 0.6, 0.9); waist.position.set(0, 2.2, 0); legL.scale.setScalar(0.78); legR.scale.setScalar(0.78); legL.position.set(-d * 0.7, -d * 1.6, 0); legR.position.set(d * 0.7, -d * 1.6, 0); midL.visible = midR.visible = true; midL.scale.setScalar(0.85); midR.scale.setScalar(0.85); midL.position.set(-d * 0.38, -d * 0.6, 0); midR.position.set(d * 0.38, -d * 0.6, 0); look = V(0, -2, 0); } else { waist.position.set(0, 0, 0); } pos = hv ? V(0, 2, 62) : V(Math.sin(0.5 - f * 0.5) * 55, 10, Math.cos(0.5 - f * 0.5) * 55); B0.disk.visible = !hv; B0.ring.visible = !hv; fov = 40; }
  else if (t < tFast - 0.05) { B0.disk.visible = true; B0.ring.visible = true; if (t < tReiss) { split(lerp(0.75, 1, cl((t - tUnd) / (tReiss - tUnd))), 0.4, 5.5); } else { const k = cl((t - tReiss) / 2.5); two(lerp(5.5, 9, K.eio(k))); flash.position.set(0, 0, 0); flash.material.opacity = Math.max(0, 1 - (t - tReiss) * 1.4); E.grade.uniforms.flash.value = Math.max(0, 0.3 - (t - tReiss) * 0.5); }
    pos = V(0, 9, lerp(62, 78, prog(t, tUnd, tFast - tUnd))); fov = 40; }
  else if (t < tAm - 0.05) { const f = prog(t, tFast, tAm - tFast); B0.disk.visible = B0.ring.visible = true; two(lerp(9, 10, f)); pos = V(Math.sin(f * 0.6) * 78, 14, Math.cos(f * 0.6) * 78); fov = 40; }
  else if (t < tAber - 0.05) { scene = su; const f = prog(t, tAm, tAber - tAm); pos = V(lerp(-10, 10, f), lerp(-10, 10, f), lerp(120, 70, K.eio(f))); look = V(0, 0, -40); fov = 50; }
  else { const f = prog(t, tAber, END - tAber); B0.disk.visible = B0.ring.visible = true; two(10 + f * 2); const a = 0.3 + f * 0.4; pos = V(Math.sin(a) * 80, 16, Math.cos(a) * 80); fov = 40; }
  cam.fov = fov; cam.near = 0.1; cam.far = 80000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("unvorstellbar") - 0.1, tDann - 0.1, "🌀 fast maximale Drehung"); seg(tHose - 0.1, tUnd - 0.1, "👖 wie eine Hose");
  seg(W("zwei", 45.5) - 0.1, tAm - 0.1, "1 ➜ 2"); seg(W("urknall") - 0.2, tAber - 0.1, "💥 kurz nach dem Urknall"); seg(W("berechnung") - 0.3, tWas2 - 0.1, "🧮 nur eine Berechnung");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
