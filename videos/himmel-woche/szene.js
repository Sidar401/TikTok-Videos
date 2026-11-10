const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
const WT = (w, ab = 0) => wortZeit(WORDS, w, ab);
K.reseed(9);
// ===== Welt: Nachtlandschaft mit Sternenhimmel =====
const sc = new THREE.Scene();
const skyU = K.sky(sc, 0x02040c, 0x0a1230, 0x1c2a50, 4000);
const st = K.stars(sc, 4500, -0.05, 3800, 2.2); st.material.opacity = 0.95;
// Milchstraßen-Band
const mw = []; for (let i = 0; i < 5000; i++) { const s = (K.rnd() - 0.5) * 3000, w = (K.rnd() + K.rnd() + K.rnd() - 1.5) * 160; mw.push(s, 900 + s * 0.45 + w, -3000 + w * 0.5); }
const mwg = new THREE.BufferGeometry(); mwg.setAttribute("position", new THREE.Float32BufferAttribute(mw, 3));
sc.add(new THREE.Points(mwg, new THREE.PointsMaterial({ color: 0xcfd8ff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0.45, fog: false })));
// Dämmerung im Osten (wird morgens heller)
const dawn = K.sprite(sc, K.glowTex("rgba(255,150,90,.55)"), 2600, V(0, -250, -3400), 0);
// Hügel (Silhouetten)
function hills(z, h, col, seed) { K.reseed(seed); const pts = [new THREE.Vector2(-3000, -50)]; for (let x = -3000; x <= 3000; x += 40) pts.push(new THREE.Vector2(x, h * (0.5 + 0.5 * Math.sin(x * 0.002 + seed) * Math.cos(x * 0.0037 + seed * 2)) + K.rnd() * h * 0.08)); pts.push(new THREE.Vector2(3000, -50));
  const shp = new THREE.Shape(pts); const m = new THREE.Mesh(new THREE.ShapeGeometry(shp), new THREE.MeshBasicMaterial({ color: col, fog: false })); m.position.z = z; sc.add(m); return m; }
const gr = new THREE.Mesh(new THREE.PlaneGeometry(9000, 9000), new THREE.MeshBasicMaterial({ color: 0x020306, fog: false })); gr.rotation.x = -Math.PI / 2; gr.position.y = 1; sc.add(gr);
hills(-1800, 140, 0x060912, 3); hills(-900, 80, 0x04060b, 7); hills(-300, 30, 0x020306, 11);
// Kleinstadt-Lichter in der Ferne + Lichtglocke
const town = []; for (let i = 0; i < 260; i++) town.push((K.rnd() - 0.5) * 500 + 650, 10 + K.rnd() * 22, -1500 - K.rnd() * 120);
const tg = new THREE.BufferGeometry(); tg.setAttribute("position", new THREE.Float32BufferAttribute(town, 3));
const townPts = new THREE.Points(tg, new THREE.PointsMaterial({ color: 0xffc070, size: 3.6, sizeAttenuation: false, transparent: true, opacity: 0.9, fog: false })); sc.add(townPts);
const townGlow = K.sprite(sc, K.glowTex("rgba(255,170,90,.45)"), 900, V(650, 40, -1520), 0.7);
// Planeten
const MJ = V(-160, 330, -2600); // Mitte zwischen Mars und Jupiter
const jup = K.sprite(sc, K.glowTex("rgba(255,250,235,1)"), 60, MJ.clone().add(V(-40, 6, 0)), 1);
const jupH = K.sprite(sc, K.glowTex("rgba(255,245,220,.35)"), 220, jup.position.clone(), 0.9);
const mars = K.sprite(sc, K.glowTex("rgba(255,120,70,1)"), 34, MJ.clone().add(V(40, -6, 0)), 1);
const marsH = K.sprite(sc, K.glowTex("rgba(255,110,60,.3)"), 120, mars.position.clone(), 0.8);
// Sternschnuppen: dünne Leuchtstreifen
const NM = 22, mets = [];
for (let i = 0; i < NM; i++) { const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, 0, 0, 0, 0], 3));
  const l = new THREE.Line(g, new THREE.LineBasicMaterial({ color: 0xe8f4ff, transparent: true, opacity: 0, fog: false })); sc.add(l); const head = K.sprite(sc, K.glowTex("rgba(220,240,255,1)"), 26, V(0, 0, 0), 0);
  K.reseed(400 + i * 13); mets.push({ l, head, t0: K.rnd(), x: (K.rnd() - 0.5) * 2600, y: 700 + K.rnd() * 900, dx: -0.6 - K.rnd() * 0.5, dy: -0.7 - K.rnd() * 0.3 }); }
function meteors(t, rate) { mets.forEach((m, i) => { const per = 1.6 / rate, ph = ((t / per + m.t0 * 7) % 1 + 1) % 1, life = 0.35; const vis = ph < life && rate > 0;
  const k = ph / life, L = 520; const hx = m.x + m.dx * L * k * 1.6, hy = m.y + m.dy * L * k * 1.6; const p = m.l.geometry.attributes.position;
  p.setXYZ(0, hx, hy, -2600); p.setXYZ(1, hx - m.dx * L * 0.6, hy - m.dy * L * 0.6, -2600); p.needsUpdate = true;
  m.l.material.opacity = vis ? Math.sin(k * Math.PI) * 0.9 : 0; m.head.position.set(hx, hy, -2600); m.head.material.opacity = vis ? Math.sin(k * Math.PI) : 0; }); }
// Mond (Supermond geht auf)
const moon = K.moon(sc, 150, V(200, -60, -2400), 0.12); moon.visible = false;
const ml = new THREE.DirectionalLight(0xfff0d8, 3); ml.position.set(0, 200, 600); ml.target = moon; sc.add(ml); sc.add(new THREE.AmbientLight(0x404a70, 0.3));
const mglow = K.sprite(sc, K.glowTex("rgba(255,220,170,.4)"), 1000, V(200, -60, -2600), 0);
// Mensch auf dem Hügel
const pc = document.createElement("canvas"); pc.width = 256; pc.height = 256; const pg = pc.getContext("2d"); pg.fillStyle = "#010204";
pg.beginPath(); pg.arc(128, 70, 26, 0, 7); pg.fill(); pg.beginPath(); pg.moveTo(90, 110); pg.quadraticCurveTo(128, 92, 166, 110); pg.lineTo(180, 200); pg.lineTo(220, 210); pg.lineTo(220, 240); pg.lineTo(40, 240); pg.lineTo(70, 200); pg.closePath(); pg.fill();
const person = new THREE.Mesh(new THREE.PlaneGeometry(36, 36), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(pc), transparent: true, depthWrite: false, fog: false })); person.position.set(-120, 28, -300); sc.add(person);

// ===== Analyse-Ebene =====
const A = new Ebene(document.getElementById("root"));
const tN1 = WT("nummer"), t16 = WT("sechzehn"), tPlatz = WT("zwischen"), tMorg = WT("besten"), tJup = WT("jupiter", 21), tMars = WT("mars", 23), tN2 = WT("nummer", 25), t17 = WT("siebzehn"), tFuenf = WT("fünfzehn"), tMitt = WT("mitternacht"), tRas = WT("rasen"), tSchn = WT("schnellsten"), tN3 = WT("nummer", 46), t24 = WT("vierundzwanzig"), tGr = WT("größer", 52), tTipp = WT("tipp"), tWel = WT("welches");
const P = (v) => { cam.updateMatrixWorld(true); const q = v.clone().project(cam); return [(q.x + 1) / 2 * 1080, (1 - q.y) / 2 * 1920]; };
// Übersicht nach dem Hook
A.karte("Diese Woche am Himmel", 140, 560, 800, 520, { t0: 4.3, t1: 7.8, unter: "NOVEMBER 2026" });
[["16.", "Mars + Jupiter"], ["17./18.", "Sternschnuppen"], ["24.", "Supermond"]].forEach(([d, n], i) => { A.hand(d, 290, 720 + i * 115, { t0: 4.6 + i * 0.5, t1: 7.8, size: 72, farbe: GELB }); A.hand(n, 620, 720 + i * 115, { t0: 4.7 + i * 0.5, t1: 7.8, size: 64, farbe: "#fff" }); });
// Nr. 1
A.stempel("NR. 1", 270, 560, { t0: tN1, t1: 13.2, rot: -8, farbe: GELB });
A.zettel("Nacht auf<br>16. November", 780, 600, { t0: t16, t1: 13.2, rot: 5, size: 56 });
let ringMJ = null;
// Abstand
A.karte("Abstand am Himmel", 160, 900, 760, 380, { t0: tPlatz - 0.2, t1: 17.4, unter: "NUR 1,2 GRAD" });
A.hand("● Jupiter", 290, 1110, { t0: tPlatz, t1: 17.4, size: 54, farbe: "#fff" }); A.hand("Mars ●", 790, 1110, { t0: tPlatz + 0.2, t1: 17.4, size: 54, farbe: "#ff8a5a" });
A.hand("◯ ◯", 540, 1110, { t0: tPlatz + 0.8, t1: 17.4, size: 90, farbe: GELB }); A.hand("≈ 2 Vollmonde", 540, 1215, { t0: tPlatz + 1.1, t1: 17.4, size: 56, farbe: GELB });
// Wann/wo
A.zettel("früh morgens,<br>vor Sonnenaufgang", 300, 640, { t0: tMorg, t1: 21.2, rot: -5, size: 54 });
A.pfeil(640, 1120, 820, 1260, { t0: tMorg + 0.6, t1: 21.2, bogen: -0.2, farbe: GELB }); A.hand("Richtung Osten", 640, 1060, { t0: tMorg + 0.8, t1: 21.2, size: 60 });
// Jupiter / Mars beschriften
const jl = A.hand("Jupiter: hell & weiß", 300, 640, { t0: tJup, t1: 25.9, size: 60, farbe: "#fff" });
const mlb = A.hand("Mars: klein & rötlich", 760, 980, { t0: tMars, t1: 25.9, size: 60, farbe: "#ff8a5a" });
const ja = A.pfeil(300, 690, 470, 820, { t0: tJup + 0.3, t1: 25.9, bogen: -0.3, farbe: "#fff", breite: 6 });
const ma = A.pfeil(760, 930, 620, 860, { t0: tMars + 0.3, t1: 25.9, bogen: 0.3, farbe: "#ff8a5a", breite: 6 });
// Nr. 2 Leoniden
A.stempel("NR. 2", 270, 560, { t0: tN2, t1: 31.1, rot: -8, farbe: GELB });
A.hand("Leoniden", 700, 600, { t0: tN2 + 1.6, t1: 31.1, size: 96, farbe: BLAU, rot: -4 });
A.zettel("17./18. Nov.", 300, 720, { t0: t17, t1: 36.3, rot: -5, size: 60 });
A.zahl(700, 900, { von: 0, bis: 15, t0: tFuenf - 0.3, t1: 36.3, dauer: 1.2, fmt: (v) => "bis " + Math.round(v), unter: "pro Stunde", farbe: BLAU });
// Mitternacht
A.karte("Beste Zeit", 160, 580, 760, 470, { t0: tMitt - 0.6, t1: 40.0, unter: "NACH MITTERNACHT" });
A.hand("🕛 0:00", 380, 830, { t0: tMitt - 0.3, t1: 40.0, size: 96, farbe: "#fff" }); A.pfeil(540, 830, 610, 830, { t0: tMitt, t1: 40, bogen: 0.1, farbe: GELB });
A.hand("Mond weg 🌙↓", 770, 830, { t0: tMitt + 0.4, t1: 40.0, size: 64, farbe: GELB });
// Geschwindigkeit
A.karte("Wie schnell?", 100, 520, 880, 760, { t0: tRas - 0.2, t1: 47.3, unter: "KILOMETER PRO SEKUNDE" });
A.balken(160, 650, 760, 460, [{ name: "Gewehr-<br>kugel", wert: 1, text: "≈ 1", farbe: "#8a949c" }, { name: "Raum-<br>station ISS", wert: 7.7, text: "7,7", farbe: "#8fb8ff" }, { name: "Leoniden", wert: 71, text: "≈ 71", farbe: BLAU }], { t0: tRas, t1: 47.3, versatz: 0.45 });
A.stempel("REKORD", 360, 860, { t0: tSchn, t1: 47.3, rot: 9, farbe: ROT });
A.hand("schnellste des Jahres!", 540, 1350, { t0: tSchn + 0.4, t1: 47.3, size: 58, farbe: GELB });
// Nr. 3 Supermond
A.stempel("NR. 3", 270, 560, { t0: tN3, t1: 53.4, rot: -8, farbe: GELB });
A.karte("3 Supermonde", 160, 960, 760, 380, { t0: t24, t1: 53.4, unter: "HINTEREINANDER" });
[["24. Nov.", 300], ["24. Dez.", 540], ["Jan. 27", 780]].forEach(([d, x], i) => { A.hand("🌕", x, 1120, { t0: t24 + 0.3 + i * 0.4, t1: 53.4, size: 90 }); A.hand(d, x, 1240, { t0: t24 + 0.4 + i * 0.4, t1: 53.4, size: 46, farbe: i ? "#fff" : GELB }); });
A.kreis(300, 1170, 110, 110, { t0: t24 + 1.6, t1: 53.4 });
A.karte("Normal vs. Super", 160, 600, 760, 520, { t0: tGr - 0.6, t1: 56.4, unter: "SCHEINBARE GRÖSSE" });
A.hand("●", 340, 880, { t0: tGr - 0.4, t1: 56.4, size: 180, farbe: "#bdb7aa" }); A.hand("●", 720, 870, { t0: tGr, t1: 56.4, size: 210, farbe: "#ffe6a8" });
A.hand("+14 %", 720, 1040, { t0: tGr + 0.3, t1: 56.4, size: 64, farbe: GELB }); A.hand("+30 % heller", 540, 1120, { t0: tGr + 0.8, t1: 56.4, size: 56, farbe: GELB });
// Tipp
A.zettel("Tipp: weg vom<br>Stadtlicht!", 330, 680, { t0: tTipp, t1: 60.2, rot: -5, size: 60 });
A.kreis(780, 1010, 180, 90, { t0: tTipp + 1.0, t1: 60.2 }); A.hand("zu hell ✗", 780, 880, { t0: tTipp + 1.2, t1: 60.2, size: 58, farbe: ROT });
A.zettel("1, 2 oder 3? 👇", 540, 760, { t0: tWel, t1: 61.8, rot: -4, size: 72 });

renderAt = (t) => {
  label(""); E.look([0.95, 0.98, 1.08], [0.004, 0.006, 0.02], 0.7, 0.8); E.grade.uniforms.flash.value = 0;
  moon.visible = false; mglow.material.opacity = 0; dawn.material.opacity = 0; meteors(t, 0);
  let look = V(0, 260, -2600), pos = V(0, 40, 60);
  if (t < 7.9) { const f = K.eio(prog(t, 0, 7.9)); pos.set(lerp(-80, 0, f), lerp(20, 40, f), 60); look.set(lerp(-400, -100, f), lerp(600, 320, f), -2600); meteors(t, 0.6); }
  else if (t < 26.4) {
    // Mars + Jupiter, Morgendämmerung
    dawn.material.opacity = 0.4 + 0.4 * prog(t, 17.6, 3.5);
    const z = t >= 13.4 && t < 17.5 ? K.eio(prog(t, 13.4, 1.2)) : (t >= 21.6 ? 1 : 0.0);
    pos.set(0, 40, 60); look.set(MJ.x, MJ.y - 40, MJ.z); cam.fov = lerp(40, 14, z); cam.updateProjectionMatrix();
  } else if (t < 47.6) {
    // Sternschnuppen
    meteors(t, t < 31.3 ? 1.6 : 3.2); pos.set(0, 40, 60); look.set(lerp(-200, 200, prog(t, 26.4, 21)), 520, -2600);
  } else if (t < 56.4) {
    // Supermond geht auf
    moon.visible = true; const r = K.eout(prog(t, 47.6, 4)); moon.position.set(200, lerp(-80, 380, r), -2400); mglow.position.copy(moon.position).add(V(0, 0, -200)); mglow.material.opacity = 0.7 * r;
    if (t >= 53.4) { moon.scale.setScalar(lerp(1 / 1.14, 1, K.eio(prog(t, tGr, 1.0)))); moon.material.emissiveIntensity = lerp(0.08, 0.2, prog(t, tGr + 0.6, 1)); }
    pos.set(0, 40, 60); look.set(150, 240, -2600);
  } else { pos.set(-40, 50, 140); look.set(200, 200, -2600); meteors(t, 1.2); }
  if (!(t >= 7.9 && t < 26.4)) { cam.fov = 40; cam.updateProjectionMatrix(); }
  cam.position.copy(pos); cam.lookAt(look);
  // Pfeile Jupiter/Mars an echte Positionen hängen
  if (t >= 21.6 && t < 26.4) { const [jx, jy] = P(jup.position), [mx, my] = P(mars.position); }
  E.render(sc, t);
  A.update(t); cap(t);
};
