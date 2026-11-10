// ===== Welt 1: Weltall – Erde mit Eis und Überflutung =====
K.reseed(21);
const space = new THREE.Scene();
K.stars(space, 3000, -1, 2800, 2.4);
const EA = K.earth(space, { day, night, topo }); EA.group.rotation.z = 0.41;
const pins = document.createElement("div"); pins.style.cssText = "position:absolute;inset:0;pointer-events:none"; document.getElementById("root").insertBefore(pins, document.getElementById("cap"));
let lastPins = "";
function setPins(list) { cam.updateMatrixWorld(true); let h = ""; list.forEach(([name, p]) => { const v = p.clone().project(cam); if (v.z < 1) h += `<div class="pin" style="left:${((v.x + 1) / 2 * 1080).toFixed(0)}px;top:${((1 - v.y) / 2 * 1920).toFixed(0)}px">${name}</div>`; }); if (h !== lastPins) { pins.innerHTML = h; lastPins = h; } }

// ===== Welt 2: Stadt im Hochwasser =====
K.reseed(33);
const city = new THREE.Scene();
K.sky(city, 0x16203a, 0x4a5878, 0xd8946e);
city.fog = new THREE.FogExp2(0x5a6a88, 0.0016);
const sunP = V(-500, 90, -1500);
const dl = new THREE.DirectionalLight(0xffc49a, 2.4); dl.position.copy(sunP); city.add(dl); city.add(new THREE.HemisphereLight(0xbfd0e6, 0x203040, 0.9));
K.sprite(city, K.glowTex("rgba(255,200,150,.6)"), 900, sunP, 0.9);
K.city(city, { n: 90, rMin: 170, rMax: 870, arc: 1.1, lit: 0.22, hMin: 40, hMax: 170, base: 0, colors: [0x2a3244, 0x3a4256, 0x232a3a, 0x454e62], glowI: 0.9, rough: 0.85, metal: 0.1, w0: 10, w1: 28 });
const NY = K.city(city, { n: 60, rMin: 900, rMax: 1300, arc: 0.6, lit: 0.25, hMin: 120, hMax: 300, base: 0, center: 1.2, colors: [0x2a3244, 0x343c50], glowI: 0.9, rough: 0.85, metal: 0.1, w0: 14, w1: 30 });
const towerTex = K.windowsTex(0.3, true); towerTex.repeat.set(2.2, 4.8);
const tower = new THREE.Mesh(new THREE.BoxGeometry(26, 190, 26), new THREE.MeshStandardMaterial({ color: 0x55607a, roughness: 0.7, metalness: 0.15, emissiveMap: towerTex, emissive: 0xffffff, emissiveIntensity: 1 }));
tower.position.set(14, 95, -70); tower.rotation.y = -0.35; city.add(tower);
const line = new THREE.Mesh(new THREE.BoxGeometry(27.5, 1.6, 27.5), new THREE.MeshBasicMaterial({ color: 0xffd23f })); line.position.set(14, 70.8, -70); line.rotation.y = -0.35; city.add(line);
// Stockwerk-Marken (alle 3 m) am Turm
const ticks = new THREE.Group(); for (let i = 1; i <= 23; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(27.2, 0.35, 27.2), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0.55 })); m.position.set(14, i * 3.04, -70); m.rotation.y = -0.35; ticks.add(m); } city.add(ticks);
const drift = []; for (let i = 0; i < 40; i++) { const s = 0.8 + rnd() * 2.5; const m = new THREE.Mesh(new THREE.BoxGeometry(s * 2, s * 0.5, s), new THREE.MeshStandardMaterial({ color: [0x7a5a3a, 0x9a9a9a, 0x5a3a2a][i % 3], roughness: 0.9 })); m.userData = [(rnd() - 0.5) * 200, -20 - rnd() * 300, rnd(), rnd() * 6]; city.add(m); drift.push(m); }
const wat = K.water(city, 0, 0x0a1424, 0x3a4a6a, 0xffc49a, sunP.clone().normalize());
let W = 0;
function setWater(h, t) { W = h; wat.mesh.position.y = h; wat.u.time.value = t; drift.forEach((m) => { const [x, z, r, ry] = m.userData; m.position.set(x + Math.sin(t * 0.3 + r * 9) * 2, h + 0.2 + Math.sin(t * 1.5 + r * 7) * 0.15, z); m.rotation.set(r + Math.sin(t + r) * 0.1, ry + t * 0.05, r); m.visible = h > 2; }); }

const EU = (lat, lon, d) => { const p = EA.ll(lat, lon); return p.clone().normalize().multiplyScalar(d); };
renderAt = (t) => {
  label(""); setPins([]);
  let scene = space;
  EA.U.ice.value = 1; EA.U.flood.value = 0; EA.U.sun.value.set(-0.4, 0.5, 0.8).normalize();
  EA.mesh.rotation.y = -1.75 + t * 0.02; EA.clouds.rotation.y = -1.75 + t * 0.025; EA.clouds.material.opacity = 0.7;
  E.look([0.95, 1.0, 1.08], [0, 0.004, 0.015], 0.3, 0.93); E.grade.uniforms.flash.value = 0;
  if (t < 6.11) {
    // Eis schmilzt (Blick schräg von oben auf den Norden)
    EA.U.ice.value = 1 - K.eio(prog(t, 0.4, 3.2));
    EA.U.flood.value = 0.25 * prog(t, 3.0, 3.0);
    const f = eio(prog(t, 0, 6.1));
    cam.position.copy(EU(lerp(62, 50, f), -30, lerp(15, 13, f))); cam.lookAt(0, 0.3, 0);
    if (t > 3.3) label(`Grönland &amp; Antarktis<small>tauen komplett auf</small>`);
  } else if (t < 12.66) {
    // Stadt: Wasser steigt auf 70 m
    scene = city; E.look([0.92, 1.0, 1.1], [0, 0.012, 0.03], 0.45, 0.9);
    const h = 70 * K.eout(prog(t, 6.2, 2.6)); setWater(h, t);
    line.visible = t > 8.7; ticks.visible = t > 9.0;
    const f = eio(prog(t, 6.1, 6.5));
    cam.position.set(-10, h + 10, lerp(120, 70, f)); cam.lookAt(10, h + 10 + Math.tan(0.16) * 400, -310);
    label(t < 9.02 ? `<span class="big blue">+${Math.round(h)} METER</span><small>Meeresspiegel</small>` : `<span class="big">23 STOCKWERKE</span><small>so hoch steht das Wasser</small>`);
  } else if (t < 18.53) {
    // Europa versinkt
    EA.U.ice.value = 0; EA.U.flood.value = K.eio(prog(t, 12.8, 2.4)); EA.U.sun.value.set(0.2, 0.6, 0.8).normalize();
    EA.mesh.rotation.y = -1.75 + 12.66 * 0.02; EA.clouds.rotation.y = EA.mesh.rotation.y; EA.clouds.material.opacity = 0.25;
    const nl = t >= 16.63; const f = eio(prog(t, 12.66, 1.4)); const g = eio(prog(t, 16.63, 1.2));
    const c = EU(lerp(50, 52.3, g), lerp(9, 5, g), lerp(lerp(13, 4.6, f), 3.5, g)); cam.position.copy(c); cam.lookAt(EA.ll(lerp(50, 52.3, g), lerp(9, 5, g)).multiplyScalar(lerp(0.4, 0.8, g)));
    if (!nl) setPins([["Hamburg", EA.ll(53.55, 10.0, 2.62)], ["Amsterdam", EA.ll(52.37, 4.9, 2.62)], ["Venedig", EA.ll(45.44, 12.33, 2.62)]].filter((p, i) => t > 13.2 + i * 0.7));
    else setPins([["Niederlande", EA.ll(52.2, 5.6, 2.62)]]);
    label(nl ? `<span class="big red">WEG</span><small>ein ganzes Land unter Wasser</small>` : `<span class="big blue">UNTER WASSER</span>`);
  } else if (t < 22.11) {
    // New York: nur die Spitzen ragen heraus
    scene = city; E.look([0.92, 1.0, 1.1], [0, 0.012, 0.03], 0.45, 0.9);
    setWater(70, t); line.visible = false; ticks.visible = false;
    const f = eio(prog(t, 18.53, 3.6));
    const a = 1.2; const p = V(Math.sin(a) * lerp(700, 820, f), 78, -Math.cos(a) * lerp(700, 820, f));
    cam.position.copy(p); cam.lookAt(Math.sin(a) * 1100, 140, -Math.cos(a) * 1100);
    label(`New York<small>nur noch die Spitzen ragen heraus</small>`);
  } else if (t < 24.55) {
    // Tausende Jahre
    EA.U.ice.value = 0; EA.U.flood.value = 1;
    const f = prog(t, 22.11, 2.44);
    EA.mesh.rotation.y = -1.75 + t * 0.25; EA.clouds.rotation.y = EA.mesh.rotation.y * 1.02;
    cam.position.set(0, 2, lerp(15, 13.5, f)); cam.lookAt(0, 0, 0);
    const y = Math.round(lerp(0, 5000, K.eout(f)) / 100) * 100;
    label(`<span class="big">${de(y)} JAHRE</span><small>so lange würde es dauern</small>`);
  } else {
    // Heute schon: ca. 4 mm pro Jahr
    scene = city; E.look([0.92, 1.0, 1.1], [0, 0.012, 0.03], 0.45, 0.9);
    setWater(1.2, t); line.visible = false; ticks.visible = false;
    const f = eio(prog(t, 24.55, 5.4));
    cam.position.set(-10, lerp(6, 14, f), lerp(130, 160, f)); cam.lookAt(10, 40, -310);
    label(t < 28.0 ? `<span class="big">+4 mm</span><small>pro Jahr – schon heute</small>` : "");
  }
  E.render(scene, t);
  cap(t);
};
