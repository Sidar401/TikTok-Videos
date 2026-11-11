const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
const WT = (w, ab = 0) => wortZeit(WORDS, w, ab);
K.reseed(3);
const sc = new THREE.Scene();
K.stars(sc, 6000, -1, 3500, 2.2);
// Milchstraßen-Band
const mw = []; for (let i = 0; i < 9000; i++) { const s = (K.rnd() - 0.5) * 7000, w = (K.rnd() + K.rnd() + K.rnd() - 1.5) * 380; mw.push(s, w + s * 0.3, -3000 + w * 0.3); }
const mwg = new THREE.BufferGeometry(); mwg.setAttribute("position", new THREE.Float32BufferAttribute(mw, 3));
const mwP = new THREE.Points(mwg, new THREE.PointsMaterial({ color: 0xd8dcff, size: 1.5, sizeAttenuation: false, transparent: true, opacity: 0.55 })); sc.add(mwP);
const sunDir = V(-1, 0.15, 0.4).normalize();
const sunL = new THREE.DirectionalLight(0xfff4e6, 3.2); sunL.position.copy(sunDir).multiplyScalar(100); sc.add(sunL); sc.add(new THREE.AmbientLight(0x556688, 0.8));
const sunSpr = K.sprite(sc, K.glowTex("rgba(255,245,220,1)"), 90, sunDir.clone().multiplyScalar(2500), 1);
// Voyager-Sonde
const vg = new THREE.Group(); sc.add(vg);
const white = new THREE.MeshStandardMaterial({ color: 0xf2f2f2, roughness: 0.5, metalness: 0.2, side: THREE.DoubleSide });
const gold = new THREE.MeshStandardMaterial({ color: 0xc9a24a, roughness: 0.35, metalness: 0.8 });
const dark = new THREE.MeshStandardMaterial({ color: 0x2b2d33, roughness: 0.6, metalness: 0.5 });
const dish = new THREE.Mesh(new THREE.SphereGeometry(2.4, 64, 16, 0, Math.PI * 2, 0, 0.62), white); dish.rotation.x = -Math.PI / 2; dish.position.z = 1.5; vg.add(dish);
const feed = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.3, 8), dark); feed.rotation.x = Math.PI / 2; feed.position.z = 1.2; vg.add(feed);
const bus = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.0, 0.5, 10), gold); bus.rotation.x = Math.PI / 2; bus.position.z = -0.1; vg.add(bus);
const boom = (len, dir, r = 0.05) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, 8), dark); m.position.copy(dir.clone().multiplyScalar(len / 2)); m.quaternion.setFromUnitVectors(V(0, 1, 0), dir.clone().normalize()); vg.add(m); return m; };
boom(13, V(0.2, 1, -0.1).normalize(), 0.03);
boom(3.2, V(1, -0.3, 0).normalize(), 0.07); [1.6, 2.2, 2.8].forEach((d) => { const r = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.55, 12), dark); r.position.copy(V(1, -0.3, 0).normalize().multiplyScalar(d)); r.quaternion.setFromUnitVectors(V(0, 1, 0), V(1, -0.3, 0).normalize()); vg.add(r); });
boom(2.6, V(-1, -0.2, 0).normalize(), 0.07); const plat = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.5, 0.6), dark); plat.position.copy(V(-1, -0.2, 0).normalize().multiplyScalar(2.6)); vg.add(plat);
const recC = document.createElement("canvas"); recC.width = recC.height = 512; const rq = recC.getContext("2d"); const rg = rq.createRadialGradient(256, 256, 30, 256, 256, 256); rg.addColorStop(0, "#f2d27a"); rg.addColorStop(1, "#a87a28"); rq.fillStyle = rg; rq.beginPath(); rq.arc(256, 256, 256, 0, 7); rq.fill();
for (let r = 60; r < 250; r += 3) { rq.strokeStyle = `rgba(90,60,10,${0.15 + (r % 9) * 0.02})`; rq.lineWidth = 1; rq.beginPath(); rq.arc(256, 256, r, 0, 7); rq.stroke(); } rq.fillStyle = "#6b4a14"; rq.beginPath(); rq.arc(256, 256, 40, 0, 7); rq.fill();
const recTex = new THREE.CanvasTexture(recC); recTex.colorSpace = THREE.SRGBColorSpace;
const rec = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.03, 64), [new THREE.MeshStandardMaterial({ color: 0xc9a24a, metalness: 0.9, roughness: 0.3 }), new THREE.MeshStandardMaterial({ map: recTex, metalness: 0.85, roughness: 0.3 }), new THREE.MeshStandardMaterial({ map: recTex, metalness: 0.85, roughness: 0.3 })]);
rec.rotation.z = Math.PI / 2; rec.position.set(1.05, 0, -0.1); vg.add(rec);
// Großes Plattenmodell für die Nahaufnahme
const bigRec = new THREE.Mesh(new THREE.CylinderGeometry(3, 3, 0.12, 96), [new THREE.MeshStandardMaterial({ color: 0xc9a24a, metalness: 0.9, roughness: 0.3 }), new THREE.MeshStandardMaterial({ map: recTex, metalness: 0.75, roughness: 0.28 }), new THREE.MeshStandardMaterial({ map: recTex, metalness: 0.75, roughness: 0.28 })]);
bigRec.visible = false; sc.add(bigRec);
const blink = K.sprite(sc, K.glowTex("rgba(120,220,255,1)"), 0.8, V(0, 0, 0), 0);
// Sonnensystem-Ansicht: Erde (blauer Punkt), Linie Erde -> Voyager, Funksignal
const earthDot = K.sprite(sc, K.glowTex("rgba(120,180,255,1)"), 26, V(0, 0, 0), 0);
const lineG = new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(1, 0, 0)]); const line = new THREE.Line(lineG, new THREE.LineDashedMaterial({ color: 0xffd23f, dashSize: 8, gapSize: 6, transparent: true, opacity: 0 })); sc.add(line);
const pulse = K.sprite(sc, K.glowTex("rgba(255,230,120,1)"), 16, V(0, 0, 0), 0);
const vDot = K.sprite(sc, K.glowTex("rgba(255,255,255,1)"), 8, V(0, 0, 0), 0);

// ===== Analyse =====
const A = new Ebene(document.getElementById("root"));
const t77 = WT("neunzehnhundert"), t18 = WT("achtzehn"), tLicht = WT("heißt"), tMrd = WT("sechsundzwanzig"), tFlieg = WT("fliegt"), tTrotz = WT("trotzdem"), tNach = WT("wenn"), tUeber = WT("übermorgen"), tPlatte = WT("goldene"), tSpr = WT("sprachen"), tMus = WT("musik"), tBild = WT("bildern"), tAlien = WT("falls"), tGer = WT("viele"), tStrom = WT("strom"), tVer = WT("verstummen"), tWeit = WT("aber", 54), tMilch = WT("milchstraße"), tHaett = WT("hättest");
A.logo("assets/logos/nasa.svg", 90, 560, 300, 240, { t0: t77 - 0.3, t1: 14.4, rot: -4 });
A.karte("Voyager 1", 450, 560, 540, 300, { t0: t77 - 0.2, t1: 14.4, unter: "START: 5. SEPT. 1977" });
A.zahl(720, 760, { von: 0, bis: 49, t0: t77 + 1.0, t1: 14.4, dauer: 2.2, fmt: (v) => Math.round(v) + " Jahre", unter: "unterwegs", farbe: GELB });
A.zettel("18. November<br>2026", 300, 650, { t0: t18, t1: 19.8, rot: -5, size: 64 });
A.stempel("ERSTMALS", 760, 760, { t0: t18 + 1.2, t1: 19.8, rot: 8, farbe: ROT });
A.hand("1 Lichttag entfernt", 540, 1240, { t0: t18 + 2.0, t1: 19.8, size: 70, farbe: GELB });
A.hand("Licht braucht", 540, 560, { t0: tLicht, t1: 23.8, size: 62, farbe: "#fff" });
A.zahl(540, 700, { von: 0, bis: 24, t0: tLicht + 0.6, t1: 23.8, dauer: 1.6, fmt: (v) => Math.round(v) + " Stunden", farbe: GELB });
A.hand("Erde", 170, 1080, { t0: tLicht + 0.4, t1: 27.2, size: 56, farbe: BLAU }); A.hand("Voyager", 900, 1080, { t0: tLicht + 0.4, t1: 27.2, size: 56, farbe: "#fff" });
A.zahl(540, 700, { von: 0, bis: 25.9, t0: tMrd - 0.4, t1: 27.2, dauer: 1.6, fmt: (v) => v.toFixed(1).replace(".", ",") + " Mrd. km", farbe: GELB, unter: "von der Erde entfernt" });
A.karte("Tempo", 160, 560, 760, 420, { t0: tFlieg - 0.2, t1: 34.0, unter: "KILOMETER PRO STUNDE" });
A.zahl(540, 790, { von: 0, bis: 61000, t0: tFlieg + 0.2, t1: 34.0, dauer: 1.8, fmt: (v) => (Math.round(v / 100) * 100).toLocaleString("de-DE"), farbe: GELB });
A.hand("≈ 17 km pro Sekunde!", 540, 920, { t0: tFlieg + 1.4, t1: 34.0, size: 56, farbe: "#fff" });
A.zettel("…und trotzdem<br>fast 50 Jahre!", 540, 1150, { t0: tTrotz, t1: 34.0, rot: -4, size: 60 });
A.karte("Eine Nachricht an Voyager", 90, 540, 900, 700, { t0: tNach - 0.2, t1: 38.9, unter: "24 STUNDEN HIN · 24 ZURÜCK" });
[["Heute:<br>senden 📡", 300, 760], ["Morgen:<br>kommt an", 760, 900], ["Übermorgen:<br>Antwort!", 300, 1080]].forEach(([n, x, y], i) => A.zettel(n, x, y, { t0: tNach + 0.3 + i * 0.9, t1: 38.9, rot: [-4, 4, -3][i], size: 48 }));
A.pfeil(440, 780, 640, 870, { t0: tNach + 0.8, t1: 38.9, bogen: -0.2 }); A.pfeil(700, 980, 460, 1070, { t0: tNach + 1.7, t1: 38.9, bogen: -0.2 });
A.karte("Die goldene Schallplatte", 120, 540, 840, 360, { t0: tPlatte - 0.2, t1: 45.8, unter: "GRUSS DER MENSCHHEIT" });
A.hand("✓ 55 Sprachen", 320, 720, { t0: tSpr - 0.2, t1: 45.8, size: 56, farbe: GELB }); A.hand("✓ Musik", 700, 720, { t0: tMus, t1: 45.8, size: 56, farbe: GELB }); A.hand("✓ Bilder der Erde", 540, 820, { t0: tBild, t1: 45.8, size: 56, farbe: GELB });
A.zettel("Hallo, Außerirdische! 👽", 540, 700, { t0: tAlien, t1: 48.2, rot: -5, size: 64 });
A.karte("Strom an Bord", 160, 560, 760, 620, { t0: tGer - 0.2, t1: 52.4, unter: "ATOMBATTERIE LÄSST NACH" });
A.balken(260, 730, 560, 330, [{ name: "1977", wert: 100, text: "voll", farbe: GRUEN }, { name: "heute", wert: 47, text: "< Hälfte", farbe: ROT }], { t0: tStrom - 0.8, t1: 52.4, versatz: 0.4 });
A.stempel("BALD STILL", 540, 820, { t0: tVer - 0.3, t1: 55.2, rot: -8, farbe: "#c8ccd4" });
A.hand("Zehntausende Jahre ➜", 540, 620, { t0: tWeit + 1.0, t1: 60.1, size: 64, farbe: GELB });
A.pfeil(300, 1150, 820, 1000, { t0: tMilch - 0.3, t1: 60.1, bogen: -0.15, farbe: BLAU });
A.zettel("Gänsehaut? 🥹", 540, 760, { t0: tHaett, t1: 62.3, rot: -4, size: 72 });

renderAt = (t) => {
  label(""); E.look([1.0, 0.98, 1.06], [0.004, 0.004, 0.018], 0.55, 0.82); E.grade.uniforms.flash.value = 0;
  vg.visible = true; bigRec.visible = false; [earthDot, pulse, vDot].forEach((s) => (s.material.opacity = 0)); line.material.opacity = 0; blink.material.opacity = 0; mwP.material.opacity = 0.55;
  vg.position.set(0, 0, 0); vg.rotation.set(0.15, t * 0.04, 0.05);
  blink.position.set(0.5, 1.0, 1.6); blink.material.opacity = (Math.sin(t * 4) > 0.6 ? 1 : 0) * (t < tGer ? 1 : 0.25);
  if (t < tLicht) {
    // Sonde fliegt – Kamera umkreist
    const a = 0.6 + t * 0.06; const d = t < 4.7 ? lerp(46, 19, K.eout(prog(t, 0, 4.7))) : 19;
    cam.position.set(Math.sin(a) * d, 3 + Math.sin(t * 0.2) * 1.5, Math.cos(a) * d); cam.lookAt(0, 0.8, 0);
  } else if (t < 27.2) {
    // Sonnensystem von weit: Erde ↔ Voyager, Funksignal
    vg.visible = false; const E0 = V(-260, -40, 0), V1 = V(260, 40, 0);
    earthDot.position.copy(E0); earthDot.material.opacity = 1; vDot.position.copy(V1); vDot.material.opacity = 1;
    lineG.setFromPoints([E0, V1]); line.computeLineDistances(); line.material.opacity = 0.8;
    const k = ((t - tLicht) / 3.2) % 1; pulse.position.copy(E0.clone().lerp(V1, k)); pulse.material.opacity = 1;
    cam.position.set(0, 0, 820); cam.lookAt(0, 0, 0);
  } else if (t < 38.9) {
    const a = 1.4 + t * 0.05; cam.position.set(Math.sin(a) * 17, 3, Math.cos(a) * 17); cam.lookAt(0, 0.6, 0);
  } else if (t < 48.2) {
    // Goldene Schallplatte groß
    vg.visible = false; bigRec.visible = true; bigRec.position.set(0, 0, 0); bigRec.rotation.set(Math.PI / 2 - 0.35, 0, t * 0.15);
    cam.position.set(0, -1.5, lerp(13, 10.5, prog(t, 38.9, 9))); cam.lookAt(0, -0.6, 0);
    E.look([1.06, 1.0, 0.9], [0.008, 0.006, 0.01], 0.6, 0.8);
  } else if (t < 55.4) {
    // Strom geht aus: Licht wird schwächer
    const f = prog(t, 48.4, 6.8); sunL.intensity = lerp(3.2, 1.2, f);
    cam.position.set(9, 2.5, 13); cam.lookAt(0, 0.6, 0);
  } else {
    // fliegt weiter durch die Milchstraße
    sunL.intensity = 1.4; mwP.material.opacity = 1;
    const f = prog(t, 55.4, 10.6); cam.position.set(lerp(6, 30, f), lerp(2, 6, f), lerp(10, 60, f)); cam.lookAt(lerp(0, -20, f), 0, lerp(0, -60, f));
  }
  if (t < 48.4) sunL.intensity = 3.2;
  E.render(sc, t); A.update(t); cap(t);
};
