const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(77);
// @modelle
const sunT = await tex("sun.jpg");
const diskMat = (hot) => new THREE.ShaderMaterial({ uniforms: { time: { value: 0 }, bright: { value: 1 }, hot: { value: hot } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec2 vP;void main(){vP=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float time,bright,hot;varying vec2 vP;void main(){float r=length(vP);float a=atan(vP.y,vP.x);float k=(r-3.6)/9.4;
    float sw=.55+.45*sin(a*7.-r*1.7+time*2.2)*sin(a*3.+r*.9-time*1.3);vec3 c=mix(vec3(1.,.97,.92),mix(vec3(1.,.55,.2),vec3(.6,.75,1.),hot),smoothstep(0.,.45,k));c=mix(c,mix(vec3(.6,.12,.05),vec3(.25,.3,.8),hot),smoothstep(.45,1.,k));
    float al=(1.-smoothstep(.0,1.,k))*(.55+.45*sw)*smoothstep(0.,.04,k);gl_FragColor=vec4(c*al*bright*1.5,al);}` });
const jetMat = () => new THREE.ShaderMaterial({ uniforms: { op: { value: 1 }, time: { value: 0 } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float op,time;varying vec2 vU;void main(){float e=sin(vU.x*3.1416);float fl=.75+.25*sin(vU.y*40.-time*8.);float a=pow(e,2.)*(1.-vU.y)*(1.-vU.y)*fl*op;gl_FragColor=vec4(vec3(.65,.8,1.)*a*1.6,a);}` });
const blackM = new THREE.MeshBasicMaterial({ color: 0x000000 });
function hole(parent, s, hot, jets = false) { const g = new THREE.Group(); const core = new THREE.Mesh(new THREE.SphereGeometry(3, 64, 48), blackM); g.add(core);
  const dm = diskMat(hot); const disk = new THREE.Mesh(new THREE.RingGeometry(3.6, 13, 160, 4), dm); disk.rotation.x = -1.35; g.add(disk);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(3.25, 0.12, 12, 128), new THREE.MeshBasicMaterial({ color: 0xffd9a8, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); g.add(ring);
  const halo = K.sprite(g, K.glowTex("rgba(255,190,120,.6)"), 40, V(0, 0, 0), 0.5); halo.material.depthTest = true; halo.renderOrder = -1;
  const js = []; if (jets) for (const sd of [1, -1]) { const jm = jetMat(); const geo = new THREE.CylinderGeometry(0.4, 5, 80, 48, 1, true); geo.translate(0, -40, 0); const j = new THREE.Mesh(geo, jm); j.rotation.x = sd > 0 ? Math.PI : 0; const jg = new THREE.Group(); jg.add(j); jg.rotation.x = -1.35 + Math.PI / 2; g.add(jg); js.push(jm); }
  g.scale.setScalar(s); parent.add(g); return { g, core, disk, dm, ring, halo, js }; }
const galaxy = (parent, R, n, seed, tilt) => { K.reseed(seed); const p = [], c = []; for (let i = 0; i < n; i++) { const core = K.rnd() < 0.15; let r, a, y; if (core) { r = Math.pow(K.rnd(), 2) * R * 0.16; a = K.rnd() * 6.283; y = (K.rnd() - 0.5) * R * 0.05; } else { const arm = i % 2; r = Math.pow(K.rnd(), 0.7) * R; a = arm * Math.PI + Math.log(r / R * 12 + 1) * 2.4 + (K.rnd() - 0.5) * 0.7; y = (K.rnd() - 0.5) * R * 0.02; }
    p.push(Math.cos(a) * r, y, Math.sin(a) * r); const col = new THREE.Color(1, 0.9, 0.78).lerp(new THREE.Color(0.65, 0.75, 1), core ? 0 : Math.min(1, r / R + 0.2)); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const m = new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false }); const G = new THREE.Group(); G.add(new THREE.Points(g, m)); G.rotation.set(tilt, 0, 0.4); parent.add(G); G.userData.m = m; return G; };
// ================= Quasar =================
const sc = new THREE.Scene(); K.stars(sc, 10000, -1, 60000, 1.7).material.opacity = 0.6;
const Q = hole(sc, 1, 0.25); const qO = new THREE.Object3D(); sc.add(qO);
const GAL = galaxy(sc, 260, 90000, 41, 1.2); const qGlow = K.sprite(sc, K.glowTex("rgba(220,230,255,1)"), 260, V(0, 0, 0), 0);
const SUN = new THREE.Mesh(new THREE.SphereGeometry(0.35, 48, 32), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(1.4, 1.05, 0.7), toneMapped: false })); SUN.position.set(0, 9, 4); sc.add(SUN); const sunG = K.sprite(sc, K.glowTex("rgba(255,190,90,.8)"), 2.2, SUN.position.clone(), 0.8);
const S1 = hole(sc, 0.25, 0.6), S2 = hole(sc, 0.22, 0.8);
// Gaswolke, die direkt zusammenfällt
const NP = 2500, pa = []; K.reseed(5); for (let i = 0; i < NP; i++) pa.push([K.rnd(), V(K.rnd() - 0.5, K.rnd() - 0.5, K.rnd() - 0.5).normalize(), 0.6 + K.rnd() * 0.8]);
const pg = new THREE.BufferGeometry(); const parr = new Float32Array(NP * 3); pg.setAttribute("position", new THREE.BufferAttribute(parr, 3));
const pts = new THREE.Points(pg, new THREE.PointsMaterial({ color: 0xffc890, size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); sc.add(pts);
const fall = (t, sp, R0) => { for (let i = 0; i < NP; i++) { const [ph, d, v] = pa[i]; const k = (ph + t * 0.15 * v * sp) % 1; const r = lerp(R0, 3.5, Math.pow(k, 0.8)); const a = k * 4; const x = d.x * Math.cos(a) - d.z * Math.sin(a), z = d.x * Math.sin(a) + d.z * Math.cos(a); parr[i * 3] = x * r; parr[i * 3 + 1] = d.y * r * 0.7; parr[i * 3 + 2] = z * r; } pg.attributes.position.needsUpdate = true; };
// ================= Euclid-Bildfeld: Millionen Lichtpunkte =================
const se = new THREE.Scene(); { K.reseed(88); const p = [], c = []; for (let i = 0; i < 60000; i++) { p.push((K.rnd() - 0.5) * 4000, (K.rnd() - 0.5) * 7000, -K.rnd() * 300); const w = K.rnd(); const col = new THREE.Color(1, 0.92, 0.85).lerp(new THREE.Color(0.6, 0.72, 1), w); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3)); se.add(new THREE.Points(g, new THREE.PointsMaterial({ size: 1.8, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false }))); }
const eMark = K.sprite(se, K.glowTex("rgba(255,80,50,1)"), 6, V(30, -40, 0), 1); const eRing = new THREE.Mesh(new THREE.TorusGeometry(9, 0.5, 8, 64), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); eRing.position.set(30, -40, 0); se.add(eRing);
// ================= Lichtreise: Galaxien fliegen vorbei =================
const sl = new THREE.Scene(); K.stars(sl, 8000, -1, 60000, 1.6).material.opacity = 0.5; const glist = []; { K.reseed(14); for (let i = 0; i < 26; i++) { const G = galaxy(sl, 40 + K.rnd() * 50, 6000, 100 + i, K.rnd() * 3); G.userData.m.opacity = 0.3; G.position.set((K.rnd() - 0.5) * 600, (K.rnd() - 0.5) * 900, -i * 900 - 400); G.rotation.y = K.rnd() * 3; glist.push(G); } }
const beam = K.sprite(sl, K.glowTex("rgba(200,220,255,1)"), 30, V(0, 0, 0), 1);
// ================= Junges Universum =================
const su = new THREE.Scene(); K.sky(su, 0x1a0602, 0x4a1a08, 0x9a4a1c, 15000); K.reseed(17); K.stars(su, 4000, -1, 20000, 1.6).material.opacity = 0.35;
const QU = hole(su, 1, 0.1); for (let i = 0; i < 40; i++) K.sprite(su, K.glowTex(i % 2 ? "rgba(255,160,110,.8)" : "rgba(180,200,255,.8)"), 10 + K.rnd() * 30, V((K.rnd() - 0.5) * 500, (K.rnd() - 0.5) * 800, -100 - K.rnd() * 500), 0.6);
// ================= James Webb =================
const sj = new THREE.Scene(); K.stars(sj, 9000, -1, 60000, 1.7).material.opacity = 0.8; sj.add(new THREE.AmbientLight(0x30343e, 0.7)); const lj = new THREE.DirectionalLight(0xfff2e0, 2.2); lj.position.set(-3, 5, 4); sj.add(lj);
const JW = MO.jwst(); sj.add(JW.g); const jwO = new THREE.Object3D(); JW.g.add(jwO); jwO.position.set(0, 7, 0);
// ===== Zeiten =====
const tEs = W("es", 3.9), tGef = W("gefunden"), tDas = W("das", 15.1), tWir = W("wir", 20.2), tDas2 = W("das", 27.9), tUnd = W("und", 35.5), tDas3 = W("das", 40.4), tUnh = W("das", 45.0), tWie = W("wie", 51.8), tEinf = W("einfach"), tViel = W("vielleicht"), tWas = W("was", 62.8), END = 67.1, KARTE = 15.1;
label("Quasar", qO, 6, { t0: W("quasar") + 0.1, t1: tUnd - 0.1, size: 56, gap: 20 }); label("James Webb", jwO, 2, { t0: W("james") - 0.1, t1: tUnh - 0.1, size: 52, gap: 18 }); label("Sonne", SUN, 0.35, { t0: W("sonne", 50.5), t1: tWie - 0.1, size: 42, gap: 10 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sc, pos = V(0, 8, 60), look = V(0, 0, 0), fov = 40;
  [Q, QU, S1, S2].forEach((b) => { b.dm.uniforms.time.value = t * 1.5; b.js.forEach((j) => (j.uniforms.time.value = t)); }); [Q, QU, S1, S2].forEach((b) => b.ring.quaternion.copy(cam.quaternion));
  GAL.visible = false; qGlow.material.opacity = 0; SUN.visible = false; sunG.material.opacity = 0; S1.g.visible = S2.g.visible = false; pts.material.opacity = 0; Q.g.scale.setScalar(1); Q.js.forEach((j) => (j.uniforms.op.value = 1)); GAL.rotation.y = t * 0.02;
  if (t < tEs - 0.05) { const f = K.eio(prog(t, 0, tEs)); const d = lerpLog(900, 70, f); GAL.visible = true; GAL.userData.m.opacity = 0.8; qGlow.material.opacity = lerp(0.5, 0, f); qGlow.scale.setScalar(120); pos = V(d * 0.25, d * 0.3 + 6, d); look = V(0, 6, 0); }
  else if (t < tGef - 0.05) { const f = prog(t, tEs, tGef - tEs); const a = 0.3 + f * 0.7; pos = V(Math.sin(a) * 52, lerp(14, 6, f), Math.cos(a) * 52); }
  else if (t < tDas - 0.05) { scene = se; const f = K.eio(prog(t, tGef, tDas - tGef)); const z = lerpLog(2500, 160, f); pos = V(lerp(0, 30, f), lerp(0, -40, f), z); look = V(lerp(0, 30, f), lerp(0, -40, f), -100); eRing.material.opacity = cl((f - 0.75) * 5); fov = 50; }
  else if (t < tWir - 0.05) { scene = sl; const f = prog(t, tDas, tWir - tDas); const z = lerp(-24000, -200, f); pos = V(0, 0, z + 120); beam.position.set(0, 0, z); look = V(0, 0, z + 500); fov = 55; glist.forEach((G, i) => (G.rotation.y += 0)); }
  else if (t < tDas2 - 0.05) { scene = su; const f = prog(t, tWir, tDas2 - tWir); const a = -0.3 + f * 0.6; const d = lerp(90, 60, f); pos = V(Math.sin(a) * d, 10, Math.cos(a) * d); }
  else if (t < tUnd - 0.05) { const f = prog(t, tDas2, tUnd - tDas2); GAL.visible = true; const k = cl((t - W("heller") + 0.2) / 1.5); GAL.userData.m.opacity = lerp(0.8, 0.25, k); qGlow.material.opacity = lerp(0.2, 0.75, k); qGlow.scale.setScalar(lerp(120, 300, k)); const d = lerp(420, 600, f); pos = V(d * 0.2, d * 0.45, d); }
  else if (t < tDas3 - 0.05) { const f = K.eio(prog(t, tUnd, tDas3 - tUnd)); GAL.visible = true; GAL.userData.m.opacity = 0.5; qGlow.material.opacity = 0.75; qGlow.scale.setScalar(300); const d = lerpLog(600, 12000, f); pos = V(d * 0.2, d * 0.3, d); }
  else if (t < tUnh - 0.05) { scene = sj; const f = prog(t, tDas3, tUnh - tDas3); JW.g.rotation.set(0.2, 0.5 + f * 0.5, 0); const a = 0.6 + f * 0.6; pos = V(Math.sin(a) * 36, 8, Math.cos(a) * 36); look = V(0, 3, 0); fov = 42; }
  else if (t < tWie - 0.05) { const f = prog(t, tUnh, tWie - tUnh); const g = 1 + 0.25 * K.eio(cl((t - W("schwer") + 0.5) / 1.5)); Q.g.scale.setScalar(g); if (t > W("sonne", 50.5) - 0.3) { SUN.visible = true; sunG.material.opacity = 0.8; SUN.rotation.y = t * 0.2; } const a = -0.5 + f * 0.6; pos = V(Math.sin(a) * 60, 12, Math.cos(a) * 60); look = V(0, -8, 0); }
  else if (t < tEinf - 0.05) { const f = prog(t, tWie, tEinf - tWie); Q.dm.uniforms.time.value = t * 1.5 + f * 8; const a = 0.1 + f * 1.2; pos = V(Math.sin(a) * 70, lerp(10, 30, f), Math.cos(a) * 70); }
  else if (t < tViel - 0.05) { const f = prog(t, tEinf, tViel - tEinf); S1.g.visible = S2.g.visible = true; const k = cl(f * 1.1); const r = lerp(32, 4, k * k); const a = k * 9; S1.g.position.set(Math.cos(a) * r, 0, Math.sin(a) * r * 0.6); S2.g.position.set(-Math.cos(a) * r, 0, -Math.sin(a) * r * 0.6); if (k >= 0.98) S1.g.visible = S2.g.visible = false; pos = V(0, 30, 80); }
  else if (t < tWas - 0.05) { const f = prog(t, tViel, tWas - tViel); pts.material.opacity = 0.9; fall(t, 1.6, 70); Q.g.scale.setScalar(lerp(0.4, 1, K.eio(cl(f * 1.2)))); Q.js.forEach((j) => (j.uniforms.op.value = cl(f * 2 - 0.6))); pos = V(Math.sin(f * 0.5) * 120, 30, Math.cos(f * 0.5) * 120); }
  else { const f = prog(t, tWas, END - tWas); GAL.visible = true; GAL.userData.m.opacity = 0.6; qGlow.material.opacity = 0.5; qGlow.scale.setScalar(150); const a = 0.2 + f * 0.5; const d = lerp(450, 560, f); pos = V(Math.sin(a) * d, lerp(20, 40, f), Math.cos(a) * d); }
  cam.fov = fov; cam.near = 0.1; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("europäische") - 0.2, tDas - 0.1, logo("esa.svg", 70) + "🔭 Euclid"); seg(W("sechshundertdreißig") - 0.1, tDas2 - 0.1, "💥 630 Mio. Jahre<br>nach dem Urknall");
  seg(W("rekord") - 0.2, tDas3 - 0.1, "🏆 neuer Rekord"); seg(W("dreihundertsechzig") - 0.1, tWie - 0.1, "⚫ 360 Mio. × Sonne");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
