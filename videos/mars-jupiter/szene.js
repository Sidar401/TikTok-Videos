const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
const W = (w, ab = 0) => wortZeit(WORDS, w, ab);
K.reseed(15);
// ===== Szene 1: Morgenhimmel über dem Land =====
const sc = new THREE.Scene();
const skyMesh = K.sky(sc, 0x02040c, 0x0a1230, 0x1c2a50, 4000);
const st = K.stars(sc, 4500, -0.05, 3800, 2.2); st.material.opacity = 0.95;
const dawn = K.sprite(sc, K.glowTex("rgba(255,150,90,.55)"), 2600, V(1400, -250, -2600), 0);
function hills(z, h, col, seed) { K.reseed(seed); const pts = [new THREE.Vector2(-3000, -50)]; for (let x = -3000; x <= 3000; x += 40) pts.push(new THREE.Vector2(x, h * (0.5 + 0.5 * Math.sin(x * 0.002 + seed) * Math.cos(x * 0.0037 + seed * 2)) + K.rnd() * h * 0.08)); pts.push(new THREE.Vector2(3000, -50));
  const m = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts)), new THREE.MeshBasicMaterial({ color: col, fog: false })); m.position.z = z; sc.add(m); return m; }
const gr = new THREE.Mesh(new THREE.PlaneGeometry(9000, 9000), new THREE.MeshBasicMaterial({ color: 0x020306, fog: false })); gr.rotation.x = -Math.PI / 2; gr.position.y = 1; sc.add(gr);
hills(-1800, 140, 0x060912, 3); hills(-900, 80, 0x04060b, 7); hills(-300, 30, 0x020306, 11);
const town = []; for (let i = 0; i < 260; i++) town.push((K.rnd() - 0.5) * 500 - 500, 10 + K.rnd() * 22, -1500 - K.rnd() * 120);
const tg = new THREE.BufferGeometry(); tg.setAttribute("position", new THREE.Float32BufferAttribute(town, 3));
sc.add(new THREE.Points(tg, new THREE.PointsMaterial({ color: 0xffc070, size: 3.6, sizeAttenuation: false, transparent: true, opacity: 0.9, fog: false })));
K.sprite(sc, K.glowTex("rgba(255,170,90,.45)"), 900, V(-500, 40, -1520), 0.7);
// Mars + Jupiter (Abstand am Himmel ≈ 1,2°; Vollmond ≈ 0,5°)
const MJ = V(-60, 1100, -2400), dMJ = MJ.length(), DEG = dMJ * Math.PI / 180;
const right = V(1, 0, 0), up = V(0, 1, 0).sub(MJ.clone().normalize().multiplyScalar(MJ.clone().normalize().y)).normalize();
const jPos = MJ.clone().add(right.clone().multiplyScalar(-0.6 * DEG)).add(up.clone().multiplyScalar(0.12 * DEG));
const mPos = MJ.clone().add(right.clone().multiplyScalar(0.6 * DEG)).add(up.clone().multiplyScalar(-0.12 * DEG));
const jup = K.sprite(sc, K.glowTex("rgba(255,252,240,1)"), 9, jPos, 1), jupH = K.sprite(sc, K.glowTex("rgba(255,245,220,.35)"), 34, jPos, 0.9);
const mars = K.sprite(sc, K.glowTex("rgba(255,120,70,1)"), 6, mPos, 1), marsH = K.sprite(sc, K.glowTex("rgba(255,110,60,.3)"), 18, mPos, 0.8);
const ghosts = [-0.25, 0.25].map((k) => { const g = new THREE.Group(); const ring = new THREE.Mesh(new THREE.RingGeometry(0.235 * DEG, 0.25 * DEG, 64), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, fog: false }));
  const disc = new THREE.Mesh(new THREE.CircleGeometry(0.235 * DEG, 64), new THREE.MeshBasicMaterial({ color: 0xfff1c0, transparent: true, opacity: 0, fog: false })); g.add(disc, ring); g.position.copy(MJ.clone().add(right.clone().multiplyScalar(k * DEG))); g.lookAt(0, 40, 60); sc.add(g); return { ring, disc }; });
// Mensch auf dem Hügel
const pc = document.createElement("canvas"); pc.width = 256; pc.height = 256; const pg = pc.getContext("2d"); pg.fillStyle = "#010204";
pg.beginPath(); pg.arc(128, 70, 26, 0, 7); pg.fill(); pg.beginPath(); pg.moveTo(90, 110); pg.quadraticCurveTo(128, 92, 166, 110); pg.lineTo(180, 200); pg.lineTo(220, 210); pg.lineTo(220, 240); pg.lineTo(40, 240); pg.lineTo(70, 200); pg.closePath(); pg.fill();
const person = new THREE.Mesh(new THREE.PlaneGeometry(36, 36), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(pc), transparent: true, depthWrite: false, fog: false })); person.position.set(60, 28, -300); sc.add(person);

// ===== Szene 2: Weltall – echte Abstände (Linie Erde → Mars → Jupiter, 1 Mio. km = 1 Einheit) =====
const sp = new THREE.Scene(); K.stars(sp, 6000, -1, 9000, 2.0);
const sunL = new THREE.DirectionalLight(0xfff4e6, 3.2); sunL.position.set(-1, 0.3, 0.8); sp.add(sunL); sp.add(new THREE.AmbientLight(0x334466, 0.35));
const EA = K.earth(sp, { day, night, topo }, 34); EA.group.position.set(0, 0, 0); EA.U.sun.value.set(-1, 0.3, 0.8).normalize();
const mc = document.createElement("canvas"); mc.width = 1024; mc.height = 512; const mg = mc.getContext("2d"); mg.fillStyle = "#b8562c"; mg.fillRect(0, 0, 1024, 512);
mg.globalCompositeOperation = "multiply"; mg.globalAlpha = 0.6; mg.filter = "brightness(0.5)"; mg.drawImage(K.noiseCanvas(512, 256, 1.4, 6, 0.45, 0.3), 0, 0, 1024, 512); mg.filter = "none"; mg.globalAlpha = 1; mg.globalCompositeOperation = "source-over";
mg.fillStyle = "rgba(255,255,255,.9)"; mg.fillRect(0, 0, 1024, 26); mg.fillRect(0, 494, 1024, 18);
const mTex = new THREE.CanvasTexture(mc); mTex.colorSpace = THREE.SRGBColorSpace;
const MARS = new THREE.Mesh(new THREE.SphereGeometry(26, 64, 48), new THREE.MeshStandardMaterial({ map: mTex, roughness: 1 })); MARS.position.set(4, 195, 0); sp.add(MARS);
const jTex = await new THREE.TextureLoader().loadAsync("assets/jupiter-cassini.jpg"); jTex.colorSpace = THREE.SRGBColorSpace;
const JUP = new THREE.Mesh(new THREE.SphereGeometry(70, 96, 64), new THREE.MeshStandardMaterial({ map: jTex, roughness: 1 })); JUP.position.set(16, 788, 0); sp.add(JUP);
const lineM = new THREE.LineDashedMaterial({ color: 0xffd23f, dashSize: 14, gapSize: 10, transparent: true, opacity: 0.8 });
const ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), JUP.position.clone()]), lineM); ln.computeLineDistances(); sp.add(ln);
const light = K.sprite(sp, K.glowTex("rgba(255,240,200,1)"), 40, V(0, 0, 0), 0);
// 20 Mars quer durch Jupiter (Jupiter ≈ 20,6 × Mars-Durchmesser)
const row = []; for (let i = 0; i < 20; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(1.7, 24, 16), MARS.material); m.position.copy(JUP.position).add(V(-66.5 + i * 7, 0, 72)); m.visible = false; sp.add(m); row.push(m); }

// ===== Analyse-Ebene =====
const A = new Ebene(document.getElementById("root"));
const P = (v) => { cam.updateMatrixWorld(true); const q = v.clone().project(cam); return [(q.x + 1) / 2 * 1080, (1 - q.y) / 2 * 1920]; };
const tAm = W("am", 8.5), tMars1 = W("mars", 11), tJup1 = W("jupiter", 11.8), tSoEin = W("so", 14), tJahre = W("jahre", 16), tZw = W("zwischen", 17), tVoll = W("vollmonde"), tAber = W("aber"), tTaeu = W("täuschung"), tMars2 = W("mars", 22), t195 = W("hundertfünf"), tJup2 = W("jupiter", 26.5), tVier = W("viermal"), t800 = W("achthundert"), tZw2 = W("zwischen", 31), t600 = W("sechshundert"), tLicht = W("sein", 35), t44 = W("vierundvierzig"), tUnd = W("und", 39), tRies = W("riesig"), t20 = W("zwanzig"), tKlappt = W("so", 45), tSonne = W("sonnenaufgang"), t6 = W("sechs", 48), tSchau = W("schau"), tSued = W("süden"), tHoch = W("hoch"), tDer = W("der", 52), tJup3 = W("jupiter", 53), tKlein = W("kleine"), tMit = W("mit", 57), tFern = W("fernglas"), tMonde = W("monde"), tWeck = W("stellst"), tFolg = W("folg", 62);
// Datum
A.zettel("15. + 16.<br>November", 300, 640, { t0: tAm, t1: tSoEin - 0.2, rot: -5, size: 64 });
const jLab = A.hand("Jupiter ↓", 0, 0, { t0: tJup1, t1: tSoEin - 0.2, size: 56, farbe: "#fff" });
const mLab = A.hand("↑ Mars", 0, 0, { t0: tMars1, t1: tSoEin - 0.2, size: 56, farbe: "#ff8a5a" });
// alle ~2 Jahre
A.karte("Mars trifft Jupiter", 140, 560, 800, 400, { t0: tSoEin - 0.1, t1: tZw - 0.2, unter: "NUR ETWA ALLE 2 JAHRE" });
[["Mai 2022", 280], ["Aug. 2024", 540], ["Nov. 2026", 800]].forEach(([y, x], i) => { A.hand("🔴⚪", x, 760, { t0: tSoEin + 0.3 + i * 0.35, t1: tZw - 0.2, size: 60 }); A.hand(y, x, 860, { t0: tSoEin + 0.4 + i * 0.35, t1: tZw - 0.2, size: 50, farbe: i === 2 ? GELB : "#fff" }); });
A.kreis(800, 820, 130, 100, { t0: tJahre, t1: tZw - 0.2, farbe: GELB });
// zwei Vollmonde
A.hand("◯ ◯ = 2 Vollmonde", 540, 640, { t0: tVoll - 0.3, t1: tAber - 0.2, size: 70, farbe: GELB });
A.hand("nur ≈ 1,2 Grad", 540, 1260, { t0: tVoll + 0.3, t1: tAber - 0.2, size: 58, farbe: "#fff" });
// Täuschung
A.stempel("TÄUSCHUNG!", 540, 640, { t0: tTaeu, t1: tMars2 - 0.2, rot: -7, farbe: ROT });
A.hand("von der Erde aus gesehen 👀", 540, 1270, { t0: tAber, t1: tMars2 - 0.2, size: 52, farbe: "#fff" });
// Abstände (Planeten stehen bei x≈364, Erde y≈1300, Mars y≈1072, Jupiter y≈559)
A.hand("🌍 Erde", 640, 1300, { t0: tMars2, t1: tUnd - 0.2, size: 56, farbe: "#7fd0ff" });
A.zahl(720, 1110, { von: 0, bis: 195, t0: t195 - 0.3, t1: tUnd - 0.2, dauer: 1.2, fmt: (v) => Math.round(v) + " Mio.", farbe: "#ff8a5a", unter: "km bis zum Mars" });
A.zahl(720, 600, { von: 0, bis: 788, t0: t800 - 0.4, t1: tUnd - 0.2, dauer: 1.3, fmt: (v) => Math.round(v) + " Mio.", farbe: GELB, unter: "km bis zum Jupiter" });
A.stempel("4× SO WEIT", 760, 780, { t0: tVier, t1: tZw2 - 0.2, rot: -6, farbe: GELB });
A.zettel("dazwischen:<br>≈ 600 Mio. km!", 760, 820, { t0: t600 - 0.4, t1: tLicht - 0.2, rot: 4, size: 52 });
A.zahl(760, 820, { von: 0, bis: 44, t0: t44 - 0.6, t1: tUnd - 0.2, dauer: 1.4, fmt: (v) => "⏱️ " + Math.round(v) + " Min.", farbe: "#fff", unter: "braucht das Licht" });
A.hand("Größen nicht maßstabsgetreu", 540, 1365, { t0: tMars2, t1: tUnd - 0.2, size: 34, farbe: "rgba(255,255,255,.6)" });
// Jupiter riesig
A.zahl(540, 640, { von: 0, bis: 20, t0: t20 - 0.1, t1: tKlappt - 0.2, dauer: 2.4, fmt: (v) => Math.round(v) + " × Mars", farbe: "#ff8a5a", unter: "passen quer durch Jupiter" });
A.hand("echte Jupiter-Karte (NASA Cassini)", 540, 1290, { t0: tUnd, t1: tKlappt - 0.2, size: 38, farbe: "rgba(255,255,255,.75)" });
// Anleitung
A.zettel("⏰ gegen 6 Uhr<br>vor Sonnenaufgang", 540, 680, { t0: tSonne - 0.3, t1: tSchau - 0.2, rot: -4, size: 60 });
A.karte("Wohin schauen?", 220, 540, 640, 380, { t0: tSchau - 0.1, t1: tDer - 0.2, unter: "BLICK NACH SÜDEN" });
A.hand("S ⬆", 540, 740, { t0: tSued - 0.2, t1: tDer - 0.2, size: 110, farbe: GELB });
A.hand("ziemlich hoch ↗", 540, 860, { t0: tHoch - 0.2, t1: tDer - 0.2, size: 56, farbe: "#fff" });
const jLab2 = A.hand("Jupiter: hell & weiß ↓", 0, 0, { t0: tJup3 - 0.2, t1: tMit - 0.2, size: 56, farbe: "#fff" });
const mLab2 = A.hand("↑ Mars: klein & rötlich", 0, 0, { t0: tKlein, t1: tMit - 0.2, size: 56, farbe: "#ff8a5a" });
// Fernglas
const fg = `<div style="position:absolute;left:70px;top:110px;width:660px;height:360px">
  <div style="position:absolute;left:0;top:0;width:360px;height:360px;border-radius:50%;background:radial-gradient(#0b1430,#02040c);border:6px solid #444"></div>
  <div style="position:absolute;left:300px;top:0;width:360px;height:360px;border-radius:50%;background:radial-gradient(#0b1430,#02040c);border:6px solid #444"></div>
  <div style="position:absolute;left:316px;top:166px;width:30px;height:30px;border-radius:50%;background:#fff8e8;box-shadow:0 0 26px #fff"></div>
  ${[[140, 6, "Io"], [235, 4, "Europa"], [430, 5, "Ganymed"], [560, 3, "Kallisto"]].map(([x, d, n]) => `<div style="position:absolute;left:${x}px;top:178px;width:9px;height:9px;border-radius:50%;background:#e8eeff;box-shadow:0 0 10px #fff"></div><div style="position:absolute;left:${x - 40}px;top:206px;width:90px;text-align:center;font:700 28px Caveat,cursive;color:#7fd0ff">${n}</div>`).join("")}</div>`;
A.karte("Durchs Fernglas 🔭", 140, 560, 800, 520, { t0: tFern - 0.2, t1: tWeck - 0.2, unter: "4 GROSSE MONDE", html: fg });
A.zettel("Wecker stellen? ⏰<br>Ja / Nein 👇", 540, 760, { t0: tWeck, t1: tFolg - 0.1, rot: -3, size: 64 });

// ===== Ablauf =====
const place = (it, p, dx, dy) => { it.el.style.left = p[0] + dx + "px"; it.el.style.top = p[1] + dy + "px"; };
renderAt = (t) => {
  label(""); E.grade.uniforms.flash.value = 0;
  ghosts.forEach((g) => { g.ring.material.opacity = 0; g.disc.material.opacity = 0; });
  light.material.opacity = 0; row.forEach((m) => (m.visible = false));
  EA.group.visible = true; ln.visible = true; MARS.scale.setScalar(1); MARS.position.x = 4; JUP.scale.setScalar(1);
  let scene = sc, pos = V(0, 40, 60), look = MJ.clone(), fov = 40;
  E.look([0.95, 0.98, 1.08], [0.004, 0.006, 0.02], 0.7, 0.8);
  const ground = t < tAber - 0.05 || t >= tKlappt - 0.05;
  if (ground) {
    dawn.material.opacity = t >= tKlappt ? 0.35 + 0.5 * prog(t, tKlappt, 8) : 0.15;
    if (t < tAm - 0.05) { const f = K.eio(prog(t, 0, tAm)); look = V(lerp(300, MJ.x, f), lerp(200, MJ.y, f), MJ.z); fov = lerp(55, 34, f); }
    else if (t < tSoEin - 0.05) { const f = K.eio(prog(t, tAm, 1.6)); fov = lerp(34, 9, f); }
    else if (t < tZw - 0.05) { fov = 22; look = MJ.clone().add(V(0, -60, 0)); }
    else if (t < tAber - 0.05) { const f = K.eio(prog(t, tZw, 1.2)); fov = lerp(22, 3.2, f); const g = cl((t - tVoll + 0.4) / 0.5);
      ghosts.forEach((q) => { q.ring.material.opacity = g; q.disc.material.opacity = g * 0.12; }); }
    else if (t < tSchau - 0.05) { const f = prog(t, tKlappt, tSchau - tKlappt); pos = V(-40, 50, 140); look = V(lerp(-200, MJ.x, f), lerp(300, 700, f), MJ.z); fov = 50; }
    else if (t < tDer - 0.05) { pos = V(-40, 50, 140); look = MJ.clone().add(V(0, -300, 0)); fov = 50; }
    else { const f = K.eio(prog(t, tDer, 1.4)); pos = V(-40, 50, 140); look = MJ.clone(); fov = lerp(50, 7, f); }
    const tw = 0.9 + 0.1 * Math.sin(t * 7); jup.material.opacity = tw; mars.material.opacity = 0.95;
  } else if (t < tMars2 - 0.05) { // hinter der Erde: beide scheinbar dicht beieinander
    scene = sp; E.look([1.0, 0.99, 1.04], [0.002, 0.002, 0.01], 0.4, 0.85);
    pos = V(0, 20, 0); look = V(10, 330, 0); fov = 12; EA.group.visible = false; ln.visible = false; MARS.scale.setScalar(0.15); MARS.position.x = 14; JUP.scale.setScalar(0.35);
  } else if (t < tUnd - 0.05) { // Seitenansicht: echte Abstände
    scene = sp; E.look([1.0, 0.99, 1.04], [0.002, 0.002, 0.01], 0.4, 0.85);
    const s = K.eio(prog(t, tMars2, 1.6)); pos = V(lerp(-2, 190, s), lerp(-120, 362, s), lerp(26, 2809, s)); look = V(lerp(10, 190, s), lerp(700, 362, s), 0); fov = lerp(9, 40, s);
    if (t >= tLicht) { const f = prog(t, tLicht + 0.3, 3.0); light.position.copy(JUP.position).lerp(V(0, 0, 0), f); light.material.opacity = f > 0 && f < 1 ? 1 : 0; }
  } else { // Jupiter ganz nah + 20 Mars
    scene = sp; E.look([1.02, 0.99, 0.98], [0.002, 0.002, 0.008], 0.3, 0.9);
    const f = K.eio(prog(t, tUnd, 1.6)); pos = JUP.position.clone().add(V(lerp(90, 0, f), lerp(-70, -12, f), lerp(480, 240, f))); look = JUP.position.clone().add(V(0, -6, 0)); fov = 40;
    row.forEach((m, i) => (m.visible = t >= t20 + i * 0.11));
  }
  EA.mesh.rotation.y = t * 0.02; EA.clouds.rotation.y = t * 0.025; JUP.rotation.y = t * 0.05; MARS.rotation.y = t * 0.03;
  cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  if (scene === sc) { const pj = P(jPos), pm = P(mPos); place(jLab, pj, 0, -110); place(mLab, pm, 0, 110); place(jLab2, pj, 0, -120); place(mLab2, pm, 0, 120); }
  E.render(scene, t); A.update(t); cap(t);
};
