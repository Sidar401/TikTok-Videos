const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
K.reseed(6);
const sc = new THREE.Scene(); K.stars(sc, 6000, -1, 3500, 2.2);
const EA = K.earth(sc, { day, night, topo }, 40); EA.group.position.set(0, -58, -20); EA.U.sun.value.set(-0.6, 0.6, 0.5).normalize();
const sunL = new THREE.DirectionalLight(0xfff4e6, 3); sunL.position.set(-30, 30, 25); sc.add(sunL); sc.add(new THREE.AmbientLight(0x445577, 0.7));
// Hubble
function makeHubble() { const g = new THREE.Group();
  const silver = new THREE.MeshStandardMaterial({ color: 0xdfe3e8, metalness: 0.75, roughness: 0.3 }), foil = new THREE.MeshStandardMaterial({ color: 0xc8ccd2, metalness: 0.9, roughness: 0.45 }), dark = new THREE.MeshStandardMaterial({ color: 0x23262c, roughness: 0.6 });
  const tube = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 6, 48), silver); tube.rotation.z = Math.PI / 2; g.add(tube);
  const aft = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, 2.4, 12), foil); aft.rotation.z = Math.PI / 2; aft.position.x = -3.9; g.add(aft);
  const door = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.25, 0.12, 48), dark); door.rotation.z = Math.PI / 2; door.position.set(3.1, 0, 0); g.add(door);
  const lid = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2.4, 2.4), silver); lid.position.set(3.3, 1.2, 0); lid.rotation.z = -0.9; g.add(lid);
  const pc = document.createElement("canvas"); pc.width = 256; pc.height = 128; const q = pc.getContext("2d"); q.fillStyle = "#1a2a5a"; q.fillRect(0, 0, 256, 128); q.strokeStyle = "#c9a24a"; q.lineWidth = 2; for (let x = 0; x <= 256; x += 21) { q.beginPath(); q.moveTo(x, 0); q.lineTo(x, 128); q.stroke(); }
  const pt = new THREE.CanvasTexture(pc); pt.colorSpace = THREE.SRGBColorSpace; const pm = new THREE.MeshStandardMaterial({ map: pt, metalness: 0.5, roughness: 0.35, emissive: 0x0a1430, side: THREE.DoubleSide });
  [-1, 1].forEach((s) => { const p = new THREE.Mesh(new THREE.BoxGeometry(5, 0.05, 1.8), pm); p.position.set(-1.5, 0, s * 3.2); g.add(p); const a = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.8, 8), dark); a.rotation.x = Math.PI / 2; a.position.set(-1.5, 0, s * 1.9); g.add(a); });
  const ant = new THREE.Mesh(new THREE.SphereGeometry(0.5, 24, 12, 0, Math.PI * 2, 0, 1.2), silver); ant.position.set(-1, 1.6, 0); g.add(ant);
  return g; }
const hub = makeHubble(); sc.add(hub);
// Rettungs-Raumschiff
const tug = new THREE.Group(); const tb = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.1, 3, 32), new THREE.MeshStandardMaterial({ color: 0xf2f2f2, metalness: 0.3, roughness: 0.4 })); tb.rotation.z = Math.PI / 2; tug.add(tb);
const tn = new THREE.Mesh(new THREE.ConeGeometry(1.0, 1.4, 32), tb.material); tn.rotation.z = -Math.PI / 2; tn.position.x = 2.2; tug.add(tn);
[-1, 1].forEach((s) => { const p = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.05, 2.4), new THREE.MeshStandardMaterial({ color: 0x1a2a5a, metalness: 0.5, roughness: 0.4 })); p.position.set(0, 0, s * 2); tug.add(p); });
sc.add(tug); const thr = K.sprite(sc, K.glowTex("rgba(150,200,255,1)"), 2.4, V(0, 0, 0), 0);
// Säulen der Schöpfung (Nebel aus Sprites)
const neb = new THREE.Group(); sc.add(neb); neb.position.set(0, 0, -400);
const nT = K.glowTex("rgba(255,170,90,.55)"), nT2 = K.glowTex("rgba(90,200,190,.35)"), nT3 = K.glowTex("rgba(40,20,10,.9)");
for (let i = 0; i < 220; i++) { K.reseed(900 + i); const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: K.rnd() < 0.5 ? nT : nT2, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.3 })); s.position.set((K.rnd() - 0.5) * 300, (K.rnd() - 0.5) * 500, (K.rnd() - 0.5) * 60); s.scale.setScalar(60 + K.rnd() * 120); neb.add(s); }
[[-60, 0.9], [20, 1.3], [90, 0.7]].forEach(([x, hgt]) => { for (let i = 0; i < 40; i++) { K.reseed(1500 + i + x); const k = i / 40; const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: nT3, transparent: true, depthWrite: false, opacity: 0.85 })); s.position.set(x + Math.sin(k * 6) * 8 + (K.rnd() - 0.5) * 10, -220 + k * 300 * hgt, 10); s.scale.setScalar(70 - k * 40); neb.add(s); }
  const tip = new THREE.Sprite(new THREE.SpriteMaterial({ map: K.glowTex("rgba(255,220,170,.9)"), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); tip.position.set(x, -220 + 300 * hgt, 12); tip.scale.setScalar(40); neb.add(tip); });
neb.visible = false;
// Absturz-Feuer
const fire = []; for (let i = 0; i < 30; i++) fire.push(K.sprite(sc, K.glowTex("rgba(255,230,180,1)"), 2, V(0, 0, 0), 0));

const A = new Ebene(document.getElementById("root"));
const W = (w, ab = 0) => wortZeit(WORDS, w, ab);
const t90 = W("neunzehnhundert"), tBus = W("schulbus"), tElf = W("elf"), tMio = W("million"), tAlt = W("alt"), tSaeul = W("säulen"), tFuenf = W("fünfmal"), t09 = W("zweitausendneun"), tSinkt = W("sinkt"), tLuft = W("luft"), tSwift = W("swift"), t33 = W("zweitausenddrei"), tFirm = W("firmen", 49), tDock = W("andocken"), t600 = W("sechshundert"), tNov = W("november"), tGeld = W("geld"), tSoll = W("sollte");
A.logo("assets/logos/nasa.svg", 90, 560, 300, 240, { t0: t90 - 0.6, t1: 12.4, rot: -4 });
A.karte("Hubble", 450, 560, 540, 300, { t0: t90 - 0.5, t1: 12.4, unter: "IM ALL SEIT" });
A.zahl(720, 770, { von: 1970, bis: 1990, t0: t90, t1: 12.4, dauer: 1.0, fmt: (v) => String(Math.round(v)), farbe: GELB });
A.karte("Größe & Gewicht", 120, 560, 840, 420, { t0: tBus - 0.6, t1: 16.3 });
A.hand("🚌 so groß wie ein Schulbus", 540, 720, { t0: tBus, t1: 16.3, size: 64, farbe: "#fff" });
A.zahl(540, 860, { von: 0, bis: 11, t0: tElf - 0.3, t1: 16.3, dauer: 0.9, fmt: (v) => "≈ " + Math.round(v) + " Tonnen", farbe: GELB });
A.zahl(540, 700, { von: 0, bis: 1000000, t0: tMio - 1.2, t1: 20.8, dauer: 1.8, fmt: (v) => (Math.round(v / 1000) * 1000).toLocaleString("de-DE") + "+", farbe: GELB, unter: "Beobachtungen in über 30 Jahren" });
A.zettel("Alter des Universums:<br>≈ 13,8 Mrd. Jahre", 540, 640, { t0: tAlt - 0.4, t1: 24.1, rot: -4, size: 56 });
A.stempel("SÄULEN DER SCHÖPFUNG", 540, 600, { t0: tSaeul, t1: 27.4, rot: -5, farbe: GELB });
A.karte("Reparaturen im All", 110, 540, 860, 520, { t0: tFuenf - 0.2, t1: 33.4, unter: "MIT DEM SPACE SHUTTLE" });
["1993", "1997", "1999", "2002", "2009"].forEach((y, i) => { A.hand("👨‍🚀", 220 + i * 160, 760, { t0: tFuenf + 0.2 + i * 0.3, t1: 33.4, size: 80 }); A.hand(y, 220 + i * 160, 870, { t0: tFuenf + 0.3 + i * 0.3, t1: 33.4, size: 46, farbe: i === 4 ? GELB : "#fff" }); });
A.kreis(860, 820, 90, 110, { t0: t09, t1: 33.4, farbe: GELB });
A.karte("Höhe von Hubble", 100, 520, 880, 700, { t0: tSinkt - 0.4, t1: 43.6, unter: "KILOMETER ÜBER DER ERDE" });
A.balken(170, 640, 740, 460, [{ name: "1990", wert: 615, text: "≈ 615", farbe: GRUEN }, { name: "2002", wert: 575, text: "≈ 575", farbe: GELB }, { name: "heute", wert: 510, text: "≈ 510", farbe: ORANGE }, { name: "Ziel", wert: 600, text: "600", farbe: BLAU }], { t0: tSinkt, t1: 43.6, versatz: 0.35, max: 640 });
A.pfeil(860, 760, 640, 980, { t0: tLuft, t1: 43.6, bogen: 0.25, farbe: ROT }); A.hand("Luft bremst ↓", 820, 700, { t0: tLuft + 0.2, t1: 43.6, size: 56, farbe: ROT });
A.zettel("wie Swift 🔥", 760, 1290, { t0: tSwift - 0.3, t1: 43.6, rot: -5, size: 58 });
A.stempel("ABSTURZ ≈ 2033", 540, 700, { t0: t33 - 0.2, t1: 48.8, rot: -7, farbe: ROT });
A.logo("assets/logos/nasa.svg", 390, 540, 300, 240, { t0: tFirm - 0.6, t1: 51.9 }); A.zettel("Gesucht:<br>Retter! 🛟", 540, 950, { t0: tFirm, t1: 51.9, rot: -4, size: 64 });
A.hand("andocken 🔗", 330, 640, { t0: tDock - 0.2, t1: 56.9, size: 66, farbe: "#fff" }); A.zahl(760, 700, { von: 510, bis: 600, t0: t600 - 0.3, t1: 56.9, dauer: 1.2, fmt: (v) => Math.round(v) + " km", farbe: BLAU, unter: "Ziel-Höhe" });
A.pfeil(760, 1180, 760, 900, { t0: t600 + 0.4, t1: 56.9, bogen: 0, farbe: BLAU });
A.karte("Frist", 210, 560, 660, 420, { t0: tNov - 1.0, t1: 60.9, unter: "IDEEN EINREICHEN BIS" }); A.hand("30. Nov.", 540, 780, { t0: tNov - 0.6, t1: 60.9, size: 120, farbe: GELB }); A.kreis(540, 790, 230, 90, { t0: tNov, t1: 60.9 });
A.stempel("GELD: 0 €", 540, 760, { t0: tGeld, t1: 63.7, rot: -8, farbe: ROT }); A.hand("noch kein Budget", 540, 900, { t0: tGeld + 0.6, t1: 63.7, size: 60, farbe: "#fff" });
A.zettel("Retten? 👍 / 👎", 540, 760, { t0: tSoll, t1: 67.3, rot: -4, size: 70 });

renderAt = (t) => {
  label(""); E.look([1.0, 0.99, 1.04], [0.002, 0.002, 0.01], 0.22, 0.93); E.grade.uniforms.flash.value = 0;
  hub.visible = true; EA.group.visible = true; tug.visible = false; thr.material.opacity = 0; neb.visible = false; fire.forEach((f) => (f.material.opacity = 0));
  EA.mesh.rotation.y = t * 0.01; EA.clouds.rotation.y = t * 0.012;
  hub.position.set(0, 0, 0); hub.rotation.set(0.2, 0.6 + t * 0.03, 0.05);
  if (t < 8.4) { const f = K.eout(prog(t, 0, 8.4)); cam.position.set(lerp(-30, -10, f), lerp(6, 3, f), lerp(40, 16, f)); cam.lookAt(0, -1, 0); }
  else if (t < 21.2) { const a = 0.8 + t * 0.05; cam.position.set(Math.sin(a) * 18, 4, Math.cos(a) * 18); cam.lookAt(0, -1.5, 0); }
  else if (t < 24.1) { cam.position.set(-14, 3, 10); cam.lookAt(0, -1, 0); }
  else if (t < 27.7) { neb.visible = true; hub.visible = false; EA.group.visible = false; const f = prog(t, 24.1, 3.6); cam.position.set(0, -40, lerp(340, 240, f)); cam.lookAt(0, -40, -400); }
  else if (t < 33.4) { const a = 2 + t * 0.04; cam.position.set(Math.sin(a) * 12, 2, Math.cos(a) * 12); cam.lookAt(0, 0, 0); }
  else if (t < 43.7) { const f = prog(t, 33.4, 10.3); hub.position.y = -f * 2; cam.position.set(30, 10, 34); cam.lookAt(0, -5, 0); }
  else if (t < 48.9) { const f = prog(t, 43.7, 5.2); hub.position.set(lerp(0, 10, f), lerp(-2, -6.5, K.eio(f)), 0); hub.rotation.set(t * 0.8, t * 0.5, t * 0.3);
    if (f > 0.4) fire.forEach((s, i) => { const k = i / fire.length; s.position.copy(hub.position).add(V(-k * 6, k * 2.5, 0)); s.scale.setScalar((2.6 - k * 2) * (f - 0.3)); s.material.opacity = (1 - k) * Math.min(1, (f - 0.4) * 3); });
    cam.position.set(10, 4, 26); cam.lookAt(4, -4, 0); E.grade.uniforms.flash.value = t > 47.8 && t < 48.2 ? 0.2 : 0; }
  else if (t < 57) { tug.visible = true; const d = K.eio(prog(t, 50, 3.6)); tug.position.set(lerp(-26, -7.6, d), 0, 0); tug.rotation.set(0, 0, 0); hub.rotation.set(0, 0, 0); hub.position.set(0, 0, 0);
    if (t > 54.7) { const up = K.eio(prog(t, 54.7, 2.3)); hub.position.y = up * 4; tug.position.y = up * 4; } thr.position.copy(tug.position).add(V(-2.2, 0, 0)); thr.material.opacity = t > 54.7 ? 1 : 0.5 * (1 - d);
    cam.position.set(-6, 5, 22); cam.lookAt(-4, hub.position.y, 0); }
  else { const a = 1 + t * 0.05; cam.position.set(Math.sin(a) * 24, 5, Math.cos(a) * 24); cam.lookAt(0, -1, 0); }
  E.render(sc, t); A.update(t); cap(t);
};
