const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(17);
const R = 10; // Erdradius
// ================= Weltraum-Szene =================
const sc = new THREE.Scene(); K.stars(sc, 8000, -1, 30000, 1.7).material.opacity = 0.6;
sc.add(new THREE.AmbientLight(0x30303a, 0.6)); const sunL = new THREE.PointLight(0xfff2e0, 4, 0, 0); sc.add(sunL); const fill = new THREE.DirectionalLight(0xdfe6ff, 1.4); sc.add(fill);
const EA = K.earth(sc, { day, night, topo }, R); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93);
EA.U.sun.value = V(0.85, 0.25, -0.45).normalize();
const D = V(0.75, -0.45, -0.35).normalize(); // Flugrichtung der Leoniden (vom Radianten weg)
// Staubkorn (Nahaufnahme)
const kg = new THREE.SphereGeometry(1, 128, 96); { const pp = kg.attributes.position; for (let i = 0; i < pp.count; i++) { const v = V(pp.getX(i), pp.getY(i), pp.getZ(i)); const n = 1 + 0.22 * Math.sin(v.x * 3.3 + 1) * Math.cos(v.y * 2.9) + 0.07 * Math.sin(v.z * 4.3 + 2); v.multiplyScalar(n); pp.setXYZ(i, v.x * 1.15, v.y * 0.85, v.z); } kg.computeVertexNormals(); }
const grain = new THREE.Mesh(kg, new THREE.MeshStandardMaterial({ map: await tex("moon.jpg"), color: 0x9a8f86, roughness: 1 })); grain.position.set(0, 0, 3000); sc.add(grain);
const grainL = new THREE.DirectionalLight(0xfff0dc, 2.2); grainL.position.set(3010, 4, 3006); grainL.target = grain; sc.add(grainL);
// Sonnensystem (1 AE = 40)
const SS = new THREE.Group(); SS.position.set(0, 0, -20000); sc.add(SS);
const sun = new THREE.Mesh(new THREE.SphereGeometry(7, 96, 64), new THREE.MeshBasicMaterial({ map: await tex("sun.jpg"), color: new THREE.Color(1.3, 1.0, 0.7), toneMapped: false })); SS.add(sun);
const sunG = K.sprite(SS, K.glowTex("rgba(255,170,70,.5)"), 46, V(0, 0, 0), 0.7);
const ring = (r, op, col = 0xaab4d0, w = 0.5) => { const o = new THREE.Mesh(new THREE.RingGeometry(r - w, r + w, 512), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op, side: THREE.DoubleSide, depthWrite: false })); o.rotation.x = -Math.PI / 2; SS.add(o); return o; };
ring(40, 0.35, 0x9fc4ff, 0.35); const outer = [ring(208, 0.16), ring(381, 0.14), ring(768, 0.12, 0xaab4d0, 1.2)];
const dayT = new THREE.Texture(day); dayT.colorSpace = THREE.SRGBColorSpace; dayT.needsUpdate = true;
const earthS = new THREE.Mesh(new THREE.SphereGeometry(2.4, 64, 48), new THREE.MeshStandardMaterial({ map: dayT, roughness: 1 })); SS.add(earthS);
const eL = new THREE.PointLight(0xfff2e0, 3, 0, 0); SS.add(eL);
// Bahn von Tempel-Tuttle: q = 0,98 AE, Q = 19,7 AE, rückläufig (162°)
const qA = 0.98 * 40, QA = 19.7 * 40, aA = (qA + QA) / 2, cA = aA - qA, bA = Math.sqrt(aA * aA - cA * cA), INC = (18 * Math.PI) / 180;
const orb = (E) => V(aA * Math.cos(E) - cA, Math.sin(E) * bA * Math.sin(INC) * 0.35, -bA * Math.sin(E));
const op = []; for (let i = 0; i <= 720; i++) op.push(orb((i / 720) * Math.PI * 2));
const orbL = new THREE.Line(new THREE.BufferGeometry().setFromPoints(op), new THREE.LineBasicMaterial({ color: 0x7fd0ff, transparent: true, opacity: 0.5 })); SS.add(orbL);
// Staubspur entlang der Bahn
const ND = 9000, dpos = new Float32Array(ND * 3); for (let i = 0; i < ND; i++) { const u = K.rnd(); const E = (u - 0.5) * 2 * Math.PI; const p = orb(E); const s = 1.2 + 3.5 * Math.abs(Math.sin(E / 2)); dpos[i * 3] = p.x + (K.rnd() - 0.5) * s; dpos[i * 3 + 1] = p.y + (K.rnd() - 0.5) * s * 0.6; dpos[i * 3 + 2] = p.z + (K.rnd() - 0.5) * s; }
const dg = new THREE.BufferGeometry(); dg.setAttribute("position", new THREE.BufferAttribute(dpos, 3));
const dust = new THREE.Points(dg, new THREE.PointsMaterial({ color: 0xd8c8b0, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0.5, blending: THREE.AdditiveBlending, depthWrite: false })); SS.add(dust);
// Komet
const comet = new THREE.Group(); SS.add(comet); const nuc = new THREE.Mesh(kg, new THREE.MeshStandardMaterial({ map: await tex("moon.jpg"), color: 0x8a8580, roughness: 1 })); nuc.scale.setScalar(1.2); comet.add(nuc);
K.sprite(comet, K.glowTex("rgba(170,220,255,.65)"), 9, V(0, 0, 0), 0.6); K.sprite(comet, K.glowTex("rgba(120,200,255,.3)"), 20, V(0, 0, 0), 0.4);
const NT = 900, tailPos = new Float32Array(NT * 3), tailSeed = []; for (let i = 0; i < NT; i++) tailSeed.push([K.rnd(), K.rnd() - 0.5, K.rnd() - 0.5]);
const tg = new THREE.BufferGeometry(); tg.setAttribute("position", new THREE.BufferAttribute(tailPos, 3));
const tail = new THREE.Points(tg, new THREE.PointsMaterial({ color: 0xa8dcff, size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending, depthWrite: false })); SS.add(tail);

// ================= Himmel-Szene (Blick vom Boden) =================
const sky = new THREE.Scene(); K.reseed(99);
const skyStars = K.stars(sky, 9000, -0.02, 3000, 1.6); skyStars.material.transparent = true;
sky.add(new THREE.AmbientLight(0x101018, 1));
const ground = new THREE.Mesh(new THREE.CircleGeometry(4000, 64), new THREE.MeshBasicMaterial({ color: 0x010203 })); ground.rotation.x = -Math.PI / 2; ground.position.y = -6; sky.add(ground);
// Hügel-Silhouette rundum
{ const pts = []; for (let i = 0; i <= 360; i++) { const a = (i / 360) * Math.PI * 2; const h = 10 + 9 * Math.sin(a * 5 + 1) * Math.sin(a * 3) + 4 * Math.sin(a * 23) + 2 * Math.sin(a * 61); pts.push(a, h); }
  const g = new THREE.BufferGeometry(); const P = [], I = []; for (let i = 0; i <= 360; i++) { const a = pts[i * 2], h = pts[i * 2 + 1]; P.push(Math.cos(a) * 900, -6, Math.sin(a) * 900, Math.cos(a) * 900, h, Math.sin(a) * 900); if (i < 360) { const k = i * 2; I.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); } }
  g.setAttribute("position", new THREE.Float32BufferAttribute(P, 3)); g.setIndex(I); sky.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: 0x010203, side: THREE.DoubleSide }))); }
const horG = [0, Math.PI].map((a) => K.sprite(sky, K.glowTex("rgba(40,60,110,.5)"), 1400, V(Math.cos(a) * 1500, -60, Math.sin(a) * 1500), 0.35));
// Richtung aus Höhe/Azimut (Azimut 90° = Osten = +x, Süden = +z… vereinfacht)
const dirAA = (alt, az) => { const a = (alt * Math.PI) / 180, z = (az * Math.PI) / 180; return V(Math.sin(z) * Math.cos(a), Math.sin(a), -Math.cos(z) * Math.cos(a)); };
// Sternbild Löwe (vereinfacht, Positionen aus RA/Dek, um den Radianten gedreht)
const LEO = { Regulus: [10.14, 11.97, 1.35], Eta: [10.12, 16.76, 3.5], Algieba: [10.33, 19.84, 2.0], Adhafera: [10.28, 23.42, 3.4], Rasalas: [9.88, 26.0, 3.9], Epsilon: [9.76, 23.77, 3.0], Zosma: [11.24, 20.52, 2.5], Chertan: [11.24, 15.43, 3.3], Denebola: [11.82, 14.57, 2.1] };
const RAD = [10.2, 22]; const leoC = [10.7, 18.5];
const ALT0 = 28, AZ0 = 92; // Löwe nach Mitternacht im Osten
const leoDir = (ra, de) => { const dx = -(ra - leoC[0]) * 15 * Math.cos((18 * Math.PI) / 180), dy = de - leoC[1]; const r = Math.hypot(dx, dy), a = Math.atan2(dy, dx) + 0.55; return dirAA(ALT0 + Math.sin(a) * r, AZ0 + Math.cos(a) * r); };
const leoPts = {}; for (const [n, [ra, de, mag]] of Object.entries(LEO)) { const d = leoDir(ra, de).multiplyScalar(1000); leoPts[n] = d; const s = 26 - mag * 4.5; K.sprite(sky, K.glowTex("rgba(255,250,240,1)"), s, d, 1); K.sprite(sky, K.glowTex("rgba(190,210,255,.35)"), s * 3, d, 0.6); }
const LL = [["Regulus", "Eta"], ["Eta", "Algieba"], ["Algieba", "Adhafera"], ["Adhafera", "Rasalas"], ["Rasalas", "Epsilon"], ["Algieba", "Zosma"], ["Zosma", "Denebola"], ["Denebola", "Chertan"], ["Chertan", "Regulus"], ["Zosma", "Chertan"]];
const leoLines = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(LL.flatMap(([a, b]) => [leoPts[a], leoPts[b]])), new THREE.LineBasicMaterial({ color: 0xbfd6ff, transparent: true, opacity: 0 })); sky.add(leoLines);
const leoMid = new THREE.Object3D(); leoMid.position.copy(leoDir(leoC[0], leoC[1] + 1).multiplyScalar(1000)); sky.add(leoMid);
const radDir = leoDir(RAD[0], RAD[1]);
const eastMark = new THREE.Object3D(); eastMark.position.copy(dirAA(1.5, 92).multiplyScalar(1000)); sky.add(eastMark);
// Mond (zunehmender Halbmond, geht im Westen unter)
const moon = new THREE.Mesh(new THREE.SphereGeometry(14, 96, 64), new THREE.MeshStandardMaterial({ map: await tex("moon.jpg"), roughness: 1 })); sky.add(moon);
const mL = new THREE.DirectionalLight(0xfff6ea, 3.2); sky.add(mL); sky.add(mL.target); const moonG = K.sprite(sky, K.glowTex("rgba(200,215,255,.35)"), 120, V(0, 0, 0), 0.5);

// ================= Sternschnuppen (Leuchtstreifen) =================
const streakMat = () => new THREE.ShaderMaterial({ uniforms: { a: { value: 0 }, col: { value: new THREE.Color(0.7, 0.88, 1.0) } }, transparent: true, depthWrite: false, depthTest: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false,
  vertexShader: `varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float a;uniform vec3 col;varying vec2 vU;void main(){float w=1.-abs(vU.y-.5)*2.;w=w*w;float h=pow(vU.x,2.2);vec3 c=mix(col,vec3(1.,.97,.85),pow(vU.x,10.));gl_FragColor=vec4(c*h*w*a*4.,h*w*a);}` });
const pool = (scene, n) => new Array(n).fill(0).map(() => { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), streakMat()); m.matrixAutoUpdate = false; m.frustumCulled = false; m.visible = false; scene.add(m); return m; });
const poolE = pool(sc, 260), poolS = pool(sky, 60);
const _x = V(0, 0, 0), _y = V(0, 0, 0), _z = V(0, 0, 0);
function place(m, tail, head, width, a) { _x.copy(head).sub(tail); const L = _x.length(); if (L < 1e-6) return (m.visible = false); _x.multiplyScalar(1 / L); const mid = tail.clone().add(head).multiplyScalar(0.5);
  _z.copy(cam.position).sub(mid).normalize(); _y.crossVectors(_z, _x).normalize(); _z.crossVectors(_x, _y);
  m.matrix.makeBasis(_x.clone().multiplyScalar(L), _y.clone().multiplyScalar(width), _z).setPosition(mid); m.matrixWorldNeedsUpdate = true; m.material.uniforms.a.value = a; m.visible = a > 0.002; }

// ===== Zeiten =====
const tEs = W("es", 7), tIhr = W("ihr"), tJede = W("jede"), tEs2 = W("es", 19), tEr = W("er", 21.4), tJed = W("jedes"), tDie = W("die", 30.4), tIn = W("in", 35.5), tNorm = W("normalerweise"), tAber = W("aber", 45), t1966 = W("neunzehnhundert"), tVier = W("vierzig"), tDies = W("dieses", 51.5), tSchau = W("schau"), tDaher = W("daher"), tUnd = W("und", 62.7), tDeine = W("deine"), tWas = W("was", 68.9), tFolg = W("folg", 72.9);
// Rate (sichtbare Sternschnuppen pro Sekunde) je Abschnitt
const rateE = (t) => (t < tJede ? 2.2 : t < tDie ? 0 : t < tIn ? 9 : t < tNorm ? 3 : t < tAber ? 0.8 : t < tDies ? (t < t1966 + 0.6 ? 2 : t < tVier ? 18 : 45) : 0);
const rateS = (t) => (t < tSchau + 1 ? 0 : t < tDeine ? 1.0 : 1.5);
const spawn = (rate, seed, life) => { K.reseed(seed); const L = []; let acc = K.rnd(); for (let t = 0; t < 76; t += 1 / 60) { acc += rate(t) / 60; while (acc >= 1) { acc -= 1; L.push({ t: t + K.rnd() / 60, r: [K.rnd(), K.rnd(), K.rnd(), K.rnd(), K.rnd()], life: life[0] + K.rnd() * life[1] }); } } return L; };
const SE = spawn(rateE, 4242, [0.45, 0.5]), SSk = spawn(rateS, 777, [0.5, 0.6]);

label("Tempel-Tuttle<small>Komet</small>", comet, 2, { t0: tEs2 + 0.9, t1: tEr + 1.2, size: 60, gap: 24 });
label("Sonne", sun, 7, { t0: tEr + 0.3, t1: tJed - 0.1, size: 48, gap: 18 });
label("Erde", earthS, 2.4, { t0: tJed + 0.3, t1: tDie - 0.1, size: 56, gap: 18 });
label("Sternbild Löwe", leoMid, 0, { t0: tSchau + 1.6, t1: tUnd - 0.1, size: 60, gap: 200 });


const camDirE = V(0, 0, 0);
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.5, 0.75);
  let upX = 0; let scene = sc, pos, look = V(0, 0, 0), fov = 40, mode = "earth";
  EA.group.rotation.y = 2.2 + t * 0.012; EA.clouds.rotation.y = t * 0.004;
  if (t < tJede - 0.05) { const f = K.eio(prog(t, 0, tJede)); const a = lerp(-0.55, -0.3, f); const d = lerp(40, 27, f); pos = V(Math.sin(a) * d, lerp(9, 5, f), Math.cos(a) * d); look = V(lerp(-3, -2, f), lerp(2, 1, f), 0); }
  else if (t < tEs2 - 0.05) { mode = "grain"; const f = prog(t, tJede, tEs2 - tJede); grain.rotation.set(t * 0.25, t * 0.4, 0.2); pos = V(0, 0.4, 3000 + lerp(5.2, 4.2, K.eio(f))); look = grain.position.clone(); }
  else if (t < tDie - 0.05) { mode = "solar";
    // Komet läuft durch das Perihel, danach zieht die Erde durch die Spur
    const E0 = lerp(-0.55, 0.5, prog(t, tEs2, tJed - tEs2)); const cp = orb(E0); comet.position.copy(cp); nuc.rotation.set(t * 0.2, t * 0.3, 0);
    const act = cl(1.6 - cp.length() / 120); const anti = cp.clone().normalize();
    for (let i = 0; i < NT; i++) { const [k, a, b] = tailSeed[i]; const L = (6 + 60 * act) * Math.pow(k, 1.4); const sp = 0.3 + L * 0.1; tailPos[i * 3] = cp.x + anti.x * L + a * sp; tailPos[i * 3 + 1] = cp.y + anti.y * L + b * sp; tailPos[i * 3 + 2] = cp.z + anti.z * L + (a - b) * sp * 0.5; }
    tg.attributes.position.needsUpdate = true;
    const ea = lerp(-0.9, 0.04, K.eio(prog(t, tEs2, tDie - tEs2))); earthS.position.set(Math.cos(ea) * 40, 0, -Math.sin(ea) * 40); earthS.rotation.y = t * 0.5;
    const C = SS.position;
    if (t < tEr - 0.05) { const f = K.eio(prog(t, tEs2, 1.6)); pos = C.clone().add(cp).add(V(lerp(8, 30, f), lerp(6, 70, f), lerp(22, 60, f))); look = C.clone().add(cp.clone().multiplyScalar(lerp(1, 0.7, f))); }
    else if (t < tJed - 0.05) { const f = K.eio(prog(t, tEr, 2.6)); pos = C.clone().add(V(lerp(60, -375, f), lerp(120, 1250, f), lerp(60, 60, f))); look = C.clone().add(V(lerp(30, -375, f), 0, 0)); upX = f; }
    else { const f = K.eio(prog(t, tJed, 1.8)); pos = C.clone().add(earthS.position).add(V(lerp(-60, -14, f), lerp(170, 26, f), lerp(60, 30, f))); look = C.clone().add(earthS.position.clone().multiplyScalar(lerp(0.5, 1, f))); }
    eL.position.set(0, 0, 0); }
  else if (t < tIn - 0.05) { const f = K.eio(prog(t, tDie, tIn - tDie)); const a = lerp(-0.1, 0.1, f); pos = V(Math.sin(a) * 25, 4, Math.cos(a) * 25); look = V(0, 1, 0); }
  else if (t < tNorm - 0.05) { E.look([1, 1, 1], [0, 0, 0], 0.3, 0.85); const f = prog(t, tIn, tNorm - tIn); pos = V(lerp(-6, -5, f), 9.2, 14.5); look = V(lerp(2, 3, f), 8.5, 0); fov = 36; }
  else if (t < tDies - 0.05) { const f = K.eio(prog(t, tNorm, tDies - tNorm)); const a = lerp(-0.25, 0.15, f); const d = lerp(30, 24, f); pos = V(Math.sin(a) * d, 5, Math.cos(a) * d); look = V(0, 1, 0);
    if (t > tVier) E.look([1, 1, 1], [0, 0, 0], 0.7, 0.7); }
  else { mode = "sky"; scene = sky; }

  // ---- Himmel ----
  if (mode === "sky") {
    // Mond geht im Westen unter, dann Schwenk nach Osten
    const mAlt = lerp(7, -6, K.eio(prog(t, tDies, tSchau - tDies + 0.2))); const md = dirAA(mAlt, 268).multiplyScalar(900); moon.position.copy(md); moonG.position.copy(md); moonG.material.opacity = 0.5 * cl((mAlt + 3) / 4);
    mL.position.copy(md).add(V(0, -150, 0)).add(dirAA(0, 182).multiplyScalar(900)); mL.target.position.copy(md);
    const pan = K.eio(prog(t, tSchau - 0.1, 1.6)); const az = lerp(268, 92 + 360, pan); const alt = lerp(6, 20, pan);
    pos = V(0, 0, 0); look = dirAA(alt, az).multiplyScalar(100); fov = lerp(30, 58, pan);
    const dark = prog(t, tDies + 1.5, 4); const adapt = K.eio(prog(t, tDeine, 4.5));
    skyStars.material.opacity = t < tDeine ? lerp(0.35, 0.45, dark) : lerp(0.45, 0.95, adapt);
    leoLines.material.opacity = 0.35 * cl((t - tSchau - 1.3) / 0.8) * (1 - cl((t - tUnd + 0.3) / 0.6));
    E.look([1, 1, 1], [0, 0, 0], 0.55, 0.7);
  }
  cam.up.set(-upX, 1 - upX, 0).normalize(); fill.position.copy(cam.position); cam.fov = fov; cam.near = mode === "sky" ? 0.5 : 0.05; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look); cam.updateMatrixWorld();
  // ---- Sternschnuppen über der Erde ----
  poolE.forEach((m) => (m.visible = false)); poolS.forEach((m) => (m.visible = false));
  if (mode === "earth") { camDirE.copy(cam.position).normalize(); const u = V(0, 1, 0).cross(camDirE).normalize(), v = camDirE.clone().cross(u); let k = 0;
    const lowAtm = t >= tIn - 0.05 && t < tNorm - 0.05;
    for (const s of SE) { if (k >= poolE.length) break; const age = t - s.t; if (age < 0 || age > s.life) continue; const [r1, r2, r3, r4, r5] = s.r;
      const ray = V(lerp(-0.95, 0.95, r1), lowAtm ? lerp(-0.1, 0.55, r2) : lerp(-0.85, 0.75, r2), 0.5).unproject(cam).sub(cam.position).normalize();
      const oc = cam.position.clone(), bb = oc.dot(ray), cc = oc.lengthSq() - (R * 1.03) ** 2, disc = bb * bb - cc; if (disc < 0) continue;
      const n = oc.add(ray.multiplyScalar(-bb - Math.sqrt(disc))).normalize();
      if (n.dot(D) > 0.05) continue; const len = (1.0 + r3 * 1.6) * (lowAtm ? 0.8 : 1); const p0 = n.clone().multiplyScalar(R * 1.03); const f = age / s.life;
      const Dt = D.clone().sub(n.clone().multiplyScalar(n.dot(D))).normalize().add(n.clone().multiplyScalar(-0.06)).normalize();
      const head = p0.clone().add(Dt.clone().multiplyScalar(len * f)); const tl = head.clone().sub(Dt.clone().multiplyScalar(Math.min(len * f, 0.6 + 1.4 * r4)));
      const a = Math.sin(Math.PI * Math.min(1, f * 1.1)) * (0.6 + 0.4 * r4); place(poolE[k++], tl, head, lowAtm ? 0.1 : 0.14, a); } }
  if (mode === "sky") { const rd = radDir.clone(); let k = 0; const ax1 = V(0, 1, 0).cross(rd).normalize(), ax2 = rd.clone().cross(ax1);
    for (const s of SSk) { if (k >= poolS.length) break; const age = t - s.t; if (age < 0 || age > s.life) continue; const [r1, r2, r3, r4] = s.r; const ang = r1 * Math.PI * 2; const dirOut = ax1.clone().multiplyScalar(Math.cos(ang)).add(ax2.clone().multiplyScalar(Math.sin(ang)));
      const d0 = 0.06 + r2 * 0.35, L = 0.06 + r3 * 0.16, f = age / s.life; const at = (d) => rd.clone().add(dirOut.clone().multiplyScalar(d)).normalize().multiplyScalar(900);
      const hd = d0 + L * f, tlD = Math.max(d0, hd - L * 0.7); if (at(hd).y < 15) continue; place(poolS[k++], at(tlD), at(hd), 5 + r4 * 4, Math.sin(Math.PI * f) * (0.7 + 0.3 * r4)); } }
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tEs + 0.2, tIhr - 0.1, "Leoniden"); seg(tIhr + 0.8, tJede - 0.1, "17. → 18. November<div class='sub'>Höhepunkt ≈ 1 Uhr nachts</div>");
  seg(W("kaum") - 0.2, tEs2 - 0.1, "≈ Sandkorn");
  seg(W("dreiunddreißig") - 0.1, tJed - 0.1, "alle 33 Jahre");
  seg(W("einundsiebzig") - 0.1, tIn - 0.1, "71 km pro Sekunde"); seg(W("hundert", 35.8) - 0.1, tNorm - 0.1, "≈ 100 km Höhe");
  seg(W("zehn", 42) - 0.1, tAber - 0.1, "10–15 pro Stunde"); seg(t1966 - 0.1, tVier - 0.1, "1966"); seg(tVier - 0.1, tDies - 0.1, "40 pro Sekunde!");
  seg(tDies + 0.3, tSchau - 0.1, "🌙 geht gegen<br>Mitternacht unter"); seg(W("osten") - 0.1, tDaher - 0.1, "↗ Osten"); seg(tDaher, tUnd - 0.1, "Löwe = Leo<div class='sub'>→ Leoniden</div>");
  seg(tDeine, tWas - 0.1, "👀 ≈ 20 Minuten<div class='sub'>bis sich die Augen gewöhnen</div>");
  word(wh, wa); cap(t);
};
