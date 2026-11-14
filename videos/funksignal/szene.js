const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(44);
const sc = new THREE.Scene(); K.stars(sc, 7000, -1, 30000, 1.7).material.opacity = 0.6;
sc.add(new THREE.AmbientLight(0x2a2228, 0.7)); const fill = new THREE.DirectionalLight(0xffe6dc, 0.5); sc.add(fill);
const sunTex = await tex("sun.jpg");
// Roter Zwerg GJ 725A (Ursprung)
const RS = 12; const star = new THREE.Mesh(new THREE.SphereGeometry(RS, 128, 96), new THREE.MeshBasicMaterial({ map: sunTex, color: new THREE.Color(1.35, 0.5, 0.28), toneMapped: false })); sc.add(star);
const sg1 = K.sprite(sc, K.glowTex("rgba(255,70,30,.55)"), RS * 5, V(0, 0, 0), 0.8), sg2 = K.sprite(sc, K.glowTex("rgba(255,140,90,.5)"), RS * 2.8, V(0, 0, 0), 0.7);
const sl = new THREE.PointLight(0xff9a70, 3.2, 0, 0); sc.add(sl);
// Sonne zum Vergleich (Radius ca. 1 : 0,35)
const sun = new THREE.Mesh(new THREE.SphereGeometry(RS / 0.35, 128, 96), new THREE.MeshBasicMaterial({ map: sunTex, color: new THREE.Color(1.25, 0.95, 0.65), toneMapped: false })); sc.add(sun);
const sunG = K.sprite(sc, K.glowTex("rgba(255,170,60,.5)"), RS / 0.35 * 3.6, V(0, 0, 0), 0.7);
// Gesteinsplanet (Jahr = 11 Tage), unbekannter Riesenplanet
const rock = new THREE.Mesh(new THREE.SphereGeometry(3.5, 96, 64), new THREE.MeshStandardMaterial({ map: await tex("mercury.jpg"), color: 0xd9b8a8, roughness: 1 })); sc.add(rock);
const orbit = new THREE.Mesh(new THREE.RingGeometry(31.9, 32.1, 256), new THREE.MeshBasicMaterial({ color: 0xffb090, transparent: true, opacity: 0.25, side: THREE.DoubleSide, depthWrite: false })); orbit.rotation.x = -Math.PI / 2; sc.add(orbit);
const GP = V(150, 20, -120); const giant = new THREE.Mesh(new THREE.SphereGeometry(14, 128, 96), new THREE.MeshStandardMaterial({ map: await tex("jupiter.jpg"), color: 0xc8b8d8, roughness: 1 })); giant.position.copy(GP); giant.rotation.z = 0.15; sc.add(giant);
const aur = [1, -1].map((s) => { const a = K.sprite(sc, K.glowTex("rgba(90,255,170,.7)"), 16, GP.clone().add(V(0, s * 13.4, 0)), 0); const b = K.sprite(sc, K.glowTex("rgba(190,110,255,.5)"), 26, GP.clone().add(V(0, s * 14.5, 0)), 0); return [a, b]; }).flat();
// Funkwellen (Ringe)
const rings = []; for (let i = 0; i < 6; i++) { const m = new THREE.Mesh(new THREE.RingGeometry(0.97, 1, 160), new THREE.MeshBasicMaterial({ color: 0x7fd0ff, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); sc.add(m); rings.push(m); }
// Magnetfeld-Linien Stern ↔ Planet
const NF = 9, fl = []; for (let i = 0; i < NF; i++) { const g = new THREE.BufferGeometry().setFromPoints(new Array(40).fill(0).map(() => V(0, 0, 0))); const l = new THREE.Line(g, new THREE.LineBasicMaterial({ color: 0x9fd8ff, transparent: true, opacity: 0, blending: THREE.AdditiveBlending })); sc.add(l); fl.push(l); }
// Ausbruch
const arc = new THREE.Mesh(new THREE.TorusGeometry(4, 0.9, 24, 96, Math.PI), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.0, 0.32, 0.08), toneMapped: false, transparent: true, opacity: 0 })); sc.add(arc);
const arcG = K.sprite(sc, K.glowTex("rgba(255,90,30,.7)"), 30, V(0, 0, 0), 0); const flare = [];
// Erde (für Entfernung)
const EA = K.earth(sc, { day, night, topo }, 6); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93);

// ===== Zeiten =====
const tDer = W("der", 7.5), tGJ = W("gj"), tEr = W("er", 11.4), tMit = W("mit", 15.5), tNur = W("nur", 18.5), tElf = W("elfeinhalb"), tFor = W("forscher", 23), tStunde = W("stunde"), tWeg = W("weg"), tUm = W("um", 30.5), tJahr = W("jahr", 33), tDie = W("die", 36), tEr1 = W("erstens"), tZw = W("zweitens"), tDr = W("drittens"), tAl = W("und", 50.9), tSig = W("das", 54), tWas = W("was", 58.5), tFolg = W("folg", 61);
// ===== Beschriftungen =====
label("GJ 725A<small>Roter Zwerg</small>", star, RS, { t0: tGJ + 0.3, t1: tEr - 0.1, size: 80, gap: 40 });
label("Sonne", sun, RS / 0.35, { t0: tEr + 0.6, t1: tMit - 0.1, size: 70, gap: 24 }); label("GJ 725A", star, RS, { t0: tEr + 0.9, t1: tMit - 0.1, size: 56, gap: 24 });
label("🌍 Erde + Sonne", EA.group, 6, { t0: tNur + 0.3, t1: tFor - 0.1, size: 48, gap: 30 }); label("GJ 725A", star, RS, { t0: tNur + 0.5, t1: tFor - 0.1, size: 48, gap: 50 });
label("Gesteinsplanet", rock, 3.5, { t0: tUm + 1.0, t1: tDie - 0.1, size: 54, gap: 26 });
label("unbekannter<br>Riesenplanet?", giant, 14, { t0: tEr1 + 0.8, t1: tZw - 0.1, size: 58, gap: 30 });

renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.4, 0.8);
  // Standard-Zustände
  sun.visible = false; sunG.material.opacity = 0; rock.visible = false; orbit.visible = false; giant.visible = false; aur.forEach((a) => (a.material.opacity = 0)); EA.group.visible = false;
  fl.forEach((l) => (l.material.opacity = 0)); arc.material.opacity = 0; arcG.material.opacity = 0;
  star.rotation.y = t * 0.06; sg1.material.opacity = 0.8; sg2.material.opacity = 0.7;
  let pos, look = V(0, 0, 0), fov = 40, rOn = 0, rMax = 120;
  const pa = 0.5 + t * (2 * Math.PI / 11) * 0.3; rock.position.set(Math.cos(pa) * 32, 0, Math.sin(pa) * 32); rock.rotation.y = t * 0.3;
  if (t < tDer - 0.05) { const f = K.eio(prog(t, 0, tDer)); const a = 0.2 + t * 0.05; const d = lerp(160, 90, f); pos = V(Math.sin(a) * d, 8, Math.cos(a) * d); rOn = 1; }
  else if (t < tEr - 0.05) { const a = 0.6 + t * 0.06; pos = V(Math.sin(a) * 70, 10, Math.cos(a) * 70); look = V(0, 3, 0); }
  else if (t < tMit - 0.05) { sun.visible = true; sun.position.set(-62, 0, -20); sunG.position.copy(sun.position).add(V(0, 0, -10)); sunG.material.opacity = 0.6; const f = K.eio(prog(t, tEr, 1.4)); pos = V(lerp(0, -28, f), 6, lerp(70, 300, f)); look = V(lerp(0, -28, f), lerp(0, 4, f), 0); }
  else if (t < tNur - 0.05) { const f = prog(t, tMit, tNur - tMit); pos = V(0, 4, lerp(220, 300, f)); look = V(0, 0, 0); E.look([1, 1, 1], [0, 0, 0], 0.25, 0.85); sg1.material.opacity = 0.25; sg2.material.opacity = 0.2; }
  else if (t < tFor - 0.05) { // Entfernung: Sonne + Erde links, Stern rechts
    sun.visible = true; EA.group.visible = true; sun.position.set(-300, -20, -40); sun.scale.setScalar(0.35); sunG.position.copy(sun.position); sunG.scale.setScalar(sun.geometry.parameters.radius * 3.6 * 0.35); sunG.material.opacity = 0.6;
    EA.group.position.set(-262, -20, 10); const f = K.eio(prog(t, tNur, 2)); pos = V(-150, lerp(-10, 30, f), lerp(320, 1000, f)); look = V(-150, 0, 0); }
  else if (t < tUm - 0.05) { const a = 0.9 + t * 0.03; pos = V(Math.sin(a) * 120, 30, Math.cos(a) * 120); rOn = t < tWeg + 0.4 ? 1 : 0; rMax = 150; }
  else if (t < tDie - 0.05) { rock.visible = true; orbit.visible = true; const f = K.eio(prog(t, tUm, 1.5)); pos = V(lerp(0, 10, f), lerp(30, 130, f), lerp(120, 150, f)); look = V(lerp(0, 10, f), 0, 0); }
  else if (t < tEr1 - 0.05) { rock.visible = true; orbit.visible = true; giant.visible = true; pos = V(55, 90, 480); look = V(55, 5, -50); }
  else if (t < tZw - 0.05) { giant.visible = true; const s = 0.6 + 0.4 * Math.sin(t * 4); aur.forEach((a, i) => (a.material.opacity = (i % 2 ? 0.45 : 0.7) * s * cl((t - tEr1) / 0.6))); giant.rotation.y = t * 0.2; const f = K.eio(prog(t, tEr1, 1.4)); pos = GP.clone().add(V(lerp(-60, -20, f), lerp(20, 10, f), lerp(130, 88, f))); look = GP.clone(); }
  else if (t < tDr - 0.05) { rock.visible = true; orbit.visible = true; const rp = rock.position; fl.forEach((l, i) => { const P = l.geometry.attributes.position; const off = (i - (NF - 1) / 2) * 0.5; const s = V(0, off * 6, 0).add(rp.clone().normalize().multiplyScalar(RS)); const c = rp.clone().multiplyScalar(0.5).add(V(0, 12 + off * 8, 0));
      for (let k = 0; k < 40; k++) { const u = k / 39; const p = s.clone().multiplyScalar((1 - u) * (1 - u)).add(c.clone().multiplyScalar(2 * u * (1 - u))).add(rp.clone().multiplyScalar(u * u)); P.setXYZ(k, p.x, p.y, p.z); } P.needsUpdate = true;
      l.material.opacity = (0.75 + 0.25 * Math.sin(t * 6 + i)) * cl((t - tZw) / 0.6); });
    pos = rock.position.clone().multiplyScalar(0.5).add(V(0, 75, 35)); look = rock.position.clone().multiplyScalar(0.5); }
  else if (t < tAl - 0.05) { const f = K.eout(prog(t, tDr + 0.5, 1.6)); const ang = 0.7; const dir = V(Math.cos(ang), Math.sin(ang), 0);
    arc.position.copy(dir.clone().multiplyScalar(RS - 0.5)); arc.rotation.set(0, 0, ang - Math.PI / 2); arc.scale.setScalar(0.3 + 1.1 * f); arc.material.opacity = f > 0 ? 1 : 0;
    arcG.position.copy(dir.clone().multiplyScalar(RS + 3)); arcG.material.opacity = f * 0.45; arcG.scale.setScalar(16 + 20 * f);
    E.grade.uniforms.flash.value = t > tDr + 0.5 && t < tDr + 0.75 ? 0.25 : 0; pos = V(0, -6, 115); look = V(4, 4, 0); E.look([1, 1, 1], [0, 0, 0], 0.45, 0.8); }
  else if (t < tSig - 0.05) { const a = 1.4 + t * 0.03; pos = V(Math.sin(a) * 150, 20, Math.cos(a) * 150); }
  else { rOn = 0.35; rMax = 200; const f = prog(t, tSig, 8); pos = V(0, 10, lerp(140, 260, f)); }
  // Funkwellen
  rings.forEach((m, i) => { const ph = ((t * 0.45 + i / rings.length) % 1); const r = RS + ph * rMax; m.scale.setScalar(r); m.position.set(0, 0, 0); m.lookAt(cam.position); m.material.opacity = rOn * (1 - ph) * 0.8; });
  fill.position.copy(cam.position); cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look); rings.forEach((m) => m.lookAt(cam.position));
  EA.mesh.rotation.y = t * 0.1; sun.rotation.y = t * 0.03; if (!(t >= tNur - 0.05 && t < tFor - 0.05)) { sun.scale.setScalar(1); sunG.scale.setScalar(RS / 0.35 * 3.6); }
  E.render(sc, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tMit + 0.2, tNur - 0.1, "👁️ unsichtbar<div class='sub'>mit bloßem Auge</div>");
  seg(tElf - 0.2, tFor - 0.1, "11,5 Lichtjahre<div class='sub'>≈ 109 Billionen Kilometer</div>");
  seg(tStunde - 0.4, tUm - 0.1, t < tWeg ? "📡 ≈ 1 Stunde lang<div class='sub'>dann war es weg</div>" : "📡 … weg");
  seg(tJahr, tDie - 0.1, "1 Jahr = 11 Tage");
  seg(tDie + 0.3, tEr1 - 0.1, "3 Erklärungen");
  seg(tEr1, tZw - 0.1, "1 · Polarlichter"); seg(tZw, tDr - 0.1, "2 · Magnetfeld"); seg(tDr, tAl - 0.1, "3 · Ausbruch");
  seg(tAl, tSig - 0.1, "👽 Aliens?<div class='sub'>kein Hinweis</div>"); seg(tSig + 0.2, tWas - 0.1, "Signal noch schwach<div class='sub'>Forscher hören weiter zu</div>");
  word(wh, wa); cap(t);
};
