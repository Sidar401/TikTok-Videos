const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(31);
// ===== Himmel am Morgen (Blick nach Südosten) =====
const sky = new THREE.Scene();
K.sky(sky, 0x02040c, 0x0b1430, 0x2a3358, 4000);
const st = K.stars(sky, 3500, 0.02, 3800, 2.0); st.material.opacity = 0.8;
const dawn = K.sprite(sky, K.glowTex("rgba(255,150,80,.6)"), 3200, V(-1500, -300, -2600), 0.55);
const dawn2 = K.sprite(sky, K.glowTex("rgba(255,200,140,.35)"), 1600, V(-1300, -60, -2700), 0.5);
function hills(z, h, col, seed) { K.reseed(seed); const pts = [new THREE.Vector2(-4000, -60)]; for (let x = -4000; x <= 4000; x += 40) pts.push(new THREE.Vector2(x, h * (0.5 + 0.5 * Math.sin(x * 0.002 + seed) * Math.cos(x * 0.0037 + seed * 2)) + K.rnd() * h * 0.06)); pts.push(new THREE.Vector2(4000, -60));
  const m = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts)), new THREE.MeshBasicMaterial({ color: col, fog: false })); m.position.z = z; sky.add(m); }
hills(-2000, 120, 0x05070d, 3); hills(-1000, 70, 0x030409, 7); hills(-400, 28, 0x010204, 11);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(9000, 9000), new THREE.MeshBasicMaterial({ color: 0x010204 })); ground.rotation.x = -Math.PI / 2; ground.position.y = 1; sky.add(ground);
// echte Höhen/Richtungen (16.11., 6:30 Uhr), seitlich etwas zusammengerückt
const SKYR = 2600, AZ0 = 150;
const skyPos = (alt, az) => { const a = (alt * Math.PI) / 180, z = (((az - AZ0) * 0.6) * Math.PI) / 180; return V(Math.sin(z) * Math.cos(a) * SKYR, Math.sin(a) * SKYR, -Math.cos(z) * Math.cos(a) * SKYR); };
// Darstellung: alle 4 in einem Bild (Reihenfolge und Richtung wie am echten Himmel)
const SP = { me: V(-680, 170, -2600), ve: V(-430, 520, -2600), ma: V(330, 1560, -2600), ju: V(400, 1500, -2600) };
const dot = (p, col, s, h) => { K.sprite(sky, K.glowTex(col), s, p, 1); return K.sprite(sky, K.glowTex(col.replace(/[\d.]+\)$/, ".25)")), h, p, 0.9); };
const dMe = dot(SP.me, "rgba(255,235,215,1)", 20, 60), dVe = dot(SP.ve, "rgba(255,255,250,1)", 46, 170), dMa = dot(SP.ma, "rgba(255,130,80,1)", 24, 70), dJu = dot(SP.ju, "rgba(255,248,230,1)", 38, 130);
const chain = new THREE.Line(new THREE.BufferGeometry().setFromPoints([SP.me, SP.ve, SP.ma.clone().lerp(SP.ju, 0.5)]), new THREE.LineDashedMaterial({ color: 0xffd23f, dashSize: 30, gapSize: 24, transparent: true, opacity: 0 }));
chain.computeLineDistances(); sky.add(chain);

// ===== Weltall: echte Kugeln =====
const sp = new THREE.Scene(); K.stars(sp, 5000, -1, 30000, 1.6).material.opacity = 0.5;
const Ld = V(-1, 0.3, 0.8).normalize(); const sl = new THREE.DirectionalLight(0xfff6ea, 3.2); sl.position.copy(Ld.clone().multiplyScalar(100)); sp.add(sl);
sp.add(new THREE.AmbientLight(0x30323a, 0.6)); const fill = new THREE.DirectionalLight(0xdde6ff, 0.6); sp.add(fill);
const T = { me: await tex("mercury.jpg"), ve: await tex("venus_atmosphere.jpg"), ma: await tex("mars.jpg"), ju: await tex("jupiter.jpg") };
const ball = (k, r, p) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshStandardMaterial({ map: T[k], roughness: 1 })); m.position.copy(p); sp.add(m); return m; };
// Reihe (Diagonale wie am Himmel)
const me = ball("me", 2.4, V(-11, -27, 0)), ve = ball("ve", 5.2, V(-5, -13, 0)), ma = ball("ma", 3.4, V(3, 4, 0)), ju = ball("ju", 10, V(12, 22, 0));
// Abstands-Linie (1 Einheit = 1 Mio. km), weit weg aufgebaut
const LX = 6000, D = { ve: 50, me: 131, ma: 195, ju: 787 };
const EA = K.earth(sp, { day, night, topo }, 13); EA.group.position.set(LX, 0, 0); EA.U.sun.value.copy(Ld); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93);
const lVe = ball("ve", 11, V(LX - 4, D.ve, 0)), lMe = ball("me", 8, V(LX + 3, D.me, 0)), lMa = ball("ma", 10, V(LX - 2, D.ma, 0)), lJu = ball("ju", 42, V(LX + 6, D.ju, 0));
const ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(LX, 0, -2), V(LX + 6, D.ju, -2)]), new THREE.LineDashedMaterial({ color: 0xffffff, dashSize: 12, gapSize: 10, transparent: true, opacity: 0.35 })); ln.computeLineDistances(); sp.add(ln);
const pulseV = K.sprite(sp, K.glowTex("rgba(255,240,200,1)"), 34, V(0, 0, 0), 0), pulseJ = K.sprite(sp, K.glowTex("rgba(255,240,200,1)"), 46, V(0, 0, 0), 0);

// ===== Zeiten =====
const tEs = W("es", 9), tMe = W("merkur", 9), tVe = W("venus", 10), tMa = W("mars", 11), tJu = W("jupiter", 11.5), tSie = W("sie", 12.8), tGanz = W("ganz", 16.8), tSteht = W("steht", 19), tEtwas = W("etwas", 22.5), tFuenfzig = W("fünfzig"), tHoch = W("hoch", 30), tUnd = W("und", 33.8), tLicht = W("das", 39), tJLicht = W("das", 42.8), tDu = W("du", 46.5), tSo = W("so", 50.5), tAm = W("am", 56.4), tRies = W("riesig"), tWel = W("welchen"), tFolg = W("folg", 61);
// ===== Beschriftungen =====
label("Merkur", me, 2.4, { t0: tMe, t1: tSie - 0.1, size: 60, gap: 18 }); label("Venus", ve, 5.2, { t0: tVe, t1: tSie - 0.1, size: 60, gap: 18 });
label("Mars", ma, 3.4, { t0: tMa, t1: tSie - 0.1, size: 60, gap: 18 }); label("Jupiter", ju, 10, { t0: tJu, t1: tSie - 0.1, size: 60, gap: 18 });
const shiftL = []; const skyLab = (txt, o, a, b, size = 50) => { const L = label(txt, o, 10, { t0: a, t1: b, size, gap: 34 }); if (o === dMa) shiftL.push([L, -90]); if (o === dJu) shiftL.push([L, 90]); return L; };
skyLab("Merkur", dMe, tSie + 1.2, tGanz - 0.1); skyLab("Venus", dVe, tSie + 1.4, tGanz - 0.1); skyLab("Mars", dMa, tSie + 1.6, tGanz - 0.1, 44); skyLab("Jupiter", dJu, tSie + 1.8, tGanz - 0.1, 44);
skyLab("Merkur", dMe, tGanz + 0.6, tSteht - 0.1, 60);
label("Merkur", me, 2.4, { t0: tSteht + 0.2, t1: tEtwas - 0.1, size: 90, gap: 30 });
label("Venus", ve, 5.2, { t0: tEtwas + 0.2, t1: tHoch - 0.1, size: 90, gap: 30 });
label("Mars", ma, 3.4, { t0: tHoch + 0.6, t1: tUnd - 0.1, size: 70, gap: 24 }); label("Jupiter", ju, 10, { t0: tHoch + 0.9, t1: tUnd - 0.1, size: 80, gap: 24 });
// Abstands-Linie: Namen rechts daneben (eigene Positionierung)
const sideL = []; const side = (html, obj, r, a, b) => { const L = label(html, obj, 0, { t0: a, t1: b, size: 50, gap: 0 }); L.d.style.textAlign = "left"; sideL.push({ L, r }); return L; };
side("🌍 Erde", EA.group, 13, tUnd + 1.2, tDu - 0.1); side("Venus <small>50 Mio. km</small>", lVe, 11, tUnd + 1.5, tRies + 0.4); side("Merkur <small>131 Mio. km</small>", lMe, 8, tUnd + 1.8, tRies + 0.4);
side("Mars <small>195 Mio. km</small>", lMa, 10, tUnd + 2.1, tDu - 0.1); side("Jupiter <small>787 Mio. km</small>", lJu, 42, tRies + 1.0, tDu - 0.1);
// Licht aus verschiedenen Zeiten
[["Merkur", dMe, "vor 7 Min."], ["Venus", dVe, "vor 3 Min."], ["Mars", dMa, "vor 11 Min."], ["Jupiter", dJu, "vor 44 Min."]].forEach(([n, d, s], i) => skyLab(`${n}<small>${s}</small>`, d, tDu + 0.3 + i * 0.35, tSo - 0.1, i > 1 ? 44 : 50));
skyLab("Merkur", dMe, tWel, 99, 44); skyLab("Venus", dVe, tWel + 0.2, 99, 44); skyLab("Mars", dMa, tWel + 0.4, 99, 40); skyLab("Jupiter", dJu, tWel + 0.6, 99, 40);

renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; let scene = sky, pos = V(0, 30, 0), look = V(0, 600, -2600), fov = 62;
  chain.material.opacity = 0; pulseV.material.opacity = 0; pulseJ.material.opacity = 0;
  if (t < tEs - 0.05) { E.look([1, 1, 1], [0, 0, 0], 0.45, 0.82); const f = K.eio(prog(t, 0, tEs)); look = V(lerp(-300, 0, f), lerp(200, 900, f), -2600); fov = 62; }
  else if (t < tSie - 0.05) { scene = sp; E.look([1, 1, 1], [0, 0, 0], 0.25, 0.92); const f = prog(t, tEs, tSie - tEs); pos = V(lerp(-6, 4, f), lerp(0, 4, f), lerp(150, 135, f)); look = V(0, 3, 0); fov = 40; }
  else if (t < tGanz - 0.05) { E.look([1, 1, 1], [0, 0, 0], 0.45, 0.82); chain.material.opacity = 0.6 * cl((t - tSie - 0.3) / 0.8); const f = K.eio(prog(t, tSie, 2)); look = V(0, lerp(1100, 900, f), -2600); fov = 62; }
  else if (t < tSteht - 0.05) { E.look([1, 1, 1], [0, 0, 0], 0.45, 0.82); const f = K.eio(prog(t, tGanz, 1.8)); look = SP.me.clone().lerp(V(0, 900, -2600), 1 - f); fov = lerp(62, 22, f); }
  else if (t < tEtwas - 0.05) { scene = sp; E.look([1, 1, 1], [0, 0, 0], 0.2, 0.92); const a = 0.3 + (t - tSteht) * 0.08; pos = me.position.clone().add(V(Math.sin(a) * 11, 1, Math.cos(a) * 11)); look = me.position.clone(); fov = 40; }
  else if (t < tHoch - 0.05) { scene = sp; E.look([1, 1, 1], [0, 0, 0], 0.2, 0.92); const a = 0.2 + (t - tEtwas) * 0.05; const d = lerp(34, 30, prog(t, tEtwas, 7)); pos = ve.position.clone().add(V(Math.sin(a) * d, 2, Math.cos(a) * d)); look = ve.position.clone().add(V(0, 1, 0)); fov = 40; }
  else if (t < tUnd - 0.05) { scene = sp; E.look([1, 1, 1], [0, 0, 0], 0.2, 0.92); const c = ma.position.clone().lerp(ju.position, 0.55); const f = prog(t, tHoch, 4); pos = c.clone().add(V(lerp(-10, 4, f), -8, 78)); look = c.clone().add(V(0, 3, 0)); fov = 40; }
  else if (t < tDu - 0.05) { scene = sp; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.88); const s = K.eio(prog(t, tUnd, 1.6)), z = K.eio(prog(t, tRies, 1.6)); const c = ma.position.clone().lerp(ju.position, 0.55);
    const inner = V(LX + 47, 90 - 50, 695), outer = V(LX + 190, 362 - 85, 2809); const cp = inner.clone().lerp(outer, z);
    pos = c.clone().add(V(0, -4, 62)).lerp(cp, s); look = c.clone().lerp(V(cp.x, cp.y, 0), s); fov = 40;
    if (t >= tLicht) { const f = prog(t, tLicht + 0.6, 1.0); pulseV.position.copy(lVe.position).lerp(EA.group.position, f); pulseV.material.opacity = f > 0 && f < 1 ? 1 : 0; }
    if (t >= tJLicht) { const f = prog(t, tJLicht + 0.4, 2.6); pulseJ.position.copy(lJu.position).lerp(EA.group.position, f); pulseJ.material.opacity = f > 0 && f < 1 ? 1 : 0; } }
  else { E.look([1, 1, 1], [0, 0, 0], 0.45, 0.82); const f = K.eio(prog(t, tDu, 1.5)); look = V(0, lerp(1100, 1000, f), -2600); fov = 64;
    dawn.material.opacity = 0.55 + 0.3 * prog(t, tSo, 8); dawn2.material.opacity = 0.5 + 0.3 * prog(t, tSo, 8); }
  fill.position.copy(cam.position);
  [me, ve, ma, ju, lVe, lMe, lMa, lJu].forEach((m, i) => (m.rotation.y = t * (0.1 + i * 0.01))); EA.mesh.rotation.y = t * 0.1; EA.clouds.rotation.y = t * 0.12;
  cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  shiftL.forEach(([L, dx]) => { L.d.style.left = parseFloat(L.d.style.left) + dx + "px"; });
  sideL.forEach(({ L, r }) => { const p = L.obj.getWorldPosition(new THREE.Vector3()); const [x, y] = P(p); L.d.style.left = x + 40 + r * 0.94 + "px"; L.d.style.top = y + "px"; L.d.style.transform = `translate(0,-50%)`; });
  let wh = "", wa = 0;
  if (t >= tFuenfzig - 0.3 && t < tHoch - 0.1) { const v = Math.round(50 * K.eout(cl((t - tFuenfzig + 0.3) / 1.0))); wh = `${v} Mio. km<div class="sub">von der Erde</div>`; wa = cl((t - tFuenfzig + 0.3) / 0.3) * (1 - cl((t - tHoch + 0.4) / 0.3)); }
  if (t >= tLicht + 0.6 && t < tDu - 0.1) { const j = t >= tJLicht; wh = j ? `☀️ 44 Min.<div class="sub">braucht Jupiters Licht</div>` : `☀️ 3 Min.<div class="sub">braucht das Licht der Venus</div>`; wa = 1 - cl((t - tDu + 0.4) / 0.3); }
  if (t >= tSo + 1.0 && t < tAm - 0.1) { wh = `⏰ 1 Std. vor Sonnenaufgang<div class="sub">Richtung Südosten</div>`; wa = cl((t - tSo - 1) / 0.3) * (1 - cl((t - tAm + 0.4) / 0.3)); }
  if (t >= tAm && t < tWel - 0.1) { wh = `bis 22. November`; wa = cl((t - tAm) / 0.3) * (1 - cl((t - tWel + 0.4) / 0.3)); }
  WORD.style.top = t >= tUnd && t < tDu ? "210px" : (scene === sky ? "820px" : ""); word(wh, wa); cap(t);
};
