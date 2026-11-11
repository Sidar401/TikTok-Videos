const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
const WT = (w, ab = 0) => wortZeit(WORDS, w, ab);
function tintTex(base, w, h, seed, sc2, cover) { K.reseed(seed); const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d"); g.fillStyle = base; g.fillRect(0, 0, w, h);
  g.globalCompositeOperation = "multiply"; g.globalAlpha = 0.6; g.filter = "brightness(0.55)"; g.drawImage(K.noiseCanvas(w / 2, h / 2, sc2, 6, cover, 0.3), 0, 0, w, h); g.filter = "none"; g.globalAlpha = 0.5; g.globalCompositeOperation = "screen"; g.drawImage(K.noiseCanvas(w / 2, h / 2, sc2 * 2.5, 5, 0.55, 0.2), 0, 0, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
// ===== Welt A: Observatorium in den Anden bei Nacht =====
K.reseed(4);
const obs = new THREE.Scene();
K.sky(obs, 0x02040c, 0x0a1230, 0x1e2a4a, 4000); K.stars(obs, 5000, -0.02, 3800, 2.2);
const mwA = []; for (let i = 0; i < 6000; i++) { const s = (K.rnd() - 0.5) * 3000, w = (K.rnd() + K.rnd() + K.rnd() - 1.5) * 170; mwA.push(s * 0.6, 700 + s * 0.5 + w, -2800 + w); }
const mga = new THREE.BufferGeometry(); mga.setAttribute("position", new THREE.Float32BufferAttribute(mwA, 3)); obs.add(new THREE.Points(mga, new THREE.PointsMaterial({ color: 0xd8dcff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0.5, fog: false })));
const mtn = new THREE.Mesh(new THREE.ConeGeometry(260, 120, 64, 1), new THREE.MeshStandardMaterial({ color: 0x1a1612, roughness: 1 })); mtn.position.set(0, -60, -60); obs.add(mtn);
const rangeM = new THREE.MeshBasicMaterial({ color: 0x070a14, fog: false }); for (let i = 0; i < 8; i++) { K.reseed(30 + i); const m = new THREE.Mesh(new THREE.ConeGeometry(300 + K.rnd() * 300, 90 + K.rnd() * 90, 48), rangeM); m.position.set(-1500 + i * 420, -40, -1500 - K.rnd() * 600); obs.add(m); }
const white = new THREE.MeshStandardMaterial({ color: 0xa8aebb, roughness: 0.55, metalness: 0.2 });
const bld = new THREE.Mesh(new THREE.BoxGeometry(40, 18, 30), white); bld.position.set(0, 9, -60); obs.add(bld);
const dome = new THREE.Group(); dome.position.set(-8, 18, -60); obs.add(dome);
const dm = new THREE.Mesh(new THREE.CylinderGeometry(13, 13, 10, 48, 1, false), white); dm.position.y = 5; dome.add(dm); const domeCap = new THREE.Mesh(new THREE.SphereGeometry(13, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), white); domeCap.position.y = 10; dome.add(domeCap);
const slit = new THREE.Mesh(new THREE.BoxGeometry(5, 14.4, 2), new THREE.MeshBasicMaterial({ color: 0x080a10 })); slit.position.set(0, 7, 12.6); dome.add(slit);
const tele = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 3.2, 10, 24), new THREE.MeshStandardMaterial({ color: 0x40444c, metalness: 0.7, roughness: 0.4 })); tele.position.set(0, 9, 9); tele.rotation.x = 0.7; dome.add(tele);
const lamp = K.sprite(obs, K.glowTex("rgba(255,60,40,.8)"), 3, V(10, 16, -44), 0.7);
obs.add(new THREE.AmbientLight(0x6070a0, 0.55)); const mlA = new THREE.DirectionalLight(0x9ab0ff, 1.2); mlA.position.set(-200, 300, 300); obs.add(mlA);
const laser = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 1400, 8), new THREE.MeshBasicMaterial({ color: 0xffb040, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, depthWrite: false }));
// ===== Welt B: äußeres Sonnensystem =====
const sp = new THREE.Scene(); K.reseed(8); K.stars(sp, 6000, -1, 3500, 2.2);
const sunS = K.sprite(sp, K.glowTex("rgba(255,248,230,1)"), 30, V(-1600, 200, -2600), 1);
const sunD = new THREE.DirectionalLight(0xfff0e0, 2.4); sunD.position.set(-1600, 200, -2600); sp.add(sunD); sp.add(new THREE.AmbientLight(0x334466, 0.25));
const ed = new THREE.Mesh(new THREE.SphereGeometry(6, 128, 128), new THREE.MeshStandardMaterial({ map: tintTex("#b89a86", 1024, 512, 61, 2.0, 0.45), roughness: 0.95 })); sp.add(ed);
const frost = new THREE.Mesh(new THREE.SphereGeometry(6.06, 96, 96), new THREE.MeshStandardMaterial({ map: (() => { const t = new THREE.CanvasTexture(K.noiseCanvas(512, 256, 3, 5, 0.55, 0.2)); return t; })(), transparent: true, opacity: 0.55, roughness: 0.6, color: 0xe8f2ff })); ed.add(frost);
// Bahnen-Skizze (Draufsicht): Sonne – Erde – Neptun – Pluto – ED138
const orb = new THREE.Group(); sp.add(orb); orb.position.set(0, -1200, 0);
const ring = (r, col, ecc = 0) => { const pts = []; for (let i = 0; i <= 240; i++) { const a = (i / 240) * Math.PI * 2; pts.push(V(Math.cos(a) * r - ecc * r, 0, Math.sin(a) * r * Math.sqrt(1 - ecc * ecc))); } const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: 0.8 })); orb.add(l); return l; };
const S = 6; ring(1 * S, 0x7fd0ff); ring(30 * S, 0x6a8cff); ring(39.5 * S, 0xc8a0ff, 0.25); ring(46 * S, 0xffd23f);
const dot = (x, z, col, size) => { const s = K.sprite(sp, K.glowTex(col), size, V(x, -1200, z), 1); return s; };
dot(0, 0, "rgba(255,245,220,1)", 40); dot(S, 0, "rgba(120,180,255,1)", 10); dot(-30 * S * 0.7, 30 * S * 0.71, "rgba(110,140,255,1)", 18); dot(39.5 * S * 0.5, -39.5 * S * 0.8, "rgba(200,160,255,1)", 14); const edDot = dot(-46 * S * 0.2, -46 * S * 0.98, "rgba(255,210,63,1)", 22);
// Größenvergleich der Zwergplaneten (echte Durchmesser, km/100)
const lineup = new THREE.Group(); sp.add(lineup); lineup.position.set(0, 2400, 0);
const DW = [["Pluto", 23.8, "#d9b99b", 1], ["Eris", 23.3, "#e6e6e6", 2], ["Haumea", 16, "#e8e4dc", 3], ["Makemake", 14.3, "#c98b5e", 4], ["Ceres", 9.4, "#8f8a84", 5], ["ED138?", 15, "#b89a86", 6]];
let x0 = -62; const dwPos = [];
DW.forEach(([n, d, col, s], i) => { const r = d / 2; const m = new THREE.Mesh(new THREE.SphereGeometry(r, 96, 96), new THREE.MeshStandardMaterial({ map: tintTex(col, 512, 256, 90 + s, 2, 0.45), roughness: 0.95 })); if (n === "Haumea") m.scale.set(1.35, 0.7, 1); x0 += r + 2.2; m.position.set(x0, 0, 0); x0 += r + 2.2; lineup.add(m); dwPos.push(m); });
lineup.children.forEach((m) => (m.position.x -= 6));
const lineL = new THREE.DirectionalLight(0xffffff, 2.2); lineL.position.set(-50, 2460, 80); sp.add(lineL); lineL.target = lineup;

// ===== Analyse =====
const A = new Ebene(document.getElementById("root"));
const tRub = WT("gefunden"), tChile = WT("chile"), tName = WT("sein"), tGr = WT("könnte"), tCer = WT("dann"), tKreis = WT("kreist"), tKalt = WT("dort"), tJahr = WT("ein", 32), tAlt = WT("verrückte"), tNie = WT("niemand"), tSechs = WT("wird"), tNeben = WT("neben"), tPluto = WT("übrigens"), t2006 = WT("zweitausendsechs", 52), tRubin2 = WT("und", 56), tWie = WT("wie", 62);
A.karte("", 210, 560, 660, 190, { t0: tRub - 0.2, t1: 11.5, html: `<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff;color:#0b1f3a;font:900 46px 'Inter Display',sans-serif;letter-spacing:1px">VERA C. RUBIN<div style="font:700 26px Inter,sans-serif;letter-spacing:6px;color:#3a5a8a">OBSERVATORY</div></div>` });
A.zettel("Chile 🇨🇱", 780, 840, { t0: tChile, t1: 11.5, rot: 6, size: 58 });
A.hand("größte Digitalkamera der Welt", 540, 1240, { t0: tChile + 0.4, t1: 11.5, size: 54, farbe: GELB });
A.hand("2026 ED138", 540, 640, { t0: tName + 0.4, t1: 16.4, size: 130, farbe: GELB, rot: -3 });
A.zettel("noch ohne<br>schönen Namen", 760, 1150, { t0: tName + 2.4, t1: 16.4, rot: 5, size: 52 });
A.karte("Größe", 100, 520, 880, 700, { t0: tGr - 0.2, t1: 23.0, unter: "DURCHMESSER IN KM" });
A.balken(170, 650, 740, 460, [{ name: "Ceres", wert: 940, text: "940", farbe: "#8f8a84" }, { name: "ED138", wert: 1500, text: "600–1.500", farbe: GELB }, { name: "Pluto", wert: 2377, text: "2.377", farbe: "#d9b99b" }], { t0: tGr, t1: 23.0, versatz: 0.35 });
A.stempel("GRÖSSER ALS CERES?", 540, 1300, { t0: tCer + 0.4, t1: 23.0, rot: -5, farbe: GELB });
A.karte("Entfernung zur Sonne", 80, 520, 920, 300, { t0: tKreis - 0.2, t1: 27.2, unter: "ERDE = 1" });
[["Erde", 1, BLAU], ["Neptun", 30, "#8fa8ff"], ["Pluto", 40, "#c8a0ff"], ["ED138", 46, GELB]].forEach(([n, v, f], i) => { const x = 150 + v / 46 * 760; A.hand("●", x, 700, { t0: tKreis + i * 0.35, t1: 27.2, size: 50, farbe: f }); A.hand(`${n}<br>${v}`, x, i === 2 ? 640 : 770, { t0: tKreis + 0.1 + i * 0.35, t1: 27.2, size: 36, farbe: "#fff" }); });
A.strich(150, 680, 910, { t0: tKreis, t1: 27.2, farbe: "rgba(255,255,255,.6)", breite: 4, dauer: 1.2 });
A.kreis(910, 720, 80, 70, { t0: tKreis + 1.8, t1: 27.2, farbe: GELB });
A.zahl(540, 640, { von: 0, bis: -200, t0: tKalt + 0.4, t1: 32.3, dauer: 1.6, fmt: (v) => "unter " + Math.round(v) + " °C", farbe: BLAU, unter: "dunkel & eiskalt" });
A.hand("❄", 860, 520, { t0: tKalt + 0.8, t1: 32.3, size: 120, farbe: BLAU, rot: 10 });
A.zahl(540, 640, { von: 0, bis: 300, t0: tJahr, t1: 35.5, dauer: 1.4, fmt: (v) => "≈ " + Math.round(v) + " Jahre", farbe: GELB, unter: "dauert 1 Jahr auf ED138" });
A.karte("Alte Bilder", 120, 520, 840, 560, { t0: tAlt - 0.2, t1: 42.3, unter: "SCHON SEIT ÜBER 10 JAHREN DRAUF" });
const field = (x, yr, dx) => { let h = ""; K.reseed(500 + dx); for (let i = 0; i < 40; i++) h += `<div style="position:absolute;left:${K.rnd() * 340}px;top:${K.rnd() * 300}px;width:${2 + K.rnd() * 3}px;height:${2 + K.rnd() * 3}px;border-radius:50%;background:#fff;opacity:${0.4 + K.rnd() * 0.6}"></div>`; h += `<div style="position:absolute;left:${150 + dx}px;top:140px;width:9px;height:9px;border-radius:50%;background:${GELB};box-shadow:0 0 12px ${GELB}"></div><div style="position:absolute;left:0;bottom:-48px;width:340px;text-align:center;font:800 34px Inter,sans-serif;color:#fff">${yr}</div>`; return h; };
A.karte("", 160, 640, 360, 320, { t0: tAlt + 0.3, t1: 42.3, html: field(0, "früher", 0) }); A.karte("", 560, 640, 360, 320, { t0: tAlt + 0.7, t1: 42.3, html: field(0, "2026", 60) });
A.kreis(345, 790, 50, 50, { t0: tNie - 0.4, t1: 42.3 }); A.kreis(805, 790, 50, 50, { t0: tNie - 0.2, t1: 42.3 });
A.stempel("ÜBERSEHEN!", 540, 1180, { t0: tNie + 0.3, t1: 42.3, rot: -7, farbe: ROT });
A.stempel("NR. 6?", 540, 640, { t0: tSechs + 0.6, t1: 47.6, rot: -8, farbe: GELB });
A.hand("offiziell nur 5 Zwergplaneten", 540, 760, { t0: tSechs + 1.4, t1: 47.6, size: 56, farbe: "#fff" });
const names = ["Pluto", "Eris", "Haumea", "Makemake", "Ceres", "ED138?"];
const lbls = names.map((n, i) => A.hand(n, 0, 0, { t0: tNeben + 0.2 + i * 0.35, t1: 56.6, size: 44, farbe: i === 5 ? GELB : "#fff" }));
A.karte("2006", 160, 560, 760, 380, { t0: tPluto + 0.3, t1: 56.6, unter: "ENTSCHEIDUNG DER ASTRONOMEN" });
A.hand("Pluto = Planet", 540, 740, { t0: t2006 - 0.4, t1: 56.6, size: 64, farbe: "#fff" }); A.strich(330, 750, 750, { t0: t2006 + 0.2, t1: 56.6, farbe: ROT, breite: 10 });
A.hand("➜ Zwergplanet", 540, 850, { t0: t2006 + 0.6, t1: 56.6, size: 64, farbe: GELB });
A.zettel("Das ist erst<br>der Anfang!", 330, 640, { t0: tRubin2 + 0.6, t1: 62.9, rot: -5, size: 60 });
A.stempel("NEUE ENTDECKUNGEN", 600, 900, { t0: tRubin2 + 3.0, t1: 62.9, rot: 6, farbe: GRUEN });
A.zettel("Dein Name für ihn? 👇", 540, 760, { t0: tWie, t1: 64.5, rot: -4, size: 64 });

renderAt = (t) => {
  label(""); E.look([0.98, 0.99, 1.06], [0.004, 0.005, 0.02], 0.55, 0.84); E.grade.uniforms.flash.value = 0;
  let scene = sp;
  ed.rotation.y = 1.6 + t * 0.03; frost.rotation.y = t * 0.01;
  if (t < 4.2) { const f = K.eout(prog(t, 0, 4.2)); ed.position.set(0, 0, 0); cam.position.set(lerp(-8, 4, f), 3, lerp(60, 22, f)); cam.lookAt(0, 0, 0); }
  else if (t < 7.4) { cam.position.set(6, 3, 21); cam.lookAt(0, 0, 0); }
  else if (t < 11.6 || (t >= 56.8 && t < 63)) {
    scene = obs; const f = t < 11.6 ? prog(t, 7.4, 4.2) : prog(t, 56.8, 6.2);
    cam.position.set(lerp(-95, -75, f), lerp(14, 20, f), lerp(70, 50, f)); cam.lookAt(-6, 40 + f * 30, -60);
    dome.rotation.y = 0.5 + Math.sin(t * 0.3) * 0.2;
  } else if (t < 23.1) { const f = prog(t, 11.6, 11.5); cam.position.set(lerp(-14, 10, f), 4, lerp(26, 20, f)); cam.lookAt(0, 0, 0); }
  else if (t < 27.4) { const f = K.eio(prog(t, 23.1, 4.1)); cam.position.set(0, -1200 + lerp(500, 380, f), lerp(260, 80, f)); cam.lookAt(-30, -1200, -120); }
  else if (t < 32.4) { const f = prog(t, 27.4, 5); cam.position.set(lerp(9, 14, f), -2, 13); cam.lookAt(0, 0, 0); E.look([0.9, 0.98, 1.12], [0, 0.006, 0.03], 0.5, 0.84); }
  else if (t < 35.8) { const f = prog(t, 32.4, 3.4); cam.position.set(0, -1200 + 420, 120); cam.lookAt(-20, -1200, -60); edDot.material.opacity = 0.6 + 0.4 * Math.sin(t * 6); }
  else if (t < 42.4) { cam.position.set(4, 2, 30); cam.lookAt(0, 0, 0); }
  else if (t < 47.8) { const f = prog(t, 42.4, 5.4); cam.position.set(lerp(-20, 0, f), 1, lerp(26, 18, f)); cam.lookAt(0, 0, 0); }
  else if (t < 56.8) { const f = prog(t, 47.8, 9); cam.position.set(lerp(-8, 8, f), 2400 - 25, 340); cam.lookAt(0, 2400 - 25, 0); }
  else { cam.position.set(-10, 6, 30); cam.lookAt(0, 0, 0); }
  // Namen unter die Zwergplaneten setzen
  if (t >= 47.8 && t < 56.8) { cam.updateMatrixWorld(true); lineup.updateMatrixWorld(true); dwPos.forEach((m, i) => { const p = m.getWorldPosition(V(0, 0, 0)).add(V(0, -14, 0)).project(cam); lbls[i].el.style.left = ((p.x + 1) / 2 * 1080).toFixed(0) + "px"; lbls[i].el.style.top = ((1 - p.y) / 2 * 1920).toFixed(0) + "px"; }); }
  E.render(scene, t); A.update(t); cap(t);
};
