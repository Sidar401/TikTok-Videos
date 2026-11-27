const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(331);
// @modelle
const moonT = await tex("moon.jpg"), jupT = await tex("jupiter.jpg"), marsT = await tex("mars.jpg");
const dayT = new THREE.Texture(day); dayT.needsUpdate = true; dayT.colorSpace = THREE.SRGBColorSpace;
// ================= Morgenhimmel nach Süden =================
const sd = new THREE.Scene(); const SKY = K.sky(sd, 0x03050c, 0x0b1230, 0x3a3048, 5000); K.reseed(4); K.stars(sd, 5000, 0.05, 4800, 1.6).material.opacity = 0.7;
K.reseed(8); K.city(sd, { n: 140, rMin: 520, rMax: 950, arc: 0.9, lit: 0.12, hMax: 70 }); K.city(sd, { n: 40, rMin: 380, rMax: 480, arc: 0.9, lit: 0.1, hMax: 28 }); const GR = new THREE.Mesh(new THREE.PlaneGeometry(20000, 20000), new THREE.MeshBasicMaterial({ color: 0x05060a })); GR.rotation.x = -Math.PI / 2; GR.position.y = -2; sd.add(GR);
const D = 2000; const dome = (dx, alt) => { const a = alt * Math.PI / 180, b = dx * Math.PI / 180; return V(D * Math.cos(a) * Math.sin(b), D * Math.sin(a), -D * Math.cos(a) * Math.cos(b)); };
const MP = dome(0, 20), JP = dome(-2.2, 21.3), RP = dome(-9.3, 21.0), MAP = dome(-8, 22.5);
const MOON = new THREE.Mesh(new THREE.SphereGeometry(26, 96, 64), new THREE.MeshStandardMaterial({ map: moonT, roughness: 1, emissive: 0x30302c, emissiveIntensity: 0.15 })); MOON.position.copy(MP); MOON.rotation.y = -0.4; sd.add(MOON);
const ml = new THREE.DirectionalLight(0xfff4e6, 3.0); ml.position.copy(MP).add(V(-1, -0.15, 0.75).multiplyScalar(500)); ml.target = MOON; sd.add(ml); sd.add(ml.target); sd.add(new THREE.AmbientLight(0x202838, 0.5));
const moonG = K.sprite(sd, K.glowTex("rgba(200,210,255,.5)"), 120, MP, 0.35);
const JS = K.sprite(sd, K.glowTex("rgba(255,248,230,1)"), 18, JP, 1), MS = K.sprite(sd, K.glowTex("rgba(255,140,70,1)"), 12, MAP, 0.9), RS = K.sprite(sd, K.glowTex("rgba(200,220,255,1)"), 11, RP, 0.9);
// ================= Jupiter + Erde im All =================
const sp = new THREE.Scene(); K.reseed(9); K.stars(sp, 9000, -1, 60000, 1.7).material.opacity = 0.75; sp.add(new THREE.AmbientLight(0x30343e, 0.5)); const lp = new THREE.DirectionalLight(0xfff2e0, 2.6); lp.position.set(-1, 0.25, 0.7); sp.add(lp);
const JUP = new THREE.Mesh(new THREE.SphereGeometry(11, 128, 96), new THREE.MeshStandardMaterial({ map: jupT, roughness: 0.9 })); sp.add(JUP);
const EAR = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshStandardMaterial({ map: dayT, roughness: 0.8 })); EAR.position.set(-9, -8, 8); sp.add(EAR);
// ================= Entfernungen (senkrecht: Erde unten, oben Jupiter) =================
const sl = new THREE.Scene(); K.reseed(10); K.stars(sl, 9000, -1, 60000, 1.7).material.opacity = 0.7; sl.add(new THREE.AmbientLight(0x30343e, 0.6)); const ll = new THREE.DirectionalLight(0xfff2e0, 2.4); ll.position.set(-1, 0.2, 0.7); sl.add(ll);
const E2 = EAR.clone(); E2.scale.setScalar(4); E2.position.set(0, 0, 0); sl.add(E2); const M2 = new THREE.Mesh(new THREE.SphereGeometry(1.1, 64, 48), new THREE.MeshStandardMaterial({ map: moonT, roughness: 1 })); M2.position.set(0, 30, 0); sl.add(M2);
const J2 = JUP.clone(); J2.position.set(0, 1600, 0); J2.scale.setScalar(4); sl.add(J2);
const lineM = new THREE.LineDashedMaterial({ color: 0xffd23f, dashSize: 4, gapSize: 3, transparent: true, opacity: 0, toneMapped: false }); const LJ = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, 4, 0), V(0, 1556, 0)]), lineM); LJ.computeLineDistances(); sl.add(LJ);
const photon = K.sprite(sl, K.glowTex("rgba(255,240,180,1)"), 6, V(0, 0, 0), 0);
// ================= Fernglas-Blick =================
const sb = new THREE.Scene(); K.reseed(12); K.stars(sb, 3000, -1, 60000, 1.6).material.opacity = 0.6; const lb = new THREE.DirectionalLight(0xfff2e0, 2.4); lb.position.set(-1, 0.1, 0.6); sb.add(lb); sb.add(new THREE.AmbientLight(0x30343e, 0.4));
const J3 = JUP.clone(); J3.scale.setScalar(0.12); sb.add(J3); const moons = [-9, -4.5, 3.5, 13].map((x) => K.sprite(sb, K.glowTex("rgba(255,250,235,1)"), 0.7, V(x * 0.5, 0.05 * x, 0), 1));
const mask = new THREE.Mesh(new THREE.RingGeometry(9, 400, 96), new THREE.MeshBasicMaterial({ color: 0x000000 })); sb.add(mask); const edge = new THREE.Mesh(new THREE.TorusGeometry(9, 0.08, 8, 128), new THREE.MeshBasicMaterial({ color: 0x5a5f68 })); sb.add(edge); const rim = K.sprite(sb, K.glowTex("rgba(0,0,0,0)"), 1, V(0, 0, 0), 0);
// ===== Zeiten =====
const tUnd = W("und", 4), tSchau = W("schau"), tDort = W("dort"), tEr = W("er", 17.9), tJup = W("jupiter", 23.5), tUndE = W("und", 29), tDerM = W("der", 36.3), tDie = W("die", 42.5), tGanz = W("ganz", 45.4), tAm = W("am", 53.6), tMit = W("mit", 56.9), tWir = W("wirst"), END = 64.9, KARTE = 8.29;
const mO = new THREE.Object3D(); mO.position.copy(MP); sd.add(mO);
label("Mond", mO, 26, { t0: tDort + 0.2, t1: tEr - 0.1, size: 54, gap: 16 }); label("Jupiter", JS, 6, { t0: W("jupiter", 16.6) - 0.1, t1: tEr - 0.1, size: 54, gap: 10 });
label("Mars", MS, 5, { t0: W("mars") - 0.1, t1: tAm - 0.1, size: 48, gap: 8 }); label("Regulus", RS, 5, { t0: W("regulus") - 0.1, t1: tAm - 0.1, size: 48, gap: 8 }); label("Jupiter", JS, 6, { t0: tGanz, t1: tAm - 0.1, size: 48, gap: 8 }); label("Mond", mO, 26, { t0: tGanz, t1: tAm - 0.1, size: 48, gap: 12 });
label("Erde", EAR, 1, { t0: W("erden") - 0.2, t1: tJup - 0.1, size: 46, gap: 10 }); label("Erde", E2, 4, { t0: tUndE, t1: tDie - 0.1, size: 46, gap: 10 }); label("Mond", M2, 1.1, { t0: tDerM, t1: tDie - 0.1, size: 46, gap: 10 }); label("Jupiter", J2, 44, { t0: tUndE, t1: tDerM - 0.1, size: 50, gap: 14 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
const skyC = (k) => { SKY.material.uniforms.h.value.setRGB(lerp(0.23, 0.85, k), lerp(0.19, 0.5, k), lerp(0.28, 0.3, k)); SKY.material.uniforms.m.value.setRGB(lerp(0.045, 0.2, k), lerp(0.07, 0.22, k), lerp(0.19, 0.38, k)); };
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sd, pos = V(0, 8, 0), look = MP.clone(), fov = 30; skyC(0); JUP.rotation.y = t * 0.08; EAR.rotation.y = t * 0.2; J2.rotation.y = t * 0.08; E2.rotation.y = t * 0.15; photon.material.opacity = 0; lineM.opacity = 0;
  const skyLook = (dxDeg, alt) => dome(dxDeg, alt);
  if (t < tUnd - 0.05) { const f = K.eio(prog(t, 0, tUnd)); fov = lerp(9, 14, f); look = skyLook(-1.1, lerp(22.4, 23.5, f)); }
  else if (t < tDort - 0.05) { const f = prog(t, tUnd, tDort - tUnd); fov = lerp(48, 42, f); look = skyLook(-1, lerp(10, 13, f)); }
  else if (t < tEr - 0.05) { const f = K.eio(prog(t, tDort, tEr - tDort)); fov = lerp(30, 8, f); look = skyLook(-1.1, lerp(17, 20.6, f)); }
  else if (t < tJup - 0.05) { scene = sp; const f = prog(t, tEr, tJup - tEr); const a = -0.2 + f * 0.3; pos = V(Math.sin(a) * 52 - 6, 6, Math.cos(a) * 52); look = V(-6, 0, 0); fov = 40; }
  else if (t < tUndE - 0.05) { scene = sp; const f = prog(t, tJup, tUndE - tJup); pos = V(lerp(-4, 2, f), 3, lerp(34, 28, f)); look = V(-2, 0, 0); fov = 40; }
  else if (t < tDerM - 0.05) { scene = sl; const f = prog(t, tUndE, tDerM - tUndE); lineM.opacity = 0.9; const k = cl((t - W("sein", 32.9)) / 3.2); photon.material.opacity = k > 0 && k < 1 ? 1 : 0; photon.position.set(0, lerp(1556, 16, k), 0); pos = V(60, 900, lerp(3350, 3250, f)); look = V(0, 900, 0); fov = 40; }
  else if (t < tDie - 0.05) { scene = sl; const f = prog(t, tDerM, tDie - tDerM); lineM.opacity = 0; const k = cl((t - W("sein", 40.1)) / 1.3); photon.material.opacity = k > 0 && k < 1 ? 1 : 0; photon.position.set(0, lerp(29, 4, k), 0); photon.scale.setScalar(2); pos = V(lerp(30, 24, f), 15, 70); look = V(0, 15, 0); fov = 40; }
  else if (t < tGanz - 0.05) { scene = sl; const f = K.eio(prog(t, tDie, tGanz - tDie)); lineM.opacity = 0.7; pos = V(lerp(24, 6, f), lerp(15, -60, f), lerp(70, 10, f)); look = V(0, 1600, 0); fov = lerp(40, 20, f); }
  else if (t < tAm - 0.05) { const f = prog(t, tGanz, tAm - tGanz); fov = lerp(24, 27, f); look = skyLook(-4.6, 21); }
  else if (t < tMit - 0.05) { const f = prog(t, tAm, tMit - tAm); skyC(K.eio(f) * 0.8); fov = lerp(42, 50, f); look = skyLook(-3, lerp(13, 11, f)); }
  else if (t < tWir - 0.05) { scene = sb; const f = prog(t, tMit, tWir - tMit); pos = V(0, 0, 30); look = V(0, 0, 0); fov = 40; moons.forEach((m) => (m.material.opacity = cl((t - W("lichtpunkte") + 0.2) / 0.6))); J3.rotation.y = t * 0.1; }
  else { const f = prog(t, tWir, END - tWir); fov = lerp(40, 26, f); look = skyLook(-2, lerp(14, 18, f)); }
  cam.fov = fov; cam.near = 0.1; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("süden") - 0.6, tDort - 0.1, "🧭 Süden" + sub("Montag, 30. November")); seg(W("tausend") - 0.1, tJup - 0.1, "🌍 × 1.000+"); seg(W("halbe") - 0.2, tDerM - 0.1, "💡 über 30 Min.");
  seg(W("sekunde") - 0.2, tDie - 0.1, "💡 gut 1 Sekunde"); seg(W("stunde", 53.6) - 0.3, tMit - 0.1, "⏰ 1 Std. vor Sonnenaufgang");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
