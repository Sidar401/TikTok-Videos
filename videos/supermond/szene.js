// ===== Welt 1: Stadt am Wasser mit Supermond =====
K.reseed(11);
const city = new THREE.Scene();
K.sky(city, 0x060a1a, 0x141a3c, 0x6a4a52); K.stars(city, 700, 0.3);
const MP = V(-60, 390, -1400);
const moon = K.moon(city, 170, MP);
const mdl = new THREE.DirectionalLight(0xfff0d8, 3.2); mdl.position.set(-100, 300, 400); mdl.target = moon; city.add(mdl); city.add(new THREE.AmbientLight(0x404a70, 0.45));
const g1 = K.sprite(city, K.glowTex("rgba(255,214,150,.45)"), 900, MP.clone().add(V(0, 0, -200)), 0.7);
const g2 = K.sprite(city, K.glowTex("rgba(255,190,120,.22)"), 2400, MP.clone().add(V(0, 0, -220)), 0.8);
const cls = K.clouds(city, [[MP.x + 120, MP.y - 150, -1150, 800, 150, 0.5], [MP.x - 220, MP.y + 90, -1100, 600, 120, 0.35], [400, 300, -1050, 700, 130, 0.3]]);
K.city(city, { n: 150, rMin: 520, rMax: 950, arc: 0.9, lit: 0.14, hMax: 75 });
K.city(city, { n: 40, rMin: 380, rMax: 480, arc: 0.9, lit: 0.12, hMax: 30 });
const wat = K.water(city, -1.5, 0x04060c, 0x1e2240, 0xffd49a, MP.clone().normalize());
// Mensch am Steg (Silhouette)
const pc = document.createElement("canvas"); pc.width = 256; pc.height = 512; const pg = pc.getContext("2d"); pg.scale(2, 2); pg.fillStyle = "#020306";
pg.beginPath(); pg.arc(64, 40, 22, 0, 7); pg.fill(); pg.beginPath(); pg.moveTo(36, 70); pg.quadraticCurveTo(64, 58, 92, 70); pg.lineTo(100, 170); pg.lineTo(84, 172); pg.lineTo(80, 256); pg.lineTo(68, 256); pg.lineTo(64, 180); pg.lineTo(60, 256); pg.lineTo(48, 256); pg.lineTo(44, 172); pg.lineTo(28, 170); pg.closePath(); pg.fill();
const person = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 3.6), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(pc), transparent: true, depthWrite: false }));
person.position.set(1.6, 1.1, -12); city.add(person);
const pier = new THREE.Mesh(new THREE.BoxGeometry(14, 0.6, 30), new THREE.MeshStandardMaterial({ color: 0x0c0d12, roughness: 0.9 })); pier.position.set(3, -1, -6); city.add(pier);
// Schnee für Heiligabend
const NS = 1500, sp = new Float32Array(NS * 3), sb = []; for (let i = 0; i < NS; i++) sb.push([(rnd() - 0.5) * 120, rnd() * 80, -10 - rnd() * 140, 0.6 + rnd()]);
const sg = new THREE.BufferGeometry(); sg.setAttribute("position", new THREE.BufferAttribute(sp, 3));
const snowM = new THREE.PointsMaterial({ color: 0xffffff, size: 0.35, transparent: true, opacity: 0 }); const snow = new THREE.Points(sg, snowM); city.add(snow);

// ===== Welt 2: Weltall – Erde und Mondbahn =====
const space = new THREE.Scene(); K.reseed(51);
K.stars(space, 3000, -1, 2800, 2.4);
const EA = K.earth(space, { day, night, topo });
EA.group.rotation.z = 0.41;
const sMoon = K.moon(space, 0.42, V(0, 0, 0), 0.03);
const sdl = new THREE.DirectionalLight(0xfff4e6, 3); sdl.position.set(-8, 3, 6); space.add(sdl); space.add(new THREE.AmbientLight(0x334466, 0.3));
const ORB = (a) => V(Math.cos(a) * 5.6 + 1.0, 0, Math.sin(a) * 4.4);  // Ellipse: nah (rechts) ↔ fern (links)
const opts = []; for (let i = 0; i <= 300; i++) opts.push(ORB((i / 300) * Math.PI * 2));
const orbit = new THREE.Line(new THREE.BufferGeometry().setFromPoints(opts), new THREE.LineBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0.55 })); space.add(orbit);
const near = K.sprite(space, K.glowTex("rgba(255,210,63,.9)"), 1.2, ORB(0), 0);

renderAt = (t) => {
  label("");
  wat.u.time.value = t;
  cls.forEach((c, i) => (c.position.x += 0)); 
  let scene = city;
  moon.scale.setScalar(1); moon.material.emissiveIntensity = 0.06; snowM.opacity = 0; person.visible = false;
  E.look([1.08, 0.98, 0.86], [0.006, 0.005, 0.02], 0.75, 0.88); E.grade.uniforms.flash.value = 0;
  cls[0].position.x = MP.x + 120 + t * 6; cls[1].position.x = MP.x - 220 + t * 4;
  const pitch = (p) => Math.tan(p) * 1000;
  if (t < 3.4) {
    // Mond rast heran
    const f = K.eout(prog(t, 0, 1.9));
    const p = V(-60, 390, -1400).lerp(V(-60, 390, -1400), 1); const far = V(-20, 260, -9000);
    moon.position.copy(far.clone().lerp(MP, f)); g1.position.copy(moon.position).add(V(0, 0, -200)); g2.position.copy(moon.position).add(V(0, 0, -220));
    g1.material.opacity = 0.5 * f; g2.material.opacity = 0.35 * f;
    const sh = t > 1.9 && t < 2.5 ? Math.sin(t * 90) * (2.5 - t) * 0.6 : 0;
    cam.position.set(sh, 12 + sh * 0.5, lerp(40, 0, eio(prog(t, 0, 3.4)))); cam.lookAt(0, 12 + pitch(0.147), -1000);
    E.grade.uniforms.flash.value = t > 1.9 && t < 2.2 ? 0.25 * (1 - (t - 1.9) / 0.3) : 0;
  } else {
    moon.position.copy(MP); g1.position.copy(MP).add(V(0, 0, -200)); g2.position.copy(MP).add(V(0, 0, -220)); g1.material.opacity = 0.5; g2.material.opacity = 0.35;
  }
  if (t >= 3.4 && t < 6.4) {
    const f = prog(t, 3.4, 3.0);
    cam.position.set(lerp(0, -8, f), 12, lerp(0, -30, f)); cam.lookAt(-10, 12 + pitch(0.15), -1000);
  } else if (t >= 6.4 && t < 9.2) {
    const f = eio(prog(t, 6.4, 2.8));
    cam.position.set(-8, lerp(12, 40, f), -30); cam.lookAt(-20, 40 + pitch(lerp(0.15, 0.12, f)), -1000);
    label(`<span class="big">24. NOVEMBER</span><small>Supermond Nr. 1</small>`);
  } else if (t >= 9.2 && t < 11.77) {
    // Weltall: Mond kommt auf seiner Bahn der Erde ganz nah
    scene = space; E.look([1, 1, 1.04], [0, 0.005, 0.02], 0.7, 0.85);
    const f = eio(prog(t, 9.2, 2.4)); const a = lerp(2.4, 0.02, f);
    sMoon.position.copy(ORB(a)); sMoon.rotation.y = t * 0.1;
    near.material.opacity = prog(t, 10.6, 0.4) * 0.9; near.scale.setScalar(1.2 + 0.15 * Math.sin(t * 7)); near.position.copy(sMoon.position);
    EA.mesh.rotation.y = -1.6 + t * 0.05; EA.clouds.rotation.y = -1.6 + t * 0.06;
    cam.position.set(lerp(-3, 3, f), 13, 26); cam.lookAt(1.8, -0.3, 0);
    label(t > 9.6 ? `Ganz nah an der Erde<small>der nächste Punkt seiner Bahn</small>` : "");
  } else if (t >= 11.77 && t < 17.17) {
    // Größer + heller
    const grow = eio(prog(t, 12.1, 1.6)); const bright = eio(prog(t, 14.4, 1.6));
    moon.scale.setScalar(lerp(1 / 1.14, 1, grow)); moon.material.emissiveIntensity = lerp(0.04, 0.16, bright);
    g1.material.opacity = 0.4 + 0.4 * bright; g2.material.opacity = 0.25 + 0.3 * bright;
    E.look([1.08, 0.98, 0.86], [0.006, 0.005, 0.02], lerp(0.7, 1.1, bright), lerp(0.88, 0.8, bright));
    cam.position.set(-12, 30, -40); cam.lookAt(-40, 30 + pitch(0.2), -1000);
    label(t < 14.3 ? `<span class="big">+14 % GRÖSSER</span><small>als ein ferner Vollmond</small>` : `<span class="big">+30 % HELLER</span><small>Nächte werden richtig hell</small>`);
  } else if (t >= 17.17 && t < 21.1) {
    // Heiligabend: Schnee
    const f = prog(t, 17.17, 3.9);
    snowM.opacity = Math.min(1, (t - 17.17) * 2) * 0.9;
    for (let i = 0; i < NS; i++) { const [x, y, z, s] = sb[i]; sp[i * 3] = x + Math.sin(t * s + i) * 1.5; sp[i * 3 + 1] = ((y - t * 4 * s) % 80 + 80) % 80 - 2; sp[i * 3 + 2] = z; }
    sg.attributes.position.needsUpdate = true;
    cam.position.set(lerp(10, 2, f), 14, 0); cam.lookAt(-30, 14 + pitch(0.16), -1000);
    E.look([1.0, 0.98, 1.0], [0.01, 0.012, 0.035], 0.8, 0.82);
    label(`<span class="big">24. DEZEMBER</span><small>🎄 der größte Supermond des Jahres</small>`);
  } else if (t >= 21.1 && t < 23.17) {
    const f = prog(t, 21.1, 2.1);
    cam.position.set(lerp(-20, -35, f), 22, -60); cam.lookAt(-60, 22 + pitch(0.15), -1000);
    label(`<span class="big">JANUAR 2027</span><small>Supermond Nr. 3</small>`);
  } else if (t >= 23.17) {
    // Rausgehen und nach oben schauen – Mensch am Steg
    person.visible = true;
    const f = eio(prog(t, 23.17, 3.4));
    cam.position.set(0.5, 2.6, 2); cam.lookAt(lerp(2, -20, f), lerp(1.5, 2.6 + 190, f), lerp(-12, -1000, f));
    label(t < 27.0 ? `Am 24.11. abends raus!<small>einfach nach oben schauen</small>` : (t < 27.9 ? `Wirst du ihn anschauen? 👇` : ""));
  }
  E.render(scene, t);
  cap(t);
};
