const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
const WT = (w, ab = 0) => wortZeit(WORDS, w, ab);
function tex(base, w, h, seed, sc2, cover, dark = 0.55) { K.reseed(seed); const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d"); g.fillStyle = base; g.fillRect(0, 0, w, h);
  g.globalCompositeOperation = "multiply"; g.globalAlpha = 0.65; g.filter = `brightness(${dark})`; g.drawImage(K.noiseCanvas(w / 2, h / 2, sc2, 6, cover, 0.3), 0, 0, w, h); g.filter = "none"; g.globalAlpha = 0.4; g.globalCompositeOperation = "screen"; g.drawImage(K.noiseCanvas(w / 2, h / 2, sc2 * 3, 5, 0.55, 0.2), 0, 0, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; }
// ===== Welt A: Mars aus dem All =====
const sp = new THREE.Scene(); K.reseed(2); K.stars(sp, 5000, -1, 3500, 2.2);
const mars = new THREE.Mesh(new THREE.SphereGeometry(10, 160, 160), new THREE.MeshStandardMaterial({ map: tex("#c1643a", 2048, 1024, 7, 1.6, 0.45, 0.5), roughness: 1 })); sp.add(mars);
const matm = new THREE.Mesh(new THREE.SphereGeometry(10.5, 96, 96), new THREE.ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, side: THREE.BackSide, depthWrite: false,
  vertexShader: `varying vec3 vN;varying vec3 vW;void main(){vN=normalize(mat3(modelMatrix)*normal);vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}`,
  fragmentShader: `varying vec3 vN;varying vec3 vW;void main(){vec3 v=normalize(cameraPosition-vW);float i=pow(max(.7-dot(vN,v),0.),4.);gl_FragColor=vec4(vec3(1.,.55,.35)*i*1.4,1.);}` })); sp.add(matm);
const spS = new THREE.DirectionalLight(0xfff0e0, 3); spS.position.set(-30, 10, 20); sp.add(spS); sp.add(new THREE.AmbientLight(0x442a20, 0.4));
const EA = K.earth(sp, { day, night, topo }, 3); EA.group.position.set(60, 18, -90); EA.group.visible = false;
const trav = []; for (let i = 0; i < 24; i++) trav.push(K.sprite(sp, K.glowTex("rgba(255,220,150,1)"), 1.2, V(0, 0, 0), 0));
// ===== Welt B: Marsoberfläche =====
const gr = new THREE.Scene(); gr.fog = new THREE.FogExp2(0xc8906a, 0.006);
K.sky(gr, 0xb87a55, 0xd8a07a, 0xe8b894, 3000);
const gt = tex("#a85a34", 1024, 1024, 11, 6, 0.45, 0.6); gt.repeat.set(30, 30);
const gg = new THREE.PlaneGeometry(1200, 1200, 200, 200); const gp = gg.attributes.position; K.reseed(13);
for (let i = 0; i < gp.count; i++) { const x = gp.getX(i), y = gp.getY(i); gp.setZ(i, Math.sin(x * 0.03) * Math.cos(y * 0.025) * 3 + Math.sin(x * 0.11 + y * 0.07) * 0.6 + Math.max(0, Math.hypot(x + 200, y + 400) < 250 ? 0 : 0)); }
gg.computeVertexNormals(); const ground = new THREE.Mesh(gg, new THREE.MeshStandardMaterial({ map: gt, roughness: 1 })); ground.rotation.x = -Math.PI / 2; gr.add(ground);
const rockM = new THREE.MeshStandardMaterial({ map: tex("#8a4a2c", 512, 256, 17, 3, 0.45), roughness: 1 });
for (let i = 0; i < 160; i++) { K.reseed(200 + i); const s = 0.3 + Math.pow(K.rnd(), 3) * 3; const r = new THREE.Mesh(new THREE.DodecahedronGeometry(s, 1), rockM); r.position.set((K.rnd() - 0.5) * 160, s * 0.3, -K.rnd() * 160 + 20); r.rotation.set(K.rnd() * 3, K.rnd() * 3, 0); r.scale.y = 0.6; gr.add(r); }
const hills = new THREE.Mesh(new THREE.ConeGeometry(160, 40, 48), new THREE.MeshStandardMaterial({ color: 0x8a4e30, roughness: 1 })); hills.position.set(-120, 0, -320); gr.add(hills);
const hill2 = hills.clone(); hill2.position.set(200, -5, -380); hill2.scale.set(1.4, 0.8, 1); gr.add(hill2);
const gS = new THREE.DirectionalLight(0xffe2c8, 2.6); gS.position.set(-40, 50, 30); gr.add(gS); gr.add(new THREE.HemisphereLight(0xe8b894, 0x4a2a1a, 0.8));
// Rover
const rover = new THREE.Group(); gr.add(rover);
const wM = new THREE.MeshStandardMaterial({ color: 0xd8d8d4, roughness: 0.5, metalness: 0.4 }), dM = new THREE.MeshStandardMaterial({ color: 0x2a2a2e, roughness: 0.7 });
const body = new THREE.Mesh(new THREE.BoxGeometry(3, 1, 2.2), wM); body.position.y = 1.6; rover.add(body);
const rtg = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 1.4, 16), dM); rtg.rotation.x = 0.8; rtg.position.set(-1.7, 2.0, 0); rover.add(rtg);
const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2, 8), wM); mast.position.set(1.1, 3, 0.6); rover.add(mast);
const head = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.35, 0.4), wM); head.position.set(1.1, 4, 0.6); rover.add(head);
const eye = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), new THREE.MeshBasicMaterial({ color: 0x66ccff })); eye.position.set(1.42, 4, 0.6); rover.add(eye);
const wheels = []; [[-1.2, -1.25], [0, -1.25], [1.2, -1.25], [-1.2, 1.25], [0, 1.25], [1.2, 1.25]].forEach(([x, z]) => { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.4, 24), dM); w.rotation.x = Math.PI / 2; w.position.set(x, 0.5, z); rover.add(w); wheels.push(w); });
const arm = new THREE.Group(); arm.position.set(1.5, 1.6, 0); rover.add(arm); const a1 = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.12, 0.12), wM); a1.position.x = 0.9; arm.add(a1);
const drill = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.03, 0.6, 12), dM); drill.position.set(1.8, -0.3, 0); arm.add(drill);
// Leoparden-Stein
const lc = document.createElement("canvas"); lc.width = lc.height = 512; const lq = lc.getContext("2d"); lq.fillStyle = "#b05a3a"; lq.fillRect(0, 0, 512, 512); K.reseed(55);
for (let i = 0; i < 70; i++) { const x = K.rnd() * 512, y = K.rnd() * 512, r = 8 + K.rnd() * 20; lq.fillStyle = "#e8c8a0"; lq.beginPath(); lq.ellipse(x, y, r, r * 0.8, K.rnd() * 3, 0, 7); lq.fill(); lq.strokeStyle = "#2a1610"; lq.lineWidth = 5 + K.rnd() * 3; lq.stroke(); }
const lt = new THREE.CanvasTexture(lc); lt.colorSpace = THREE.SRGBColorSpace;
const leo = new THREE.Mesh(new THREE.DodecahedronGeometry(2.2, 2), new THREE.MeshStandardMaterial({ map: lt, roughness: 0.9 })); leo.scale.set(1.3, 0.7, 1); leo.position.set(8, 0.8, -6); gr.add(leo);
// Röhrchen
const H = (x, z) => Math.sin(x * 0.03) * Math.cos(-z * 0.025) * 3 + Math.sin(x * 0.11 - z * 0.07) * 0.6;
const tubes = new THREE.Group(); gr.add(tubes);
for (let i = 0; i < 10; i++) { const t = new THREE.Group(); const g1 = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 1.4, 24), new THREE.MeshStandardMaterial({ color: 0xe6e8ec, metalness: 0.9, roughness: 0.25 })); t.add(g1); const c1 = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.22, 24), new THREE.MeshStandardMaterial({ color: 0xc9a24a, metalness: 0.9, roughness: 0.3 })); c1.position.y = 0.78; t.add(c1);
  K.reseed(300 + i); { const x = -6 + (K.rnd() - 0.5) * 4, z = -4.5 - K.rnd() * 3; t.position.set(x, H(x, z) + 0.35, z); } t.rotation.set(Math.PI / 2, 0, K.rnd() * 3); t.scale.setScalar(1.8); tubes.add(t); }
// Rakete für Abholung
const rocket = new THREE.Group(); const rb = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.9, 7, 24), wM); rb.position.y = 3.5; rocket.add(rb); const rn = new THREE.Mesh(new THREE.ConeGeometry(0.8, 2, 24), wM); rn.position.y = 8; rocket.add(rn);
rocket.position.set(-14, 0, -18); gr.add(rocket); const flame = K.sprite(gr, K.glowTex("rgba(255,220,160,1)"), 4, V(-14, 0, -18), 0);

// ===== Analyse =====
const A = new Ebene(document.getElementById("root"));
const t21 = WT("zweitausendein"), tBohr = WT("bohrt"), tStift = WT("stift"), t25 = WT("zweitausendfünf"), tLeo = WT("leopardenfell"), tErde = WT("erde", 27), tNasa = WT("nasa", 31), tProb = WT("problem"), tLab = WT("labor"), tAlt = WT("alte"), tStopp = WT("gestoppt"), tNeu = WT("jetzt", 45), tChina = WT("china"), t28 = WT("zweitausendacht"), tGesch = WT("geschichte"), tGlaub = WT("glaubst");
A.logo("assets/logos/nasa.svg", 90, 560, 300, 240, { t0: t21 - 0.3, t1: 13.4, rot: -4 });
A.karte("Perseverance", 450, 560, 540, 300, { t0: t21 - 0.2, t1: 13.4, unter: "AUF DEM MARS SEIT" });
A.zahl(720, 770, { von: 2000, bis: 2021, t0: t21 + 0.4, t1: 13.4, dauer: 1.2, fmt: (v) => String(Math.round(v)), farbe: GELB });
A.hand("so groß wie ein Auto", 540, 1250, { t0: t21 + 2.0, t1: 13.4, size: 56, farbe: "#fff" });
A.hand("bohrt ↓", 330, 760, { t0: tBohr, t1: tStift - 2.5, size: 70, farbe: GELB });
const tubeHtml = Array.from({ length: 6 }, (_, i) => `<div style="position:absolute;left:${70 + i * 115}px;top:120px;width:46px;height:250px;border-radius:23px 23px 10px 10px;background:linear-gradient(90deg,#9aa0a8,#f4f6f8 45%,#b8bec6);box-shadow:0 0 18px rgba(255,255,255,.25)"><div style="position:absolute;left:-4px;top:-8px;width:54px;height:40px;border-radius:10px;background:linear-gradient(90deg,#a07a2a,#f2d27a,#a07a2a)"></div><div style="position:absolute;left:8px;bottom:12px;width:30px;height:${80 + (i * 37) % 90}px;border-radius:6px;background:${["#a85a34", "#8a4a2c", "#c07048"][i % 3]}"></div></div>`).join("");
A.karte("Proben-Röhrchen", 120, 560, 840, 480, { t0: tStift - 2.4, t1: 19.3, unter: "JE ETWA SO GROSS WIE EIN STIFT", html: tubeHtml });
A.hand("✏️ ≈ gleich groß", 540, 1110, { t0: tStift, t1: 19.3, size: 60, farbe: GELB });
A.stempel("2025", 300, 600, { t0: t25, t1: 23.0, rot: -8, farbe: GELB }); A.hand("„Sapphire Canyon“", 650, 620, { t0: t25 + 0.6, t1: 23.0, size: 60, farbe: "#fff" });
A.kreis(540, 980, 300, 170, { t0: tLeo - 0.6, t1: 27.0 }); A.hand("Leopardenflecken 🐆", 540, 760, { t0: tLeo - 0.2, t1: 27.0, size: 72, farbe: GELB });
A.karte("Auf der Erde", 120, 540, 840, 420, { t0: tErde - 0.2, t1: 31.2, unter: "SOLCHE MUSTER ENTSTEHEN OFT DURCH" });
A.hand("🦠 winzige Lebewesen", 540, 770, { t0: tErde + 0.4, t1: 31.2, size: 76, farbe: GRUEN }); A.hand("(Mikroben)", 540, 870, { t0: tErde + 0.9, t1: 31.2, size: 52, farbe: "#fff" });
A.logo("assets/logos/nasa.svg", 390, 540, 300, 240, { t0: tNasa - 0.2, t1: 37.3 });
A.stempel("DEUTLICHSTER HINWEIS", 540, 880, { t0: tNasa + 1.2, t1: 37.3, rot: -6, farbe: GRUEN }); A.hand("…auf früheres Leben?", 540, 1010, { t0: tNasa + 2.4, t1: 37.3, size: 60, farbe: GELB });
A.karte("Der Weg ins Labor", 90, 520, 900, 660, { t0: tProb - 0.2, t1: 42.5, unter: "MARS → ERDE" });
A.hand("🔴 Mars", 270, 760, { t0: tProb + 0.4, t1: 42.5, size: 72, farbe: "#ff8a5a" }); A.hand("🌍 Erde", 810, 760, { t0: tProb + 0.6, t1: 42.5, size: 72, farbe: BLAU });
A.pfeil(380, 760, 690, 760, { t0: tLab - 0.6, t1: 42.5, bogen: 0.15, farbe: GELB }); A.hand("🔬 Labor", 810, 920, { t0: tLab, t1: 42.5, size: 64, farbe: "#fff" });
A.hand("über 300 Mio. km", 540, 1080, { t0: tLab + 0.6, t1: 42.5, size: 52, farbe: GELB });
A.karte("Alter Plan", 160, 560, 760, 420, { t0: tAlt - 0.2, t1: 45.7, unter: "MARS SAMPLE RETURN" }); A.hand("💸 zu teuer", 540, 790, { t0: tAlt + 0.5, t1: 45.7, size: 80, farbe: ROT });
A.stempel("GESTOPPT", 540, 900, { t0: tStopp, t1: 45.7, rot: -10, farbe: ROT });
A.zettel("Neuer Plan<br>gesucht! 🔎", 540, 760, { t0: tNeu + 0.3, t1: 50.5, rot: -4, size: 66 }); A.hand("günstiger", 540, 950, { t0: tNeu + 2.2, t1: 50.5, size: 60, farbe: GRUEN });
A.karte("Das Rennen zum Mars", 100, 520, 880, 640, { t0: tChina - 0.3, t1: 56.8, unter: "WER BRINGT ZUERST GESTEIN?" });
A.hand("🇺🇸 NASA", 300, 720, { t0: tChina, t1: 56.8, size: 64, farbe: "#fff" }); A.hand("neuer Plan offen", 300, 810, { t0: tChina + 0.2, t1: 56.8, size: 44, farbe: GELB });
A.hand("🇨🇳 China", 780, 720, { t0: tChina + 0.5, t1: 56.8, size: 64, farbe: "#fff" }); A.hand("Start 2028", 780, 810, { t0: t28, t1: 56.8, size: 52, farbe: ROT });
A.stempel("VS.", 540, 760, { t0: tChina + 0.8, t1: 56.8, rot: 0, farbe: GELB });
A.stempel("GESCHICHTE!", 540, 760, { t0: tGesch - 0.4, t1: 60.5, rot: -6, farbe: GELB });
A.zettel("Gab es Leben? 👽<br>Ja / Nein 👇", 540, 760, { t0: tGlaub, t1: 65.3, rot: -4, size: 62 });

renderAt = (t) => {
  label(""); E.look([1.06, 0.98, 0.92], [0.01, 0.006, 0.004], 0.45, 0.86); E.grade.uniforms.flash.value = 0;
  let scene = gr; flame.material.opacity = 0; rocket.visible = t >= 45.9 && t < 50.6;
  mars.rotation.y = t * 0.03; rover.position.set(0, 0, 0); rover.rotation.y = 0.4; arm.rotation.z = 0;
  wheels.forEach((w) => (w.rotation.y = 0));
  if (t < 8.3 || (t >= 42.7 && t < 45.9) || (t >= 50.6 && t < 57)) {
    scene = sp; EA.group.visible = t >= 50.6; trav.forEach((s) => (s.material.opacity = 0));
    if (t < 8.3) { const f = K.eout(prog(t, 0, 8.3)); cam.position.set(lerp(-10, 4, f), 4, lerp(60, 30, f)); cam.lookAt(0, 0, 0); }
    else if (t < 45.9) { cam.position.set(-6, 10, 34); cam.lookAt(0, 0, 0); }
    else { cam.position.set(20, 14, 60); cam.lookAt(28, 8, -40); trav.forEach((s, i) => { const k = ((t * 0.25 + i / 24) % 1); s.position.copy(V(0, 0, 0).lerp(V(60, 18, -90), k)); s.material.opacity = 0.8 * Math.sin(k * Math.PI); }); }
  } else if (t < 19.3) {
    const f = prog(t, 8.3, 11); rover.position.set(lerp(-6, 0, prog(t, 8.3, 5)), 0, 0); wheels.forEach((w) => (w.rotation.y = -t * 2));
    arm.rotation.z = t > 13.6 ? -0.35 + Math.sin(t * 2) * 0.05 : 0;
    cam.position.set(lerp(12, 8, f), lerp(5, 3.6, f), lerp(14, 9, f)); cam.lookAt(0.5, 1.6, 0);
    
  } else if (t < 31.2) {
    const f = prog(t, 19.3, 12); cam.position.set(lerp(18, 15, f), lerp(7, 5.5, f), lerp(4, 1, f)); cam.lookAt(8, 0.6, -6); rover.position.set(3, 0, -3); rover.rotation.y = -0.6;
  } else if (t < 42.7) { cam.position.set(-2, 5, 10); cam.lookAt(-6, 0.3, -6); rover.position.set(6, 0, -10); }
  else if (t < 50.6) { const k = prog(t, 47, 3.6); rocket.position.y = k * k * 60; flame.position.set(-14, rocket.position.y - 0.5, -18); flame.material.opacity = k > 0 ? 1 : 0; flame.scale.setScalar(4 + Math.sin(t * 30) * 0.4); cam.position.set(6, 6, 22); cam.lookAt(-14, 6 + rocket.position.y * 0.6, -18); }
  else { const f = prog(t, 57, 11); cam.position.set(lerp(10, 14, f), lerp(5, 7, f), lerp(14, 20, f)); cam.lookAt(0, 2, 0); }
  E.render(scene, t); A.update(t); cap(t);
};
