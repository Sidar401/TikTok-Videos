const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(127);
// @modelle
const sunT = await tex("sun.jpg");
// ===== Starmind-Satellit (flach wie Starlink, ein langes Solarsegel, KI-Chip) =====
const satM = MO.plain(0xcfd2d6, 0.35, 0.5, 0.5);
function starmind() { const g = new THREE.Group(); const body = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.22, 1.4), satM); g.add(body);
  const top = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.03, 1.2), MO.plain(0x2a2d33, 0.6, 0.35)); top.position.y = 0.125; g.add(top);
  const chip = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.05, 0.7), new THREE.MeshBasicMaterial({ color: 0xa78bfa, toneMapped: false })); chip.position.set(-0.6, 0.15, 0); g.add(chip);
  const chipG = K.sprite(g, K.glowTex("rgba(170,140,255,1)"), 2.2, V(-0.6, 0.25, 0), 0);
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.2, 8), MO.plain(0x8a8f96, 0.7, 0.3)); arm.rotation.z = Math.PI / 2; arm.position.set(1.9, 0, 0); g.add(arm);
  const pan = new THREE.Group(); pan.position.set(2.5, 0, 0); g.add(pan); const cells = new THREE.Mesh(new THREE.BoxGeometry(9, 0.04, 2.4), MO.cellM()); cells.position.x = 4.5; pan.add(cells);
  const back = new THREE.Mesh(new THREE.BoxGeometry(9.02, 0.02, 2.42), MO.plain(0xd8dadd, 0.4, 0.5)); back.position.set(4.5, -0.03, 0); pan.add(back); pan.rotation.x = -0.35;
  for (const s of [-1, 1]) { const ph = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.12, 20), MO.plain(0xe6e6e8, 0.3, 0.4)); ph.position.set(s * 0.9 + 0.2, -0.16, 0.3); g.add(ph); }
  return { g, chip, chipG }; }
// ================= Orbit: Erde + Satelliten-Hülle =================
const so = new THREE.Scene(); K.stars(so, 9000, -1, 60000, 1.7).material.opacity = 0.7; so.add(new THREE.AmbientLight(0x30343e, 0.6));
const sunL = new THREE.DirectionalLight(0xfff2e0, 2.0); sunL.position.set(-1, 0.3, 0.4); so.add(sunL); const sunS = K.sprite(so, K.glowTex("rgba(255,235,200,1)"), 4000, V(-30000, 9000, 12000), 0.9);
const RE = 100; const EA = K.earth(so, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-1, 0.3, 0.4).normalize();
// Punkte: erst 17.000 (davon 2/3 SpaceX blau), dann 1 Mio. (dargestellt mit 250.000 Punkten)
const shell = (n, rMin, rMax, seed, colA, colB, share) => { K.reseed(seed); const p = new Float32Array(n * 3), c = new Float32Array(n * 3); const A = new THREE.Color(colA), B = new THREE.Color(colB);
  for (let i = 0; i < n; i++) { const u = K.rnd() * 2 - 1, a = K.rnd() * 6.2832; const ring = K.rnd() < 0.6; const r = rMin + (rMax - rMin) * K.rnd(); let x = Math.sqrt(1 - u * u) * Math.cos(a), y = u, z = Math.sqrt(1 - u * u) * Math.sin(a);
    if (ring) { const inc = [0.53, 1.71, 0.95][i % 3], node = (i * 0.618) % 1 * 6.2832; const ca = Math.cos(a), sa = Math.sin(a); x = ca; y = sa * Math.sin(inc); z = sa * Math.cos(inc); const xx = x * Math.cos(node) - z * Math.sin(node), zz = x * Math.sin(node) + z * Math.cos(node); x = xx; z = zz; }
    p[i * 3] = x * r; p[i * 3 + 1] = y * r; p[i * 3 + 2] = z * r; const col = K.rnd() < share ? A : B; c[i * 3] = col.r; c[i * 3 + 1] = col.g; c[i * 3 + 2] = col.b; }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); g.setAttribute("color", new THREE.BufferAttribute(c, 3));
  const m = new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false }); const P = new THREE.Points(g, m); so.add(P); return P; };
const NOW = shell(17000, RE * 1.08, RE * 1.2, 3, 0x7ab8ff, 0xffffff, 0.66);
NOW.material.size = 2.8; const MIO = shell(250000, RE * 1.08, RE * 1.16, 9, 0xc4b5fd, 0xffe7b0, 0.85); MIO.material.size = 1.2;
const hi = (r, col) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 96, 64), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, wireframe: true, toneMapped: false, depthWrite: false })); so.add(m); return m; };
const ringM = (r, col) => { const m = new THREE.Mesh(new THREE.TorusGeometry(r, 0.35, 8, 256), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, toneMapped: false })); m.rotation.x = Math.PI / 2 - 0.25; so.add(m); const o = new THREE.Object3D(); o.position.set(r, 0, 0); m.add(o); return { m, o }; };
const H500 = ringM(RE * 1.08 + 6, 0x7ab8ff), H1000 = ringM(RE * 1.16 + 14, 0xffd23f);
// Nahaufnahme-Szene: Satellit über großer Erde
const sn = new THREE.Scene(); K.stars(sn, 9000, -1, 60000, 1.7).material.opacity = 0.7; sn.add(new THREE.AmbientLight(0x30343e, 0.7));
const snL = new THREE.DirectionalLight(0xfff2e0, 2.0); snL.position.set(-1, 0.3, 0.4); sn.add(snL); const snSun = K.sprite(sn, K.glowTex("rgba(255,235,200,1)"), 4000, V(-30000, 9000, 12000), 0.9);
const R2 = 600; const EB = K.earth(sn, { day, night, topo }, R2); EB.group.children[EB.group.children.length - 1].scale.setScalar(0.93); EB.U.sun.value = V(-1, 0.3, 0.4).normalize(); EB.group.position.set(0, -R2 * 1.45, 0);
const SM = starmind(); sn.add(SM.g); const smO = new THREE.Object3D(); SM.g.add(smO); smO.position.set(6, 0.8, -0.5);
const flock = []; for (let i = 0; i < 14; i++) { const s = starmind(); s.g.position.set((i % 7 - 3) * 16 + (i > 6 ? 8 : 0), i > 6 ? -6 : 0, -10 - Math.floor(i / 7) * 20); sn.add(s.g); flock.push(s); }
const beamM = new THREE.LineBasicMaterial({ color: 0x7ab8ff, transparent: true, opacity: 0, toneMapped: false }); const beams = [];
// ================= Rechenzentrum auf der Erde =================
const sd = new THREE.Scene(); sd.add(new THREE.AmbientLight(0x404858, 0.5)); const ld = new THREE.PointLight(0x9fb4ff, 60, 120, 1.4); ld.position.set(0, 12, 10); sd.add(ld);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), MO.plain(0x16181d, 0.3, 0.6)); floor.rotation.x = -Math.PI / 2; floor.position.y = -1.05; sd.add(floor);
const racks = []; for (let r = 0; r < 2; r++) for (let i = 0; i < 26; i++) { const k = MO.rack(); k.g.position.set(r ? 1.8 : -1.8, 0, -i * 1.15); k.g.rotation.y = r ? -Math.PI / 2 : Math.PI / 2; sd.add(k.g); racks.push(k); }
// ================= Starship =================
const steel = MO.plain(0xc9ced6, 0.75, 0.3, 0.6), dark = MO.plain(0x1c1e22, 0.5, 0.5);
function makeBooster() { const g = new THREE.Group(); const c = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 4.5, 72, 48), steel); c.position.y = 36; g.add(c);
  const e = new THREE.Mesh(new THREE.CylinderGeometry(4.6, 4.2, 2.5, 48), dark); e.position.y = 1; g.add(e);
  for (let i = 0; i < 4; i++) { const f = new THREE.Mesh(new THREE.BoxGeometry(3.5, 4, 0.5), dark); const a = i * Math.PI / 2 + 0.4; f.position.set(Math.cos(a) * 5.2, 68, Math.sin(a) * 5.2); f.rotation.y = -a; g.add(f); }
  const ring = new THREE.Mesh(new THREE.CylinderGeometry(4.55, 4.55, 1.2, 48), dark); ring.position.y = 70; g.add(ring); return g; }
function makeShip() { const g = new THREE.Group(); const tc = document.createElement("canvas"); tc.width = 256; tc.height = 64; const q = tc.getContext("2d"); q.fillStyle = "#c9ced6"; q.fillRect(0, 0, 256, 64); q.fillStyle = "#16181c"; q.fillRect(0, 0, 128, 64);
  const tm = new THREE.MeshStandardMaterial({ map: new THREE.CanvasTexture(tc), metalness: 0.3, roughness: 0.42 });
  const pts = []; for (let i = 0; i <= 20; i++) { const y = i / 20; pts.push(new THREE.Vector2(4.5 * Math.sqrt(1 - Math.pow(y, 2.2)), 38 + y * 14)); }
  g.add(new THREE.Mesh(new THREE.LatheGeometry(pts, 48), tm)); const body = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 4.5, 38, 48), tm); body.position.y = 19; g.add(body);
  [[-1, 6], [1, 6], [-1, 42], [1, 42]].forEach(([s, y]) => { const f = new THREE.Mesh(new THREE.BoxGeometry(0.5, y > 20 ? 6 : 9, 4), dark); f.position.set(s * 5, y, 0); g.add(f); }); return g; }
const sr = new THREE.Scene(); K.reseed(6); K.stars(sr, 7000, -1, 20000, 1.6); K.sky(sr, 0x02040a, 0x0a1a3a, 0x24406e, 15000); sr.add(new THREE.AmbientLight(0x404858, 0.7)); const lr = new THREE.DirectionalLight(0xfff2e0, 1.4); lr.position.set(300, 200, 400); sr.add(lr);
const ROCK = new THREE.Group(); sr.add(ROCK); const BO = makeBooster(); ROCK.add(BO); const SH = makeShip(); SH.position.y = 72; ROCK.add(SH); const rkO = new THREE.Object3D(); ROCK.add(rkO); rkO.position.set(0, 128, 0);
const padM = new THREE.Mesh(new THREE.CylinderGeometry(40, 40, 2, 48), MO.plain(0x55585e, 0.2, 0.8)); padM.position.y = -3; sr.add(padM);
const flame = MO.exhaust(70, 5); flame.position.y = -1; ROCK.add(flame); const fireG = K.sprite(sr, K.glowTex("rgba(255,170,80,1)"), 120, V(0, 0, 0), 0); const smoke = MO.smoke(sr, 60);
// ================= Teleskop-Bild mit Satelliten-Strichen =================
const st = new THREE.Scene(); { K.reseed(31); const p = [], c = []; for (let i = 0; i < 40000; i++) { p.push((K.rnd() - 0.5) * 3000, (K.rnd() - 0.5) * 5400, -K.rnd() * 50); const col = new THREE.Color(1, 0.93, 0.86).lerp(new THREE.Color(0.65, 0.75, 1), K.rnd()); c.push(col.r, col.g, col.b); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(c, 3)); st.add(new THREE.Points(g, new THREE.PointsMaterial({ size: 1.8, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false })));
  for (let i = 0; i < 4; i++) K.sprite(st, K.glowTex(i % 2 ? "rgba(255,170,130,.5)" : "rgba(150,180,255,.5)"), 400 + K.rnd() * 300, V((K.rnd() - 0.5) * 1600, (K.rnd() - 0.5) * 2600, -60), 0.35); }
const streaks = []; for (let i = 0; i < 9; i++) { K.reseed(400 + i); const a = V((K.rnd() - 0.5) * 900, (K.rnd() - 0.5) * 1600, 0), d = V(K.rnd() - 0.5, K.rnd() - 0.5, 0).normalize(); const geo = new THREE.PlaneGeometry(1, 4); const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, toneMapped: false })); m.rotation.z = Math.atan2(d.y, d.x); st.add(m); streaks.push({ m, a, d, t0: i * 0.55 }); }
// ===== Zeiten =====
const tDie = W("die", 4), tDas = W("das", 8.4), tHeute = W("heute"), tEine = W("eine", 18.3), tAber = W("aber", 21.7), tIn = W("in", 26.3), tDenn = W("denn"), tIm = W("im", 35.9), tErg = W("die", 38.8), tFlieg = W("fliegen"), tErst = W("der", 47.6), tAstro = W("astronomen"), tUnd = W("und", 59.7), tWas = W("was", 63.5), END = 67.4, KARTE = 10.72;
label("500 km", H500.o, 1, { t0: W("fünfhundert"), t1: tErst - 0.1, size: 48, gap: 10 }); label("1.000 km", H1000.o, 1, { t0: W("tausend", 44), t1: tErst - 0.1, size: 48, gap: 10 });
label("Starmind", smO, 1, { t0: tDas + 0.3, t1: tHeute - 0.1, size: 64, gap: 24 }); label("Starship", rkO, 4, { t0: W("starship") - 0.2, t1: tAstro - 0.1, size: 56, gap: 20 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = so, pos = V(0, 30, 300), look = V(0, 0, 0), fov = 42; EA.group.rotation.y = 2.0 + t * 0.01; EA.clouds.rotation.y = t * 0.004;
  NOW.visible = false; MIO.visible = false; MIO.geometry.setDrawRange(0, 250000); H500.m.material.opacity = 0; H1000.m.material.opacity = 0; EB.group.rotation.y = 2.0 + t * 0.006; EB.clouds.rotation.y = t * 0.003; SM.g.visible = false; flock.forEach((s) => (s.g.visible = false)); beamM.opacity = 0;
  NOW.rotation.y = MIO.rotation.y = t * 0.02; const chipOn = (s, k) => { s.chip.material.color.setRGB(0.25 + 0.4 * k, 0.2 + 0.35 * k, 0.4 + 0.6 * k); s.chipG.material.opacity = k * (0.7 + 0.3 * Math.sin(t * 5)); };
  SM.g.position.set(0, 0, 0); SM.g.rotation.set(0, 0.6 + t * 0.05, 0); chipOn(SM, 0.3); flame.visible = false; fireG.material.opacity = 0; smoke.forEach((s) => (s.material.opacity = 0)); ROCK.position.y = 0;
  const atSat = (dx, dy, dz) => SM.g.position.clone().add(V(dx, dy, dz));
  if (t < tDie - 0.05) { const f = K.eio(prog(t, 0, tDie)); MIO.visible = true; const d = lerp(330, 520, f); const a = 0.5 + f * 0.3; pos = V(Math.sin(a) * d, lerp(60, 130, f), Math.cos(a) * d); }
  else if (t < tHeute - 0.05) { scene = sn; const f = prog(t, tDie, tHeute - tDie); SM.g.visible = true; chipOn(SM, cl((t - tDas) / 1)); SM.g.rotation.set(0.15, 0.4 + f * 0.9, 0.05); pos = atSat(lerp(7, 3, f), 13, 17); look = atSat(4, -1.5, 0); fov = 50; }
  else if (t < tEine - 0.05) { const f = prog(t, tHeute, tEine - tHeute); NOW.visible = true; const a = 0.2 + f * 0.6; const d = lerp(360, 300, f); pos = V(Math.sin(a) * d, 90, Math.cos(a) * d); look = V(0, 0, 0); }
  else if (t < tAber - 0.05) { const f = prog(t, tEine, tAber - tEine); MIO.visible = true; MIO.geometry.setDrawRange(0, Math.floor(lerp(17000, 250000, K.eio(cl(f * 1.4))))); const a = 0.8 + f * 0.4; const d = lerp(300, 380, f); pos = V(Math.sin(a) * d, 90, Math.cos(a) * d); }
  else if (t < tIn - 0.05) { scene = sn; const f = prog(t, tAber, tIn - tAber); SM.g.visible = true; chipOn(SM, cl((t - W("denken") + 0.2) / 0.6)); SM.g.rotation.set(0.3, 1.2 + f * 0.3, 0); pos = atSat(-3 + f * 2, 8, 13); look = atSat(2.5, -0.5, 0); fov = 48; }
  else if (t < tDenn - 0.05) { scene = sn; const f = prog(t, tIn, tDenn - tIn); SM.g.visible = true; chipOn(SM, 1); SM.g.rotation.set(0.2, 2.2 + f * 0.6, 0); const d = lerp(14, 34, K.eio(f)); pos = atSat(-d * 0.5, d * 0.35 + 3, d); look = atSat(4, -d * 0.15, 0); fov = 44; }
  else if (t < tIm - 0.05) { scene = sd; racks.forEach((k) => k.leds.forEach((l, i) => (l.visible = Math.sin(t * 7 + i * 2.3 + k.g.position.z) > -0.3))); const f = prog(t, tDenn, tIm - tDenn); pos = V(0, lerp(1.2, 1.6, f), lerp(4, -14, f)); look = V(0, 0.4, lerp(-6, -26, f)); fov = 52; }
  else if (t < tErg - 0.05) { scene = sn; const f = prog(t, tIm, tErg - tIm); SM.g.visible = true; chipOn(SM, 1); SM.g.rotation.set(0.7, -0.4 + f * 0.3, 0.1); pos = V(lerp(26, 20, f), -5, lerp(-8, -6, f)); look = V(-12, 3, 4); fov = 50; }
  else if (t < tFlieg - 0.05) { scene = sn; const f = prog(t, tErg, tFlieg - tErg); flock.forEach((s) => { s.g.visible = true; s.g.position.y += 0; chipOn(s, 1); }); flock.forEach((s, i) => s.g.position.set((i % 7 - 3) * 16 + (i > 6 ? 8 : 0), (i > 6 ? -6 : 0), -10 - Math.floor(i / 7) * 20)); beamM.opacity = 0.7 * cl((t - tErg - 0.6) / 0.5);
    if (!beams.length) flock.forEach((s) => { const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(0, -250, 0)]), beamM); s.g.add(l); beams.push(l); });
    const a = 0.3 + f * 0.3; pos = V(Math.sin(a) * 110, 35, Math.cos(a) * 110); look = V(0, -30, -20); fov = 46; }
  else if (t < tErst - 0.05) { const f = prog(t, tFlieg, tErst - tFlieg); NOW.visible = true; H500.m.material.opacity = 0.9 * cl((t - W("fünfhundert") + 0.1) / 0.5); H1000.m.material.opacity = 0.9 * cl((t - W("tausend", 44) + 0.1) / 0.5); const a = 1.0 + f * 0.3; pos = V(Math.sin(a) * 380, 110, Math.cos(a) * 380); }
  else if (t < tAstro - 0.05) { scene = sr; const f = prog(t, tErst, tAstro - tErst); const k = cl((t - tErst - 1.2) / 4.5); flame.visible = true; fireG.material.opacity = 0.9; ROCK.position.y = 200 * k * k; fireG.position.set(0, ROCK.position.y - 10, 0); fireG.scale.setScalar(110 + 40 * Math.sin(t * 30));
    smoke.forEach((s, i) => { const kk = ((i / smoke.length) + t * 0.25) % 1; s.position.set(Math.sin(i * 7.3) * (8 + kk * 110), 2 + kk * 30, Math.cos(i * 3.1) * (8 + kk * 110)); s.scale.setScalar(30 + kk * 90); s.material.opacity = 0.28 * (1 - kk); });
    pos = V(150, 30 + ROCK.position.y * 0.6, 260); look = V(0, 60 + ROCK.position.y * 0.9, 0); fov = 46; }
  else if (t < tUnd - 0.05) { scene = st; const f = prog(t, tAstro, tUnd - tAstro); fov = 50; pos = V(0, 0, lerp(2600, 2200, f)); look = V(0, 0, 0);
    streaks.forEach((s) => { const k = cl((t - tAstro - 1.0 - s.t0) / 1.2); const L = 3000 * k; s.m.position.z = 5; s.m.scale.set(Math.max(1, L), 1, 1); s.m.position.copy(s.a.clone().add(s.d.clone().multiplyScalar(L / 2 - 1500))); s.m.material.opacity = k > 0 ? 0.85 : 0; }); }
  else if (t < tWas - 0.05) { scene = sn; const f = prog(t, tUnd, tWas - tUnd); flock.forEach((s, i) => { s.g.visible = true; chipOn(s, 0.5 + 0.5 * Math.sin(t * 2 + i)); s.g.position.set((i % 7 - 3) * 16 + (i > 6 ? 8 : 0), (i > 6 ? -6 : 0), -10 - Math.floor(i / 7) * 20); }); const a = -0.4 + f * 0.5; pos = V(Math.sin(a) * 70, 30, Math.cos(a) * 70); look = V(0, -12, -20); fov = 48; }
  else { const f = prog(t, tWas, END - tWas); MIO.visible = true; const a = 2.0 + f * 0.4; const d = lerp(330, 420, f); pos = V(Math.sin(a) * d, lerp(70, 110, f), Math.cos(a) * d); }
  cam.fov = fov; cam.near = 0.05; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("fcc") - 0.2, tDas - 0.1, logo("fcc.svg", 80) + "✅ erlaubt"); seg(W("eine", 18.3) - 0.1, tAber - 0.1, "17.000 ➜ <span class='y' style='color:#ffd23f'>1.000.000</span>");
  seg(W("denken") - 0.1, tIn + 2.5, "🧠 KI im All"); seg(W("starlink") - 0.2, tFlieg - 0.1, logo("starlink.svg", 60)); seg(W("zweitausendsiebenundzwanzig") - 0.1, tAstro - 0.1, "🚀 2027");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
