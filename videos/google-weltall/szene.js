const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(71);
// @modelle
// ================= Orbit: Erde + Satelliten-Schwarm =================
const so = new THREE.Scene(); K.stars(so, 9000, -1, 60000, 1.7).material.opacity = 0.7; so.add(new THREE.AmbientLight(0x30343e, 0.6));
const sunL = new THREE.DirectionalLight(0xfff2e0, 2.0); sunL.position.set(-1, 0.3, 0.4); so.add(sunL); const sunS = K.sprite(so, K.glowTex("rgba(255,235,200,1)"), 4000, V(-30000, 9000, 12000), 0.9);
const RE = 600; const EA = K.earth(so, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-1, 0.3, 0.4).normalize(); EA.group.position.set(0, -RE * 1.45, 0);
const swarm = new THREE.Group(); so.add(swarm); const sats = []; for (let i = 0; i < 9; i++) for (let j = 0; j < 9; j++) { const s = MO.suncatcher(); s.g.position.set((i - 4) * 9, Math.sin(i * 1.3 + j) * 0.8, (j - 4) * 9); s.g.rotation.y = 0.785; swarm.add(s.g); sats.push(s); }
const lasers = []; const lm = new THREE.LineBasicMaterial({ color: 0xff3b5c, transparent: true, opacity: 0, toneMapped: false }); for (let k = 0; k < 40; k++) { const a = sats[Math.floor(K.rnd() * 81)], b = sats[Math.floor(K.rnd() * 81)]; const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints([a.g.position, b.g.position]), lm); swarm.add(l); lasers.push(l); }
const one = MO.suncatcher(); so.add(one.g); const two = MO.suncatcher(); so.add(two.g); const rack = MO.rack(); so.add(rack.g); const oneO = new THREE.Object3D(); one.g.add(oneO); oneO.position.set(0, 2.2, 0);
const term = new THREE.Mesh(new THREE.TorusGeometry(RE * 1.2, 2, 8, 256), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); term.position.copy(EA.group.position); term.rotation.set(0, Math.PI / 2 - 0.4, 0); so.add(term);
// ================= Rechenzentrum auf der Erde =================
const sd = new THREE.Scene(); sd.add(new THREE.AmbientLight(0x404858, 0.5)); const ld = new THREE.PointLight(0x9fb4ff, 60, 120, 1.4); ld.position.set(0, 12, 10); sd.add(ld);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), MO.plain(0x16181d, 0.3, 0.6)); floor.rotation.x = -Math.PI / 2; floor.position.y = -1.05; sd.add(floor);
const racks = []; for (let r = 0; r < 2; r++) for (let i = 0; i < 26; i++) { const k = MO.rack(); k.g.position.set(r ? 1.8 : -1.8, 0, -i * 1.15); k.g.rotation.y = r ? -Math.PI / 2 : Math.PI / 2; sd.add(k.g); racks.push(k); }
// ================= Rakete New Glenn =================
const sr = new THREE.Scene(); K.reseed(6); K.stars(sr, 7000, -1, 20000, 1.6); const skyR = K.sky(sr, 0x02040a, 0x0a1a3a, 0x24406e, 15000); sr.add(new THREE.AmbientLight(0x404858, 0.6)); const lr = new THREE.DirectionalLight(0xfff2e0, 1.3); lr.position.set(300, 200, 400); sr.add(lr);
const NG = MO.newGlenn(); sr.add(NG.g); const ngO = new THREE.Object3D(); NG.g.add(ngO); ngO.position.set(0, 104, 0); const pad = new THREE.Mesh(new THREE.CylinderGeometry(40, 40, 2, 48), MO.plain(0x55585e, 0.2, 0.8)); pad.position.y = -1; sr.add(pad);
const ngx = MO.exhaust(60, 4); ngx.position.y = -1.5; NG.g.add(ngx); const fire = K.sprite(sr, K.glowTex("rgba(255,170,80,1)"), 200, V(0, 30, 0), 0); const smoke = MO.smoke(sr, 60);
// ===== Zeiten =====
const tUnd = W("und", 2.5), tDas = W("das", 5.2), tProj = W("das", 10), tProb = W("das", 13.5), tIm = W("im", 22.3), tLaut = W("laut"), tJed = W("jeder"), tViele = W("viele"), tSchon = W("schon"), tUnd2 = W("und", 51.3), tFirma = W("die", 58.2), tHaken = W("ein", 61.2), END = 68.0, KARTE = 10.1;
label("Suncatcher", oneO, 1.5, { t0: tProj + 0.4, t1: tProb - 0.1, size: 52, gap: 18 }); label("New Glenn", ngO, 4, { t0: W("new", 54.5) - 0.1, t1: tFirma - 0.1, size: 54, gap: 18 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = so, pos = V(0, 30, 120), look = V(0, 0, 0), fov = 42; EA.group.rotation.y = 2.0 + t * 0.006; EA.clouds.rotation.y = t * 0.003; swarm.visible = true; one.g.visible = false; two.g.visible = false; rack.g.visible = false; lm.opacity = 0; term.material.opacity = 0;
  sats.forEach((s, i) => (s.chip.material.color.setHSL(0.6, 0.9, 0.45 + 0.15 * Math.sin(t * 3 + i)))); ngx.visible = false; fire.material.opacity = 0; smoke.forEach((s) => (s.material.opacity = 0)); NG.g.visible = true;
  const blink = (k) => k.leds.forEach((l, i) => (l.visible = Math.sin(t * 7 + i * 2.3 + k.g.position.z) > -0.3));
  if (t < tDas - 0.05) { const f = prog(t, 0, tDas); const a = 0.5 + f * 0.5; const d = lerp(70, 140, K.eio(f)); pos = V(Math.sin(a) * d, lerp(12, 40, f), Math.cos(a) * d); look = V(0, -4, 0); fov = 44; }
  else if (t < tProj - 0.05) { swarm.visible = false; one.g.visible = true; one.g.position.set(0, 0, 0); one.g.rotation.set(0.2, t * 0.3, 0.1); const f = prog(t, tDas, tProj - tDas); pos = V(Math.sin(f) * 8, 3, 8); look = V(0, 0.3, 0); fov = 42; }
  else if (t < tProb - 0.05) { const f = prog(t, tProj, tProb - tProj); swarm.visible = false; one.g.visible = true; one.g.position.set(0, 0, 0); one.g.rotation.set(0.25, 1 + t * 0.2, 0); const d = lerp(10, 40, K.eio(f)); pos = V(-d * 0.6, d * 0.2 + 2, d); look = V(0, -d * 0.2, 0); fov = 44; }
  else if (t < tIm - 0.05) { scene = sd; racks.forEach(blink); const f = prog(t, tProb, tIm - tProb); pos = V(0, lerp(1.2, 1.6, f), lerp(4, -14, f)); look = V(0, 0.4, lerp(-6, -26, f)); fov = 52; }
  else if (t < tLaut - 0.05) { const f = prog(t, tIm, tLaut - tIm); swarm.visible = false; term.material.opacity = 0.8 * cl((t - W("auf", 25.5)) / 0.6); const d = lerp(1700, 2300, f); pos = V(-d * 0.3, d * 0.25, d); look = EA.group.position.clone().add(V(0, RE * 0.4, 0)); fov = 44; }
  else if (t < tJed - 0.05) { swarm.visible = false; one.g.visible = true; one.g.position.set(0, 0, 0); one.g.rotation.set(0.6, 0.4, 0); const f = prog(t, tLaut, tJed - tLaut); pos = V(-4, 6 - f, 5); look = V(0, 0.3, 0); fov = 42; }
  else if (t < tViele - 0.05) { swarm.visible = false; one.g.visible = true; one.g.position.set(0, 0, 0); one.g.rotation.set(0.1, 0.6 + t * 0.1, 0); rack.g.visible = t > W("ungefähr") - 0.2; rack.g.position.set(2.4, -0.4, 0.3); rack.g.rotation.y = -0.4; blink(rack); const f = prog(t, tJed, tViele - tJed); pos = V(lerp(0.8, 1.4, f), 1.2, 9); look = V(rack.g.visible ? 1.1 : 0, 0, 0); fov = 46; }
  else if (t < tSchon - 0.05) { const f = prog(t, tViele, tSchon - tViele); lm.opacity = t > W("laser") - 0.2 ? 0.75 : 0; const a = 0.3 + f * 0.5; const d = lerp(150, 110, f); pos = V(Math.sin(a) * d, 50, Math.cos(a) * d); look = V(0, -4, 0); fov = 44; }
  else if (t < tUnd2 - 0.05) { swarm.visible = false; const f = prog(t, tSchon, tUnd2 - tSchon); one.g.visible = true; one.g.position.set(-2.2, 0.6, 0); one.g.rotation.set(0.3, t * 0.2, 0); two.g.visible = true; two.g.position.set(2.2, -0.6, -1); two.g.rotation.set(0.3, t * 0.2 + 1, 0); lm.opacity = 0; pos = V(0, 3, 13); look = V(0, 0, 0); fov = 44; }
  else if (t < tHaken - 0.05) { scene = sr; const f = prog(t, tUnd2, tHaken - tUnd2); const a = 0.4 + f * 0.6; pos = V(Math.sin(a) * 190, lerp(25, 60, f), Math.cos(a) * 190); look = V(0, 50, 0); fov = 44; }
  else { scene = sr; const f = prog(t, tHaken, END - tHaken); const tx = W("explodiert") - 0.4; if (t > tx) { const k = cl((t - tx) / 2.5); NG.g.visible = k < 0.15; fire.material.opacity = Math.max(0, 1 - k * 0.8); fire.scale.setScalar(150 + k * 300); fire.position.set(0, 40 + k * 20, 0); E.grade.uniforms.flash.value = Math.max(0, 0.4 - k);
      smoke.forEach((s, i) => { const kk = ((i / smoke.length) * 0.7 + k * 0.6) % 1; s.position.set(Math.sin(i * 7.3) * (10 + kk * 90), 30 + kk * 120 * Math.cos(i), Math.cos(i * 3.1) * (10 + kk * 90)); s.scale.setScalar(30 + kk * 120); s.material.opacity = 0.25 * (1 - kk) * cl(k * 3); }); }
    pos = V(120, 40, 220); look = V(0, 50, 0); fov = 46; }
  cam.fov = fov; cam.near = 0.05; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(0.1, 2.6, logo("google.svg", 70)); seg(W("strom", 20) - 0.1, tIm - 0.1, "⚡ Strom wie ganze Städte"); seg(W("achtmal") - 0.2, tJed - 0.1, "☀️ bis zu 8× mehr Strom");
  seg(W("anfang") - 0.1, tFirma - 0.1, "🚀 Anfang 2029" + sub("Blue Origin · Jeff Bezos")); seg(W("mai") - 0.1, END, "💥 Mai: explodiert");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
