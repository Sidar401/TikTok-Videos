// Sonne im leuchtenden Raumzeit-Gitter, Planeten mit echten Oberflächen kreisen
const sc = new THREE.Scene();
const st = K.stars(sc, 4000, -1, 20000, 1.8); st.material.opacity = 0.6;
sc.add(new THREE.AmbientLight(0x3a3230, 0.9)); const fill = new THREE.DirectionalLight(0xffe2c8, 1.1); sc.add(fill);
const pL = new THREE.PointLight(0xfff0dd, 4.5, 0, 0); sc.add(pL);
const WELL = (x, z, extra) => { const r2 = x * x + z * z; let h = -58 * Math.exp(-r2 / (2 * 40 * 40)); extra.forEach((p) => { const dx = x - p.x, dz = z - p.z; h -= p.m * Math.exp(-(dx * dx + dz * dz) / (2 * p.s * p.s)); }); return h; };
// Gitterlinien
const N = 61, SZ = 420, STP = SZ / (N - 1), SEG = 220; const pos = [], col = [];
const pushLine = (fx) => { for (let k = 0; k < SEG; k++) { const a = fx(k / SEG), b = fx((k + 1) / SEG); pos.push(...a, ...b); col.push(0, 0, 0, 0, 0, 0); } };
const lines = []; for (let i = 0; i < N; i++) { const c = -SZ / 2 + i * STP; lines.push({ dir: 0, c }); lines.push({ dir: 1, c }); }
lines.forEach(() => pushLine(() => [0, 0, 0]));
const gg = new THREE.BufferGeometry(); gg.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); gg.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
const grid = new THREE.LineSegments(gg, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false, fog: false })); sc.add(grid);
const updGrid = (extra) => { const P = gg.attributes.position, C = gg.attributes.color; let v = 0;
  lines.forEach((L) => { for (let k = 0; k <= SEG; k++) { if (k > 0 && k < SEG) { /* zwei Punkte pro Segment */ } } for (let k = 0; k < SEG; k++) for (let e = 0; e < 2; e++) { const u = -SZ / 2 + ((k + e) / SEG) * SZ; const x = L.dir ? u : L.c, z = L.dir ? L.c : u; const y = WELL(x, z, extra);
    const r = Math.sqrt(x * x + z * z); const fade = Math.max(0, 1 - r / (SZ * 0.5)); const hot = Math.exp(-r / 70);
    P.setXYZ(v, x, y, z); C.setXYZ(v, (0.55 + 0.45 * hot) * fade, (0.06 + 0.4 * hot) * fade, (0.04 + 0.1 * hot) * fade); v++; } });
  P.needsUpdate = true; C.needsUpdate = true; };
// Sonne
const sunR = 20; const sun = new THREE.Mesh(new THREE.SphereGeometry(sunR, 128, 96), new THREE.MeshBasicMaterial({ map: await tex("sun.jpg"), color: new THREE.Color(1.15, 0.85, 0.6), toneMapped: false })); sc.add(sun);
const sy = -58 + sunR * 0.75; sun.position.y = sy; pL.position.set(0, sy, 0);
K.sprite(sc, K.glowTex("rgba(255,120,30,.5)"), 80, V(0, sy, 0), 0.55); K.sprite(sc, K.glowTex("rgba(255,190,110,.45)"), 52, V(0, sy, 0), 0.5);
const pool = K.sprite(sc, K.glowTex("rgba(255,110,30,.5)"), 160, V(0, -50, 0), 0.3);
// Planeten
const ball = async (f, r) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 96, 64), new THREE.MeshStandardMaterial({ map: await tex(f), roughness: 1 })); sc.add(m); return m; };
const PL = [{ m: await ball("mercury.jpg", 3.4), R: 38, w: 0.42, ph: 1.0, mass: 2, s: 6 }, { m: await ball("venus_atmosphere.jpg", 5.4), R: 54, w: 0.3, ph: 3.6, mass: 4, s: 8 },
  { m: null, R: 72, w: 0.24, ph: 5.1, mass: 4, s: 8, r: 5.6 }, { m: await ball("mars.jpg", 4.2), R: 92, w: 0.18, ph: 0.2, mass: 3, s: 7 }, { m: await ball("jupiter.jpg", 15), R: 140, w: 0.09, ph: 2.25, mass: 12, s: 16 }];
const EA = K.earth(sc, { day, night, topo }, 5.6); PL[2].m = EA.group; EA.group.children[EA.group.children.length - 1].scale.setScalar(0.92);
const moon = await ball("moon.jpg", 1.5);
PL.forEach((p) => { const o = new THREE.Mesh(new THREE.RingGeometry(p.R - 0.12, p.R + 0.12, 256), new THREE.MeshBasicMaterial({ color: 0xffb070, transparent: true, opacity: 0.18, side: THREE.DoubleSide, depthWrite: false })); o.rotation.x = -Math.PI / 2; o.position.y = 2; sc.add(o); p.orbit = o; });
label("Sonne", sun, sunR, { t0: 1.0, t1: 7.6, size: 84 });
label("Erde", EA.group, 5.6, { t0: 4.0, t1: 6.6, size: 56, gap: 20 });
label("Jupiter", PL[4].m, 15, { t0: 2.6, t1: 8.6, size: 64, gap: 24 });
renderAt = (t) => {
  E.look([1.02, 0.98, 0.96], [0, 0, 0], 0.4, 0.85); E.grade.uniforms.flash.value = 0;
  const extra = PL.map((p) => { const a = p.ph + t * p.w; const x = Math.cos(a) * p.R, z = Math.sin(a) * p.R; return { x, z, m: p.mass, s: p.s }; });
  PL.forEach((p, i) => { const e = extra[i]; const r = p.r ?? p.m.geometry.parameters.radius; const y = WELL(e.x, e.z, extra) + r * 1.05; p.m.position.set(e.x, y, e.z); p.m.rotation.y = t * 0.3; p.orbit.position.y = WELL(p.R, 0, []) + 0.5; });
  const ep = EA.group.position; moon.position.set(ep.x + Math.cos(t * 1.4) * 9, ep.y + 1.5, ep.z + Math.sin(t * 1.4) * 9); moon.rotation.y = t;
  EA.mesh.rotation.y = t * 0.3; EA.clouds.rotation.y = t * 0.33; EA.U.sun.value.copy(V(0, sy, 0).sub(ep).normalize());
  sun.rotation.y = t * 0.05; updGrid(extra);
  const f = K.eio(prog(t, 0, 15)); const ang = lerp(2.0, 0.95, f), dist = lerp(205, 250, f), h = lerp(16, 95, f);
  const jp = PL[4].m.position; const look = V(0, lerp(-6, -24, f), 0);
  fill.position.copy(cam.position); cam.fov = 42; cam.updateProjectionMatrix(); cam.position.set(Math.cos(ang) * dist, h, Math.sin(ang) * dist); cam.lookAt(look);
  E.render(sc, t); updLabels(t);
  word("Raumzeit<div style='font:600 42px Inter,sans-serif;color:rgba(255,255,255,.75);margin-top:12px'>Die Sonne verbiegt den Raum</div>", cl((t - 9.2) / 0.6));
};
