const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
const WT = (w, ab = 0) => wortZeit(WORDS, w, ab);
K.reseed(5);
// ===== Welt: Starbase am Meer bei Abenddämmerung =====
const sc = new THREE.Scene();
K.sky(sc, 0x1a2140, 0x6a6a88, 0xf0a070, 4000); K.stars(sc, 300, 0.45, 3800, 2);
sc.fog = new THREE.FogExp2(0x9a8a98, 0.0011);
const sunP = V(-900, 120, -2200);
const sun = new THREE.DirectionalLight(0xffc89a, 2.6); sun.position.copy(sunP); sc.add(sun); sc.add(new THREE.HemisphereLight(0xc8d4ff, 0x40302a, 0.9));
K.sprite(sc, K.glowTex("rgba(255,190,130,.7)"), 900, sunP.clone().multiplyScalar(0.8), 0.9);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(1400, 1400), new THREE.MeshStandardMaterial({ color: 0x6a5a48, roughness: 1 })); ground.rotation.x = -Math.PI / 2; ground.position.set(0, 0, 300); sc.add(ground);
const wat = K.water(sc, -0.5, 0x0a1424, 0x8a7a90, 0xffc49a, sunP.clone().normalize()); wat.mesh.position.z = -900; wat.u.fogD.value = 0.0015;
const steel = new THREE.MeshStandardMaterial({ color: 0xd8dce2, metalness: 0.35, roughness: 0.38 });
const dark = new THREE.MeshStandardMaterial({ color: 0x1b1d22, metalness: 0.4, roughness: 0.7 });
const beam = new THREE.MeshStandardMaterial({ color: 0x2a2d33, metalness: 0.6, roughness: 0.6 });
// Startturm (Gitter)
const tower = new THREE.Group(); sc.add(tower);
const TH = 146, TW = 12;
[[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([a, b]) => { const p = new THREE.Mesh(new THREE.BoxGeometry(1.6, TH, 1.6), beam); p.position.set(a * TW / 2, TH / 2, b * TW / 2); tower.add(p); });
for (let y = 6; y < TH; y += 9) { [[0, -1, 0], [0, 1, 0]].forEach(([, b]) => { const h = new THREE.Mesh(new THREE.BoxGeometry(TW, 0.8, 0.8), beam); h.position.set(0, y, b * TW / 2); tower.add(h); }); [[-1], [1]].forEach(([a]) => { const h = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, TW), beam); h.position.set(a * TW / 2, y, 0); tower.add(h); });
  const d = new THREE.Mesh(new THREE.BoxGeometry(0.5, Math.hypot(TW, 9), 0.5), beam); d.position.set(0, y + 4.5, TW / 2); d.rotation.z = Math.atan2(TW, 9); tower.add(d); }
const topLight = new THREE.Mesh(new THREE.SphereGeometry(1, 8, 8), new THREE.MeshBasicMaterial({ color: 0xff3030 })); topLight.position.set(0, TH + 1, 0); tower.add(topLight);
// Fangarme ("Stäbchen")
const ARMH = 118, RX = 24;
const arms = [-1, 1].map((s) => { const g = new THREE.Group(); g.position.set(TW / 2, ARMH, s * 5.5); const a = new THREE.Mesh(new THREE.BoxGeometry(34, 3.2, 2.4), steel); a.position.x = 17; g.add(a);
  const r = new THREE.Mesh(new THREE.BoxGeometry(34, 0.6, 2.6), new THREE.MeshBasicMaterial({ color: 0xffd23f })); r.position.set(17, 1.9, 0); g.add(r); tower.add(g); return { g, s }; });
function setArms(close) { arms.forEach(({ g, s }) => (g.rotation.y = -s * K.lerp(0.62, 0.13, close))); }
// Startrampe
const mount = new THREE.Mesh(new THREE.CylinderGeometry(9, 10, 20, 24, 1, true), dark); mount.position.set(RX, 10, 0); sc.add(mount);
// Rakete: Booster (72 m) + Raumschiff (52 m), Radius 4.5
function makeBooster() { const g = new THREE.Group(); const c = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 4.5, 72, 48), steel); c.position.y = 36; g.add(c);
  const e = new THREE.Mesh(new THREE.CylinderGeometry(4.6, 4.2, 2.5, 48), dark); e.position.y = 1; g.add(e);
  for (let i = 0; i < 4; i++) { const f = new THREE.Mesh(new THREE.BoxGeometry(3.5, 4, 0.5), dark); const a = i * Math.PI / 2 + 0.4; f.position.set(Math.cos(a) * 5.2, 68, Math.sin(a) * 5.2); f.rotation.y = -a; g.add(f); }
  const ring = new THREE.Mesh(new THREE.CylinderGeometry(4.55, 4.55, 1.2, 48), dark); ring.position.y = 70; g.add(ring); return g; }
function makeShip() { const g = new THREE.Group(); const tc = document.createElement("canvas"); tc.width = 256; tc.height = 64; const q = tc.getContext("2d"); q.fillStyle = "#c9ced6"; q.fillRect(0, 0, 256, 64); q.fillStyle = "#16181c"; q.fillRect(0, 0, 128, 64);
  for (let x = 0; x < 128; x += 8) for (let y = 0; y < 64; y += 6) { q.fillStyle = `rgba(255,255,255,${0.02 + (x * 7 + y * 3) % 5 * 0.01})`; q.fillRect(x, y, 7, 5); }
  const tm = new THREE.MeshStandardMaterial({ map: new THREE.CanvasTexture(tc), metalness: 0.3, roughness: 0.42 });
  const pts = []; for (let i = 0; i <= 20; i++) { const y = i / 20; pts.push(new THREE.Vector2(4.5 * Math.sqrt(1 - Math.pow(y, 2.2)), 38 + y * 14)); }
  const nose = new THREE.Mesh(new THREE.LatheGeometry(pts, 48), tm); g.add(nose);
  const body = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 4.5, 38, 48), tm); body.position.y = 19; g.add(body);
  [[-1, 6], [1, 6], [-1, 42], [1, 42]].forEach(([s, y]) => { const f = new THREE.Mesh(new THREE.BoxGeometry(0.5, y > 20 ? 6 : 9, 4), dark); f.position.set(s * 5, y, 0); g.add(f); }); return g; }
const booster = makeBooster(), ship = makeShip(); sc.add(booster); sc.add(ship);
// Feuer
const fireTex = K.glowTex("rgba(255,230,180,1)"), smokeTex = K.glowTex("rgba(160,150,150,.55)");
const flames = []; for (let i = 0; i < 18; i++) flames.push(K.sprite(sc, fireTex, 10, V(0, 0, 0), 0));
const smoke = []; for (let i = 0; i < 40; i++) smoke.push(new THREE.Sprite(new THREE.SpriteMaterial({ map: smokeTex, transparent: true, depthWrite: false, opacity: 0 }))), sc.add(smoke[i]);
const flameLight = new THREE.PointLight(0xffaa55, 0, 400); sc.add(flameLight);
function fire(base, power, t, down = true) { flames.forEach((s, i) => { const k = i / flames.length; s.position.set(base.x + Math.sin(t * 40 + i) * 0.6, base.y - (down ? 1 : -1) * (2 + k * 30 * power), base.z); s.scale.setScalar((14 - k * 9) * (0.6 + power * 0.6)); s.material.opacity = power * (1 - k) * 0.95; });
  flameLight.position.copy(base).add(V(0, -6, 0)); flameLight.intensity = power * 4000; }
function puff(base, amount, t) { smoke.forEach((s, i) => { K.reseed(700 + i); const a = K.rnd() * 6.28, life = (t * 0.6 + K.rnd()) % 1; s.position.set(base.x + Math.cos(a) * life * 60, 4 + life * 20 + K.rnd() * 6, base.z + Math.sin(a) * life * 60); s.scale.setScalar(18 + life * 60); s.material.opacity = amount * (1 - life) * 0.6; }); }
// Wiedereintritt (eigene kleine Welt)
const sky2 = new THREE.Scene(); K.reseed(77); K.stars(sky2, 2500, -1, 2800, 2.2);
const EA = K.earth(sky2, { day, night, topo }, 400); EA.group.position.set(0, -560, -80); EA.U.sun.value.set(-0.5, 0.6, 0.3).normalize();
const ship2 = makeShip(); ship2.scale.setScalar(0.06); sky2.add(ship2); sky2.add(new THREE.AmbientLight(0x667799, 0.6)); const s2l = new THREE.DirectionalLight(0xffffff, 2); s2l.position.set(-5, 5, 5); sky2.add(s2l);
const plasma = []; for (let i = 0; i < 16; i++) plasma.push(K.sprite(sky2, K.glowTex("rgba(255,140,220,.9)"), 2, V(0, 0, 0), 0));

// ===== Analyse-Ebene =====
const A = new Ebene(document.getElementById("root"));
const t13 = WT("dreizehn"), t124 = WT("hundertvier"), tFrei = WT("freiheitsstatue"), tBoo = WT("booster"), tStart = WT("nach"), tArme = WT("arme"), tEss = WT("wie", 31), tMehr = WT("mehrmals"), tNeu = WT("neue"), tErst = WT("ersten", 37), tAll = WT("all", 40), tGlueh = WT("glüht"), tLand = WT("landet"), tFlug = WT("flugzeug"), tBill = WT("billiger"), tGen = WT("genehmigung"), tGlaub = WT("glaubst");
// Termin
A.karte("Starship · Flug 15", 90, 560, 520, 330, { t0: t13 - 0.2, t1: 10.7, unter: "STARBASE, TEXAS" });
A.hand("13. Nov.", 350, 760, { t0: t13, t1: 10.7, size: 120, farbe: GELB, rot: -4 });
A.logo("assets/logos/spacex.svg", 640, 600, 360, 150, { t0: t13 + 0.3, t1: 10.7, rot: 3 });
A.zettel("frühestens!", 800, 840, { t0: t13 + 1.0, t1: 10.7, rot: 6, size: 58 });
A.strich(230, 815, 470, { t0: t13 + 0.5, t1: 10.7 });
// 124 m
A.zahl(330, 640, { von: 0, bis: 124, t0: t124 - 0.3, t1: 15.1, dauer: 1.3, fmt: (v) => Math.round(v) + " m", unter: "größte Rakete der Welt" });
A.pfeil(470, 760, 640, 980, { t0: t124 + 0.9, t1: 15.1, bogen: -0.3 });
A.hand("ganz oben bis ganz unten!", 360, 1240, { t0: t124 + 1.3, t1: 15.1, size: 56, rot: -3, farbe: "#fff" });
// Vergleich Freiheitsstatue
A.karte("Höhenvergleich", 80, 520, 600, 620, { t0: tFrei - 0.3, t1: 18.3, unter: "IN METERN" });
A.balken(130, 640, 500, 380, [{ name: "Freiheits-<br>statue", wert: 93, text: "93 m", farbe: "#8fb8a0" }, { name: "Starship", wert: 124.4, text: "124 m", farbe: ORANGE }], { t0: tFrei - 0.1, t1: 18.3, versatz: 0.15 });
A.stempel("+31 m", 830, 700, { t0: tFrei + 1.4, t1: 18.3, rot: 10, farbe: GELB });
// Booster
A.zettel("Booster<br>72 m ≈ 24 Stockwerke", 300, 700, { t0: tBoo, t1: 23.2, rot: -5, size: 54 });
A.pfeil(470, 790, 660, 1060, { t0: tBoo + 0.6, t1: 23.2, bogen: -0.25 });
A.kreis(745, 1150, 70, 220, { t0: tBoo + 1.0, t1: 23.2 });
// Rückflug
A.pfeil(860, 620, 690, 760, { t0: tStart + 0.6, t1: 26.4, bogen: 0.5, farbe: GELB });
A.hand("zurück zum Turm!", 700, 560, { t0: tStart + 0.8, t1: 26.4, size: 60 });
// Fang
A.stempel("GEFANGEN!", 540, 640, { t0: 30.0, t1: 31.4, rot: -9, farbe: GRUEN });
A.kreis(560, 980, 250, 120, { t0: tEss, t1: 32.6, farbe: GELB, dauer: 0.4 });
A.hand("wie Essstäbchen 🥢", 540, 760, { t0: tEss + 0.1, t1: 32.6, size: 76 });
// Schon mehrmals
A.karte("Booster-Fänge", 160, 560, 760, 420, { t0: tMehr - 0.4, t1: 35.3, unter: "SEIT OKTOBER 2024" });
A.hand("✓", 300, 800, { t0: tMehr, t1: 35.3, size: 140, farbe: GRUEN }); A.hand("✓", 470, 800, { t0: tMehr + 0.3, t1: 35.3, size: 140, farbe: GRUEN }); A.hand("✓", 640, 800, { t0: tMehr + 0.6, t1: 35.3, size: 140, farbe: GRUEN }); A.hand("…", 790, 800, { t0: tMehr + 0.9, t1: 35.3, size: 140, farbe: GRUEN });
// Das Neue
A.stempel("NEU", 540, 820, { t0: tNeu, t1: 37.2, rot: -6, farbe: GELB });
A.karte("Der Plan", 120, 540, 840, 560, { t0: tErst - 0.3, t1: 41.3, unter: "FLUG 15" });
A.hand("Booster", 330, 760, { t0: tErst, t1: 41.3, size: 70, farbe: "#fff" }); A.hand("✓ gefangen", 330, 860, { t0: tErst + 0.2, t1: 41.3, size: 60, farbe: GRUEN });
A.hand("Raumschiff", 730, 760, { t0: tErst + 0.6, t1: 41.3, size: 70, farbe: "#fff" }); A.hand("?", 730, 880, { t0: tErst + 0.8, t1: 41.3, size: 120, farbe: GELB });
A.stempel("ERSTMALS", 540, 1020, { t0: tErst + 1.4, t1: 41.3, rot: -7, farbe: ROT });
// Wiedereintritt
A.hand("glüht!", 760, 640, { t0: tGlueh, t1: 45.2, size: 92, farbe: "#ff8ad8", rot: 6 });
A.pfeil(700, 700, 600, 900, { t0: tGlueh + 0.2, t1: 45.2, farbe: "#ff8ad8", bogen: 0.2 });
A.stempel("GEFANGEN?", 540, 640, { t0: 47.3, t1: 48.3, rot: -8, farbe: GELB });
// Wiederverwendung: Kreislauf
const tImm = WT("immer", 48);
A.karte("Wie ein Flugzeug", 110, 520, 860, 700, { t0: tImm - 0.3, t1: 52.9, unter: "IMMER WIEDER FLIEGEN" });
const ab = [["Start", 540, 700], ["Flug", 820, 930], ["Fang", 540, 1120], ["Tanken", 260, 930]];
ab.forEach(([n, x, y], i) => A.zettel(n, x, y, { t0: tImm + i * 0.35, t1: 52.9, size: 52, rot: [-3, 4, -2, 5][i] }));
[[620, 720, 800, 860], [800, 1010, 630, 1110], [450, 1110, 280, 1010], [270, 860, 450, 720]].forEach(([a, b, c, d], i) => A.pfeil(a, b, c, d, { t0: tImm + 0.2 + i * 0.35, t1: 52.9, bogen: 0.25, breite: 7 }));
// Billiger
A.karte("Kosten pro Flug", 120, 560, 840, 560, { t0: tBill - 1.6, t1: 55.5, unter: "WEGWERFEN VS. WIEDERVERWENDEN" });
A.hand("€€€€€", 330, 820, { t0: tBill - 1.3, t1: 55.5, size: 130, farbe: ROT });
A.hand("neu bauen", 330, 940, { t0: tBill - 1.1, t1: 55.5, size: 52, farbe: "#fff" });
A.pfeil(520, 820, 640, 820, { t0: tBill - 0.7, t1: 55.5, bogen: 0.15, farbe: GELB });
A.hand("€", 780, 820, { t0: tBill - 0.4, t1: 55.5, size: 130, farbe: GRUEN });
A.hand("nur tanken", 780, 940, { t0: tBill - 0.3, t1: 55.5, size: 52, farbe: "#fff" });
A.stempel("VIEL BILLIGER", 540, 1050, { t0: tBill, t1: 55.5, rot: -6, farbe: GRUEN });
// Genehmigung
A.logo("assets/logos/faa.svg", 330, 560, 420, 420, { t0: tGen - 0.4, t1: 58.1 });
A.stempel("AUSSTEHEND", 540, 1060, { t0: tGen + 0.5, t1: 58.1, rot: -8, farbe: ORANGE });
A.hand("US-Luftfahrtbehörde", 540, 1190, { t0: tGen + 0.2, t1: 58.1, size: 54, farbe: "#fff" });
A.zettel("Klappt es? 🤔", 540, 760, { t0: tGlaub, t1: 59.6, rot: -4, size: 72 });

// ===== Zeit-Logik =====
const PAD = V(RX, 20, 0);
renderAt = (t) => {
  label(""); wat.u.time.value = t;
  let scene = sc; E.look([1.06, 0.98, 0.92], [0.008, 0.008, 0.02], 0.55, 0.86); E.grade.uniforms.flash.value = 0;
  flames.forEach((s) => (s.material.opacity = 0)); smoke.forEach((s) => (s.material.opacity = 0)); flameLight.intensity = 0;
  booster.visible = true; ship.visible = true; setArms(0);
  booster.position.copy(PAD); booster.rotation.set(0, 0, 0); ship.position.set(RX, 92, 0);
  const tL = tStart + 0.2; // Abheben
  if (t < tL) {
    // auf der Rampe – Kamerafahrten
    if (t < 7.5) { const f = K.eio(t / 7.5); cam.position.set(lerp(-260, -150, f), lerp(30, 60, f), lerp(360, 240, f)); cam.lookAt(RX, 80, 0); }
    else if (t < 10.8) { const f = prog(t, 7.6, 3.2); cam.position.set(lerp(160, 120, f), 40, 240); cam.lookAt(RX - 10, 70, 0); }
    else if (t < 15.2) { const f = K.eio(prog(t, 10.9, 4.2)); cam.position.set(RX + 70, lerp(6, 30, f), 110); cam.lookAt(RX, lerp(40, 120, f), 0); }
    else if (t < 18.4) { cam.position.set(-160, 50, 260); cam.lookAt(RX, 70, 0); }
    else { const f = prog(t, 18.5, 5); cam.position.set(RX + lerp(110, 90, f), 30, lerp(150, 130, f)); cam.lookAt(RX, 45, 0); }
  } else if (t < 26.5) {
    // Start
    const d = t - tL; const y = 20 + 0.5 * 9 * d * d;
    booster.position.set(RX, y, 0); ship.position.set(RX, y + 72, 0);
    fire(V(RX, y, 0), Math.min(1, d * 2 + 0.3), t); puff(V(RX, 0, 0), Math.min(1, d * 1.5), t);
    cam.position.set(-180, 20 + d * 6, 300); cam.lookAt(RX, 60 + y * 0.6, 0);
    E.look([1.08, 0.98, 0.9], [0.01, 0.008, 0.015], 0.9, 0.8);
  } else if (t < 37.5) {
    // Booster kommt zurück und wird gefangen
    ship.visible = false;
    const tc = 29.9; const catchY = ARMH - 66; // Booster-Oberkante knapp über den Armen
    let y; if (t < tc) { const k = prog(t, 26.5, tc - 26.5); y = lerp(420, catchY, 1 - Math.pow(1 - k, 2.2)); fire(V(RX, y, 0), 0.7 * (1 - prog(t, tc - 0.3, 0.3)), t); }
    else { y = catchY + Math.max(0, Math.sin((t - tc) * 18) * 1.2 * Math.exp(-(t - tc) * 4)); }
    booster.position.set(RX, y, 0); setArms(K.eio(prog(t, tc - 0.9, 0.9)));
    if (t < 33) { cam.position.set(-150, 140, 170); cam.lookAt(RX - 4, lerp(150, 110, prog(t, 26.5, 3.5)), 0); }
    else { const f = prog(t, 33, 4.5); cam.position.set(lerp(140, 100, f), 100, 160); cam.lookAt(RX - 6, 110, 0); }
    E.grade.uniforms.flash.value = t > tc && t < tc + 0.2 ? 0.2 * (1 - (t - tc) / 0.2) : 0;
  } else if (t < 45.2 && t >= tAll - 0.3) {
    // Wiedereintritt aus dem All
    scene = sky2; E.look([1.02, 0.98, 1.05], [0.005, 0.0, 0.02], 0.5, 0.82);
    const f = prog(t, tAll - 0.3, 45.2 - tAll + 0.3);
    ship2.position.set(lerp(-6, 4, f), lerp(6, -3, f), 0); ship2.rotation.set(0, 0.4, -1.25);
    ship2.updateMatrixWorld(true); plasma.forEach((s, i) => { const k = i / plasma.length; s.position.copy(ship2.localToWorld(V(-6 - k * 10, 50 - k * 48, 0))); s.scale.setScalar(1.6 - k * 0.8 + Math.sin(t * 30 + i) * 0.12); s.material.opacity = (0.4 + 0.6 * prog(t, tAll, 1.5)) * (1 - k * 0.8); });
    cam.position.set(0, 2, 18); cam.lookAt(0, 0, 0);
  } else if (t < 48.4 && t >= 45.2) {
    // Raumschiff landet zwischen den Armen
    booster.visible = false; const tc = 47.3; const catchY = ARMH - 30;
    let y; if (t < tc) { const k = prog(t, 45.2, tc - 45.2); y = lerp(330, catchY, 1 - Math.pow(1 - k, 2)); fire(V(RX, y, 0), 0.6, t); } else y = catchY;
    ship.position.set(RX, y, 0); setArms(K.eio(prog(t, tc - 0.8, 0.8)));
    cam.position.set(-140, 130, 170); cam.lookAt(RX - 4, 120, 0);
    E.grade.uniforms.flash.value = t > tc && t < tc + 0.2 ? 0.2 * (1 - (t - tc) / 0.2) : 0;
  } else if (t < 37.5 + 4.2) {
    // "Das Neue" – Raumschiff oben auf dem Booster, Blick nach oben
    booster.position.copy(PAD); ship.position.set(RX, 92, 0);
    const f = prog(t, 37.5, 4.2); cam.position.set(RX + 60, 10, 80); cam.lookAt(RX, lerp(100, 140, f), 0);
  } else {
    // Rest: ganze Anlage, beide Teile wieder auf der Rampe
    const f = prog(t, 48.4, 15); cam.position.set(lerp(-220, -300, f), lerp(60, 90, f), lerp(280, 380, f)); cam.lookAt(RX, 75, 0);
  }
  E.render(scene, t);
  A.update(t); cap(t);
};
