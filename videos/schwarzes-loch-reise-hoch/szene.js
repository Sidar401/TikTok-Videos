const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
const LAND = FMT.W > FMT.H; const FV = (f) => (LAND ? f * 0.82 : f * 1.22);
K.reseed(77);
// @modelle
E.R.localClippingEnabled = true;
const sunT = await tex("sun.jpg");
// ================= Linsen-Effekt (Licht wird verbogen) =================
const { ShaderPass } = await import("three/addons/postprocessing/ShaderPass.js");
const { RenderPass } = await import("three/addons/postprocessing/RenderPass.js");
const lens = new ShaderPass({ uniforms: { tDiffuse: { value: null }, c: { value: new THREE.Vector2(0.5, 0.5) }, rs: { value: 0.1 }, re: { value: 0.16 }, asp: { value: FMT.W / FMT.H }, on: { value: 0 }, ring: { value: 1 } },
  vertexShader: `varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform sampler2D tDiffuse;uniform vec2 c;uniform float rs,re,asp,on,ring;varying vec2 vUv;
    void main(){vec2 d=(vUv-c)*vec2(asp,1.);float r=max(length(d),1e-5);float k=min(on*re*re/(r*r),8.);vec2 s=c+d*(1.-k)/vec2(asp,1.);
    vec3 col=texture2D(tDiffuse,s).rgb;float inside=step(0.,s.x)*step(s.x,1.)*step(0.,s.y)*step(s.y,1.);col*=mix(.0,1.,inside);
    if(on>0.){col*=smoothstep(rs*.985,rs*1.02,r);col+=vec3(1.,.82,.6)*ring*on*exp(-pow((r-rs*1.035)/(rs*.022),2.));}
    else col=texture2D(tDiffuse,vUv).rgb;gl_FragColor=vec4(col,1.);}` });
E.comp.insertPass(lens, 1);
const fsc = new THREE.Scene(); const front = new RenderPass(fsc, cam); front.clear = false; front.clearDepth = true; E.comp.insertPass(front, 2);
const emptyS = new THREE.Scene();
// ================= Bausteine =================
const diskMat = (hot, clip) => new THREE.ShaderMaterial({ uniforms: { time: { value: 0 }, bright: { value: 1 }, hot: { value: hot } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, clipping: !!clip, clippingPlanes: clip ? [clip] : null,
  vertexShader: `#include <clipping_planes_pars_vertex>
  varying vec2 vP;void main(){vP=position.xy;vec4 mvPosition=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mvPosition;
  #include <clipping_planes_vertex>
  }`,
  fragmentShader: `#include <clipping_planes_pars_fragment>
  uniform float time,bright,hot;varying vec2 vP;void main(){
  #include <clipping_planes_fragment>
  float r=length(vP);float a=atan(vP.y,vP.x);float k=(r-4.2)/12.;
    float sw=.55+.45*sin(a*7.-r*1.4+time*2.2)*sin(a*3.+r*.8-time*1.3);float st=.9+.1*sin(r*5.+sin(a*5.+time)*1.5);vec3 c=mix(vec3(1.,.97,.92),mix(vec3(1.,.58,.22),vec3(.6,.75,1.),hot),smoothstep(0.,.4,k));c=mix(c,mix(vec3(.55,.12,.04),vec3(.25,.3,.8),hot),smoothstep(.4,1.,k));
    float al=(1.-smoothstep(.0,1.,k))*(.5+.5*sw)*st*smoothstep(0.,.05,k);gl_FragColor=vec4(c*al*bright*1.15,al*bright);}` });
const blackM = new THREE.MeshBasicMaterial({ color: 0x000000 });
// kleine Löcher ohne Linse (Vergleich)
function hole(parent, s, hot) { const g = new THREE.Group(); const core = new THREE.Mesh(new THREE.SphereGeometry(3, 64, 48), blackM); g.add(core);
  const dm = diskMat(hot); const disk = new THREE.Mesh(new THREE.RingGeometry(4.2, 16, 160, 4), dm); disk.rotation.x = -1.35; g.add(disk);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(3.25, 0.12, 12, 128), new THREE.MeshBasicMaterial({ color: 0xffd9a8, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); g.add(ring);
  const halo = K.sprite(g, K.glowTex("rgba(255,170,90,.5)"), 40, V(0, 0, 0), 0.4); halo.material.depthTest = true; halo.renderOrder = -1; g.scale.setScalar(s); parent.add(g); return { g, core, disk, dm, ring, halo }; }
const colStars = (sc, n, r, seed, sz = 2.2) => { K.reseed(seed); const p = [], c = []; for (let i = 0; i < n; i++) { const a = K.rnd() * 6.283, u = K.rnd() * 2 - 1; p.push(Math.cos(a) * Math.sqrt(1 - u * u) * r, u * r, Math.sin(a) * Math.sqrt(1 - u * u) * r); const col = new THREE.Color().setHSL(K.rnd() < 0.5 ? 0.6 : 0.08, 0.5, 0.6 + K.rnd() * 0.35); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const m = new THREE.PointsMaterial({ size: sz, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.9, depthWrite: false }); const P = new THREE.Points(g, m); sc.add(P); return P; };
const nebula = (sc, r, seed) => { K.reseed(seed); const cols = ["rgba(90,120,255,.35)", "rgba(200,80,160,.3)", "rgba(80,200,220,.25)", "rgba(255,140,80,.25)"]; const out = []; for (let i = 0; i < 14; i++) { const a = K.rnd() * 6.283, u = K.rnd() * 1.6 - 0.8; out.push(K.sprite(sc, K.glowTex(cols[i % 4]), r * (0.25 + K.rnd() * 0.35), V(Math.cos(a) * Math.sqrt(1 - u * u) * r, u * r, Math.sin(a) * Math.sqrt(1 - u * u) * r), 0.55)); } return out; };
// Astronaut (Raumanzug)
function astro() { const g = new THREE.Group(); const suit = MO.plain(0xe9e8e3, 0.0, 0.75, 0.5), dark = MO.plain(0x30343a, 0.4, 0.5, 0.5), visor = MO.plain(0xd8a040, 1.0, 0.12, 1.4), red = MO.plain(0xb3262b, 0, 0.6, 0.4);
  const cap = (r, l, m) => new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 8, 24), m);
  const torso = cap(0.3, 0.42, suit); torso.position.y = 0.95; g.add(torso);
  const pack = new THREE.Mesh(MO.RBox(0.56, 0.66, 0.26, 2, 0.05), suit); pack.position.set(0, 1.0, -0.3); g.add(pack);
  const chest = new THREE.Mesh(MO.RBox(0.3, 0.18, 0.1, 2, 0.02), dark); chest.position.set(0, 1.02, 0.29); g.add(chest);
  const band = new THREE.Mesh(new THREE.TorusGeometry(0.305, 0.03, 8, 40), red); band.rotation.x = Math.PI / 2; band.position.y = 1.2; g.add(band);
  const helm = new THREE.Mesh(new THREE.SphereGeometry(0.25, 48, 32), suit); helm.position.y = 1.5; g.add(helm);
  const vis = new THREE.Mesh(new THREE.SphereGeometry(0.255, 48, 32, -1.1, 2.2, 0.55, 1.35), visor); vis.position.y = 1.5; vis.rotation.y = Math.PI / 2 - Math.PI / 2; g.add(vis);
  const arm = (s) => { const a = new THREE.Group(); const up = cap(0.095, 0.3, suit); up.position.y = -0.2; a.add(up); const lo = cap(0.085, 0.26, suit); lo.position.set(0, -0.48, 0.06); lo.rotation.x = -0.3; a.add(lo); const gl = new THREE.Mesh(new THREE.SphereGeometry(0.09, 16, 12), dark); gl.position.set(0, -0.68, 0.12); a.add(gl); a.position.set(s * 0.38, 1.22, 0); a.rotation.z = s * 0.35; return a; };
  const leg = (s) => { const l = new THREE.Group(); const up = cap(0.12, 0.34, suit); up.position.y = -0.22; l.add(up); const lo = cap(0.11, 0.32, suit); lo.position.set(0, -0.62, -0.05); lo.rotation.x = 0.25; l.add(lo); const b = new THREE.Mesh(MO.RBox(0.2, 0.14, 0.3, 2, 0.04), dark); b.position.set(0, -0.86, 0.02); l.add(b); l.position.set(s * 0.15, 0.62, 0); l.rotation.z = s * 0.12; return l; };
  const aL = arm(-1), aR = arm(1), lL = leg(-1), lR = leg(1); g.add(aL, aR, lL, lR); g.userData = { aL, aR, lL, lR, mats: [suit, dark, visor, red] };
  const P = new THREE.Group(); g.position.y = -0.95; P.add(g); P.userData = g.userData; return P; }
const tintA = (A, k, fade = 1) => { A.userData.mats.forEach((m, i) => { m.transparent = fade < 1; m.opacity = fade; if (!m.userData.c0) m.userData.c0 = m.color.clone(); m.color.copy(m.userData.c0).lerp(new THREE.Color(0.55, 0.05, 0.02), k); }); };
const pose = (A, t, s = 1) => { const u = A.userData; u.aL.rotation.x = Math.sin(t * 0.7) * 0.25 * s; u.aR.rotation.x = -Math.sin(t * 0.6 + 1) * 0.25 * s; u.lL.rotation.x = Math.sin(t * 0.5) * 0.18 * s; u.lR.rotation.x = -Math.sin(t * 0.55 + 2) * 0.18 * s; };
// ================= Hauptszene: Sagittarius A* =================
const sc = new THREE.Scene(); K.reseed(3); K.stars(sc, 9000, -1, 30000, 1.6).material.opacity = 0.6; const CS = colStars(sc, 5000, 25000, 9, 2.6); const NEB = nebula(sc, 22000, 12);
sc.add(new THREE.AmbientLight(0x404858, 0.55)); const diskL = new THREE.PointLight(0xffc890, 900, 0, 1.6); sc.add(diskL); const rim = new THREE.DirectionalLight(0x9fb8ff, 0.9); rim.position.set(-3, 2, -4); sc.add(rim);
const HG = new THREE.Group(); sc.add(HG); const HR = 3; // Ereignishorizont-Radius
const DM = diskMat(0.0); const DISK = new THREE.Mesh(new THREE.RingGeometry(4.2, 16, 200, 6), DM); DISK.rotation.x = -Math.PI / 2 + 0.12; HG.add(DISK);
const clipP = new THREE.Plane(); const DMF = diskMat(0.0, clipP); const DISKF = new THREE.Mesh(DISK.geometry, DMF); DISKF.matrixAutoUpdate = false; fsc.add(DISKF);
const CORE = new THREE.Mesh(new THREE.SphereGeometry(HR * 1.02, 64, 48), blackM); sc.add(CORE); CORE.visible = false;
const HALO = K.sprite(sc, K.glowTex("rgba(255,160,80,.45)"), 46, V(0, 0, 0), 0.35);
const A = astro(); fsc.add(A); fsc.add(new THREE.AmbientLight(0x404858, 0.7)); const fL = new THREE.PointLight(0xffc890, 160, 0, 1.6); fsc.add(fL); const fR = new THREE.DirectionalLight(0x9fb8ff, 0.9); fR.position.set(-3, 2, 4); fsc.add(fR); const aO = new THREE.Object3D(); sc.add(aO);
// Photonenring (Licht kreist)
const PR = new THREE.Mesh(new THREE.TorusGeometry(HR * 1.5, 0.035, 8, 256), new THREE.MeshBasicMaterial({ color: 0xfff0d8, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); sc.add(PR);
const PD = K.sprite(sc, K.glowTex("rgba(255,250,235,1)"), 2.2, V(0, 0, 0), 0); const trail = []; for (let i = 0; i < 26; i++) trail.push(K.sprite(sc, K.glowTex("rgba(255,230,190,1)"), 1.4, V(0, 0, 0), 0));
// Horizont-Gitter
const HZ = new THREE.Mesh(new THREE.SphereGeometry(HR * 1.25, 48, 24), new THREE.MeshBasicMaterial({ color: 0xff9a5a, wireframe: true, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); fsc.add(HZ);
const hzO = new THREE.Object3D(); hzO.position.set(0, 0, 0); sc.add(hzO);
// Info-Punkte auf dem Horizont (gespeichert?)
const INF = (() => { K.reseed(31); const p = []; for (let i = 0; i < 9000; i++) { const u = K.rnd() * 2 - 1, a = K.rnd() * 6.283; p.push(Math.cos(a) * Math.sqrt(1 - u * u) * HR * 1.03, u * HR * 1.03, Math.sin(a) * Math.sqrt(1 - u * u) * HR * 1.03); } const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); const m = new THREE.PointsMaterial({ color: 0x9fd0ff, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }); const P = new THREE.Points(g, m); sc.add(P); return P; })();
// Raumschiff des Freundes
const SHIP = MO.shenzhou().g; SHIP.remove(SHIP.children[SHIP.children.length - 1]); sc.add(SHIP); SHIP.visible = false; const shipO = new THREE.Object3D(); sc.add(shipO);
// Licht, das hineinfällt
const NP = 900, pa = []; K.reseed(5); for (let i = 0; i < NP; i++) pa.push([K.rnd(), K.rnd() * 6.28, 0.6 + K.rnd() * 0.8, (K.rnd() - 0.5) * 2]);
const pg = new THREE.BufferGeometry(); const parr = new Float32Array(NP * 3); pg.setAttribute("position", new THREE.BufferAttribute(parr, 3));
const PTS = new THREE.Points(pg, new THREE.PointsMaterial({ color: 0xffe2b0, size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); sc.add(PTS);
const fall = (t, sp, r0 = 60, flat = 1) => { for (let i = 0; i < NP; i++) { const [ph, a0, v, yy] = pa[i]; const k = (ph + t * 0.1 * v * sp) % 1; const r = lerp(r0, HR * 1.05, Math.pow(k, 0.75)); const a = a0 + k * 7; parr[i * 3] = Math.cos(a) * r; parr[i * 3 + 1] = yy * r * 0.25 * flat; parr[i * 3 + 2] = Math.sin(a) * r; } pg.attributes.position.needsUpdate = true; };
// ================= Milchstraße =================
const sg = new THREE.Scene(); K.reseed(8); K.stars(sg, 6000, -1, 60000, 1.5).material.opacity = 0.5;
const galaxy = (parent, R, n, seed, tilt) => { K.reseed(seed); const p = [], c = []; for (let i = 0; i < n; i++) { const core = K.rnd() < 0.15; let r, a, y; if (core) { r = Math.pow(K.rnd(), 2) * R * 0.16; a = K.rnd() * 6.283; y = (K.rnd() - 0.5) * R * 0.05; } else { const arm = i % 4; r = Math.pow(K.rnd(), 0.7) * R; a = arm * Math.PI / 2 + Math.log(r / R * 12 + 1) * 2.4 + (K.rnd() - 0.5) * 0.6; y = (K.rnd() - 0.5) * R * 0.02; }
    p.push(Math.cos(a) * r, y, Math.sin(a) * r); const col = new THREE.Color(1, 0.88, 0.72).lerp(new THREE.Color(0.6, 0.72, 1), core ? 0 : Math.min(1, r / R + 0.2)); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const m = new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.75, blending: THREE.AdditiveBlending, depthWrite: false }); const G = new THREE.Group(); G.add(new THREE.Points(g, m)); G.rotation.set(tilt, 0, 0); parent.add(G); G.userData.m = m; return G; };
const MW = galaxy(sg, 500, 110000, 41, 0); MW.userData.m.opacity = 0.5; const mwGlow = K.sprite(sg, K.glowTex("rgba(255,220,170,.6)"), 90, V(0, 0, 0), 0.35);
const sgrM = K.sprite(sg, K.glowTex("rgba(255,120,60,1)"), 8, V(0, 0, 0), 0); const sgrO = new THREE.Object3D(); sg.add(sgrO); const mwO = new THREE.Object3D(); mwO.position.set(0, 0, 380); sg.add(mwO);
// ================= Vergleich: klein / riesig =================
const sv = new THREE.Scene(); K.reseed(14); K.stars(sv, 9000, -1, 30000, 1.6).material.opacity = 0.6;
const SMALL = hole(sv, 0.35, 0.0); SMALL.g.position.set(-22, 0, 0); const BIG = hole(sv, 2.6, 0.15); BIG.dm.uniforms.bright.value = 0.55; BIG.halo.material.opacity = 0.2; BIG.g.position.set(30, 0, -40);
const smO = new THREE.Object3D(); sv.add(smO); const bgO = new THREE.Object3D(); sv.add(bgO);
sv.add(new THREE.AmbientLight(0x404858, 0.6)); const svL = new THREE.PointLight(0xffc890, 5, 0, 1.6); sv.add(svL); const A2 = astro(); sv.add(A2);
// ================= Innen =================
const si = new THREE.Scene(); K.sky(si, 0x050102, 0x120406, 0x220806, 8000);
const TUN = (() => { K.reseed(51); const p = [], c = []; for (let i = 0; i < 2600; i++) { const a = K.rnd() * 6.283, r = 6 + K.rnd() * 60, z = -K.rnd() * 900; p.push(Math.cos(a) * r, Math.sin(a) * r, z, Math.cos(a) * r * 0.02, Math.sin(a) * r * 0.02, z - 60); const k = K.rnd(); const col = new THREE.Color(1, 0.45 + k * 0.4, 0.25 + k * 0.3); c.push(col.r * 0.25, col.g * 0.25, col.b * 0.25, col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const L = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false })); si.add(L); return L; })();
const SING = K.sprite(si, K.glowTex("rgba(255,245,230,1)"), 30, V(0, 0, -900), 1); const SING2 = K.sprite(si, K.glowTex("rgba(255,120,60,.7)"), 160, V(0, 0, -900), 0.6);
const OUT = K.sprite(si, K.glowTex("rgba(170,200,255,1)"), 200, V(0, 0, 300), 0);
si.add(new THREE.AmbientLight(0x603020, 0.8)); const siL = new THREE.PointLight(0xffd0a0, 600, 0, 1.5); siL.position.set(0, 0, -30); si.add(siL); const A3 = astro(); si.add(A3);
// ================= Tunnel + neues Universum =================
const sw = new THREE.Scene(); const RINGS = []; for (let i = 0; i < 60; i++) { const r = new THREE.Mesh(new THREE.TorusGeometry(10 + Math.sin(i * 0.4) * 2, 0.08, 8, 96), new THREE.MeshBasicMaterial({ color: new THREE.Color().setHSL(0.58 + 0.1 * Math.sin(i * 0.3), 0.7, 0.6), transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); r.position.z = -i * 14; sw.add(r); RINGS.push(r); }
K.reseed(66); K.stars(sw, 5000, -1, 20000, 1.6).material.opacity = 0.3; const WEND = K.sprite(sw, K.glowTex("rgba(230,240,255,1)"), 60, V(0, 0, -860), 1);
const su = new THREE.Scene(); K.reseed(71); K.stars(su, 6000, -1, 40000, 1.5).material.opacity = 0.5; const GALS = []; for (let i = 0; i < 40; i++) { const G = galaxy(su, 30 + K.rnd() * 40, 7000, 100 + i, K.rnd() * 3); G.userData.m.size = 1.2; G.rotation.y = K.rnd() * 6; const d = V(K.rnd() - 0.5, K.rnd() - 0.5, K.rnd() - 0.5).normalize().multiplyScalar(250 + K.rnd() * 700); G.userData.dir = d; GALS.push(G); }
const BANG = K.sprite(su, K.glowTex("rgba(255,250,240,1)"), 400, V(0, 0, 0), 0); const BUB = new THREE.Mesh(new THREE.SphereGeometry(1100, 64, 48), new THREE.ShaderMaterial({ uniforms: { op: { value: 0 } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  vertexShader: `varying vec3 vN;varying vec3 vV;void main(){vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-mv.xyz);gl_Position=projectionMatrix*mv;}`,
  fragmentShader: `uniform float op;varying vec3 vN;varying vec3 vV;void main(){float f=1.-abs(dot(vN,vV));gl_FragColor=vec4(vec3(1.,.65,.35)*pow(f,3.)*op,pow(f,3.)*op);}` })); su.add(BUB);
const UB = hole(su, 50, 0.0); UB.g.position.set(0, 0, 0); UB.g.visible = false;
// ================= Zeiten =================
const tHeute = W("heute"), tFolg = W("folg"), tStell = W("stell"), tVor = W("vor", 28), tEs = W("es", 33.8), tUnd1 = W("und", 37), tDenn = W("denn"), tDu = W("du", 44), tDieses = W("dieses"), tJetzt = W("jetzt", 56);
const tUndD = W("und", 62.4), tDieS = W("die", 69.3), tEtwas = W("etwas", 74.7), tHier = W("hier", 78.5), tWenn = W("wenn", 83.5), tJetzt2 = W("jetzt", 88.4), tFuer = W("für", 93.8), tDein = W("dein", 99.6), tUndK = W("und", 102.2), tEr = W("er", 107.4);
const tFuerD = W("für", 109.2), tDiese = W("diese", 114.8), tAber = W("aber", 120.3), tSelbst = W("selbst"), tUndW = W("und", 126.1), tDeineF = W("deine", 129), tBei = W("bei", 134.7), tForscher = W("forscher", 140.6), tDoch = W("doch", 143.6), tDarum = W("darum");
const tDrinnen = W("drinnen"), tHierA = W("hier", 154.1), tDerM = W("der", 158.6), tIhm = W("ihm"), tBeiS = W("bei", 167.1), tBeiM = W("bei", 172.1), tJetzt3 = W("jetzt", 180.2), tUndD2 = W("und", 187.4), tHierW = W("hier", 189.8), tDieP = W("die", 192.2);
const tUndG = W("und", 195.5), tWird1 = W("wird", 201.4), tWird2 = W("wird", 203.2), tOder = W("oder", 205.1), tManche = W("manche"), tViel = W("vielleicht", 213), tWasG = W("was", 215.2), END = 219.9, KARTE = tFolg;
// Beschriftungen
label("Sagittarius A*", sgrO, 6, { t0: W("sagittarius") + 0.2, t1: tEs - 0.1, size: LAND ? 46 : 52, gap: 18 });
label("Milchstraße", mwO, 0, { t0: tVor + 0.3, t1: W("sagittarius") - 0.1, size: LAND ? 46 : 52, gap: 0 });
label("Ereignishorizont", hzO, HR * 1.05, { t0: W("ereignishorizont") - 0.1, t1: tAber + 1.6, size: LAND ? 44 : 50, gap: 22 });
label("dein Freund", shipO, 2.2, { t0: W("freund", 89) - 0.1, t1: tFuer + 0.6, size: LAND ? 40 : 46, gap: 14 });
label("du", aO, 1.1, { t0: tFuer - 0.1, t1: tEr + 0.5, size: LAND ? 40 : 46, gap: 10 });
label("Sagittarius A*", smO, 3.5, { t0: tBeiS + 0.3, t1: tJetzt3 - 0.1, size: LAND ? 40 : 46, gap: 16 }); label("M87*", bgO, 25, { t0: W("monster", 172) - 0.1, t1: tJetzt3 - 0.1, size: LAND ? 48 : 54, gap: 16 });
const WORDEL = document.getElementById("word");
const proj = (p) => { const q = p.clone().project(cam); return new THREE.Vector2((q.x + 1) / 2, (q.y + 1) / 2); };
const lensOn = (str, ringB = 1) => { cam.updateMatrixWorld(true); const c = proj(HG.position); const d = cam.position.distanceTo(HG.position); const ang = Math.asin(Math.min(1, HR * 1.25 / d)); const rs = Math.tan(ang) / Math.tan(cam.fov * Math.PI / 360) * 0.5;
  lens.uniforms.c.value.copy(c); lens.uniforms.rs.value = rs; lens.uniforms.re.value = rs * 1.45; lens.uniforms.on.value = str; lens.uniforms.ring.value = ringB; };
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.5, 0.82);
  let scene = sc, pos = V(0, 6, 60), look = V(0, 0, 0), fov = 40, L = 1, ringB = 1, fr = true;
  const spin = t * 0.8 + Math.max(0, t - tDieses) * 1.6; DM.uniforms.time.value = spin; DMF.uniforms.time.value = spin; [SMALL, BIG, UB].forEach((h) => (h.dm.uniforms.time.value = t));
  DM.uniforms.bright.value = DMF.uniforms.bright.value = 1; DISK.visible = DISKF.visible = true; HALO.material.opacity = 0.35; A.visible = false; A.scale.set(1, 1, 1); A.rotation.set(0, 0, 0); tintA(A, 0, 1);
  PR.material.opacity = 0; PD.material.opacity = 0; trail.forEach((s) => (s.material.opacity = 0)); HZ.material.opacity = 0; INF.material.opacity = 0; SHIP.visible = false; PTS.material.opacity = 0; CS.material.opacity = 0.9; NEB.forEach((n) => (n.material.opacity = 0.55));
  A2.visible = false; A3.visible = false; CORE.visible = false; UB.g.visible = false; BUB.material.uniforms.op.value = 0; BANG.material.opacity = 0; OUT.material.opacity = 0;
  const orbit = (a, d, y) => V(Math.sin(a) * d, y, Math.cos(a) * d);
  if (t < tHeute - 0.05) { const f = prog(t, 0, tHeute); pos = orbit(0.3 - f * 0.25, lerp(70, 52, K.eout(f)), lerp(9, 6, f)); look = V(0, LAND ? 5 : 9, 0); fov = FV(40);
    A.visible = true; A.position.set(lerp(9, 5, f), lerp(5, 3, f), lerp(30, 22, f)); A.rotation.set(0.6, 2.6 + t * 0.15, 0.3); pose(A, t); }
  else if (t < tFolg - 0.05) { const f = prog(t, tHeute, tFolg - tHeute); pos = orbit(-0.6 + f * 0.9, lerp(110, 70, K.eio(f)), lerp(22, 8, f)); fov = FV(40); }
  else if (t < tStell - 0.05) { const f = prog(t, tFolg, tStell - tFolg); pos = orbit(0.3 + f * 0.5, 78, 4); look = V(0, LAND ? 11 : -12, 0); fov = FV(40); }
  else if (t < tVor - 0.05) { const f = prog(t, tStell, tVor - tStell); A.visible = true; A.position.set(0, 0, 40); A.rotation.set(0.15, Math.PI + 0.3 + f * 0.2, 0.08); pose(A, t);
    pos = LAND ? V(lerp(2.6, 2.0, f), lerp(1.4, 1.1, f), lerp(44.5, 43.6, f)) : V(lerp(1.3, 1.0, f), lerp(1.6, 1.3, f), lerp(46.5, 45.6, f)); look = V(-0.6, 0.2, 20); fov = FV(42); }
  else if (t < tEs - 0.05) { scene = sg; L = 0; const f = K.eio(prog(t, tVor, tEs - tVor)); const d = lerpLog(1400, 70, f); pos = V(d * 0.05, d * 0.75, d * 0.66); sgrM.material.opacity = cl((f - 0.45) * 3); sgrM.scale.setScalar(d * 0.05); MW.rotation.y = t * 0.01; fov = FV(45); }
  else if (t < tUnd1 - 0.05) { const f = prog(t, tEs, tUnd1 - tEs); pos = orbit(0.8 + f * 0.25, lerp(62, 55, f), 5); fov = FV(40); }
  else if (t < tDu - 0.05) { const f = prog(t, tUnd1, tDu - tUnd1); DISK.visible = DISKF.visible = false; HALO.material.opacity = 0; ringB = 0.25; PTS.material.opacity = t > tDenn ? cl((t - tDenn) * 2) * 0.9 : 0; fall(t, 1.6, 50, 0.6); pos = orbit(-0.2 + f * 0.2, lerp(48, 40, f), 3); fov = FV(40); }
  else if (t < tDieses - 0.05) { const f = prog(t, tDu, tDieses - tDu); const k = K.eio(cl((t - W("leuchtenden") + 0.4) / 2)); DM.uniforms.bright.value = DMF.uniforms.bright.value = k; HALO.material.opacity = 0.35 * k; ringB = lerp(0.25, 1, k); pos = orbit(f * 0.3, 46, lerp(3, 6, f)); fov = FV(40); }
  else if (t < tJetzt - 0.05) { const f = prog(t, tDieses, tJetzt - tDieses); pos = orbit(0.4 + f * 0.5, lerp(38, 32, f), lerp(9, 4, f)); fov = FV(40); E.look([1.0, 0.98, 0.95], [0, 0, 0], 0.35, 0.86); }
  else if (t < tUndD - 0.05) { const f = prog(t, tJetzt, tUndD - tJetzt); const k = f * f; pos = orbit(0.9 + f * 0.1, lerp(140, 45, k), lerp(14, 4, k)); fov = FV(lerp(40, 46, k)); A.visible = f < 0.35; A.position.copy(orbit(0.9, lerp(120, 100, f), 12)); }
  else if (t < tEtwas - 0.05) { const f = prog(t, tUndD, tEtwas - tUndD); const k = K.eio(cl((t - tDieS + 1) / 3)); DM.uniforms.bright.value = DMF.uniforms.bright.value = lerp(1, 0.35, k); HALO.material.opacity = 0.1; NEB.forEach((n) => (n.material.opacity = 0.8)); CS.material.opacity = 1; pos = orbit(0.95 + f * 0.15, lerp(42, 30, f), lerp(3, 1.5, f)); fov = FV(44); L = lerp(0.45, 1.25, K.eio(f)); }
  else if (t < tJetzt2 - 0.05) { const f = prog(t, tEtwas, tJetzt2 - tEtwas); const k = cl((t - tHier) / 1.2); PR.material.opacity = 0.9 * k; PR.rotation.x = Math.PI / 2; DM.uniforms.bright.value = DMF.uniforms.bright.value = 0.18; HALO.material.opacity = 0.08;
    const aA = 0.6; A.visible = true; A.scale.setScalar(1.2); A.position.set(Math.sin(aA) * HR * 1.5, 0, Math.cos(aA) * HR * 1.5); A.rotation.set(0, aA - Math.PI / 2, 0); pose(A, t, 0.5);
    if (t > tWenn) { const g = ((t - tWenn) / 2.4) % 1; for (let i = 0; i < trail.length; i++) { const gg = g - i * 0.012; const ph = aA + 0.2 + gg * 6.283; trail[i].position.set(Math.sin(ph) * HR * 1.5, 0.6, Math.cos(ph) * HR * 1.5); trail[i].material.opacity = gg > 0 ? 0.9 * (1 - i / trail.length) : 0; } PD.position.copy(trail[0].position); PD.material.opacity = 1; }
    pos = orbit(aA + 0.15 + f * 0.25, lerp(30, 22, f), lerp(14, 10, f)); look = V(0, 0, 0); fov = FV(40); L = 0.3; ringB = 0.5; }
  else if (t < tFuerD - 0.05) { const f = prog(t, tJetzt2, tFuerD - tJetzt2); SHIP.visible = true; SHIP.scale.setScalar(0.16); SHIP.position.set(LAND ? -17.5 : -16.2, LAND ? 4.4 : 3.9, 92.1); SHIP.rotation.set(0.1, 0.9 + t * 0.01, 0.15); shipO.position.copy(SHIP.position).add(V(0, 1.2, 0));
    const ff = cl((t - tFuer) / (tEr - tFuer)); const r = lerp(40, HR * 1.12, 1 - Math.pow(1 - ff, 3)); A.visible = true; A.scale.setScalar(1.6); A.position.set(r * 0.25, r * 0.1, r * 0.95); A.rotation.set(0.3, 0.5, 0.3 + t * 0.05); pose(A, t * lerp(1, 0.05, ff)); aO.position.copy(A.position);
    tintA(A, cl((t - tDein + 0.3) / 2), 1 - cl((t - W("verblassen") + 0.3) / 2) * 0.97); pos = V(lerp(-17, -16, f), lerp(6.5, 6, f), lerp(104, 102, f)); look = V(-2, 0, 0); fov = FV(34); }
  else if (t < tUndW - 0.05) { const f = prog(t, tFuerD, tUndW - tFuerD); HZ.material.opacity = t > tDiese - 0.4 ? 0.22 * cl((t - tDiese + 0.4) * 2) : 0; HZ.rotation.y = t * 0.05; hzO.position.set(0, HR * 0.2, 0);
    const k = K.eio(cl((t - tFuerD) / (tAber - tFuerD + 0.5))); const z = lerp(12, 0, k); A.visible = z > 0.6; A.scale.setScalar(lerp(1, 0.5, k)); A.position.set(0.3, 0.5, z); A.rotation.set(0.3, Math.PI * 0.85, 0.2); pose(A, t);
    DM.uniforms.bright.value = DMF.uniforms.bright.value = 0.45; HALO.material.opacity = 0.12; pos = V(lerp(4, 2, f), lerp(3, 2.2, f), lerp(26, 22, f)); look = V(0, 0, 0); fov = FV(44); L = 1; }
  else if (t < tDrinnen - 0.05) { scene = sv; L = 0; fr = false; const small = t < tDoch - 0.05; A2.visible = true; SMALL.ring.quaternion.copy(cam.quaternion); BIG.ring.quaternion.copy(cam.quaternion); smO.position.copy(SMALL.g.position); bgO.position.copy(BIG.g.position);
    if (small) { const f = prog(t, tUndW, tDoch - tUndW); const st = K.eio(cl((t - tBei) / 3.2)); A2.position.set(-22, 4 + st * 2, 0); A2.scale.set(lerp(1, 0.3, st), lerp(1, 4, st), lerp(1, 0.3, st)); A2.rotation.set(0, 0.4 + t * 0.1, 0); pose(A2, t); svL.position.set(-22, 0, 3); pos = V(-22 + lerp(-3, 3, f), lerp(5, 6, f), lerp(16, 26, st)); look = V(-22, lerp(3.5, 4 + st * 2 - 1, st), 0); fov = FV(40); }
    else { const f = prog(t, tDoch, tDrinnen - tDoch); A2.position.set(30, 8, -10); A2.scale.setScalar(1.3); A2.rotation.set(0.2, 0.6 + t * 0.1, 0.1); pose(A2, t); svL.position.set(32, 9, -6); pos = V(lerp(35, 33, f), 12, lerp(7, 5, f)); look = V(30, 5, -16); fov = FV(44); } }
  else if (t < tBeiS - 0.05) { scene = si; L = 0; fr = false; const f = prog(t, tDrinnen, tBeiS - tDrinnen); TUN.position.z = (t * 40) % 60; A3.visible = false; A3.position.set(0, -1.2, -9); A3.rotation.set(-1.1, Math.PI, t * 0.08); pose(A3, t); pos = V(Math.sin(t * 0.2) * 3, 4 + Math.cos(t * 0.15) * 2, 0); look = V(0, 0, -200); fov = FV(60); OUT.position.set(0, 0, 300); }
  else if (t < tJetzt3 - 0.05) { scene = sv; L = 0; fr = false; const f = prog(t, tBeiS, tJetzt3 - tBeiS); SMALL.ring.quaternion.copy(cam.quaternion); BIG.ring.quaternion.copy(cam.quaternion); smO.position.copy(SMALL.g.position); bgO.position.copy(BIG.g.position); pos = V(lerp(-30, 6, K.eio(f)), lerp(10, 30, f), lerp(40, 190, K.eio(f))); look = V(lerp(-22, 8, K.eio(f)), 0, lerp(0, -25, f)); fov = FV(44); }
  else if (t < tUndG - 0.05) { scene = si; L = 0; fr = false; const f = prog(t, tJetzt3, tUndG - tJetzt3); TUN.position.z = (t * lerp(40, 160, f)) % 60; const st = K.eio(cl((t - W("gestreckt") + 0.3) / 4)); A3.visible = t < tHierW; A3.position.set(0, 0, -12 - f * 30); A3.scale.set(lerp(1, 0.3, st), lerp(1, 6, st), lerp(1, 0.3, st)); A3.rotation.set(Math.PI / 2, 0, t * 0.1); pose(A3, t);
    SING.scale.setScalar(lerp(30, 140, f)); const fl = t > tHierW ? Math.max(0, 1 - (t - tHierW) * 1.6) : 0; E.grade.uniforms.flash.value = fl * 0.9; if (t > tDieP) { E.look([1, 1, 1], [0, 0, 0], 0.5, 0.82); E.grade.uniforms.seed.value = Math.floor(t * 30); TUN.material.opacity = 0.8 * (0.5 + 0.5 * Math.sin(t * 40)); } else TUN.material.opacity = 0.8; pos = V(0, 3, 0); look = V(0, 0, -300); fov = FV(lerp(60, 80, f)); }
  else if (t < tWird1 - 0.05) { const f = prog(t, tUndG, tWird1 - tUndG); TUN.material.opacity = 0.8; PTS.material.opacity = 0.8; fall(t, 1.4, 70, 0.4); pos = orbit(-0.4 + f * 0.4, lerp(90, 60, f), lerp(12, 7, f)); fov = FV(40); }
  else if (t < tWird2 - 0.05) { const f = prog(t, tWird1, tWird2 - tWird1); PTS.material.opacity = 0.9 * (1 - f); fall(t, 4, 30, 0.4); pos = orbit(0.1 + f * 0.2, 34, 6); fov = FV(40); }
  else if (t < tOder - 0.05) { const f = prog(t, tWird2, tOder - tWird2); INF.material.opacity = 0.9 * cl(f * 3); INF.rotation.y = t * 0.1; CORE.visible = true; HALO.material.opacity = 0; L = 0; fr = false; DISK.visible = false; pos = orbit(0.4 + f * 0.3, 15, 4); fov = FV(40); }
  else if (t < tManche - 0.05) { scene = sw; L = 0; fr = false; const f = prog(t, tOder, tManche - tOder); RINGS.forEach((r, i) => { r.rotation.z = t * 0.2 + i * 0.1; r.position.x = Math.sin(i * 0.15 + t * 0.4) * 4; r.position.y = Math.cos(i * 0.12 + t * 0.3) * 4; }); pos = V(0, 0, lerp(20, -700, K.eio(f))); look = V(0, 0, pos.z - 100); WEND.material.opacity = 1; fov = FV(60); E.grade.uniforms.flash.value = cl((f - 0.85) / 0.15) * 0.9; }
  else if (t < tViel - 0.05) { E.look([1, 1, 1], [0, 0, 0], 0.25, 0.9); scene = su; L = 0; fr = false; const f = prog(t, tManche, tViel - tManche); const k = K.eout(f); BANG.material.opacity = Math.max(0, 1 - f * 2.5); BANG.scale.setScalar(lerp(100, 900, f)); E.grade.uniforms.flash.value = Math.max(0, 0.9 - f * 4);
    GALS.forEach((G) => { G.position.copy(G.userData.dir).multiplyScalar(lerp(0.02, 1, k)); G.userData.m.opacity = 0.4 * cl(f * 3); G.rotation.y += 0; }); pos = V(0, 80, lerp(500, 900, f)); look = V(0, 0, 0); fov = FV(50); }
  else if (t < tWasG - 0.05) { E.look([1, 1, 1], [0, 0, 0], 0.25, 0.9); scene = su; L = 0; fr = false; const f = prog(t, tViel, tWasG - tViel); GALS.forEach((G) => { G.position.copy(G.userData.dir); G.userData.m.opacity = 0.4; }); BUB.material.uniforms.op.value = cl(f * 2) * 1.2; const d = lerpLog(900, 4200, K.eio(f)); pos = V(d * 0.2, d * 0.25, d); look = V(0, 0, 0); fov = FV(50); }
  else { const f = prog(t, tWasG, END - tWasG); pos = orbit(-0.2 + f * 0.35, lerp(75, 60, f), lerp(8, 5, f)); look = V(0, LAND ? 0 : -3, 0); fov = FV(40); }
  cam.aspect = FMT.W / FMT.H; cam.fov = fov; cam.near = 0.05; cam.far = 90000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look); cam.updateMatrixWorld(true);
  fL.intensity = 60 * DM.uniforms.bright.value; diskL.intensity = 260 * DM.uniforms.bright.value * (DISK.visible ? 1 : 0.1);
  if (scene === sc && L > 0) { lensOn(L, ringB); } else lens.uniforms.on.value = 0;
  if (scene === sc) { HG.updateMatrixWorld(true); DISKF.matrix.copy(DISK.matrixWorld); const dir = cam.position.clone().sub(HG.position).setY(0).normalize(); clipP.setFromNormalAndCoplanarPoint(dir, V(0, 0, 0)); DISKF.visible = fr && DISK.visible; front.scene = fsc; } else { front.scene = emptyS; }
  if (scene === sc) { DISK.visible = DISK.visible && true; }
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("vier", 34) - 0.1, tUnd1 - 0.1, "⚫ 4 Mio. × Sonne"); seg(W("millionen", 54) - 0.1, tJetzt - 0.1, "🔥 Millionen Grad heiß");
  seg(tAber - 0.1, tUndW - 0.1, "🚫 kein Zurück"); seg(W("spaghettifizierung") - 0.2, tDoch - 0.1, "🍝 Spaghettifizierung");
  seg(W("höchstens") - 0.2, tBeiM - 0.1, "⏱️ ca. 1 Minute"); seg(W("wären", 178) - 0.2, tJetzt3 - 0.1, "⏱️ bis zu 1 Tag");
  seg(W("neues", 210) - 0.1, tViel - 0.1, "🌌 ein neues Universum?");
  WORDEL.style.top = !LAND && t >= KARTE && t < KARTE + 8.6 ? "300px" : "";
  word(wh, wa); cap(t);
};
