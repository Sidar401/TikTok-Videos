// Longform: Wie groß sind Sterne wirklich? – läuft in 16:9 und 9:16 (Kamera passt sich an)
const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const ASP = window.FMT.W / window.FMT.H, LAND = ASP > 1, TAN = Math.tan((20 * Math.PI) / 180);
const TAG = document.querySelector("#tag span");
const fitD = (w, h) => Math.max(h / 2 / TAN, w / 2 / (TAN * ASP)) * (LAND ? 1.18 : 1.12);
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
const track = (keys, t, dur = 1.6) => { let i = 0; while (i < keys.length - 1 && t >= keys[i + 1][0]) i++; const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
  const f = i < keys.length - 1 ? K.eio(cl((t - b[0] + dur) / dur)) : 0; const da = fitD(a[2], a[3]), db = fitD(b[2], b[3]); return { x: lerp(a[1], b[1], f), d: lerpLog(da, db, f) }; };
const sunT = await tex("sun.jpg");
const grayT = (() => { const im = sunT.image; const c = document.createElement("canvas"); c.width = im.width; c.height = im.height; const g = c.getContext("2d"); g.drawImage(im, 0, 0); const d = g.getImageData(0, 0, c.width, c.height);
  for (let i = 0; i < d.data.length; i += 4) { const l = 0.45 * d.data[i] + 0.4 * d.data[i + 1] + 0.15 * d.data[i + 2]; const v = Math.min(255, 120 + l * 0.55); d.data[i] = d.data[i + 1] = d.data[i + 2] = v; } g.putImageData(d, 0, 0);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
const starBall = (sc, r, x, col, glow, gs = 3.2, gray = false) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshBasicMaterial({ map: gray ? grayT : sunT, color: new THREE.Color(...col), toneMapped: false })); m.position.set(x, 0, 0); sc.add(m);
  m.userData.glow = K.sprite(sc, K.glowTex(glow), r * gs, V(x, 0, -r * 0.2), 0.55); return m; };
const ball = async (sc, f, r, x) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshStandardMaterial({ map: await tex(f), roughness: 1 })); m.position.set(x, 0, 0); sc.add(m); return m; };
const ring = (sc, r, col, op = 0.8, th = 0.008) => { const l = new THREE.Mesh(new THREE.TorusGeometry(r, r * th, 8, 256), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, depthTest: false, toneMapped: false }));
  l.renderOrder = 10; l.userData.op = op; sc.add(l); return l; };
const fo = (o, tt, a, b, op = 1) => (o.material.opacity = op * cl((tt - a) / 0.6) * (1 - cl((tt - b) / 0.5)));
const glowDot = (sc, col, size) => K.sprite(sc, K.glowTex(col), size, V(0, 0, 0), 0);

// ================= Szene N: Neutronenstern (1 Einheit = 1 km) =================
const SN = new THREE.Scene(); K.stars(SN, 7000, -1, 4e5, 1.6).material.opacity = 0.55;
const nsMat = new THREE.ShaderMaterial({ uniforms: { t: { value: 0 } }, toneMapped: false,
  vertexShader: `varying vec3 vN;varying vec3 vP;void main(){vN=normalize(normalMatrix*normal);vP=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float t;varying vec3 vN;varying vec3 vP;float h(vec3 p){return fract(sin(dot(p,vec3(12.9,78.2,37.7)))*43758.5);}
    void main(){float r=pow(1.-abs(vN.z),2.);float s=.85+.15*sin(vP.x*1.7+t*3.)*sin(vP.y*2.1-t*2.);vec3 c=mix(vec3(.75,.85,1.),vec3(1.),.5)*s*1.6+vec3(.3,.5,1.)*r*1.5;gl_FragColor=vec4(c,1.);}` });
const NS = new THREE.Mesh(new THREE.SphereGeometry(10, 96, 64), nsMat); SN.add(NS); K.sprite(SN, K.glowTex("rgba(150,190,255,1)"), 60, V(0, 0, -2), 0.6);
const beamMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false, uniforms: { o: { value: 1 } },
  vertexShader: `varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float o;varying vec2 vU;void main(){float a=pow(vU.y,1.5)*o*.55;gl_FragColor=vec4(vec3(.55,.75,1.)*a,a);}` });
const beams = new THREE.Group(); SN.add(beams); for (const s of [1, -1]) { const c = new THREE.Mesh(new THREE.ConeGeometry(28, 260, 48, 1, true), beamMat); c.position.y = s * 135; if (s < 0) c.rotation.z = Math.PI; beams.add(c); } beams.rotation.z = 0.45;
// Stadt (20 km) als Leuchtkarte daneben
const cityT = (() => { const c = document.createElement("canvas"); c.width = c.height = 1024; const g = c.getContext("2d"); const gr = g.createRadialGradient(512, 512, 0, 512, 512, 512); gr.addColorStop(0, "rgba(255,200,120,.35)"); gr.addColorStop(1, "rgba(255,200,120,0)"); g.fillStyle = gr; g.fillRect(0, 0, 1024, 1024);
  K.reseed(8); g.strokeStyle = "rgba(255,210,140,.9)"; for (let i = 0; i < 70; i++) { const y = K.rnd() * 1024; g.lineWidth = K.rnd() < 0.15 ? 4 : 1.2; g.beginPath(); g.moveTo(0, y); g.lineTo(1024, y + (K.rnd() - 0.5) * 200); g.stroke(); const x = K.rnd() * 1024; g.beginPath(); g.moveTo(x, 0); g.lineTo(x + (K.rnd() - 0.5) * 200, 1024); g.stroke(); }
  for (let i = 0; i < 2500; i++) { const a = K.rnd() * 6.28, r = Math.pow(K.rnd(), 0.7) * 500; g.fillStyle = `rgba(255,${200 + K.rnd() * 55},${140 + K.rnd() * 80},${0.5 + K.rnd() * 0.5})`; g.fillRect(512 + Math.cos(a) * r, 512 + Math.sin(a) * r, 2.5, 2.5); }
  g.globalCompositeOperation = "destination-in"; const m = g.createRadialGradient(512, 512, 380, 512, 512, 512); m.addColorStop(0, "#000"); m.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = m; g.fillRect(0, 0, 1024, 1024);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
const city = new THREE.Mesh(new THREE.PlaneGeometry(22, 22), new THREE.MeshBasicMaterial({ map: cityT, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); city.position.set(34, 0, 0); SN.add(city);
const cityRing = ring(SN, 10.2, 0xffd23f, 0.9, 0.012); cityRing.position.set(34, 0, 0.2); const nsRing = ring(SN, 10.6, 0x7fd0ff, 0.9, 0.012);

// ================= Szene A: Weißer Zwerg, Erde, Jupiter, Proxima, Sonne (1 Einheit = 1000 km) =================
const SA = new THREE.Scene(); K.stars(SA, 6000, -1, 4e6, 1.6).material.opacity = 0.45;
const LA = new THREE.DirectionalLight(0xfff6ea, 3.0); LA.position.set(1, 0.35, 0.9); SA.add(LA); SA.add(new THREE.AmbientLight(0x2a2e3a, 0.5));
const RA = { wd: 5.85, er: 6.37, ju: 69.9, px: 107, so: 696 }; const OA = ["wd", "er", "ju", "px", "so"]; const XA = {}; { let px = 0, pr = 0; OA.forEach((k, i) => { const r = RA[k]; XA[k] = i ? px + pr + 0.5 * Math.max(pr, r) + (k === "so" ? 150 : 0) + r : 0; px = XA[k]; pr = r; }); }
const A = {}; A.wd = starBall(SA, RA.wd, XA.wd, [0.95, 1.05, 1.35], "rgba(200,220,255,.8)", 4, true);
const EA = K.earth(SA, { day, night, topo }, RA.er); EA.group.position.set(XA.er, 0, 0); EA.U.sun.value.set(1, 0.35, 0.9).normalize(); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); A.er = EA.group;
A.ju = await ball(SA, "jupiter.jpg", RA.ju, XA.ju); A.px = starBall(SA, RA.px, XA.px, [1.35, 0.42, 0.25], "rgba(255,80,40,.6)"); A.so = starBall(SA, RA.so, XA.so, [1.3, 1.0, 0.72], "rgba(255,160,60,.5)");
const NAMEA = { wd: "Sirius B", er: "Erde", ju: "Jupiter", px: "Proxima Centauri", so: "Sonne" };
const spanA = (a, b) => { const ks = OA.slice(OA.indexOf(a), OA.indexOf(b) + 1); return [(XA[a] - RA[a] + XA[b] + RA[b]) / 2, XA[b] + RA[b] - (XA[a] - RA[a]), 2 * Math.max(...ks.map((k) => RA[k])) * 1.6]; };
const spA = (t, a, b) => [t, ...spanA(a, b)];
const plane = glowDot(SA, "rgba(255,240,200,1)", 2.2); const planeTrail = ring(SA, 1, 0xffd23f, 0.7, 0.01);
// Rote-Zwerge-Feld (Milchstraße)
const SG = new THREE.Scene(); { K.reseed(44); const p = [], c = []; for (let i = 0; i < 70000; i++) { const core = K.rnd() < 0.15; let r, a, y; if (core) { r = Math.pow(K.rnd(), 2) * 9; a = K.rnd() * 6.283; y = (K.rnd() - 0.5) * 4; } else { const arm = i % 4; r = Math.pow(K.rnd(), 0.7) * 50; a = arm * Math.PI / 2 + Math.log(r / 50 * 12 + 1) * 2.1 + (K.rnd() - 0.5) * 0.6; y = (K.rnd() - 0.5) * 1; }
    p.push(Math.cos(a) * r, y, Math.sin(a) * r); const red = K.rnd() < 0.75; const col = red ? new THREE.Color(1, 0.35 + K.rnd() * 0.15, 0.25) : new THREE.Color(1, 0.92, 0.8); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3));
  SG.add(new THREE.Points(g, new THREE.PointsMaterial({ size: 1.7, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false }))); K.sprite(SG, K.glowTex("rgba(255,210,170,.6)"), 16, V(0, 0, 0), 0.3); }

// ================= Szene B: Sterne (1 Einheit = 1 Sonnenradius) =================
const SB = new THREE.Scene(); K.stars(SB, 6000, -1, 4e6, 1.6).material.opacity = 0.45;
const RB = { so: 1, si: 1.71, po: 8.8, ar: 25.4, al: 45, ri: 79, an: 700, be: 750, vy: 1420, st: 2150 }; const OB = ["so", "si", "po", "ar", "al", "ri", "an", "be", "vy", "st"]; const XB = {}; { let px = 0, pr = 0; OB.forEach((k, i) => { const r = RB[k]; XB[k] = i ? px + pr + 0.35 * Math.max(pr, r) + r : 0; px = XB[k]; pr = r; }); }
const COL = { so: [[1.3, 1.0, 0.72], "rgba(255,170,70,.55)"], si: [[0.9, 1.0, 1.35], "rgba(170,200,255,.55)"], po: [[1.35, 0.85, 0.5], "rgba(255,170,90,.5)"], ar: [[1.35, 0.78, 0.45], "rgba(255,150,70,.5)"], al: [[1.35, 0.65, 0.38], "rgba(255,120,60,.5)"],
  ri: [[0.8, 0.92, 1.4], "rgba(150,190,255,.5)"], an: [[1.35, 0.5, 0.3], "rgba(255,90,40,.5)"], be: [[1.35, 0.55, 0.3], "rgba(255,90,40,.5)"], vy: [[1.3, 0.45, 0.28], "rgba(255,80,35,.5)"], st: [[1.25, 0.42, 0.25], "rgba(255,70,30,.5)"] };
const B = {}; OB.forEach((k) => (B[k] = starBall(SB, RB[k], XB[k], COL[k][0], COL[k][1], 3.2, k === "si" || k === "ri")));
const NAMEB = { so: "Sonne", si: "Sirius", po: "Pollux", ar: "Arktur", al: "Aldebaran", ri: "Rigel", an: "Antares", be: "Beteigeuze", vy: "VY Canis Majoris", st: "Stephenson 2-18" };
const spanB = (a, b) => [(XB[a] - RB[a] + XB[b] + RB[b]) / 2, XB[b] + RB[b] - (XB[a] - RB[a]), 2 * RB[b] * 1.7];
const spB = (t, a, b) => [t, ...spanB(a, b)];
const AU = 215; const orbB = [["Merkur", 0.39, 0xb0b0b0], ["Venus", 0.72, 0xffd9a0], ["Erde", 1, 0x7fd0ff], ["Mars", 1.52, 0xff7a50]].map(([n, a, c]) => { const r = ring(SB, a * AU, c, 0.95, 0.014); r.position.set(XB.be, 0, RB.be * 1.02); return r; });
const satB = ring(SB, 9.54 * AU, 0xffd23f, 0.95, 0.008); satB.position.set(XB.st, 0, RB.st * 1.02);
const dotB = glowDot(SB, "rgba(255,255,255,1)", 240);
const shell = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshBasicMaterial({ color: 0xffd0a0, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.BackSide, toneMapped: false })); shell.position.set(XB.be, 0, 0); SB.add(shell);
const snFlash = glowDot(SB, "rgba(255,240,220,1)", 4000); snFlash.position.set(XB.be, 0, 50); const nsDot = glowDot(SB, "rgba(150,200,255,1)", 60); nsDot.position.set(XB.be, 0, 10);

// ================= Szene R: Sonne wird Roter Riese (1 Einheit = 1 Sonnenradius) =================
const SR = new THREE.Scene(); K.stars(SR, 6000, -1, 4e6, 1.6).material.opacity = 0.45;
const sunR = starBall(SR, 1, 0, [1.3, 1.0, 0.72], "rgba(255,170,70,.55)");
const plR = [["Merkur", 0.39, "rgba(200,200,200,1)"], ["Venus", 0.72, "rgba(255,220,170,1)"], ["Erde", 1, "rgba(120,200,255,1)"]].map(([n, a, c], i) => { const r = ring(SR, a * AU, 0xffffff, 0.35, 0.006); r.rotation.x = 0; const d = glowDot(SR, c, 26); const o = new THREE.Object3D(); SR.add(o); return { n, R: a * AU, r, d, o, ph: 0.6 + i * 1.9 }; });

// ================= Zeiten =================
const t = {}; Object.entries({ aber: ["aber", 2], heute: ["heute"], und: ["und", 10], wir: ["wir", 13.8], das: ["das", 15.8], er: ["er", 18], aber2: ["aber", 22], tee: ["ein", 25], dreh: ["und", 29.4], etwas: ["etwas"], sirB: ["sirius", 36.8], aber3: ["aber", 40], dann: ["dann", 42.2], prox: ["proxima"], er2: ["er", 48.5], solche: ["und", 51.7], jetzt: ["und", 56.5], hund: ["hundertneunmal"], ueber: ["über", 64.5], fl: ["würdest"], umS: ["um", 74.4], cta: ["übrigens"], si: ["sirius", 81.9], po: ["pollux"], ar: ["arktur"], al: ["aldebaran"], ri: ["rigel"], hell: ["und", 101.6], jetzt2: ["jetzt", 105.6], an: ["antares"], be: ["beteigeuze", 113], stell: ["stell"], mit: ["mit", 125], vy: ["vy"], lange: ["lange"], st: ["und", 141.8], nach: ["nach", 146.2], an2: ["an", 150.5], mit2: ["mit", 154.5], licht: ["sogar"], ueberr: ["aber", 162], sonne10: ["unsere", 166.6], riese: ["ein", 170.7], er3: ["er", 174.5], expl: ["und", 177.1], uebrig: ["bleibt", 180], sonne2: ["und", 186.4], merkur: ["merkur", 192], danach: ["danach"], zu: ["zu", 197.6], punkt: ["der", 201], abo: ["wenn", 204.5] }).forEach(([k, [w, ab]]) => (t[k] = W(w, ab ?? 0)));
const END = 210;
// Kamerastationen
const KA = [[t.etwas, XA.wd, 30, 22], [t.sirB, XA.wd, 30, 22], spA(t.sirB + 2.2, "wd", "er"), spA(t.dann, "wd", "ju"), spA(t.prox, "er", "px"), [t.er2 + 1.5, (XA.ju + XA.px) / 2, 420, 300]];
const KS = [[t.jetzt, XA.so, 1800, 2000], spA(t.hund, "er", "so"), [t.ueber, XA.so, 1800, 2000], [t.fl, XA.er, 22, 22], [t.umS, XA.so, 1800, 2050], [t.cta, XA.so, 1900, 2100]];
const KB = [[t.si, XB.so, 6, 4], spB(t.si + 0.3, "so", "si"), spB(t.po, "so", "po"), spB(t.ar, "so", "ar"), spB(t.al, "so", "al"), spB(t.ri, "so", "ri"), spB(t.an, "so", "an"), spB(t.be, "ri", "be"), [t.stell + 0.3, XB.be, 2 * 1.6 * AU, 2 * 1.6 * AU * 1.1], [t.mit, XB.be, 1900, 2000], spB(t.vy, "an", "vy"), spB(t.st, "be", "st"), [t.an2 + 0.4, XB.st, 9.54 * AU * 2.3, 9.54 * AU * 2.3]];
// Beschriftungen
const lab = (n, o, r, a, b, size, gap) => label(n, o, r, { t0: a, t1: b, size: size ?? (LAND ? 50 : 56), gap: gap ?? 24 });
const nsO = new THREE.Object3D(); nsO.position.set(0, 10, 0); SN.add(nsO); const cityO = new THREE.Object3D(); cityO.position.set(34, 11, 0); SN.add(cityO);
lab("Neutronenstern", nsO, 2, t.das + 0.6, t.etwas); lab("Stadt", cityO, 2, t.er + 2.4, t.aber2);
[["wd", t.etwas + 1, t.prox], ["er", t.sirB + 1.6, t.prox], ["ju", t.dann, t.jetzt], ["px", t.prox, t.solche]].forEach(([k, a, b]) => lab(NAMEA[k], A[k], RA[k], a, b));
lab("Sonne", A.so, RA.so, t.jetzt + 0.6, t.cta); lab("Erde", A.er, RA.er, t.hund, t.cta);
OB.forEach((k, i) => { const a = k === "so" ? t.si : t[k]; const b = k === "vy" ? t.an2 : k === "st" ? t.ueberr : OB[i + 2] ? t[OB[i + 2]] : t.ueberr; lab(NAMEB[k], B[k], RB[k], a + (k === "so" ? 0 : 0.2), b); });
const planO = plR.map((p) => p.o); plR.forEach((p) => lab(p.n, p.o, 0, t.sonne2 + 1.6, t.danach, LAND ? 40 : 44, 22));
const CH = [[0, ""], [t.wir, "1 · DIE KLEINSTEN"], [t.jetzt, "2 · UNSERE SONNE"], [t.si, "3 · DIE RIESEN"], [t.jetzt2, "4 · DIE GIGANTEN"], [t.ueberr, "5 · LEBEN UND STERBEN"], [t.abo, ""]];

renderAt = (tt) => {
  E.grade.uniforms.flash.value = 0; let ch = ""; CH.forEach(([a, s]) => { if (tt >= a) ch = s; }); if (TAG.textContent !== ch) TAG.textContent = ch;
  let scene, pos, look; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.88);
  Object.values(B).forEach((m, i) => (m.rotation.y = tt * 0.02 * (1 + i * 0.2))); A.so.rotation.y = tt * 0.02; A.px.rotation.y = tt * 0.03; A.wd.rotation.y = tt * 0.05; A.ju.rotation.y = tt * 0.08; EA.mesh.rotation.y = tt * 0.06; EA.clouds.rotation.y = tt * 0.07;
  orbB.forEach((o) => (o.material.opacity = 0)); satB.material.opacity = 0; dotB.material.opacity = 0; shell.material.opacity = 0; snFlash.material.opacity = 0; nsDot.material.opacity = 0; B.be.visible = true; B.be.userData.glow.visible = true;
  plane.material.opacity = 0; planeTrail.material.opacity = 0; nsRing.material.opacity = 0; cityRing.material.opacity = 0;
  if (tt < t.wir) { // Hook: Sonne -> riesiger Stern
    scene = SB; let c; if (tt < t.heute) { const f = K.eio(prog(tt, t.aber + 0.4, 2.2)); const [cx, w, h] = spanB("so", "st"); c = { x: lerp(XB.so, cx, f), d: lerpLog(fitD(6, 4), fitD(w, h), f) }; }
    else if (tt < t.und) { const [cx, w, h] = spanB("so", "st"); c = { x: cx, d: fitD(w, h) * (1 + 0.04 * (tt - t.heute)) }; }
    else { const f = prog(tt, t.und, t.wir - t.und); c = { x: XB.so, d: fitD(6, 4) * lerp(1.15, 0.9, f) }; }
    pos = V(c.x, c.d * 0.05, c.d); look = V(c.x, 0, 0); }
  else if (tt < t.etwas) { scene = SN; nsMat.uniforms.t.value = tt; const spin = tt > t.dreh ? (tt - t.dreh) * 9 : tt * 0.6; beams.rotation.set(0.45, spin, 0); beamMat.uniforms.o.value = 1;
    const f = prog(tt, t.wir, t.etwas - t.wir); let d, cx = 0; if (tt < t.er + 1.8) d = lerpLog(300, 70, K.eio(prog(tt, t.wir, 3))); else if (tt < t.aber2) { const g = K.eio(prog(tt, t.er + 1.8, 1.6)); d = lerp(70, fitD(70, 40) / 1.15, g); cx = lerp(0, 17, g); fo(nsRing, tt, t.er + 2.2, t.aber2 - 0.3, 0.9); fo(cityRing, tt, t.er + 2.6, t.aber2 - 0.3, 0.9); }
    else d = lerp(70, 110, K.eio(prog(tt, t.aber2, 3))); nsRing.lookAt(cam.position); pos = V(cx + Math.sin(f * 0.8) * d * 0.3, d * 0.12, d); look = V(cx, 0, 0); }
  else if (tt < t.jetzt) { scene = SA; if (tt > t.solche - 0.05) { scene = SG; const f = prog(tt, t.solche, t.jetzt - t.solche); const d = lerp(150, 110, K.eio(f)); pos = V(0, d * 0.7, d * 0.7); look = V(0, 0, 0); SG.rotation.y = tt * 0.02; }
    else { const c = track(KA, tt); pos = V(c.x + c.d * 0.04, c.d * 0.07, c.d); look = V(c.x, 0, 0); } }
  else if (tt < t.si) { scene = SA; const c = track(KS, tt); pos = V(c.x + c.d * 0.04, c.d * 0.07, c.d); look = V(c.x, 0, 0);
    if (tt > t.fl + 0.8 && tt < t.umS) { const f = prog(tt, t.fl + 0.8, t.umS - t.fl - 1.2); const a = f * Math.PI * 2 + Math.PI / 2; const R = RA.er * 1.15; plane.position.set(XA.er + Math.cos(a) * R, Math.sin(a) * R, RA.er * 1.2); plane.scale.setScalar(1.6); plane.material.opacity = f > 0 && f < 1 ? 1 : 0; planeTrail.scale.setScalar(R); planeTrail.position.set(XA.er, 0, RA.er * 1.1); planeTrail.material.opacity = 0.5 * cl(f * 8); }
    if (tt > t.umS + 0.8 && tt < t.cta) { const f = prog(tt, t.umS + 0.8, t.cta - t.umS - 0.9); const a = f * Math.PI * 2 + Math.PI / 2; const R = RA.so * 1.08; plane.position.set(XA.so + Math.cos(a) * R, Math.sin(a) * R, RA.so * 1.2); plane.scale.setScalar(60); plane.material.opacity = f > 0 && f < 1 ? 1 : 0; planeTrail.scale.setScalar(R); planeTrail.position.set(XA.so, 0, RA.so * 1.1); planeTrail.material.opacity = 0.5 * cl(f * 8); } }
  else if (tt < t.ueberr) { scene = SB; E.look([1, 1, 1], [0, 0, 0], 0.4, 0.85); const c = track(KB, tt); pos = V(c.x, c.d * 0.05, c.d); look = V(c.x, 0, 0);
    orbB.forEach((o, i) => fo(o, tt, t.stell + 1.2 + i * 0.6, t.vy - 0.6, 0.95));
    if (tt > t.mit + 0.8 && tt < t.vy - 0.3) { const f = prog(tt, t.mit + 0.8, t.vy - t.mit - 1.2); const a = f * 6.283 + Math.PI / 2; dotB.position.set(XB.be + Math.cos(a) * RB.be * 1.05, Math.sin(a) * RB.be * 1.05, RB.be); dotB.scale.setScalar(110); dotB.material.opacity = f > 0 && f < 1 ? 1 : 0; }
    fo(satB, tt, t.an2 + 1.2, t.ueberr - 0.4, 0.95);
    if (tt > t.mit2 + 0.6 && tt < t.ueberr - 0.3) { const k = tt < t.licht ? prog(tt, t.mit2 + 0.6, t.licht - t.mit2 - 0.8) : prog(tt, t.licht + 0.3, 2.6); const a = k * 6.283 + Math.PI / 2; dotB.position.set(XB.st + Math.cos(a) * RB.st * 1.04, Math.sin(a) * RB.st * 1.04, RB.st); dotB.scale.setScalar(tt < t.licht ? 260 : 340); dotB.material.opacity = k > 0 && k < 1 ? 1 : 0; } }
  else if (tt < t.uebrig) { scene = SB; E.look([1, 1, 1], [0, 0, 0], 0.4, 0.85);
    if (tt < t.riese) { const f = K.eio(prog(tt, t.ueberr, 2)); const c = { x: lerp(XB.st, XB.so, f), d: lerpLog(fitD(9.54 * AU * 2.3, 9.54 * AU * 2.3), fitD(8, 6), f) }; pos = V(c.x, c.d * 0.05, c.d); look = V(c.x, 0, 0); }
    else { const f = K.eio(prog(tt, t.riese, 1.8)); const d = lerpLog(fitD(8, 6), fitD(2200, 1800), f); const x = lerp(XB.so, XB.be, f); pos = V(x, d * 0.05, d); look = V(x, 0, 0);
      if (tt > t.expl + 0.6) { const k = prog(tt, t.expl + 0.6, 2.4); B.be.visible = k < 0.08; B.be.userData.glow.visible = k < 0.08; snFlash.material.opacity = Math.max(0, 1 - k * 1.6); snFlash.scale.setScalar(3000 + k * 6000); shell.scale.setScalar(RB.be * (0.9 + k * 2.2)); shell.material.opacity = 0.5 * (1 - k); E.grade.uniforms.flash.value = Math.max(0, 0.5 - k * 2); nsDot.material.opacity = cl((k - 0.3) * 3); } } }
  else if (tt < t.sonne2) { scene = SN; nsMat.uniforms.t.value = tt; beams.rotation.set(0.45, (tt - t.uebrig) * 9, 0); const f = prog(tt, t.uebrig, t.sonne2 - t.uebrig); const d = lerpLog(2000, 80, K.eio(cl(f * 1.6))); pos = V(d * 0.2, d * 0.1, d); look = V(0, 0, 0); }
  else if (tt < t.zu) { scene = SR; const g = cl((tt - t.sonne2 - 2.2) / (t.merkur + 1.6 - t.sonne2 - 2.2)); const shrink = cl((tt - t.danach - 0.2) / 1.3); const Rs = shrink > 0 ? lerpLog(AU * 0.98, 0.05, K.eio(shrink)) : lerpLog(1, AU * 0.98, K.eio(g));
    sunR.scale.setScalar(Rs); sunR.userData.glow.scale.setScalar(Rs * 3.2); const red = cl(g * 1.3); sunR.material.color.setRGB(1.3, lerp(1.0, 0.5, red) + shrink * 0.6, lerp(0.72, 0.3, red) + shrink * 0.9);
    plR.forEach((p, i) => { const a = p.ph + tt * 0.05 * (3 - i); const ps = V(Math.cos(a) * p.R, 0, Math.sin(a) * p.R); p.d.position.copy(ps); p.o.position.copy(ps); const eaten = Rs > p.R * 0.97 && i < 2; p.d.material.opacity = eaten ? 0 : (i === 2 && Rs > p.R * 0.9 ? 0.5 + 0.5 * Math.sin(tt * 12) : 1); p.r.material.opacity = p.r.userData.op * cl((tt - t.sonne2 - 0.5) / 0.8); });
    const f = prog(tt, t.sonne2, t.zu - t.sonne2); const d = lerpLog(12, 950, K.eio(cl((tt - t.sonne2) / 3))); pos = V(0, d * 0.75, d * 0.75); look = V(0, 0, 0); }
  else { scene = SA; const f = prog(tt, t.zu, t.punkt - t.zu); let c; const [cx, w, h] = spanA("wd", "er"); if (tt < t.punkt) c = { x: cx, d: lerpLog(fitD(w * 1.4, h * 1.4), fitD(w, h), K.eio(f)) }; else { const g = K.eio(prog(tt, t.punkt, 4)); c = { x: lerp(cx, XA.wd, g), d: lerpLog(fitD(w, h), 4000, g) }; }
    pos = V(c.x + c.d * 0.04, c.d * 0.07, c.d); look = V(c.x, 0, 0); }
  const dist = pos.distanceTo(look); cam.near = Math.max(0.01, dist / 400); cam.far = Math.max(dist * 1000, 2e8); cam.fov = 40; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  if (scene === SN) cityRing.lookAt(cam.position);
  E.render(scene, tt); updLabels(tt);
  const pxPerUnit = (o) => window.FMT.H / (2 * TAN * Math.max(1e-6, cam.position.distanceTo(o.getWorldPosition(new THREE.Vector3()))));
  labels.forEach((L) => { if (L.r > 0 && L.r * pxPerUnit(L.obj) < 20) L.d.style.opacity = 0; });
  let wh = "", wa = 0; const seg = (a, b, h) => { if (tt >= a && tt < b) { wh = h; wa = cl((tt - a) / 0.3) * (1 - cl((tt - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(t.aber + 1.6, t.heute - 0.1, "☀️ = Staubkorn?"); seg(t.heute + 0.2, t.und - 0.1, "vom kleinsten zum größten ⭐"); seg(t.und + 0.2, t.wir - 0.1, "☀️ Zukunft?");
  seg(W("zwanzig", 18.5) - 0.2, t.aber2 - 0.1, "≈ 20 km breit" + sub("so groß wie eine Stadt")); seg(t.aber2, t.tee - 0.1, "schwerer als die Sonne"); seg(t.tee, t.dreh - 0.1, "🥄 1 Teelöffel ≈ 1 Mrd. Tonnen"); seg(t.dreh + 0.3, t.etwas - 0.1, "🌀 Hunderte Drehungen pro Sekunde");
  seg(t.etwas + 0.4, t.sirB - 0.1, "Weißer Zwerg"); seg(W("ungefähr", 37.5) - 0.2, t.aber3 - 0.1, "≈ so groß wie die Erde"); seg(t.aber3, t.dann - 0.1, "fast so schwer wie die Sonne");
  seg(t.dann + 0.2, t.prox - 0.1, "Rote Zwerge"); seg(W("nächsten", 46.5) - 0.2, t.er2 - 0.1, "nächster Stern" + sub("4,2 Lichtjahre entfernt")); seg(W("anderthalbmal") - 0.2, t.solche - 0.1, "≈ 1,5× Jupiter"); seg(t.solche + 0.4, t.jetzt - 0.1, "🔴 die häufigsten Sterne");
  seg(W("eins", 58.8) - 0.1, t.hund - 0.1, "1,4 Mio. km"); seg(t.hund - 0.1, t.ueber - 0.1, "109× Erde"); seg(t.ueber, t.fl - 0.1, "> 1 Mio. Erden passen hinein"); seg(W("rund", 72.3), t.umS - 0.1, "✈️ um die Erde: 2 Tage"); seg(W("sieben", 76) - 0.2, t.cta - 0.1, "✈️ um die Sonne: 7 Monate");
  seg(W("knapp", 84.7) - 0.2, t.po - 0.1, "≈ 2× Sonne"); seg(W("neunmal") - 0.2, t.ar - 0.1, "9× Sonne"); seg(W("rund", 91) - 0.1, t.al - 0.1, "25× Sonne"); seg(W("fünfundvierzigmal") - 0.2, t.ri - 0.1, "45× Sonne" + sub("rotes Auge des Stiers"));
  seg(W("rund", 100) - 0.1, t.hell - 0.1, "80× Sonne"); seg(t.hell, t.jetzt2 - 0.1, "💡 > 100.000× so hell");
  seg(t.jetzt2 + 0.2, t.an - 0.1, "jetzt wird's verrückt 🤯"); seg(W("siebenhundertmal") - 0.2, t.be - 0.1, "700× Sonne" + sub("Herz des Skorpions")); seg(W("siebenhundertfünfzigmal") - 0.2, t.stell - 0.1, "750× Sonne");
  seg(t.stell + 0.5, t.mit - 0.1, "Merkur, Venus, Erde, Mars: weg"); seg(W("über", 126.7) - 0.1, t.vy - 0.1, "✈️ > 400 Jahre für 1 Runde");
  seg(W("vierzehnhundertmal") - 0.2, t.lange - 0.1, "≈ 1.400× Sonne"); seg(t.lange, t.st - 0.1, "lange der Rekordhalter 🏆");
  seg(W("über", 147.4) - 0.1, t.an2 - 0.1, "> 2.000× Sonne"); seg(t.an2 + 0.4, t.mit2 - 0.1, "bis über die Saturnbahn 🪐"); seg(W("über", 155.7) - 0.1, t.licht - 0.1, "✈️ > 1.000 Jahre"); seg(t.licht, t.ueberr - 0.1, "💡 Licht: fast 9 Stunden");
  seg(t.ueberr + 1, t.sonne10 - 0.1, "Riesen leben nicht lange ⏳"); seg(W("rund", 168.5) - 0.1, t.riese - 0.1, "☀️ ≈ 10 Mrd. Jahre"); seg(W("rund", 175) - 0.1, t.expl - 0.1, "🔴 ≈ 10 Mio. Jahre"); seg(t.expl + 0.6, t.uebrig - 0.1, "💥 Supernova");
  seg(W("neutronenstern", 183.5) - 0.1, t.sonne2 - 0.1, "Neutronenstern" + sub("20 km klein"));
  seg(W("in", 187.7) - 0.1, t.merkur - 0.1, "in ≈ 5 Mrd. Jahren: Roter Riese"); seg(t.merkur, t.danach - 0.1, "Merkur & Venus: verschluckt"); seg(t.danach + 0.2, t.zu - 0.1, "fällt zusammen");
  seg(t.zu, t.punkt - 0.1, "Weißer Zwerg" + sub("≈ so groß wie die Erde")); seg(t.punkt + 0.3, t.abo - 0.1, "unsere Zukunft ✨");
  word(wh, wa); cap(tt);
};
// ===== Titelbild: Sterne-Treppe (t < 1) =====
const _o = renderAt; const ST2 = new THREE.Scene(); K.reseed(3); K.stars(ST2, 5000, -1, 4e6, 1.6).material.opacity = 0.5;
const LINE = [["Sonne", "so", 26], ["Sirius", "si", 40], ["Arktur", "ar", 70], ["Rigel", "ri", 112], ["Beteigeuze", "be", 190], ["Stephenson 2-18", "st", 340]];
const tb = LINE.map(([n, k, r]) => ({ n, r, m: starBall(ST2, r, 0, k === "si" || k === "ri" ? [0.7, 0.9, 1.7] : COL[k][0], k === "si" || k === "ri" ? "rgba(140,180,255,.7)" : COL[k][1], 2.6, k === "si" || k === "ri") }));
renderAt = (tt) => { if (tt >= 1) return _o(tt);
  const Wd = window.FMT.W, Hd = window.FMT.H; let x = LAND ? -Wd / 2 + 70 : -Wd / 2 + 40; const base = LAND ? -Hd / 2 + 150 : -Hd / 2 + 520; const sc = LAND ? 1 : 0.52;
  const out = []; if (!LAND) { const PP = [[85, 1555, 16], [165, 1530, 26], [280, 1480, 46], [440, 1395, 76], [660, 1245, 128], [905, 985, 245]];
    tb.forEach((b, i) => { const [cx, cy, r] = PP[i]; const x = cx - Wd / 2, y = Hd / 2 - cy; b.m.position.set(x, y, 0); b.m.scale.setScalar(r / b.r); b.m.userData.glow.position.set(x, y, -r * 0.2); b.m.userData.glow.scale.setScalar(r * 2.6); b.m.rotation.y = i; out.push([b.n, x, y - r]); }); }
  else tb.forEach((b, i) => { const r = b.r * sc; x += r; const y = base + r + (LAND ? i * 6 : i * 4);  b.m.position.set(x, y, 0); b.m.scale.setScalar(sc); b.m.userData.glow.position.set(x, y, -r * 0.2); b.m.userData.glow.scale.setScalar(r * 2.6); b.m.rotation.y = i; out.push([b.n, x, y - r]); x += r + (LAND ? 46 : 14); });
  const D = 20000; const fov = 2 * Math.atan(Hd / 2 / D) * 180 / Math.PI; cam.fov = fov; cam.near = 100; cam.far = 1e6; cam.updateProjectionMatrix(); cam.position.set(0, 0, D); cam.lookAt(0, 0, 0);
  E.look([1, 1, 1], [0, 0, 0], 0.35, 0.85); E.render(ST2, tt);
  let o = document.getElementById("thx"); if (!o) { o = document.createElement("div"); o.id = "thx"; o.style.cssText = "position:absolute;inset:0;z-index:120;pointer-events:none"; document.getElementById("root").appendChild(o); }
  o.innerHTML = out.map(([n, px, py]) => `<div style="position:absolute;left:${Wd / 2 + px - 200}px;top:${Hd / 2 - py + 14}px;width:400px;text-align:center;font:800 ${LAND ? 30 : 27}px Inter,sans-serif;color:rgba(255,255,255,.92);text-shadow:0 3px 14px #000">${n}</div>`).join("");
};
