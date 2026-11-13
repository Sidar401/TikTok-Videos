const { Ebene, wortZeit, ORANGE, GELB, ROT, GRUEN, BLAU } = await import("./assets/analyse.js");
const W = (w, ab = 0) => wortZeit(WORDS, w, ab);
K.reseed(21);
const sc = new THREE.Scene();
K.stars(sc, 7000, -1, 9000, 2.0);
sc.add(new THREE.AmbientLight(0x404a70, 0.8));
const key = new THREE.DirectionalLight(0xfff2dd, 3.2); key.position.set(20, 30, 40); sc.add(key);
const rim = new THREE.DirectionalLight(0x8fb0ff, 1.6); rim.position.set(-30, -10, -20); sc.add(rim);

// ===== A: James-Webb-Teleskop (Ursprung) =====
const jw = new THREE.Group(); sc.add(jw);
const gold = new THREE.MeshStandardMaterial({ color: 0xffc04a, metalness: 0.85, roughness: 0.22, emissive: 0xc88a1a, emissiveIntensity: 0.75 });
const mir = new THREE.Group(); jw.add(mir);
const hexes = [];
for (let q = -2; q <= 2; q++) for (let r = -2; r <= 2; r++) { const s = -q - r; if (Math.abs(s) > 2 || (q === 0 && r === 0)) continue;
  const h = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 0.12, 6), gold); h.rotation.x = Math.PI / 2; h.rotation.y = Math.PI / 6;
  h.position.set(1.5 * q, Math.sqrt(3) * (r + q / 2), -0.08 * (q * q + r * r)); mir.add(h); hexes.push(h); }
const dark = new THREE.MeshStandardMaterial({ color: 0x1b1d24, roughness: 0.6, metalness: 0.4 });
const sec = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.1, 16), gold); sec.rotation.x = Math.PI / 2; sec.position.z = 5; mir.add(sec);
[[0, 4.6], [-4, -2.3], [4, -2.3]].forEach(([x, y]) => { const a = V(x, y, 0), b = V(0, 0, 5); const L = a.distanceTo(b);
  const s = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, L, 6), dark); s.position.copy(a.clone().add(b).multiplyScalar(0.5)); s.lookAt(b); s.rotateX(Math.PI / 2); mir.add(s); });
mir.rotation.x = -0.35; mir.position.set(0, 2.2, 0);
const shieldM = new THREE.MeshStandardMaterial({ color: 0xb8aed0, metalness: 0.8, roughness: 0.35, emissive: 0x1c1430, emissiveIntensity: 0.4, side: THREE.DoubleSide });
for (let i = 0; i < 5; i++) { const sh = new THREE.Shape([new THREE.Vector2(-10, 0), new THREE.Vector2(-4, 4), new THREE.Vector2(4, 4), new THREE.Vector2(10, 0), new THREE.Vector2(4, -4), new THREE.Vector2(-4, -4)]);
  const m = new THREE.Mesh(new THREE.ShapeGeometry(sh), shieldM); m.rotation.x = -Math.PI / 2; m.position.y = -1.6 - i * 0.22; m.scale.setScalar(1 - i * 0.03); jw.add(m); }
const bus = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.2, 2.2), dark); bus.position.y = -3.2; jw.add(bus);
const tower = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 2, 8), dark); tower.position.y = -0.6; jw.add(tower);
const sunGlow = K.sprite(sc, K.glowTex("rgba(255,220,170,1)"), 60, V(60, -40, -140), 0.9);

// ===== B: echtes Webb-Bild (NASA, gemeinfrei) mit roten Punkten =====
const B = V(0, 0, -4000);
const deepTex = await new THREE.TextureLoader().loadAsync("assets/webb-deep-field.jpg"); deepTex.colorSpace = THREE.SRGBColorSpace;
const deep = new THREE.Mesh(new THREE.PlaneGeometry(300, 306), new THREE.MeshBasicMaterial({ map: deepTex, toneMapped: false, fog: false, transparent: true }));
deep.position.copy(B); sc.add(deep);
const redTex = K.glowTex("rgba(255,45,30,1)"), redCore = K.glowTex("rgba(255,200,180,1)");
const dotPos = [[-38, 22], [52, 70], [-90, -40], [18, -96], [96, -8], [-60, 108], [70, -70], [-14, 58], [120, 110], [-118, 30], [36, 12], [-40, -120], [6, 128], [-100, -100]];
const dots = dotPos.map(([x, y], i) => { const p = B.clone().add(V(x, y, 1.5)); return { glow: K.sprite(sc, redTex, 9, p, 0), core: K.sprite(sc, redCore, 2.2, p.clone().add(V(0, 0, 0.2)), 0), i }; });
const DOT0 = B.clone().add(V(dotPos[0][0], dotPos[0][1], 0));

// ===== C: Schwarzes-Loch-Stern =====
const C = V(4000, 0, 0); const bhs = new THREE.Group(); bhs.position.copy(C); sc.add(bhs);
const bh = new THREE.Mesh(new THREE.SphereGeometry(3, 48, 32), new THREE.MeshBasicMaterial({ color: 0x000000 })); bhs.add(bh);
const diskU = { time: { value: 0 }, bright: { value: 1 } };
const disk = new THREE.Mesh(new THREE.RingGeometry(3.6, 13, 160, 4), new THREE.ShaderMaterial({ uniforms: diskU, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec2 vP;void main(){vP=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float time,bright;varying vec2 vP;void main(){float r=length(vP);float a=atan(vP.y,vP.x);float k=(r-3.6)/9.4;
    float sw=.55+.45*sin(a*7.-r*1.7+time*2.2)*sin(a*3.+r*.9-time*1.3);vec3 c=mix(vec3(1.,.95,.85),vec3(1.,.42,.12),smoothstep(0.,.45,k));c=mix(c,vec3(.6,.08,.04),smoothstep(.45,1.,k));
    float al=(1.-smoothstep(.0,1.,k))*(.55+.45*sw)*smoothstep(0.,.04,k);gl_FragColor=vec4(c*al*bright*1.6,al);}` }));
disk.rotation.x = -1.25; bhs.add(disk);
const ringGlow = K.sprite(bhs, K.glowTex("rgba(255,210,150,.9)"), 10, V(0, 0, 0), 0.8);
const gasU = { time: { value: 0 }, heat: { value: 0 }, op: { value: 0.3 } };
const gas = new THREE.Mesh(new THREE.SphereGeometry(30, 96, 64), new THREE.ShaderMaterial({ uniforms: gasU, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec3 vN,vV,vP;void main(){vP=position;vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-mv.xyz);gl_Position=projectionMatrix*mv;}`,
  fragmentShader: `uniform float time,heat,op;varying vec3 vN,vV,vP;
    float n3(vec3 p){return sin(p.x*.21+time*.3)*sin(p.y*.17-time*.25)*sin(p.z*.19+time*.2)+.5*sin(p.x*.5+p.y*.4-time*.5)*sin(p.z*.45+time*.35);}
    void main(){float mu=max(dot(normalize(vN),normalize(vV)),0.);float n=.65+.35*n3(vP);
    vec3 cold=vec3(.75,.08,.05),hot=vec3(1.,.55,.2);vec3 c=mix(cold,hot,heat)*n;
    float edge=pow(1.-mu,2.);float body=mix(.25+.75*edge,.55+.45*mu,heat);
    gl_FragColor=vec4(c*body*(op*1.3+heat*0.45),1.);}` }));
bhs.add(gas);
const puffs = []; for (let i = 0; i < 70; i++) { K.reseed(300 + i); const a = K.rnd() * 6.283, b = Math.acos(2 * K.rnd() - 1), r = 18 + K.rnd() * 18;
  puffs.push({ s: K.sprite(bhs, K.glowTex("rgba(255,70,40,.35)"), 18 + K.rnd() * 22, V(Math.sin(b) * Math.cos(a) * r, Math.cos(b) * r, Math.sin(b) * Math.sin(a) * r), 0.5), a, b, r, w: 0.05 + K.rnd() * 0.08 }); }
const farDot = K.sprite(sc, redTex, 140, C.clone(), 0);

// ===== Analyse-Ebene =====
const A = new Ebene(document.getElementById("root"));
const P = (v) => { cam.updateMatrixWorld(true); const q = v.clone().project(cam); return [(q.x + 1) / 2 * 1080, (1 - q.y) / 2 * 1920]; };
const tJW = W("james"), tVerg = W("vergangenheit"), tDabei = W("dabei"), tHund = W("hunderte"), tIhr = W("ihr", 18), t12 = W("zwölf"), tStamm = W("stammen"), tUrk = W("urknall"), tSelt = W("seltsame"), tHell = W("hell", 27), tGr = W("größe"), tWaer = W("wären"), tSter = W("sterne", 31), tMoegl = W("möglich"), tFor = W("forscher", 34), tZerb = W("zerbrechen"), tJetzt = W("jetzt"), tErkl = W("erklärung"), tBHS = W("schwarzelochsterne"), tInnen = W("innen"), tSL = W("schwarzes", 45), tEin = W("eingehüllt"), tGas = W("gas", 49.5), tHeiss = W("heiß"), tLeucht = W("leuchtet"), tViel = W("vielleicht"), tErst = W("allerersten"), tGanz = W("ganz", 59), tWas = W("was", 61), tFolg = W("folg", 63);
// Webb
A.logo("assets/logos/nasa.svg", 90, 540, 260, 210, { t0: tJW - 0.3, t1: tDabei - 0.2, rot: -4 });
A.karte("James Webb", 400, 540, 590, 330, { t0: tJW - 0.2, t1: tDabei - 0.2, unter: "STÄRKSTES WELTRAUM-TELESKOP" });
A.hand("seit 2021 im All 🚀", 695, 680, { t0: tJW + 0.4, t1: tDabei - 0.2, size: 54, farbe: "#fff" });
A.hand("Spiegel: 6,5 m", 695, 780, { t0: tJW + 0.9, t1: tDabei - 0.2, size: 54, farbe: GELB });
A.zettel("weiter weg =<br>früher ⏳", 540, 1110, { t0: tVerg - 0.1, t1: tDabei - 0.2, rot: -4, size: 62 });
// Hunderte rote Punkte
A.zettel("Hunderte! 🔴", 300, 600, { t0: tHund, t1: tIhr - 0.2, rot: -5, size: 70 });
A.hand("echtes Webb-Bild (NASA)", 700, 1300, { t0: tDabei, t1: tIhr - 0.2, size: 40, farbe: "rgba(255,255,255,.8)" });
// Zeitstrahl
const tlHtml = `<div style="position:absolute;left:40px;right:40px;top:150px;height:10px;border-radius:5px;background:linear-gradient(90deg,#fff,#7fd0ff)"></div>
  <div style="position:absolute;left:62px;top:136px;width:58px;height:38px;border-radius:10px;background:#ff3b2f;box-shadow:0 0 30px #ff3b2f"></div>
  <div style="position:absolute;left:24px;top:190px;font:800 30px Inter,sans-serif;color:#fff">Urknall 💥</div>
  <div style="position:absolute;right:30px;top:190px;font:800 30px Inter,sans-serif;color:#7fd0ff">heute 🌍</div>
  <div style="position:absolute;left:150px;top:96px;font:700 30px Caveat,cursive;font-size:40px;color:#ff6a5e">← rote Punkte</div>`;
A.karte("Zeitreise", 110, 520, 860, 270, { t0: tIhr - 0.2, t1: tSelt - 0.2, unter: "13,8 MILLIARDEN JAHRE", html: tlHtml });
A.zahl(540, 1000, { von: 0, bis: 12, t0: t12 - 0.2, t1: tSelt - 0.2, dauer: 1.1, fmt: (v) => "> " + Math.round(v) + " Mrd.", farbe: ROT, unter: "Jahre war das Licht unterwegs" });
A.stempel("KURZ NACH DEM URKNALL", 540, 1230, { t0: tUrk - 0.1, t1: tSelt - 0.2, rot: -4, farbe: GELB });
// zu hell
A.hand("winzig 🔍", 300, 640, { t0: tSelt + 0.4, t1: tWaer - 0.2, size: 80, farbe: "#fff" });
A.hand("aber viel zu hell 💡", 600, 1220, { t0: tHell - 0.2, t1: tWaer - 0.2, size: 74, farbe: GELB });
A.kreis(540, 960, 150, 150, { t0: tSelt + 0.2, t1: tWaer - 0.2, farbe: GELB });
// zu viele Sterne
A.karte("Wenn es Galaxien wären …", 110, 520, 860, 700, { t0: tWaer - 0.1, t1: tFor - 0.2, unter: "ANZAHL STERNE" });
A.balken(220, 660, 640, 440, [{ name: "damals möglich", wert: 1, text: "✓", farbe: GRUEN }, { name: "nötig", wert: 3.2, text: "?!", farbe: ROT }], { t0: tSter - 0.4, t1: tFor - 0.2, versatz: 0.6 });
A.stempel("UNMÖGLICH?", 540, 1270, { t0: tMoegl, t1: tFor - 0.2, rot: -6, farbe: ROT });
// Universum zerbricht
A.zettel("„Universums-Brecher“", 540, 620, { t0: tFor + 0.4, t1: tJetzt - 0.2, rot: -4, size: 62 });
const crack = ["M540,960 L470,880 L500,800 L430,720", "M540,960 L640,900 L700,940 L790,860", "M540,960 L560,1060 L500,1140 L520,1250", "M540,960 L420,1010 L340,980 L250,1050", "M540,960 L650,1040 L700,1150 L820,1180"];
crack.forEach((d, i) => A._path(d, { t0: tZerb + i * 0.05, t1: tJetzt - 0.2, farbe: "#ffffff", breite: 6, dauer: 0.25 }));
A.stempel("UNIVERSUM KAPUTT?", 540, 1250, { t0: tZerb + 0.2, t1: tJetzt - 0.2, rot: 5, farbe: ROT });
// Neue Erklärung
A.zettel("Neue Idee 💡", 290, 610, { t0: tJetzt, t1: tInnen - 0.2, rot: -5, size: 64 });
A.hand("Schwarzes-Loch-Stern", 540, 1260, { t0: tBHS, t1: tInnen - 0.2, size: 80, farbe: GELB });
// Innen
const lBH = A.hand("Schwarzes Loch ⚫", 300, 620, { t0: tSL - 0.2, t1: tGas - 0.2, size: 62, farbe: "#fff" });
const aBH = A.pfeil(320, 670, 520, 900, { t0: tSL, t1: tGas - 0.2, bogen: -0.25, farbe: "#fff", breite: 7 });
A.hand("dichte Gaswolke ☁️", 720, 1250, { t0: tEin, t1: tGas - 0.2, size: 62, farbe: "#ff7a5e" });
A.pfeil(780, 1200, 800, 1060, { t0: tEin + 0.2, t1: tGas - 0.2, bogen: 0.25, farbe: "#ff7a5e", breite: 7 });
// heiß
A.stempel("🌡️ SUPERHEISS", 540, 640, { t0: tHeiss, t1: tViel - 0.2, rot: -6, farbe: ORANGE });
A.hand("leuchtet wie ein Riesen-Stern ⭐", 540, 1260, { t0: tLeucht, t1: tViel - 0.2, size: 60, farbe: GELB });
// erste Schwarze Löcher
A.zettel("Babyfotos der ersten<br>Riesen-Schwarzen Löcher? 👶", 540, 700, { t0: tViel, t1: tGanz - 0.2, rot: -3, size: 54 });
A.hand("…von weitem: ein roter Punkt 🔴", 540, 1260, { t0: tErst + 0.4, t1: tGanz - 0.2, size: 52, farbe: "#ff7a5e" });
A.stempel("NOCH NICHT SICHER", 540, 760, { t0: tGanz, t1: tWas - 0.2, rot: -7, farbe: GELB });
A.zettel("Was glaubst du? 👇<br>⚫ Schwarzes Loch<br>🌌 Galaxie", 540, 780, { t0: tWas, t1: tFolg - 0.1, rot: -3, size: 58 });

// ===== Ablauf =====
renderAt = (t) => {
  label(""); E.grade.uniforms.flash.value = 0;
  diskU.time.value = t; gasU.time.value = t;
  dots.forEach((d) => { const on = cl((t - 0.2 - d.i * 0.12) / 0.4); const tl = t >= 14.6 ? cl((t - tHund + 0.3 - d.i * 0.09) / 0.3) : on; const pu = 0.75 + 0.25 * Math.sin(t * 3 + d.i * 1.7);
    d.glow.material.opacity = tl * pu; d.core.material.opacity = tl * 0.9; });
  farDot.material.opacity = 0;
  let pos, look; cam.fov = 40;
  E.look([1.0, 0.98, 1.0], [0.0, 0.0, 0.004], 0.45, 0.82);
  if (t < tJW - 0.05) { // Hook + Folgen: rote Punkte im echten Webb-Bild
    const f = K.eout(prog(t, 0, 5.2)); const g = prog(t, 5.2, 4.4);
    pos = DOT0.clone().add(V(lerp(0, 30, f) + g * 20, lerp(0, -20, f), lerp(14, 300, f) + g * 60)); look = DOT0.clone().add(V(lerp(0, 30, f) + g * 20, lerp(0, -20, f), 0));
  } else if (t < tDabei - 0.05) { // Webb im All
    E.look([1.02, 0.99, 0.98], [0.002, 0.002, 0.012], 0.55, 0.7);
    const a = 0.6 + (t - tJW) * 0.12; const d = lerp(42, 34, prog(t, tJW, 5));
    pos = V(Math.sin(a) * d, 7 + Math.sin(t * 0.3), Math.cos(a) * d); look = V(0, 3.6, 0);
    mir.rotation.y = 0.05 * Math.sin(t * 0.4);
  } else if (t < tSelt - 0.05) { // Webb-Bild, Hunderte Punkte, Zeitreise
    const f = K.eio(prog(t, tDabei, 3)); const g = prog(t, tIhr, 7);
    pos = B.clone().add(V(lerp(0, -20, g), lerp(0, -30, g), lerp(620, 400, f) - g * 60)); look = B.clone().add(V(lerp(0, -20, g), lerp(0, -30, g), 0));
  } else if (t < tWaer - 0.05) { // Zoom auf einen Punkt
    const f = K.eio(prog(t, tSelt, 1.6));
    pos = DOT0.clone().add(V(0, 0, lerp(360, 24, f))); look = DOT0.clone();
    E.look([1.0, 0.97, 0.98], [0, 0, 0], lerp(0.45, 1.1, f), 0.6);
  } else if (t < tJetzt - 0.05) { // Galaxien? Universum zerbricht
    const f = prog(t, tWaer, 9); pos = B.clone().add(V(lerp(-40, 30, f), lerp(20, -10, f), lerp(500, 300, f))); look = B.clone().add(V(lerp(-40, 30, f), lerp(20, -10, f), 0));
    if (t > tZerb && t < tZerb + 0.15) E.grade.uniforms.flash.value = 0.25 * (1 - (t - tZerb) / 0.15);
    const sh = t > tZerb && t < tZerb + 0.6 ? (1 - (t - tZerb) / 0.6) * 4 : 0; pos.x += Math.sin(t * 90) * sh; pos.y += Math.cos(t * 77) * sh;
  } else { // Schwarzes-Loch-Stern
    bhs.rotation.y = t * 0.05; disk.rotation.z = t * 0.1;
    puffs.forEach((p) => { const a = p.a + t * p.w; p.s.position.set(Math.sin(p.b) * Math.cos(a) * p.r, Math.cos(p.b) * p.r, Math.sin(p.b) * Math.sin(a) * p.r); });
    let heat = 0, op = 0.32, puffOp = 0.45, dist, el = 0.25;
    if (t < tInnen - 0.05) { const f = K.eio(prog(t, tJetzt, tInnen - tJetzt)); dist = lerp(900, 120, f); op = lerp(0.6, 0.45, f); farDot.material.opacity = 0; }
    else if (t < tGas - 0.05) { const f = K.eio(prog(t, tInnen, 1.5)); dist = lerp(120, 62, f); op = lerp(0.45, 0.22, f); puffOp = lerp(0.45, 0.22, f); }
    else if (t < tViel - 0.05) { const f = K.eio(prog(t, tGas, 2.4)); heat = f; dist = lerp(62, 115, f); op = lerp(0.22, 0.5, f); puffOp = lerp(0.22, 0.6, f); el = 0.2; }
    else { const f = K.eio(prog(t, tViel, 3.6)); heat = 1 - 0.5 * f; dist = lerp(115, 2600, f); op = 0.5; puffOp = 0.6; farDot.material.opacity = cl(f * 1.5 - 0.3) * (0.8 + 0.2 * Math.sin(t * 3)); }
    gasU.heat.value = heat; gasU.op.value = op; puffs.forEach((p) => (p.s.material.opacity = puffOp * (1 - 0.75 * heat)));
    diskU.bright.value = 1 - 0.55 * heat; ringGlow.material.opacity = 0.8 * (1 - 0.6 * heat);
    const a = 0.4 + t * 0.06; pos = C.clone().add(V(Math.sin(a) * dist, dist * el, Math.cos(a) * dist)); look = C.clone();
    E.look([1.02, 0.97, 0.95], [0.004, 0.0, 0.0], lerp(0.7, 0.5, heat), 0.7);
    if (t >= tGanz - 0.05) { // zurück zum Webb-Bild mit allen Punkten
      const f = prog(t, tGanz, 6); pos = B.clone().add(V(0, 0, lerp(520, 420, f))); look = B.clone();
    }
  }
  cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(sc, t); A.update(t); cap(t);
};
