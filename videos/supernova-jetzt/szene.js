const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(11);
const sunTex = await tex("sun.jpg");
// ---------- Balken-Spiralgalaxie (NGC 1433) ----------
function barred(sc, R0, n, seed) { K.reseed(seed); const p = [], c = []; const cCore = new THREE.Color("#ffe2b4"), cArm = new THREE.Color("#a9c2ff"), cPink = new THREE.Color("#ff9cc0");
  const g = () => (K.rnd() + K.rnd() + K.rnd() - 1.5) / 1.5;
  for (let i = 0; i < n; i++) { const k = K.rnd(); let x, y, z, col;
    if (k < 0.16) { const r = Math.abs(g()) * R0 * 0.12, a = K.rnd() * 6.283; x = Math.cos(a) * r; z = Math.sin(a) * r; y = g() * R0 * 0.05; col = cCore; }
    else if (k < 0.32) { x = (K.rnd() * 2 - 1) * R0 * 0.42; z = g() * R0 * 0.06; y = g() * R0 * 0.02; col = cCore.clone().lerp(cArm, 0.2); }
    else if (k < 0.46) { const a = K.rnd() * 6.283, r = R0 * (0.42 + g() * 0.04); x = Math.cos(a) * r * 1.05; z = Math.sin(a) * r * 0.85; y = g() * R0 * 0.015; col = cArm.clone().lerp(cCore, 0.35); }
    else if (k < 0.62) { const r = -Math.log(1 - K.rnd() * 0.97) * R0 * 0.3, a = K.rnd() * 6.283; x = Math.cos(a) * r; z = Math.sin(a) * r; y = g() * R0 * 0.02; col = cArm.clone().lerp(cCore, 0.5); }
    else { const arm = i % 2; const r = R0 * (0.42 + Math.pow(K.rnd(), 0.8) * 0.65) * (1 + g() * 0.07); const a = arm * Math.PI + (r / R0 - 0.42) * 3.6 + g() * 0.5; x = Math.cos(a) * r; z = Math.sin(a) * r; y = g() * R0 * 0.015; col = K.rnd() < 0.05 ? cPink : cArm.clone().lerp(cCore, 0.15 * K.rnd()); }
    p.push(x, y, z); c.push(col.r, col.g, col.b); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); geo.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const pts = new THREE.Points(geo, new THREE.PointsMaterial({ size: 1.5, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.5, blending: THREE.AdditiveBlending, depthWrite: false }));
  const grp = new THREE.Group(); grp.add(pts); grp.pts = pts;
  K.sprite(grp, K.glowTex("rgba(255,225,180,.75)"), R0 * 0.3, V(0, 0, 0), 0.3); K.sprite(grp, K.glowTex("rgba(150,170,255,.25)"), R0 * 1.8, V(0, 0, 0), 0.1);
  sc.add(grp); return grp; }
// ================= Szene: Galaxie =================
const scG = new THREE.Scene(); K.stars(scG, 7000, -1, 30000, 1.5).material.opacity = 0.55;
const GAL = barred(scG, 100, 140000, 7); GAL.rotation.set(0.55, 0, 0.25);
const snO = new THREE.Object3D(); snO.position.set(22, 0, 14); GAL.add(snO);
const sn1 = K.sprite(GAL, K.glowTex("rgba(255,255,255,1)"), 6, snO.position, 0), sn2 = K.sprite(GAL, K.glowTex("rgba(190,215,255,.55)"), 30, snO.position, 0), sn3 = K.sprite(GAL, K.glowTex("rgba(255,255,255,.9)"), 3, snO.position, 0);
const setSN = (b) => { const s = Math.max(0, b); sn1.material.opacity = Math.min(1, s * 1.2); sn2.material.opacity = Math.min(0.9, s * 0.7); sn3.material.opacity = Math.min(1, s * 2); sn1.scale.setScalar(4 + 10 * s); sn2.scale.setScalar(14 + 46 * s); sn3.scale.setScalar(2 + 3 * s); };
// ================= Szene: Lichtreise =================
const scL = new THREE.Scene(); K.stars(scL, 9000, -1, 40000, 1.6).material.opacity = 0.6;
scL.add(new THREE.AmbientLight(0x30303a, 0.4));
const GAL2 = barred(scL, 260, 140000, 7); GAL2.pts.material.opacity = 0.35; GAL2.children.slice(1).forEach((c) => (c.material.opacity *= 0.35)); GAL2.position.set(-200, 1300, -2600); GAL2.rotation.set(1.0, 0.3, 0.3);
const snL = K.sprite(GAL2, K.glowTex("rgba(255,255,255,1)"), 70, V(57, 0, 36), 1);
const EAL = K.earth(scL, { day, night, topo }, 14); EAL.group.children[EAL.group.children.length - 1].scale.setScalar(0.93); EAL.U.sun.value = V(0.6, 0.5, 0.7).normalize();
const pulse = [0, 1, 2, 3, 4, 5].map((i) => K.sprite(scL, K.glowTex(i ? "rgba(190,215,255,.6)" : "rgba(255,255,255,1)"), i ? 40 - i * 4 : 26, V(0, 0, 0), 0));
const beamMat = new THREE.LineBasicMaterial({ color: 0x9fbcff, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false });
const beamGeo = new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(0, 0, 0)]); const beamL = new THREE.Line(beamGeo, beamMat); beamL.frustumCulled = false; scL.add(beamL);
// ================= Szene: Himmel + Teleskop (ATLAS) =================
const sky = new THREE.Scene(); K.reseed(99); K.stars(sky, 9000, -0.02, 3000, 1.6).material.opacity = 0.85; sky.add(new THREE.AmbientLight(0x14161e, 1));
{ const P = [], I = []; for (let i = 0; i <= 360; i++) { const a = (i / 360) * Math.PI * 2; const h = 10 + 9 * Math.sin(a * 5 + 1) * Math.sin(a * 3) + 4 * Math.sin(a * 23) + 2 * Math.sin(a * 61); P.push(Math.cos(a) * 900, -6, Math.sin(a) * 900, Math.cos(a) * 900, h, Math.sin(a) * 900); if (i < 360) { const k = i * 2; I.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); } }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(P, 3)); g.setIndex(I); sky.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: 0x010203, side: THREE.DoubleSide }))); }
const gnd = new THREE.Mesh(new THREE.CircleGeometry(4000, 64), new THREE.MeshBasicMaterial({ color: 0x010203 })); gnd.rotation.x = -Math.PI / 2; gnd.position.y = -6; sky.add(gnd);
K.sprite(sky, K.glowTex("rgba(40,60,110,.5)"), 1400, V(0, -60, -1500), 0.35);
const dirAA = (alt, az) => { const a = (alt * Math.PI) / 180, z = (az * Math.PI) / 180; return V(Math.sin(z) * Math.cos(a), Math.sin(a), -Math.cos(z) * Math.cos(a)); };
const skyGalP = dirAA(38, 12).multiplyScalar(900); const skyGal = K.sprite(sky, K.glowTex("rgba(230,225,255,.55)"), 34, skyGalP, 0.7); const skySN = K.sprite(sky, K.glowTex("rgba(255,255,255,1)"), 10, skyGalP.clone().add(V(4, 1, 0)), 0);
const skySNO = new THREE.Object3D(); skySNO.position.copy(skyGalP); sky.add(skySNO);
const scope = new THREE.Group(); sky.add(scope); scope.position.set(10, -6, -40);
{ const mt = new THREE.MeshStandardMaterial({ color: 0xc8ced8, metalness: 0.3, roughness: 0.45 }); const tube = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, 11, 40), mt); tube.rotation.x = -0.55; tube.rotation.z = 0.2; tube.position.y = 9.5; scope.add(tube);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1.65, 0.18, 12, 40), new THREE.MeshStandardMaterial({ color: 0x222222 })); ring.position.copy(tube.position).add(V(-1.1, 4.4, -2.9)); ring.rotation.copy(tube.rotation); ring.rotateX(Math.PI / 2); scope.add(ring);
  const pier = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 1.1, 9, 24), new THREE.MeshStandardMaterial({ color: 0x3a3d44, roughness: 0.6 })); pier.position.y = 3.5; scope.add(pier); }
const scopeL = new THREE.DirectionalLight(0xdfe6ff, 1.8); scopeL.position.set(-60, 40, 80); sky.add(scopeL);
// ================= Szene: Weißer Zwerg + Erde + Begleiter =================
const scW = new THREE.Scene(); K.stars(scW, 9000, -1, 30000, 1.7).material.opacity = 0.6;
scW.add(new THREE.AmbientLight(0x30303a, 0.6)); const fill = new THREE.DirectionalLight(0xdfe6ff, 1.4); fill.position.set(-1, 0.5, 1); scW.add(fill);
const wdC = K.noiseCanvas(1024, 512, 6, 6, 0.5, 0.6); const wdTex = new THREE.CanvasTexture(wdC); wdTex.wrapS = wdTex.wrapT = THREE.RepeatWrapping; wdTex.colorSpace = THREE.SRGBColorSpace; const RW = 2;
const wd = new THREE.Group(); scW.add(wd);
const wdM = new THREE.Mesh(new THREE.SphereGeometry(RW, 96, 64), new THREE.ShaderMaterial({ uniforms: { n: { value: wdTex } }, toneMapped: false,
  vertexShader: `varying vec2 vU;varying vec3 vN;varying vec3 vV;void main(){vU=uv;vN=normalize(mat3(modelMatrix)*normal);vec4 w=modelMatrix*vec4(position,1.);vV=normalize(cameraPosition-w.xyz);gl_Position=projectionMatrix*viewMatrix*w;}`,
  fragmentShader: `uniform sampler2D n;varying vec2 vU;varying vec3 vN;varying vec3 vV;void main(){float g=texture2D(n,vU*vec2(2.,2.)).r;float mu=clamp(dot(vN,vV),0.,1.);vec3 c=mix(vec3(.62,.74,1.),vec3(1.,1.,1.),smoothstep(.2,.9,g));c*=.45+.5*pow(mu,.6);gl_FragColor=vec4(c*.8,1.);}` })); wd.add(wdM);
K.sprite(wd, K.glowTex("rgba(170,200,255,.75)"), RW * 3, V(0, 0, 0), 0.35); K.sprite(wd, K.glowTex("rgba(120,160,255,.3)"), RW * 6, V(0, 0, 0), 0.15);
const EAW = K.earth(scW, { day, night, topo }, RW); EAW.group.children[EAW.group.children.length - 1].scale.setScalar(0.93); EAW.U.sun.value = V(-0.4, 0.3, 1).normalize(); EAW.group.position.set(6.5, 0, 0);
// Begleitstern (Sonnen-Textur, orange) + Gasstrom + Scheibe
const RC = 26; const compP = V(-60, 0, -20); const comp = new THREE.Mesh(new THREE.SphereGeometry(RC, 128, 96), new THREE.MeshBasicMaterial({ map: sunTex, color: new THREE.Color(1.35, 0.85, 0.55), toneMapped: false })); comp.position.copy(compP); scW.add(comp);
const compG = K.sprite(scW, K.glowTex("rgba(255,150,60,.5)"), RC * 4, compP, 0.7);
const NS = 2600; const sp = new Float32Array(NS * 3), sSeed = []; for (let i = 0; i < NS; i++) sSeed.push([K.rnd(), (K.rnd() - 0.5), (K.rnd() - 0.5)]);
const sGeo = new THREE.BufferGeometry(); sGeo.setAttribute("position", new THREE.BufferAttribute(sp, 3));
const stream = new THREE.Points(sGeo, new THREE.PointsMaterial({ color: 0xffb070, size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); stream.frustumCulled = false; scW.add(stream);
const L1 = compP.clone().add(V(RC * 0.98, 0, 0).applyAxisAngle(V(0, 1, 0), -0.32));
const streamAt = (t) => { for (let i = 0; i < NS; i++) { const [u0, a, b] = sSeed[i]; const u = (u0 + t * 0.12) % 1; let x;
    if (u < 0.55) { const f = u / 0.55; x = L1.clone().lerp(V(-2, 0, 9), f); x.y += a * (1.5 + f * 2); x.x += b * 1.5; x.z += Math.sin(f * 3) * 4; }
    else { const f = (u - 0.55) / 0.45; const r = lerp(10, RW * 1.4, f), ang = 1.9 + f * 9; x = V(Math.cos(ang) * r, a * 0.4 * (1 - f), Math.sin(ang) * r); }
    sp[i * 3] = x.x; sp[i * 3 + 1] = x.y; sp[i * 3 + 2] = x.z; } sGeo.attributes.position.needsUpdate = true; };
const disk = new THREE.Mesh(new THREE.RingGeometry(RW * 1.3, 11, 128), new THREE.ShaderMaterial({ uniforms: { a: { value: 0 } }, transparent: true, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false,
  vertexShader: `varying vec3 vP;void main(){vP=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float a;varying vec3 vP;void main(){float r=length(vP.xy);float f=1.-smoothstep(2.6,11.,r);vec3 c=mix(vec3(1.,.55,.25),vec3(.85,.9,1.),f*f);gl_FragColor=vec4(c*f*a*1.4,f*a);}` })); disk.rotation.x = -Math.PI / 2; scW.add(disk);
// Explosion
const NB = 9000; const bp = new Float32Array(NB * 3), bDir = []; for (let i = 0; i < NB; i++) { const u = K.rnd() * 2 - 1, a = K.rnd() * 6.283, q = Math.sqrt(1 - u * u); bDir.push([Math.cos(a) * q, u, Math.sin(a) * q, 0.75 + K.rnd() * 0.35]); }
const bGeo = new THREE.BufferGeometry(); bGeo.setAttribute("position", new THREE.BufferAttribute(bp, 3));
const blast = new THREE.Points(bGeo, new THREE.PointsMaterial({ color: 0xcfe0ff, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); blast.frustumCulled = false; scW.add(blast);
const bF1 = K.sprite(scW, K.glowTex("rgba(255,255,255,1)"), 10, V(0, 0, 0), 0), bF2 = K.sprite(scW, K.glowTex("rgba(160,190,255,.6)"), 40, V(0, 0, 0), 0), bF3 = K.sprite(scW, K.glowTex("rgba(255,180,120,.35)"), 80, V(0, 0, 0), 0);
// ================= Szene: Erde (Süden / Deutschland) =================
const scE = new THREE.Scene(); K.stars(scE, 9000, -1, 30000, 1.7).material.opacity = 0.6; scE.add(new THREE.AmbientLight(0x30303a, 0.5));
const RE = 100; const EA = K.earth(scE, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(0.2, 0.1, 1).normalize();
EA.group.rotation.y = -0.45; EA.group.rotation.x = 0.0;
const deO = new THREE.Object3D(), suO = new THREE.Object3D(); scE.add(deO); scE.add(suO);
const deDot = K.sprite(scE, K.glowTex("rgba(255,120,110,1)"), 5, V(0, 0, 0), 0), suDot = K.sprite(scE, K.glowTex("rgba(140,255,170,1)"), 5, V(0, 0, 0), 0);
// ================= Szene: Maßband =================
const scM = new THREE.Scene(); K.stars(scM, 7000, -1, 40000, 1.4).material.opacity = 0.4;
const GS = []; for (let i = 0; i < 5; i++) { const g = barred(scM, 55, 22000, 20 + i); g.pts.material.opacity = 0.3; g.children.slice(1).forEach((c) => (c.material.opacity *= 0.3)); g.position.set((i % 2 ? 1 : -1) * (50 + i * 95), (i % 3 - 1) * (30 + i * 45), -i * 420); g.rotation.set(0.5 + i * 0.3, i * 0.7, 0.2 * i); g.base = g.position.clone();
  g.sn = K.sprite(g, K.glowTex("rgba(255,255,255,1)"), 10, V(5, 0, 2), 0); g.sn2 = K.sprite(g, K.glowTex("rgba(190,215,255,.55)"), 34, V(5, 0, 2), 0); GS.push(g); }
const rulerPts = []; const rulerMat = new THREE.LineBasicMaterial({ color: 0xffd36a, linewidth: 2, transparent: true, opacity: 0, depthWrite: false });
const ruler = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, -70, 120), V(0, -70, -1800)]), rulerMat); scM.add(ruler);
const ticks = []; for (let i = 0; i < 5; i++) { const m = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(-8, -70, -i * 420), V(8, -70, -i * 420)]), rulerMat); scM.add(m); ticks.push(m); }

// ===== Zeiten =====
const tDie = W("die", 4.3), tDas = W("das", 12), tFolg = W("folg"), tEnt = W("entdeckt"), tIn = W("in", 27.3), tExp = W("explodiert", 31), tEr = W("er", 38.6), tDann = W("dann", 42.8), tAuf = W("auf", 45), tUnd = W("und", 49.6), tMit = W("mit", 55), tVon = W("von", 59.2), tFur = W("für", 61.3), tSolche = W("solche", 63.5), tDamit = W("damit", 66.8), tUndW = W("und", 69.9);
label("NGC 1433", GAL, 70, { t0: tDie + 0.4, t1: tDas - 0.1, size: 60, gap: 10 });
label("Supernova", snO, 8, { t0: 1.4, t1: tDie - 0.1, size: 52, gap: 40 });
label("Weißer Zwerg", wd, RW * 1.4, { t0: tExp + 0.5, t1: tEr - 0.1, size: 50, gap: 30 }); label("Erde", EAW.group, RW * 1.4, { t0: W("so", 35.7), t1: tEr - 0.1, size: 50, gap: 30 });
label("Nachbarstern", comp, RC * 1.1, { t0: tEr + 0.5, t1: tDann - 0.1, size: 52, gap: 20 });
label("Deutschland", deO, 2, { t0: tVon - 0.1, t1: tFur - 0.1, size: 48, gap: 16 }); label("Süden", suO, 2, { t0: W("nur", 57.8), t1: tFur - 0.1, size: 48, gap: 16 });


renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.45, 0.8);
  let scene = scG, pos = V(0, 0, 300), look = V(0, 0, 0), fov = 40; cam.up.set(0, 1, 0);
  GAL.rotation.y = t * 0.01; setSN(0); stream.material.opacity = 0; disk.material.uniforms.a.value = 0; blast.material.opacity = 0; [bF1, bF2, bF3].forEach((s) => (s.material.opacity = 0)); wd.visible = true; comp.visible = true; compG.material.opacity = 0.7; EAW.group.visible = true;
  const snW = () => snO.getWorldPosition(V(0, 0, 0));
  if (t < tDie - 0.05) { // Hook: Stern flammt auf
    const b = K.eout(cl((t - 0.5) / 1.6)); setSN(0.35 + 0.65 * b + 0.05 * Math.sin(t * 9)); const f = K.eio(prog(t, 0, tDie)); const s = snW(); pos = s.clone().add(V(lerp(20, 50, f), lerp(90, 120, f), lerp(150, 240, f))); look = s.clone().lerp(V(0, 0, 0), 0.25);
    if (t > 0.5 && t < 1.2) E.grade.uniforms.flash.value = 0.25 * Math.sin(Math.PI * prog(t, 0.5, 0.7)); }
  else if (t < tDas - 0.05) { setSN(0.9); const f = K.eio(prog(t, tDie, tDas - tDie)); pos = V(lerp(60, 0, f), lerp(120, 210, f), lerp(240, 330, f)); look = V(0, 0, 0); }
  else if (t < tEnt - 0.05) { // Lichtreise zur Erde
    scene = scL; const f = cl((t - tDas - 0.3) / (W("die", 15.8) - tDas)); const gp = GAL2.localToWorld(V(57, 0, 36)); const ep = V(0, 0, 0); const head = gp.clone().lerp(ep, K.eio(f) * 0.985);
    pulse.forEach((p, i) => { p.position.copy(gp.clone().lerp(ep, Math.max(0, K.eio(f) * 0.985 - i * 0.012))); p.material.opacity = f > 0 && f < 1 ? (i ? 0.55 : 1) : f >= 1 ? 0 : 0; });
    beamGeo.attributes.position.setXYZ(0, gp.x, gp.y, gp.z); beamGeo.attributes.position.setXYZ(1, head.x, head.y, head.z); beamGeo.attributes.position.needsUpdate = true; beamMat.opacity = 0.35;
    if (t < W("die", 15.8)) { const q = K.eio(prog(t, tDas, W("die", 15.8) - tDas)); pos = V(lerp(6, 0, q), lerp(-10, -6, q), lerp(70, 58, q)); look = V(-40, 230, -900); fov = 50; EAL.group.rotation.y = 2.3 + t * 0.02; }
    else { const q = K.eio(prog(t, W("die", 15.8), 1.6)); pos = V(lerp(40, 30, q), lerp(25, 14, q), lerp(110, 70, q)); look = V(0, 0, 0); EAL.group.rotation.y = 2.3 + t * 0.02; if (q < 1 && t < W("die", 15.8) + 0.4) E.grade.uniforms.flash.value = 0.12 * Math.sin(Math.PI * prog(t, W("die", 15.8), 0.4)); } }
  else if (t < tIn - 0.05) { // Himmel + Teleskop
    setSN(0.15 + 0.1 * cl((t - tEnt) / 3)); const f = K.eio(prog(t, tEnt, tIn - tEnt)); const a = 0.6 + f * 0.5; pos = V(Math.sin(a) * 300, 140, Math.cos(a) * 300); look = V(0, 0, 0); fov = 42; }
  else if (t < tExp - 0.05) { // 25-mal heller
    const k = cl((t - W("fünfundzwanzigmal") + 0.3) / 1.6); setSN(0.12 + 0.88 * K.eio(k)); const s = snW(); const f = K.eio(prog(t, tIn, tExp - tIn)); pos = s.clone().add(V(lerp(10, 20, f), lerp(60, 70, f), lerp(130, 150, f))); look = s.clone().lerp(V(0, 0, 0), 0.3); fov = 38; }
  else if (t < tEr - 0.05) { // Weißer Zwerg vs Erde
    scene = scW; comp.visible = false; compG.material.opacity = 0; wd.position.set(0, 0, 0); EAW.group.rotation.y = t * 0.15; wdM.rotation.y = t * 0.1; const f = K.eio(prog(t, tExp, tEr - tExp)); pos = V(3.25, lerp(1, 0.6, f), lerp(34, 28, f)); look = V(3.25, 0, 0); fov = 38; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.9); }
  else if (t < tAuf - 0.05) { // Gas klauen + Explosion
    scene = scW; EAW.group.visible = false; streamAt(t); const go = cl((t - tEr) / 0.8); stream.material.opacity = 0.75 * go; disk.material.uniforms.a.value = 0.8 * go; wdM.rotation.y = t * 0.3;
    const tb = W("auseinander") - 0.15; const f = K.eio(prog(t, tEr, tb - tEr)); pos = V(lerp(-20, 10, f), lerp(45, 22, f), lerp(85, 55, f)); look = V(lerp(-30, -6, f), 0, lerp(-10, 0, f)); fov = 42;
    if (t > tb) { const e = t - tb; stream.material.opacity *= cl(1 - e / 0.3); disk.material.uniforms.a.value *= cl(1 - e / 0.3); wd.visible = e < 0.1; bF1.material.opacity = cl(1 - e / 1.2); bF1.scale.setScalar(10 + e * 30); bF2.material.opacity = cl(1 - e / 1.5) * 0.6; bF2.scale.setScalar(30 + e * 50);
      E.grade.uniforms.flash.value = 0.3 * Math.max(0, 1 - e / 0.4); } }
  else if (t < tUnd - 0.05) { // Hülle dehnt sich aus
    scene = scW; EAW.group.visible = false; wd.visible = false; const e = t - (W("auseinander") - 0.15); const R = 4 + e * 9; for (let i = 0; i < NB; i++) { const d = bDir[i]; const r = R * d[3]; bp[i * 3] = d[0] * r; bp[i * 3 + 1] = d[1] * r; bp[i * 3 + 2] = d[2] * r; } bGeo.attributes.position.needsUpdate = true;
    blast.material.opacity = 0.85; bF1.material.opacity = 0.9; bF1.scale.setScalar(16 + Math.sin(t * 5) * 1.5); bF2.material.opacity = 0.7; bF2.scale.setScalar(R * 2.4); bF3.material.opacity = 0.5; bF3.scale.setScalar(R * 4); compG.material.opacity = 0.4;
    const a = (t - tAuf) * 0.12; pos = V(Math.sin(a) * 110, 30, Math.cos(a) * 110); look = V(-10, 0, 0); fov = 44; }
  else if (t < tMit - 0.05) { // Höhepunkt jetzt
    setSN(1.05 + 0.08 * Math.sin(t * 4)); const f = K.eio(prog(t, tUnd, tMit - tUnd)); const s = snW(); pos = s.clone().add(V(lerp(-60, -20, f), lerp(150, 90, f), lerp(260, 170, f))); look = s.clone().lerp(V(0, 0, 0), 0.5); }
  else if (t < tFur - 0.05) { // Erde: Süden ja, Deutschland nein
    scene = scE; const de = EA.ll(51, 10, RE * 1.01), su = EA.ll(-30, 24, RE * 1.01); deO.position.copy(de); suO.position.copy(su); deDot.position.copy(de); suDot.position.copy(su);
    deDot.material.opacity = cl((t - tVon + 0.1) / 0.4); suDot.material.opacity = cl((t - W("nur", 57.8)) / 0.4); EA.group.rotation.y = -0.45 + (t - tMit) * 0.01;
    const f = K.eio(prog(t, tMit, tFur - tMit)); const mid = EA.ll(10, 16, RE).normalize(); pos = mid.multiplyScalar(lerp(470, 420, f)); look = V(0, 0, 0); fov = 36; }
  else { // kosmisches Maßband
    scene = scM; const grow = cl((t - tUndW) / 2); GS.forEach((g, i) => { g.position.copy(g.base).multiplyScalar(1 + grow * 0.35); const fl = cl((t - tSolche - 0.2 - i * 0.35) / 0.3); g.sn.material.opacity = fl * (0.85 + 0.15 * Math.sin(t * 6 + i)); g.sn2.material.opacity = fl * 0.6; g.rotation.y += 0.0; });
    rulerMat.opacity = 1 * cl((t - tDamit + 0.2) / 0.6);
    const f = K.eio(prog(t, tFur, 72 - tFur)); pos = V(lerp(150, 190, f), lerp(60, 110, f), lerp(380, 520, f)); look = V(0, -20, lerp(-650, -800, f)); fov = 42; }
  if (scene !== scL) { beamMat.opacity = 0; pulse.forEach((p) => (p.material.opacity = 0)); }
  if (scene !== scE) { deDot.material.opacity = 0; suDot.material.opacity = 0; }
  if (scene !== sky) skySN.material.opacity = 0;
  cam.fov = fov; cam.near = 0.05; cam.far = 80000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("rund", 8.8) - 0.1, tDas - 0.1, "≈ 50 Mio. Lichtjahre");
  seg(W("licht", 13) - 0.1, W("die", 15.8) - 0.1, "50 Mio. Jahre unterwegs");
  seg(W("die", 15.8), W("menschen") - 0.1, "🦖 schon ausgestorben"); seg(W("menschen") - 0.1, tFolg - 0.2, "Menschen? Noch lange nicht");
  seg(W("fünfundzwanzigmal") - 0.2, tExp - 0.1, `${Math.round(1 + 24 * K.eio(cl((t - W("fünfundzwanzigmal") + 0.3) / 1.6)))}× heller`);
  seg(W("so", 35.7) - 0.1, W("aber", 37) - 0.1, "so groß wie die Erde"); seg(W("aber", 37) - 0.1, tEr - 0.1, "so schwer wie die Sonne");
  seg(W("gas") - 0.1, tDann - 0.1, "Gas wird geklaut");
  seg(W("milliarden") - 0.3, tUnd - 0.1, "so hell wie<br>Milliarden Sonnen");
  seg(W("zwischen", 51.8) - 0.1, tMit - 0.1, "Höhepunkt<div class='sub'>18.–23. November</div>");
  seg(W("hobby") - 0.2, tVon - 0.1, "🔭 Hobby-Teleskop"); seg(tVon, tFur - 0.1, "Deutschland: zu tief");
  seg(W("kosmische") - 0.1, tDamit - 0.1, "📏 kosmisches Maßband"); seg(tDamit, tUndW - 0.1, "Entfernung messen"); seg(tUndW, 72, "Weltall wächst");
  word(wh, wa); cap(t);
};
