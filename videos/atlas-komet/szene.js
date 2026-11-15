const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(5);
const sc = new THREE.Scene(); K.stars(sc, 8000, -1, 30000, 1.7).material.opacity = 0.6;
sc.add(new THREE.AmbientLight(0x30303a, 0.5)); const sunL = new THREE.PointLight(0xfff2e0, 4, 0, 0); sc.add(sunL); const fill = new THREE.DirectionalLight(0xdfe6ff, 1.6); sc.add(fill);
// Sonnensystem (Draufsicht-Maßstab, nicht maßstabsgetreu)
const sun = new THREE.Mesh(new THREE.SphereGeometry(7, 96, 64), new THREE.MeshBasicMaterial({ map: await tex("sun.jpg"), color: new THREE.Color(1.3, 1.0, 0.7), toneMapped: false })); sc.add(sun);
K.sprite(sc, K.glowTex("rgba(255,170,70,.5)"), 40, V(0, 0, 0), 0.7);
const dayT = new THREE.Texture(day); dayT.colorSpace = THREE.SRGBColorSpace; dayT.needsUpdate = true;
const PL = [["mercury.jpg", 1.0, 16, 0.9], ["venus_atmosphere.jpg", 1.6, 24, 0.6], [dayT, 1.7, 33, 0.45], ["mars.jpg", 1.3, 44, 0.33], ["jupiter.jpg", 4.5, 78, 0.12]];
const planets = []; for (const [f, r, R, w] of PL) { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 64, 48), new THREE.MeshStandardMaterial({ map: typeof f === "string" ? await tex(f) : f, roughness: 1 })); sc.add(m);
  const o = new THREE.Mesh(new THREE.RingGeometry(R - 0.08, R + 0.08, 256), new THREE.MeshBasicMaterial({ color: 0xaab4d0, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false })); o.rotation.x = -Math.PI / 2; sc.add(o); planets.push({ m, R, w }); }
// Bahn von 3I/ATLAS (Hyperbel, kommt von weit draußen, fliegt einmal vorbei und verschwindet)
const hyp = (u) => V(Math.sinh(u) * 60, Math.sinh(u) * 4, 38 - (Math.cosh(u) - 1) * 26);
const path = []; for (let u = -3.2; u <= 3.2; u += 0.02) path.push(hyp(u));
const pathL = new THREE.Line(new THREE.BufferGeometry().setFromPoints(path), new THREE.LineDashedMaterial({ color: 0x7fd0ff, dashSize: 3, gapSize: 2.2, transparent: true, opacity: 0 })); pathL.computeLineDistances(); sc.add(pathL);
// Komet: unregelmäßiger Kern + Koma + Schweif
const kg = new THREE.IcosahedronGeometry(1, 5); const pp = kg.attributes.position; for (let i = 0; i < pp.count; i++) { const v = V(pp.getX(i), pp.getY(i), pp.getZ(i)); const n = 1 + 0.18 * Math.sin(v.x * 3.1 + 1) * Math.cos(v.y * 2.7) + 0.08 * Math.sin(v.z * 7.3) + 0.12 * v.x; v.multiplyScalar(n); pp.setXYZ(i, v.x, v.y * 0.8, v.z); } kg.computeVertexNormals();
const nucleus = new THREE.Mesh(kg, new THREE.MeshStandardMaterial({ map: await tex("moon.jpg"), color: 0x8a8580, roughness: 1 }));
const comet = new THREE.Group(); comet.add(nucleus); sc.add(comet);
const coma = K.sprite(comet, K.glowTex("rgba(170,220,255,.6)"), 4.5, V(0, 0, 0), 0.5), coma2 = K.sprite(comet, K.glowTex("rgba(120,200,255,.3)"), 9, V(0, 0, 0), 0.35);
const NT = 900, tailPos = new Float32Array(NT * 3), tailSeed = []; for (let i = 0; i < NT; i++) { K.reseed(1000 + i); tailSeed.push([K.rnd(), K.rnd() - 0.5, K.rnd() - 0.5]); }
const tg = new THREE.BufferGeometry(); tg.setAttribute("position", new THREE.BufferAttribute(tailPos, 3));
const tail = new THREE.Points(tg, new THREE.PointsMaterial({ color: 0xa8dcff, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending, depthWrite: false })); sc.add(tail);
// Eis-Glitzer (Webb)
const sparks = []; for (let i = 0; i < 40; i++) { K.reseed(2000 + i); const d = V(K.rnd() - 0.5, K.rnd() - 0.5, K.rnd() - 0.5).normalize(); sparks.push({ s: K.sprite(comet, K.glowTex("rgba(220,240,255,1)"), 0.14, d.multiplyScalar(1.02), 0), ph: K.rnd() * 6 }); }

const tEs = W("es", 6), tEnt = W("entdeckt"), tEr = W("er", 14), tDie = W("die", 19.5), tRast = W("rast"), tDas = W("das", 30), tGew = W("gewehrkugel"), tUnd = W("und", 37.5), tFor = W("forscher", 40), tJetzt = W("jetzt", 44), tErg = W("ergebnis"), tViel = W("vielleicht"), tNie = W("und", 57.7), tWue = W("würdest"), tFolg = W("folg", 65);
label("3I/ATLAS", comet, 1.3, { t0: tEs + 0.6, t1: tEnt - 0.1, size: 80, gap: 30 });
label("Sonne", sun, 7, { t0: tRast - 0.2, t1: tUnd - 0.1, size: 54, gap: 20 });

const at = (t) => { // Position auf der Bahn je nach Zeit (Vorbeiflug um tRast..tUnd)
  const u = t < tRast ? -1.25 + (t / tRast) * 0.3 : t < tUnd ? lerp(-0.95, 0.9, prog(t, tRast, tUnd - tRast)) : t < tNie ? 0.9 + (t - tUnd) * 0.01 : lerp(1.05, 3.0, K.eio(prog(t, tNie, 6))); return u; };
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.35, 0.85); pathL.material.opacity = 0;
  planets.forEach((p, i) => { const a = 1 + i * 1.3 + t * p.w * 0.12; p.m.position.set(Math.cos(a) * p.R, 0, Math.sin(a) * p.R); p.m.rotation.y = t * 0.3; });
  const u = at(t); const cp = hyp(u); comet.position.copy(cp); nucleus.rotation.set(t * 0.2, t * 0.35, 0);
  const anti = cp.clone().normalize(); const act = cl(1.4 - cp.length() / 80); coma.material.opacity = 0.2 + 0.4 * act; coma2.material.opacity = 0.12 + 0.3 * act;
  for (let i = 0; i < NT; i++) { const [k, a, b] = tailSeed[i]; const L = (4 + 30 * act) * Math.pow(k, 1.4); const sp = 0.15 + L * 0.12; tailPos[i * 3] = cp.x + anti.x * L + a * sp; tailPos[i * 3 + 1] = cp.y + anti.y * L + b * sp; tailPos[i * 3 + 2] = cp.z + anti.z * L + (a - b) * sp * 0.5; }
  tg.attributes.position.needsUpdate = true; tail.material.opacity = 0.25 + 0.45 * act;
  sparks.forEach((s) => (s.s.material.opacity = 0));
  let pos, look;
  if (t < tEs - 0.05) { const f = K.eio(prog(t, 0, tEs)); pos = cp.clone().add(V(lerp(-2, 6, f), lerp(1, 3, f), lerp(5, 16, f))); look = cp.clone(); }
  else if (t < tEnt - 0.05) { const b = 0.4 + (t - tEs) * 0.12; pos = cp.clone().add(V(Math.sin(b) * 9, 2, Math.cos(b) * 9)); look = cp.clone(); }
  else if (t < tRast - 0.05) { pathL.material.opacity = 0.6 * cl((t - tEr) / 1); const f = K.eio(prog(t, tEnt, 3)); pos = V(lerp(cp.x + 10, 20, f), lerp(5, 170, f), lerp(cp.z + 20, 140, f)); look = V(lerp(cp.x, 0, f), 0, lerp(cp.z, 0, f)); }
  else if (t < tUnd - 0.05) { pathL.material.opacity = 0.6; pos = V(10, 150, 120); look = V(0, 0, 10); }
  else if (t < tJetzt - 0.05) { const b = 1.0 + (t - tUnd) * 0.08; pos = cp.clone().add(V(Math.sin(b) * 14, 4, Math.cos(b) * 14)); look = cp.clone(); }
  else if (t < tNie - 0.05) { const f = K.eio(prog(t, tJetzt, 2)); const b = 0.2 + (t - tJetzt) * 0.1; const d = lerp(12, 7, f); pos = cp.clone().add(V(Math.sin(b) * d, 1, Math.cos(b) * d)); look = cp.clone();
    sparks.forEach((s) => (s.s.material.opacity = (t > tJetzt + 1.5 ? 1 : 0) * (0.5 + 0.5 * Math.sin(t * 5 + s.ph)))); }
  else { pathL.material.opacity = 0.4; const f = prog(t, tNie, 8); pos = V(lerp(40, 60, f), lerp(120, 200, f), lerp(120, 220, f)); look = V(30, 0, 0); }
  fill.position.copy(cam.position); cam.fov = 40; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(sc, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tEnt, tEr - 0.1, "entdeckt: Juli 2025");
  seg(tEr, tDie - 0.1, "Nr. 3<div class='sub'>aus einem anderen Sternsystem</div>");
  seg(tDie, tRast - 0.1, "<div style='font-size:62px;line-height:1.35'>1 · ʻOumuamua 2017<br>2 · Borisov 2019<br>3 · ATLAS 2025</div>");
  seg(W("sechzig") - 0.2, tDas - 0.1, "≈ 58 km/s"); seg(tDas, tGew - 0.1, "> 200.000 km/h"); seg(tGew, tUnd - 0.1, "Gewehrkugel: ≈ 1 km/s");
  seg(tUnd, tJetzt - 0.1, "> 7 Mrd. Jahre alt?<div class='sub'>unsere Sonne: 4,6 Mrd.</div>");
  seg(tErg, tViel - 0.1, "Eis wie weit<br>hinter dem Neptun"); seg(tViel, tNie - 0.1, "Eiswelten auch<br>bei anderen Sternen?");
  seg(tNie + 0.5, tWue - 0.1, "kommt nie wieder 👋");
  word(wh, wa); cap(t);
};
