const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(18);
const { RoomEnvironment } = await import("three/addons/environments/RoomEnvironment.js");
const pm = new THREE.PMREMGenerator(E.R); const env = pm.fromScene(new RoomEnvironment(), 0.04).texture;
const mirrorMat = new THREE.MeshStandardMaterial({ color: 0xe8ecf4, metalness: 1, roughness: 0.14, envMap: env, envMapIntensity: 0.7, side: THREE.DoubleSide });
const bodyMat = new THREE.MeshStandardMaterial({ color: 0x8a8f99, metalness: 0.7, roughness: 0.4, envMap: env, envMapIntensity: 0.6 });
const goldMat = new THREE.MeshStandardMaterial({ color: 0xc89b3c, metalness: 0.9, roughness: 0.35, envMap: env, envMapIntensity: 0.7 });
// ---------- Spiegel-Satellit (Spiegel 18 x 18 m) ----------
function makeSat() { const g = new THREE.Group(); const b = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.0, 1.0), goldMat); g.add(b);
  const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.2, 12), bodyMat); boom.position.y = 1.4; g.add(boom);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(18, 18, 1, 1), mirrorMat); m.position.y = 2.6; m.rotation.x = -Math.PI / 2 + 0.25; g.add(m);
  const frame = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(18, 18)), new THREE.LineBasicMaterial({ color: 0x9aa2b0 })); frame.position.copy(m.position); frame.rotation.copy(m.rotation); g.add(frame);
  const glint = K.sprite(g, K.glowTex("rgba(255,250,235,1)"), 8, V(0, 2.8, 0), 0); return { g, m, glint }; }
// ================= Weltraum =================
const scE = new THREE.Scene(); K.stars(scE, 9000, -1, 30000, 1.7).material.opacity = 0.65;
scE.add(new THREE.AmbientLight(0x30303a, 0.5)); const sunD = new THREE.DirectionalLight(0xfff4e6, 2.4); sunD.position.set(-500, 150, -500); scE.add(sunD);
const RE = 120; const EA = K.earth(scE, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-500, 150, -500).normalize();
EA.group.rotation.y = -0.6;
const S1 = makeSat(); S1.g.scale.setScalar(0.12); scE.add(S1.g);
// Lichtstrahlen + Lichtflecken (bis zu 6)
const beams = [], spots = []; for (let i = 0; i < 6; i++) { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 1.6, 1, 32, 1, true), new THREE.MeshBasicMaterial({ color: 0xfff1c8, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, side: THREE.DoubleSide })); scE.add(c); beams.push(c);
  spots.push([K.sprite(scE, K.glowTex("rgba(255,245,210,1)"), 4, V(0, 0, 0), 0), K.sprite(scE, K.glowTex("rgba(255,220,150,.5)"), 14, V(0, 0, 0), 0)]); }
const sats = [S1]; for (let i = 1; i < 6; i++) { const s = makeSat(); s.g.scale.setScalar(0.12); scE.add(s.g); sats.push(s); }
// 50.000 Spiegel als Lichtpunkte
const NM = 6000, mp = new Float32Array(NM * 3); for (let i = 0; i < NM; i++) { const u = K.rnd() * 2 - 1, a = K.rnd() * Math.PI * 2, r = RE + 4.5 + K.rnd() * 2; const q = Math.sqrt(1 - u * u); mp[i * 3] = Math.cos(a) * q * r; mp[i * 3 + 1] = u * r; mp[i * 3 + 2] = Math.sin(a) * q * r; }
const mg = new THREE.BufferGeometry(); mg.setAttribute("position", new THREE.BufferAttribute(mp, 3));
const many = new THREE.Points(mg, new THREE.PointsMaterial({ color: 0xfff6e0, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: true })); scE.add(many);
const site = (lat, lon) => EA.ll(lat, lon, RE * 1.001);
// ================= Himmel (vom Boden) =================
const sky = new THREE.Scene(); K.reseed(99); const skyStars = K.stars(sky, 9000, -0.02, 3000, 1.6); skyStars.material.opacity = 0.85;
sky.add(new THREE.AmbientLight(0x14161e, 1));
{ const P = [], I = []; for (let i = 0; i <= 360; i++) { const a = (i / 360) * Math.PI * 2; const h = 10 + 9 * Math.sin(a * 5 + 1) * Math.sin(a * 3) + 4 * Math.sin(a * 23) + 2 * Math.sin(a * 61); P.push(Math.cos(a) * 900, -6, Math.sin(a) * 900, Math.cos(a) * 900, h, Math.sin(a) * 900); if (i < 360) { const k = i * 2; I.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); } }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(P, 3)); g.setIndex(I); sky.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: 0x010203, side: THREE.DoubleSide }))); }
const gnd = new THREE.Mesh(new THREE.CircleGeometry(4000, 64), new THREE.MeshBasicMaterial({ color: 0x010203 })); gnd.rotation.x = -Math.PI / 2; gnd.position.y = -6; sky.add(gnd);
K.sprite(sky, K.glowTex("rgba(40,60,110,.5)"), 1400, V(0, -60, -1500), 0.35);
const dirAA = (alt, az) => { const a = (alt * Math.PI) / 180, z = (az * Math.PI) / 180; return V(Math.sin(z) * Math.cos(a), Math.sin(a), -Math.cos(z) * Math.cos(a)); };
const fullMoon = new THREE.Mesh(new THREE.SphereGeometry(20, 96, 64), new THREE.MeshBasicMaterial({ map: await tex("moon.jpg"), color: 0xd8d8d8 })); fullMoon.position.copy(dirAA(20, 0).multiplyScalar(900)); sky.add(fullMoon);
K.sprite(sky, K.glowTex("rgba(200,215,255,.3)"), 110, fullMoon.position, 0.5);
const mirStar = [K.sprite(sky, K.glowTex("rgba(255,252,240,1)"), 26, V(0, 0, 0), 0), K.sprite(sky, K.glowTex("rgba(255,240,200,.5)"), 160, V(0, 0, 0), 0)];
const mirO = new THREE.Object3D(); sky.add(mirO); const moonO = new THREE.Object3D(); moonO.position.copy(fullMoon.position); sky.add(moonO);
// Satelliten-Spuren (Lichtstreifen)
const trailMat = () => new THREE.ShaderMaterial({ uniforms: { a: { value: 0 } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false,
  vertexShader: `varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`, fragmentShader: `uniform float a;varying vec2 vU;void main(){float w=1.-abs(vU.y-.5)*2.;gl_FragColor=vec4(vec3(1.,.97,.9)*w*w*a*2.,w*w*a);}` });
const _x = V(0, 0, 0), _y = V(0, 0, 0), _z = V(0, 0, 0);
function place(m, tail, head, width, a) { _x.copy(head).sub(tail); const L = _x.length(); _x.multiplyScalar(1 / L); const mid = tail.clone().add(head).multiplyScalar(0.5); _z.copy(cam.position).sub(mid).normalize(); _y.crossVectors(_z, _x).normalize(); _z.crossVectors(_x, _y);
  m.matrixAutoUpdate = false; m.matrix.makeBasis(_x.clone().multiplyScalar(L), _y.clone().multiplyScalar(width), _z).setPosition(mid); m.matrixWorldNeedsUpdate = true; m.material.uniforms.a.value = a; m.frustumCulled = false; }
const trails = []; K.reseed(5); for (let i = 0; i < 40; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), trailMat()); sky.add(m); trails.push({ m, a0: K.rnd() * 360, alt0: 15 + K.rnd() * 60, sp: 4 + K.rnd() * 6, dir: K.rnd() * Math.PI * 2, t0: K.rnd() }); }
// Teleskop
const scope = new THREE.Group(); sky.add(scope); scope.position.set(14, -6, -40);
{ const tube = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 12, 32), new THREE.MeshStandardMaterial({ color: 0xb8bec8, metalness: 0.2, roughness: 0.5 })); tube.rotation.x = -0.75; tube.rotation.z = -0.3; tube.position.y = 10; scope.add(tube);
  for (let i = 0; i < 3; i++) { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 11, 8), new THREE.MeshStandardMaterial({ color: 0x333333 })); const a = (i / 3) * Math.PI * 2; l.position.set(Math.cos(a) * 2, 4.5, Math.sin(a) * 2); l.rotation.set(Math.sin(a) * 0.35, 0, -Math.cos(a) * 0.35); scope.add(l); } }
const scopeL = new THREE.DirectionalLight(0xfff0d0, 2.2); scopeL.position.set(0, 50, 100); sky.add(scopeL);
// ================= Solarpark bei Nacht =================
const park = new THREE.Scene(); K.stars(park, 6000, 0.02, 3000, 1.5).material.opacity = 0.7; park.add(new THREE.AmbientLight(0x1a2030, 0.6));
const pg = new THREE.Mesh(new THREE.CircleGeometry(3000, 64), new THREE.MeshStandardMaterial({ color: 0x0c0d0f, roughness: 1 })); pg.rotation.x = -Math.PI / 2; park.add(pg);
const panels = []; { const geo = new THREE.BoxGeometry(6, 0.2, 3.4); const mat = new THREE.MeshStandardMaterial({ color: 0x0f1d3c, metalness: 0.5, roughness: 0.25, envMap: env, envMapIntensity: 0.5 }); const N = 12 * 18; const im = new THREE.InstancedMesh(geo, mat, N); const m4 = new THREE.Matrix4(); let k = 0;
  for (let r = 0; r < 18; r++) for (let c = 0; c < 12; c++) { m4.compose(V((c - 5.5) * 7, 1.6, (r - 9) * 6), new THREE.Quaternion().setFromEuler(new THREE.Euler(-0.5, 0, 0)), V(1, 1, 1)); im.setMatrixAt(k++, m4); } park.add(im); }
const parkStar = [K.sprite(park, K.glowTex("rgba(255,252,240,1)"), 30, V(260, 330, -800), 0), K.sprite(park, K.glowTex("rgba(255,240,200,.5)"), 180, V(260, 330, -800), 0)];
const spot = new THREE.SpotLight(0xfff0c8, 0, 0, 0.11, 0.7, 0); spot.position.set(30, 400, -80); spot.target.position.set(0, 0, 0); park.add(spot); park.add(spot.target);
const parkBeam = new THREE.Mesh(new THREE.CylinderGeometry(2, 45, 400, 48, 1, true), new THREE.MeshBasicMaterial({ color: 0xfff0c8, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, toneMapped: false })); parkBeam.position.set(15, 200, -40); parkBeam.lookAt(V(30, 400, -80)); parkBeam.rotateX(Math.PI / 2); park.add(parkBeam);

// ===== Zeiten =====
const tDie = W("die", 4.6), tIhr = W("ihr", 8), tWas = W("was", 14), tDer = W("der", 21), tIm = W("im", 27), tVon = W("von", 32.8), tBest = W("bestellen"), tUnd = W("und", 43.2), tAber = W("aber", 50.4), tDieS = W("die", 56.5), tWer = W("wer", 63.8);
label("Eärendil-1<small>Spiegel 18 × 18 m</small>", S1.g, 1.5, { t0: W("sein", 24.4) + 0.2, t1: tVon - 0.1, size: 60, gap: 20 });
label("Vollmond", moonO, 13, { t0: tVon + 0.5, t1: tBest - 0.1, size: 52, gap: 20 }); label("Spiegel", mirO, 6, { t0: tVon + 0.5, t1: tBest - 0.1, size: 52, gap: 30 });

let closeBeam = false; const setBeam = (i, from, to, a, w = 1) => { const b = beams[i]; const d = to.clone().sub(from); const L = d.length(); b.position.copy(from).add(to).multiplyScalar(0.5); b.scale.set(w, L, w); b.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize().negate()); b.material.opacity = (closeBeam ? 0.06 : 0.26) * a;
  spots[i][0].position.copy(to); spots[i][1].position.copy(to); spots[i][0].material.opacity = a; spots[i][1].material.opacity = 0.7 * a; };
const satAt = (s, lat, lon, h, t) => { const ground = site(lat, lon); const n = ground.clone().normalize(); const p = n.clone().multiplyScalar(RE + h); s.g.position.copy(p); s.g.lookAt(V(0, 0, 0)); s.g.rotateX(-Math.PI / 2); s.g.rotateY(t * 0.05); return { p, ground }; };
const SITES = [[35, -119], [40, -104], [33, -97], [42, -88], [31, -84], [45, -74]];
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.4, 0.82);
  closeBeam = false; let scene = scE, pos, look = V(0, 0, 0), fov = 40;
  beams.forEach((b) => (b.material.opacity = 0)); spots.flat().forEach((s) => (s.material.opacity = 0)); sats.forEach((s) => (s.g.visible = false)); many.material.opacity = 0;
  EA.group.rotation.y = -0.6 + t * 0.004;
  const cal = site(35, -119); const cn = cal.clone().normalize(); const sd = cn.clone().negate().applyAxisAngle(V(0, 1, 0), 1.15).add(V(0, 0.15, 0)).normalize(); EA.U.sun.value.copy(sd); sunD.position.copy(sd.clone().multiplyScalar(500)); scope.visible = false;
  if (t < tWas - 0.05 || (t >= tWas - 0.05 && t < tDer - 0.05)) { // Erde + Strahl(en)
    const nOn = t < tIhr ? 1 : Math.min(6, 1 + Math.floor((t - tIhr) * 1.6));
    for (let i = 0; i < nOn; i++) { const [la, lo] = SITES[i]; const s = sats[i]; s.g.visible = true; const { p, ground } = satAt(s, la, lo, 8, t); const fade = i === 0 ? 1 : cl((t - tIhr - i / 1.6) / 0.6); setBeam(i, p, ground, fade * (0.85 + 0.15 * Math.sin(t * 3 + i)), 1); s.glint.material.opacity = fade; }
    if (t < tDie - 0.05) { const f = K.eio(prog(t, 0, tDie)); pos = cn.clone().multiplyScalar(RE + lerp(70, 30, f)).add(V(lerp(-30, -14, f), lerp(20, 8, f), 0)); look = cn.clone().multiplyScalar(RE + 4); }
    else if (t < tIhr - 0.05) { const f = K.eio(prog(t, tDie, 2)); pos = cn.clone().multiplyScalar(RE + lerp(30, 120, f)).add(V(-20, 10, 0)); look = cn.clone().multiplyScalar(RE * lerp(1, 0.6, f)); }
    else { const a = (t - tIhr) * 0.025; pos = cn.clone().multiplyScalar(RE + 260).applyAxisAngle(V(0, 1, 0), 0.25 + a).add(V(0, 60, 0)); look = cn.clone().multiplyScalar(30); } }
  else if (t < tVon - 0.05) { closeBeam = true; S1.g.visible = true; const { p, ground } = satAt(S1, 35, -119, 8, t); setBeam(0, p, ground, t > tIm ? 1 : 0.6); S1.glint.material.opacity = 0.8; const f = K.eio(prog(t, tDer, 2)); const side = p.clone().normalize().cross(V(0, 1, 0)).normalize();
    pos = p.clone().add(side.clone().multiplyScalar(lerp(16, 7.5, f))).add(p.clone().normalize().multiplyScalar(lerp(7, 4, f))).add(V(0, lerp(3, 2, f), 0)); look = p.clone().add(p.clone().normalize().multiplyScalar(0.4)); E.look([1, 1, 1], [0, 0, 0], 0.3, 0.88); }
  else if (t < tBest - 0.05) { scene = sky; const md = dirAA(31, 15).multiplyScalar(900); mirO.position.copy(md); mirStar.forEach((s, i) => { s.position.copy(md); s.material.opacity = (i ? 0.7 : 1) * cl((t - tVon - 0.3) / 0.8); }); pos = V(0, 0, 0); look = dirAA(25, 7).multiplyScalar(100); fov = 50; }
  else if (t < tUnd - 0.05) { scene = park; const on = cl((t - tBest - 0.4) / 0.8); spot.intensity = 9 * on; parkBeam.material.opacity = 0; parkStar.forEach((p, i) => (p.material.opacity = on * (i ? 0.6 : 1))); const f = prog(t, tBest, tUnd - tBest); pos = V(lerp(-95, -80, f), lerp(22, 18, f), lerp(110, 90, f)); look = V(15, 38, -70); fov = 48; }
  else if (t < tAber - 0.05) { many.material.opacity = cl((t - tUnd - 0.5) / 1.5); const a = (t - tUnd) * 0.04; pos = V(Math.sin(a) * 430, 120, Math.cos(a) * 430); look = V(0, 0, 0); }
  else { scene = sky; const md = dirAA(32, 18).multiplyScalar(900); mirO.position.copy(md); mirStar.forEach((s, i) => { s.position.copy(md); s.material.opacity = i ? 0.7 : 1; }); fov = 56;
    const nT = t < tDieS ? Math.floor(cl((t - tAber) / 3) * 25) : 40; const T = t;
    trails.forEach((tr, i) => { if (i >= nT) { tr.m.visible = false; return; } tr.m.visible = true; const ph = ((T * tr.sp) / 60 + tr.t0) % 1; const az0 = tr.a0, alt = tr.alt0; const d1 = dirAA(alt + Math.sin(tr.dir) * 20 * ph, az0 + Math.cos(tr.dir) * 40 * ph).multiplyScalar(800), d2 = dirAA(alt + Math.sin(tr.dir) * 20 * (ph - 0.12), az0 + Math.cos(tr.dir) * 40 * (ph - 0.12)).multiplyScalar(800);
      place(tr.m, d2, d1, 1.8, 0.55); });
    if (t >= tWer - 0.05) scope.visible = true; if (t < tWer - 0.05) { const a = (t - tAber) * 0.6; pos = V(0, 0, 0); look = dirAA(28, 10 + a).multiplyScalar(100); }
    else { const f = K.eio(prog(t, tWer, 1.5)); pos = V(lerp(0, -12, f), lerp(0, 3, f), lerp(0, 30, f)); look = scope.position.clone().add(V(0, 12, -6)).lerp(dirAA(32, 18).multiplyScalar(100), 0.3); fov = 46; if (t > tWer + 2.4) E.grade.uniforms.flash.value = 0.25 * Math.sin(Math.PI * prog(t, tWer + 2.4, 0.8)); } }
  if (!(scene === sky && t >= tAber - 0.05)) trails.forEach((tr) => (tr.m.visible = false));
  if (scene !== park) { spot.intensity = 0; parkBeam.material.opacity = 0; parkStar.forEach((p) => (p.material.opacity = 0)); }
  cam.fov = fov; cam.near = 0.05; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tDie + 0.2, tIhr - 0.1, "Reflect Orbital<div class='sub'>Kalifornien, USA</div>");
  seg(W("achtzehn") - 0.1, W("sein", 24.4) - 0.1, "18 m breit");
  seg(tIm, W("er", 30) - 0.1, "✓ erlaubt<div class='sub'>Juli 2026</div>"); seg(W("er", 30), tVon - 0.1, "Start: noch 2026?");
  seg(W("viermal") - 0.2, tBest - 0.1, "bis zu 4× heller<div class='sub'>als der Vollmond</div>");
  seg(W("solarparks") - 0.3, tUnd - 0.1, "☀️ Solarstrom<div class='sub'>auch nachts</div>");
  seg(W("zweitausendfünfunddreißig") - 0.1, tAber - 0.1, "bis 2035: ≈ 50.000 Spiegel");
  seg(W("fast") - 0.1, tDieS - 0.1, "≈ 2.000 Beschwerden");
  seg(W("nachthimmel", 58) - 0.1, W("teleskope") - 0.1, "🌌 Nachthimmel"); seg(W("teleskope") - 0.1, W("piloten") - 0.1, "🔭 Teleskope"); seg(W("piloten") - 0.1, tWer - 0.1, "✈️ Piloten");
  seg(W("augen") - 0.4, 69, "⚠️ Gefahr für die Augen");
  word(wh, wa); cap(t);
};
