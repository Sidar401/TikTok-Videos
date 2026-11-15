// Longform: Größenvergleich des Universums – läuft in 16:9 und 9:16 (Kamera passt sich an)
const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const ASP = window.FMT.W / window.FMT.H, LAND = ASP > 1, TAN = Math.tan((20 * Math.PI) / 180);
const TAG = document.querySelector("#tag span");
// Kamera so weit weg, dass Breite w und Höhe h ins Bild passen
const fitD = (w, h) => Math.max(h / 2 / TAN, w / 2 / (TAN * ASP)) * (LAND ? 1.18 : 1.12);
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
// Kamerafahrt aus Stationen [zeit, mitteX, breite, höhe]
const track = (keys, t, dur = 1.6) => { let i = 0; while (i < keys.length - 1 && t >= keys[i + 1][0]) i++; const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
  const f = i < keys.length - 1 ? K.eio(cl((t - b[0] + dur) / dur)) : 0; const da = fitD(a[2], a[3]), db = fitD(b[2], b[3]); return { x: lerp(a[1], b[1], f), d: lerpLog(da, db, f), y: lerp(a[4] ?? 0, b[4] ?? 0, f) }; };
const ball = async (sc, f, r, x, opt = {}) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshStandardMaterial({ map: await tex(f), roughness: 1, ...opt })); m.position.set(x, 0, 0); sc.add(m); return m; };
const starBall = async (sc, r, x, col, glow) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(...col), toneMapped: false })); m.position.set(x, 0, 0); sc.add(m);
  K.sprite(sc, K.glowTex(glow), r * 3.2, V(x, 0, -r * 0.2), 0.55); return m; };
const ring = (sc, r, col, op = 0.8, th = 0.008) => { const l = new THREE.Mesh(new THREE.TorusGeometry(r, r * th, 8, 256), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, depthTest: false, toneMapped: false }));
  l.renderOrder = 10; l.userData.op = op; sc.add(l); return l; };
const sunT = await tex("sun.jpg");
const diskMat = () => new THREE.ShaderMaterial({ uniforms: { time: { value: 0 } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec2 vP;void main(){vP=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float time;varying vec2 vP;void main(){float r=length(vP);float a=atan(vP.y,vP.x);float k=(r-1.2)/2.4;
    float sw=.55+.45*sin(a*7.-r*5.+time*2.2)*sin(a*3.+r*2.-time*1.3);vec3 c=mix(vec3(1.,.95,.85),vec3(1.,.5,.15),smoothstep(0.,.45,k));c=mix(c,vec3(.6,.1,.04),smoothstep(.45,1.,k));
    float al=(1.-smoothstep(.0,1.,k))*(.55+.45*sw)*smoothstep(0.,.04,k);gl_FragColor=vec4(c*al*1.4,al);}` });
const blackHole = (sc, r, x) => { const g = new THREE.Group(); g.position.set(x, 0, 0); g.add(new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshBasicMaterial({ color: 0 })));
  const dm = diskMat(); const disk = new THREE.Mesh(new THREE.RingGeometry(1.2, 3.6, 200, 4), dm); disk.rotation.x = -1.25; g.add(disk); K.sprite(g, K.glowTex("rgba(255,190,120,.35)"), 4, V(0, 0, 0), 0.25); g.scale.setScalar(r); sc.add(g); return { g, dm, disk }; };

// ================= Szene 1: Planeten + Sonne (1 Einheit = 1000 km) =================
const S1 = new THREE.Scene(); K.stars(S1, 6000, -1, 4e6, 1.6).material.opacity = 0.45;
const L1 = new THREE.DirectionalLight(0xfff6ea, 3.2); L1.position.set(1, 0.35, 0.9); S1.add(L1); S1.add(new THREE.AmbientLight(0x2a2e3a, 0.5));
const R = { mo: 1.737, me: 2.44, ma: 3.39, ve: 6.05, er: 6.37, ur: 25.36, ne: 24.62, sa: 58.2, ju: 69.9, so: 696 };
const order = ["mo", "me", "ma", "ve", "er", "ur", "ne", "sa", "ju", "so"]; const X = {}; let px = 0, pr = 0;
order.forEach((k, i) => { const r = R[k]; X[k] = i ? px + pr + 0.45 * Math.max(pr, r) + (k === "so" ? 120 : k === "sa" ? 75 : 0) + (k === "ju" ? 70 : 0) + r : 0; px = X[k]; pr = r; });
const B = {}; B.mo = await ball(S1, "moon.jpg", R.mo, X.mo); B.me = await ball(S1, "mercury.jpg", R.me, X.me); B.ma = await ball(S1, "mars.jpg", R.ma, X.ma); B.ve = await ball(S1, "venus_atmosphere.jpg", R.ve, X.ve);
const EA = K.earth(S1, { day, night, topo }, R.er); EA.group.position.set(X.er, 0, 0); EA.U.sun.value.set(1, 0.35, 0.9).normalize(); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); B.er = EA.group;
B.ur = await ball(S1, "uranus.jpg", R.ur, X.ur); B.ne = await ball(S1, "neptune.jpg", R.ne, X.ne); B.sa = await ball(S1, "saturn.jpg", R.sa, X.sa); B.ju = await ball(S1, "jupiter.jpg", R.ju, X.ju);
B.ur.rotation.z = 1.7; B.sa.rotation.z = 0.47;
{ const rt = await tex("saturn_ring.png"); const rg = new THREE.RingGeometry(R.sa * 1.24, R.sa * 2.35, 256, 1); const uv = rg.attributes.uv, pp = rg.attributes.position;
  for (let i = 0; i < pp.count; i++) { const l = Math.hypot(pp.getX(i), pp.getY(i)); uv.setXY(i, (l - R.sa * 1.24) / (R.sa * 1.11), 0.5); }
  const rm = new THREE.Mesh(rg, new THREE.MeshStandardMaterial({ map: rt, transparent: true, side: THREE.DoubleSide, roughness: 1, depthWrite: false })); rm.rotation.x = -Math.PI / 2 + 0.47; rm.position.copy(B.sa.position); S1.add(rm); }
B.so = new THREE.Mesh(new THREE.SphereGeometry(R.so, 160, 120), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(1.3, 1.0, 0.72), toneMapped: false })); B.so.position.set(X.so, 0, 0); S1.add(B.so);
K.sprite(S1, K.glowTex("rgba(255,160,60,.5)"), R.so * 3.2, V(X.so, 0, -100), 0.7);
const NAME = { mo: "Mond", me: "Merkur", ma: "Mars", ve: "Venus", er: "Erde", ur: "Uranus", ne: "Neptun", sa: "Saturn", ju: "Jupiter", so: "Sonne" };
const span = (a, b) => [(X[a] - R[a] + X[b] + R[b]) / 2, X[b] + R[b] - (X[a] - R[a]), 2 * Math.max(...order.slice(order.indexOf(a), order.indexOf(b) + 1).map((k) => R[k] * (k === "sa" ? 1.2 : 1)))];
const sp = (t, a, b, w = 1.0) => { const [c, wd, h] = span(a, b); return [t, c, wd * w, h * 1.35]; };

// ================= Szene 2: Sterne (1 Einheit = 1 Sonnenradius) =================
const S2 = new THREE.Scene(); K.stars(S2, 6000, -1, 4e6, 1.6).material.opacity = 0.45;
const SR = { so: 1, si: 1.71, ar: 25, ri: 79, be: 750, st: 2150 }; const SO = ["so", "si", "ar", "ri", "be", "st"]; const SX = {}; px = 0; pr = 0;
SO.forEach((k, i) => { const r = SR[k]; SX[k] = i ? px + pr + 0.35 * Math.max(pr, r) + r : 0; px = SX[k]; pr = r; });
const ST = {}; ST.so = await starBall(S2, 1, SX.so, [1.3, 1.0, 0.72], "rgba(255,170,70,.55)"); ST.si = await starBall(S2, SR.si, SX.si, [0.85, 1.0, 1.35], "rgba(170,200,255,.55)");
ST.ar = await starBall(S2, SR.ar, SX.ar, [1.35, 0.8, 0.45], "rgba(255,150,70,.5)"); ST.ri = await starBall(S2, SR.ri, SX.ri, [0.8, 0.95, 1.4], "rgba(150,190,255,.5)");
ST.be = await starBall(S2, SR.be, SX.be, [1.35, 0.55, 0.3], "rgba(255,90,40,.5)"); ST.st = await starBall(S2, SR.st, SX.st, [1.25, 0.42, 0.25], "rgba(255,70,30,.5)");
const marsOrbit = ring(S2, 1.52 * 215, 0xffffff, 0.95, 0.018); marsOrbit.position.set(SX.be, 0, SR.be * 1.02); const earthOrbit = ring(S2, 215, 0x7fd0ff, 0.95, 0.018); earthOrbit.position.set(SX.be, 0, SR.be * 1.02);
const satOrbit = ring(S2, 9.54 * 215, 0xffd23f, 0.95, 0.008); satOrbit.position.set(SX.st, 0, SR.st * 1.02);
const photon = K.sprite(S2, K.glowTex("rgba(255,255,255,1)"), 220, V(0, 0, 0), 0);
const SNAME = { so: "Sonne", si: "Sirius", ar: "Arktur", ri: "Rigel", be: "Beteigeuze", st: "Stephenson 2-18" };
const sspan = (a, b) => [(SX[a] - SR[a] + SX[b] + SR[b]) / 2, SX[b] + SR[b] - (SX[a] - SR[a]), 2 * SR[b]];
const ssp = (t, a, b) => { const [c, wd, h] = sspan(a, b); return [t, c, wd, h * 1.7]; };

// ================= Szene 3: Schwarze Löcher (1 Einheit = 1 Sonnenradius) =================
const S3 = new THREE.Scene(); K.stars(S3, 6000, -1, 6e7, 1.6).material.opacity = 0.4;
const sun3 = await starBall(S3, 1, -32, [1.3, 1.0, 0.72], "rgba(255,170,70,.55)");
const SGR = blackHole(S3, 17, 0); const TONR = 170000, TONX = 17 * 4 + 40000 + TONR; const TON = blackHole(S3, TONR, TONX);
const plutos = []; for (let i = 0; i < 20; i++) { const r = ring(S3, 8490, 0x7fd0ff, 1.0, 0.03); r.position.set(TONX - TONR + 8490 + i * 16980, 0, TONR * 1.15); plutos.push(r); }

// ================= Szene 4: Galaxien (1 Einheit = 1000 Lichtjahre) =================
const S4 = new THREE.Scene(); K.stars(S4, 4000, -1, 9e4, 1.4).material.opacity = 0.3;
const galaxy = (sc, R0, n, col, seed, x, tilt) => { K.reseed(seed); const p = [], c = []; const c1 = new THREE.Color(col[0]), c2 = new THREE.Color(col[1]);
  for (let i = 0; i < n; i++) { const core = K.rnd() < 0.18; let r, a, y;
    if (core) { r = Math.pow(K.rnd(), 2) * R0 * 0.18; a = K.rnd() * 6.283; y = (K.rnd() - 0.5) * R0 * 0.08; } else { const arm = i % 4; r = Math.pow(K.rnd(), 0.7) * R0; a = arm * Math.PI / 2 + Math.log(r / R0 * 12 + 1) * 2.1 + (K.rnd() - 0.5) * 0.6; y = (K.rnd() - 0.5) * R0 * 0.02; }
    p.push(Math.cos(a) * r, y, Math.sin(a) * r); const m = core ? c1 : c1.clone().lerp(c2, Math.min(1, r / R0 + 0.2)); c.push(m.r, m.g, m.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  const pts = new THREE.Points(g, new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false }));
  const grp = new THREE.Group(); grp.add(pts); K.sprite(grp, K.glowTex("rgba(255,230,190,.6)"), R0 * 0.3, V(0, 0, 0), 0.22); grp.position.set(x, 0, 0); grp.rotation.x = tilt; sc.add(grp); return grp; };
const MW = galaxy(S4, 50, 60000, ["#ffe9c4", "#9fbcff"], 21, 0, 0.0); const AND = galaxy(S4, 76, 70000, ["#ffe2bd", "#a8c4ff"], 33, 2500, 0.9);
const sunDot = K.sprite(MW, K.glowTex("rgba(255,230,120,1)"), 2.2, V(26, 0, 0), 1); const sunPath = new THREE.Mesh(new THREE.RingGeometry(25.8, 26.2, 256), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false })); sunPath.rotation.x = -Math.PI / 2; MW.add(sunPath);

// ================= Szene 5: Kosmisches Netz (1 Einheit = 1 Mio. Lichtjahre) =================
const S5 = new THREE.Scene();
const web = (R0, n, seed, col) => { K.reseed(seed); const nodes = []; for (let i = 0; i < 90; i++) { const v = V(K.rnd() - 0.5, K.rnd() - 0.5, K.rnd() - 0.5).normalize().multiplyScalar(Math.cbrt(K.rnd()) * R0); nodes.push(v); }
  const p = []; for (let i = 0; i < n; i++) { const a = nodes[Math.floor(K.rnd() * nodes.length)]; let best = null, bd = 1e30; for (let k = 0; k < 6; k++) { const b = nodes[Math.floor(K.rnd() * nodes.length)]; const d = a.distanceTo(b); if (b !== a && d < bd) { bd = d; best = b; } }
    const f = K.rnd(), s = R0 * 0.025 * (K.rnd() + K.rnd() - 1); const q = K.rnd() < 0.3 ? a.clone().add(V(K.rnd() - 0.5, K.rnd() - 0.5, K.rnd() - 0.5).multiplyScalar(R0 * 0.06)) : a.clone().lerp(best, f).add(V(s, s * 0.7, -s)); p.push(q.x, q.y, q.z); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
  const pts = new THREE.Points(g, new THREE.PointsMaterial({ color: col, size: 1.5, sizeAttenuation: false, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false })); S5.add(pts); return pts; };
const webS = web(400, 60000, 5, 0xb9c8ff), webL = web(46500, 90000, 9, 0xc8b8ff);
const lanSphere = ring(S5, 260, 0xffd23f, 0.9, 0.006);
const obsSphere = new THREE.Mesh(new THREE.SphereGeometry(46500, 64, 48), new THREE.MeshBasicMaterial({ color: 0x7fd0ff, transparent: true, opacity: 0, depthWrite: false, side: THREE.BackSide, blending: THREE.AdditiveBlending })); S5.add(obsSphere);
const lg1 = K.sprite(S5, K.glowTex("rgba(255,230,190,1)"), 0.25, V(0, 0, 0), 1), lg2 = K.sprite(S5, K.glowTex("rgba(255,230,190,1)"), 0.3, V(2.5, 0, 0), 1);
const here = new THREE.Object3D(); S5.add(here);

// ================= Zeiten =================
const t = {}; Object.entries({ mond: ["das", 16], vier: ["fast", 21], merkur: ["merkur"], mars: ["mars", 33], venus: ["venus", 36], erde: ["und", 40.8], cta: ["übrigens"], uranus: ["uranus"], saturn: ["saturn", 62], jupiter: ["und", 73], sonne: ["aber", 85], stern: ["und", 102.8], sirius: ["sirius"], arktur: ["arktur"], rigel: ["rigel"], bet: ["und", 116.9], setzt: ["setzt"], irgend: ["irgendwann", 128], einer: ["einer", 133], licht9: ["licht", 141], schwarz: ["aber", 145.9], herz: ["im", 150.9], dunkel: ["sein", 159.9], ton: ["und", 163.8], ton2: ["sein", 173], mw: ["unsere", 180.5], mwb: ["die", 185], runde: ["und", 192.4], andro: ["unsere", 198.9], stoss: ["vielleicht", 205], gruppen: ["galaxien", 208.7], lan: ["unser", 213], sicht: ["und", 222], teil: ["und", 231], punkt: ["und", 237.5], frage: ["was", 243.5], abo: ["und", 247] }).forEach(([k, [w, ab]]) => (t[k] = W(w, ab ?? 0)));

// Kamerastationen
const K1 = [[0, X.er, 40, 30], [5.6, X.mo, 9, 9], [8.0, (X.mo + X.so + R.so) / 2, X.so + R.so + 10, 2 * R.so * 1.1], [t.mond - 1.2, X.mo, 9, 9], sp(t.vier, "mo", "er"), sp(t.merkur, "mo", "me"), sp(t.mars, "mo", "ma"), sp(t.venus, "mo", "ve"), sp(t.erde, "mo", "er"), [t.erde + 3.5, X.er, 26, 22], sp(t.cta, "mo", "er"), sp(t.uranus, "er", "ne"), sp(t.saturn, "er", "sa"), sp(t.jupiter, "er", "ju"), sp(t.sonne, "er", "so"), [t.stern - 0.01, X.so - 300, 2400, 1700]];
const K2 = [[t.stern, SX.so, 7, 5], ssp(t.sirius, "so", "si"), ssp(t.arktur, "so", "ar"), ssp(t.rigel, "so", "ri"), ssp(t.bet, "so", "be"), [t.setzt, SX.be, 1900, 2000], [t.irgend, SX.be, 2100, 2300], ssp(t.einer, "so", "st"), [t.einer + 4.2, SX.st, 5200, 5600]];
const K3 = [[t.schwarz, 0, 160, 100], [t.herz, -10, 150, 170], [t.ton + 1.2, TONX * 0.55, TONX + TONR * 1.1, 2 * TONR * 1.6], [t.ton2, TONX, 2 * TONR * 1.15, 2 * TONR * 1.6]];
// Beschriftungen
const lab = (n, o, r, a, b, size, gap) => label(n, o, r, { t0: a, t1: b, size: size ?? (LAND ? 52 : 58), gap: gap ?? 26 });
const S1L = [["mo", t.mond, t.uranus], ["me", t.merkur, t.uranus], ["ma", t.mars, t.uranus], ["ve", t.venus, t.uranus], ["er", t.erde, t.stern], ["ur", t.uranus, t.sonne], ["ne", t.uranus + 0.6, t.sonne], ["sa", t.saturn, t.sonne], ["ju", t.jupiter, t.stern], ["so", t.sonne, t.stern]];
S1L.forEach(([k, a, b]) => lab(NAME[k], B[k], R[k] * (k === "sa" ? 1.3 : 1), a, b));
[["so", t.stern, t.schwarz], ["si", t.sirius, t.schwarz], ["ar", t.arktur, t.schwarz], ["ri", t.rigel, t.schwarz], ["be", t.bet, t.schwarz], ["st", t.einer, t.schwarz]].forEach(([k, a, b]) => lab(SNAME[k], ST[k], SR[k], a, b));
lab("Sonne", sun3, 1, t.herz + 1, t.ton + 1); lab("Sagittarius A*", SGR.g, 17 * 3, t.herz + 3, t.ton + 1); lab("TON 618", TON.g, TONR * 1.2, t.ton + 1.5, t.mw);
lab("Milchstraße", MW, 30, t.mw + 0.5, t.mw + 4.5); lab("Sonne ☀️", sunDot, 1, t.mwb, t.andro); lab("Milchstraße", MW, 50, t.andro + 0.8, t.gruppen); lab("Andromeda", AND, 60, t.andro + 1.2, t.gruppen);
lab("Lokale Gruppe", lg1, 3, t.gruppen + 0.2, t.gruppen + 1.6); lab("Laniakea", lanSphere, 260, t.lan + 0.4, t.sicht); lab("Du bist hier 🫵", here, 0, t.punkt + 0.6, t.frage + 0.5, LAND ? 60 : 66, 40);
// Kapitel oben
const CH = [[0, ""], [t.mond, "1 · UNSERE NACHBARSCHAFT"], [t.uranus, "2 · DIE RIESEN"], [t.sonne, "3 · DIE STERNE"], [t.schwarz, "4 · SCHWARZE LÖCHER"], [t.mw, "5 · GALAXIEN"], [t.gruppen, "6 · DAS UNIVERSUM"], [t.punkt, ""]];

renderAt = (tt) => {
  E.grade.uniforms.flash.value = 0; let ch = ""; CH.forEach(([a, s]) => { if (tt >= a) ch = s; }); if (TAG.textContent !== ch) TAG.textContent = ch;
  let scene, pos, look; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.88);
  if (tt < t.stern) { scene = S1; const c = track(K1, tt); pos = V(c.x + c.d * 0.04, c.d * 0.07, c.d); look = V(c.x, 0, 0);
    Object.values(B).forEach((m, i) => { if (m !== B.er) m.rotation.y = tt * (0.05 + i * 0.004); }); EA.mesh.rotation.y = tt * 0.06; EA.clouds.rotation.y = tt * 0.07; }
  else if (tt < t.schwarz) { scene = S2; const c = track(K2, tt); pos = V(c.x, c.d * 0.05, c.d); look = V(c.x, 0, 0); E.look([1, 1, 1], [0, 0, 0], 0.4, 0.85);
    Object.values(ST).forEach((m, i) => (m.rotation.y = tt * 0.02 * (i + 1)));
    const fo = (l, a, b) => (l.material.opacity = l.userData.op * cl((tt - a) / 0.6) * (1 - cl((tt - b) / 0.5)));
    fo(earthOrbit, t.setzt + 0.6, t.irgend); fo(marsOrbit, t.setzt + 1.6, t.irgend); fo(satOrbit, t.einer + 4.6, t.schwarz - 0.6);
    if (tt > t.irgend + 1.0 && tt < t.einer) ST.be.material.color.setRGB(1.35 + 0.35 * Math.max(0, Math.sin(tt * 9)), 0.55 + 0.2 * Math.max(0, Math.sin(tt * 9)), 0.3); else ST.be.material.color.setRGB(1.35, 0.55, 0.3);
    if (tt > t.licht9 && tt < t.schwarz - 0.4) { const f = prog(tt, t.licht9 + 0.4, 3.4); const a = f * Math.PI * 2; photon.position.set(SX.st + Math.cos(a) * SR.st * 1.03, Math.sin(a) * SR.st * 1.03, SR.st); photon.material.opacity = f > 0 && f < 1 ? 1 : 0; } else photon.material.opacity = 0; }
  else if (tt < t.mw) { scene = S3; const c = track(K3, tt, 2.6); pos = V(c.x, c.d * 0.1, c.d); look = V(c.x, 0, 0); E.look([1, 1, 1], [0, 0, 0], tt > t.ton ? 0.12 : 0.3, 0.9);
    const dark = cl((tt - t.schwarz) / 0.8) * (1 - cl((tt - t.herz + 0.6) / 0.6)); if (dark > 0) { pos = V(-200, 0, 400); look = V(-400, 0, 0); }
    TON.g.visible = tt >= t.ton; [SGR, TON].forEach((b) => { b.dm.uniforms.time.value = tt; b.disk.rotation.z = tt * 0.15; });
    plutos.forEach((p, i) => (p.material.opacity = p.userData.op * cl((tt - t.ton2 - 1.5 - i * 0.12) / 0.4))); }
  else if (tt < t.gruppen) { scene = S4; E.look([1, 1, 1], [0, 0, 0], 0.25, 0.88); MW.rotation.y = tt * 0.01; AND.rotation.y = -tt * 0.008;
    sunPath.material.opacity = 0.7 * cl((tt - t.runde) / 0.6) * (1 - cl((tt - t.andro) / 0.5));
    if (tt < t.andro) { const f = K.eio(prog(tt, t.mw, 3)); const d = lerp(LAND ? 120 : 210, LAND ? 95 : 170, f); pos = V(0, d * 0.75, d * 0.66); look = V(0, 0, 0); }
    else { const f = K.eio(prog(tt, t.andro, 2.4)); const g = prog(tt, t.stoss, 4); AND.position.x = lerp(2500, 2200, g); const cx = lerp(0, 1250, f); const d = lerp(LAND ? 110 : 190, fitD(2800, 400), f); pos = V(cx, d * 0.35, d); look = V(cx, 0, 0); } }
  else { scene = S5; E.look([1, 1, 1], [0, 0, 0], 0.4, 0.82);
    lanSphere.lookAt(cam.position); lanSphere.material.opacity = 0.9 * cl((tt - t.lan - 1.4) / 0.6) * (1 - cl((tt - t.sicht) / 0.8)); obsSphere.material.opacity = 0.06 * cl((tt - t.teil) / 0.8);
    webS.material.opacity = 0.8 * (1 - cl((tt - t.sicht - 1) / 1.5)); webL.material.opacity = 0.8 * cl((tt - t.sicht) / 1.5);
    let d; if (tt < t.lan) d = lerpLog(12, 300, K.eio(prog(tt, t.gruppen, t.lan - t.gruppen))); else if (tt < t.sicht) d = lerpLog(300, 1400, K.eio(prog(tt, t.lan, 1.6))); else if (tt < t.punkt) d = lerpLog(1100, 160000, K.eio(prog(tt, t.sicht, 4))); else d = lerpLog(160000, 0.4, K.eio(prog(tt, t.punkt, 3.2)));
    const a = 0.3 + tt * 0.01; pos = V(Math.sin(a) * d, d * 0.25, Math.cos(a) * d); look = V(0, 0, 0);
    if (tt > t.punkt + 2.6) { scene = S1; const f = K.eio(prog(tt, t.punkt + 2.6, 3)); const dd = lerpLog(2500, 26, f); pos = V(X.er + dd * 0.1, dd * 0.06, dd); look = V(X.er, 0, 0); here.position.set(0, 0, 0); } }
  if (scene === S4) { const dg = pos.distanceTo(look); [MW, AND].forEach((g) => (g.children[0].material.opacity = Math.min(0.85, 260 / Math.max(1, dg)))); }
  const dist = pos.distanceTo(look); cam.near = Math.max(0.01, dist / 400); cam.far = Math.max(dist * 1000, 2e8); cam.fov = 40; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, tt); updLabels(tt);
  // winzige Objekte: Namen ausblenden (sonst überlappen sie)
  const pxPerUnit = (o) => window.FMT.H / (2 * TAN * Math.max(1e-6, cam.position.distanceTo(o.getWorldPosition(new THREE.Vector3()))));
  labels.forEach((L) => { if (L.r > 0 && L.r * pxPerUnit(L.obj) < 22) L.d.style.opacity = 0; });
  // "Du bist hier" an der Erde festmachen
  if (scene === S1 && tt > t.punkt) { const L = labels[labels.length - 1]; const [x, y] = P(EA.group.position.clone()); L.d.style.left = x + "px"; L.d.style.top = y - 40 + "px"; }
  let wh = "", wa = 0; const seg = (a, b, h) => { if (tt >= a && tt < b) { wh = h; wa = cl((tt - a) / 0.3) * (1 - cl((tt - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("dreitausend") - 0.2, t.vier - 0.1, "≈ 3.500 km" + sub("Durchmesser")); seg(t.vier + 0.4, t.vier + 4, "4 Monde = 1 Erde"); seg(W("sein", 25) , t.merkur - 0.1, "💡 1,3 Sekunden" + sub("Licht vom Mond zu uns"));
  seg(W("halb") - 0.2, t.venus - 0.1, "½ Erde"); seg(W("genauso") - 0.2, t.erde - 0.1, "≈ Erde");
  seg(W("dreizehntausend") - 0.2, W("würdest") - 0.1, "≈ 12.700 km"); seg(W("würdest"), t.cta - 0.1, "🚗 100 km/h → 16 Tage");
  seg(W("viermal") - 0.2, t.saturn - 0.1, "4× Erde"); seg(W("neunmal") - 0.2, W("und", 64.7) - 0.1, "9× Erde"); seg(W("und", 64.7), W("und", 68.7) - 0.1, "Ringe: fast 300.000 km"); seg(W("und", 68.7), t.jupiter - 0.1, "🛁 Saturn würde schwimmen");
  seg(W("elfmal") - 0.2, W("über", 76.5) - 0.1, "11× Erde"); seg(W("über", 76.5), W("sein", 80) - 0.1, "1.300 Erden passen hinein"); seg(W("sein", 80), t.sonne - 0.1, "Großer Roter Fleck 🌀" + sub("größer als die Erde"));
  seg(W("hundertneunmal") - 0.2, W("rund", 91) - 0.1, "109× Erde"); seg(W("rund", 91), W("ihr", 95) - 0.1, "1,3 Mio. Erden"); seg(W("ihr", 95), W("und", 97.7) - 0.1, "☀️ → 🌍 8 Minuten"); seg(W("und", 97.7), t.stern - 0.1, "> 99 % der Masse" + sub("unseres Sonnensystems"));
  seg(t.stern + 0.4, t.sirius - 0.1, "ein ganz normaler Stern"); seg(W("fast", 108.6), t.arktur - 0.1, "≈ 1,7× Sonne"); seg(W("fünfundzwanzigmal") - 0.2, t.rigel - 0.1, "25× Sonne"); seg(W("rund", 115.5), t.bet - 0.1, "80× Sonne");
  seg(W("rund", 120.4), t.setzt - 0.1, "750× Sonne"); seg(t.setzt + 0.5, t.irgend - 0.1, "reicht über die Marsbahn"); seg(t.irgend, t.einer - 0.1, "💥 irgendwann Supernova");
  seg(W("nach", 137.7), t.licht9 - 0.1, "bis über die Saturnbahn"); seg(t.licht9, t.schwarz - 0.1, "Licht: 9 Std. für eine Runde");
  seg(W("es", 156.5), t.dunkel - 0.1, "4 Mio. Sonnen schwer"); seg(t.dunkel, t.ton - 0.1, "17× so breit wie die Sonne"); seg(W("nach", 169.7), t.ton2 - 0.1, "≈ 40 Mrd. Sonnen schwer"); seg(t.ton2 + 1.2, t.mw - 0.1, "20 Sonnensysteme" + sub("bis zum Pluto, nebeneinander"));
  seg(W("über", 182), t.mwb - 0.1, "> 100 Mrd. Sterne"); seg(W("hunderttausend", 186) - 0.2, t.runde - 0.1, "100.000 Lichtjahre"); seg(W("zweihundertdreißig") - 0.2, t.andro - 0.1, "1 Runde = 230 Mio. Jahre");
  seg(t.andro + 1, t.stoss - 0.1, "2,5 Mio. Lichtjahre entfernt"); seg(t.stoss, t.gruppen - 0.1, "Zusammenstoß? 💥");
  seg(t.lan + 1.2, W("er", 218.6) - 0.1, "Laniakea" + sub("„unermesslicher Himmel“")); seg(W("er", 218.6), t.sicht - 0.1, "> 500 Mio. Lichtjahre");
  seg(W("dreiundneunzig") - 0.2, W("mit", 227) - 0.1, "93 Mrd. Lichtjahre"); seg(W("mit", 227), t.teil - 0.1, "Hunderte Milliarden Galaxien"); seg(t.teil, t.punkt - 0.1, "nur der sichtbare Teil");
  seg(t.frage, t.abo - 0.1, "💬 Was hat dich überrascht?");
  word(wh, wa); cap(tt);
};
