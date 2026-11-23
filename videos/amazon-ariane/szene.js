const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(81);
// @modelle
// ================= Startplatz Kourou (Dschungel, Dämmerung) =================
const sp = new THREE.Scene(); const stP = K.stars(sp, 6000, -1, 20000, 1.5); stP.material.opacity = 0.5; const skyP = K.sky(sp, 0x040814, 0x1d3358, 0xd88a52, 15000);
sp.add(new THREE.AmbientLight(0x4a5266, 0.7)); sp.add(new THREE.HemisphereLight(0x9fb0d8, 0x1d3a1a, 0.5)); const sunP = new THREE.DirectionalLight(0xffc58a, 1.4); sunP.position.set(-300, 120, 300); sp.add(sunP);
const jungleT = (() => { const c = document.createElement("canvas"); c.width = c.height = 512; const g = c.getContext("2d"); g.fillStyle = "#1f3a1c"; g.fillRect(0, 0, 512, 512); for (let i = 0; i < 6000; i++) { const v = K.rnd(); g.fillStyle = `rgba(${20 + v * 40},${50 + v * 60},${20 + v * 25},${0.5 * K.rnd()})`; g.beginPath(); g.arc(K.rnd() * 512, K.rnd() * 512, 2 + K.rnd() * 9, 0, 7); g.fill(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(40, 40); t.colorSpace = THREE.SRGBColorSpace; return t; })();
const ground = new THREE.Mesh(new THREE.PlaneGeometry(8000, 8000), new THREE.MeshStandardMaterial({ map: jungleT, roughness: 1 })); ground.rotation.x = -Math.PI / 2; sp.add(ground);
const padC = new THREE.Mesh(new THREE.BoxGeometry(70, 4, 70), MO.plain(0x6a6d72, 0.1, 0.9, 0.2)); padC.position.y = 2; sp.add(padC);
const AR = MO.ariane6(); sp.add(AR.g); AR.g.position.y = 4; const arO = new THREE.Object3D(); AR.g.add(arO); arO.position.set(0, 66, 0);
const tower = MO.pad(); tower.position.set(-6, 4, 0); sp.add(tower);
const lamps = []; for (const [x, z] of [[60, -60], [-60, -60], [60, 60], [-60, 60]]) { lamps.push(K.sprite(sp, K.glowTex("rgba(255,240,210,1)"), 16, V(x, 90, z), 0.85)); }
// ================= Orbit: Erde, Satelliten-Schwärme =================
const so = new THREE.Scene(); K.stars(so, 9000, -1, 60000, 1.7).material.opacity = 0.7; so.add(new THREE.AmbientLight(0x30343e, 0.6)); const sunO = new THREE.DirectionalLight(0xfff2e0, 1.8); sunO.position.set(-1, 0.4, 0.6); so.add(sunO);
const RE = 100; const EA = K.earth(so, { day, night, topo }, RE); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93); EA.U.sun.value = V(-1, 0.4, 0.6).normalize();
const swarm = (n, R, col, seed) => { K.reseed(seed); const p = []; for (let i = 0; i < n; i++) { const v = V(K.rnd() - 0.5, (K.rnd() - 0.5) * 1.2, K.rnd() - 0.5).normalize().multiplyScalar(R * (1 + K.rnd() * 0.06)); p.push(v.x, v.y, v.z); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); const m = new THREE.Points(g, new THREE.PointsMaterial({ color: col, size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); so.add(m); return m; };
const amzS = swarm(3200, RE * 1.09, 0xffa63d, 3), slS = swarm(9000, RE * 1.07, 0x9fd8ff, 7);
// Satelliten-Stapel (36) im Freiraum
const stack = new THREE.Group(); so.add(stack); const sats = []; for (let i = 0; i < 36; i++) { const s = MO.kuiperFlat(); s.position.set(((i % 3) - 1) * 1.55, Math.floor(i / 6) * 0.36 - 1, (Math.floor(i / 3) % 2 - 0.5) * 1.1); s.rotation.x = Math.PI / 2; stack.add(s); sats.push(s); } stack.scale.setScalar(4);
// ================= Vulcan-Absturz (Rückblick) =================
const sv = new THREE.Scene(); K.reseed(5); K.stars(sv, 6000, -1, 20000, 1.5); const skyV = K.sky(sv, 0x02040a, 0x0a1a3a, 0x24406e, 15000); sv.add(new THREE.AmbientLight(0x404858, 0.6)); const lv = new THREE.DirectionalLight(0xfff2e0, 1.2); lv.position.set(300, 200, 400); sv.add(lv);
const VU = MO.vulcan(); sv.add(VU.g); const vx = MO.exhaust(50, 3); vx.position.y = -1; VU.g.add(vx); const boom = K.sprite(sv, K.glowTex("rgba(255,180,90,1)"), 300, V(0, 40, 0), 0); const smk = MO.smoke(sv, 50);
// ===== Zeiten =====
const tWied = W("wieder"), tDoch = W("doch", 8.7), tAm = W("am", 11.3), tMit = W("mit", 15.8), tJetzt = W("jetzt", 19.3), tAn = W("an", 26.5), tGest = W("gestern"), tNeu = W("neuer"), tFuer = W("für", 47), tEs = W("es", 52.5), tAmz = W("amazon", 56.4), tUnd = W("und", 62.2), END = 66.6, KARTE = 11.2;
label("Ariane 6", arO, 4, { t0: tJetzt + 0.4, t1: tAn - 0.1, size: 54, gap: 20 }); label("Vulcan", VU.g, 0, { t0: W("vulcan") - 0.1, t1: tMit - 0.1, size: 52, gap: 0 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sp, pos = V(120, 30, 160), look = V(0, 40, 0), fov = 44; EA.group.rotation.y = 2 + t * 0.01; EA.clouds.rotation.y = t * 0.004; amzS.material.opacity = 0; slS.material.opacity = 0; stack.visible = false; boom.material.opacity = 0; vx.visible = false; smk.forEach((s) => (s.material.opacity = 0)); VU.g.visible = true;
  if (t < tWied - 0.05) { scene = sv; const f = prog(t, 0, tWied); VU.g.position.set(0, f * 40, 0); VU.g.rotation.z = f * 0.4; vx.visible = f < 0.6; vx.userData.mat.uniforms.t.value = t; vx.userData.mat.uniforms.power.value = 1; if (f > 0.6) { const k = (f - 0.6) / 0.4; VU.g.visible = k < 0.2; boom.position.set(0, 70, 0); boom.material.opacity = 1 - k * 0.5; boom.scale.setScalar(200 + k * 400); E.grade.uniforms.flash.value = Math.max(0, 0.4 - k); }
    pos = V(150, 40, 220); look = V(0, 60, 0); fov = 46; }
  else if (t < tAm - 0.05) { const f = prog(t, tWied, tAm - tWied); lamps.forEach((l) => (l.material.opacity = 0.85)); const a = 0.6 + f * 0.5; pos = V(Math.sin(a) * 150, lerp(10, 30, f), Math.cos(a) * 150); look = V(0, 40, 0); fov = 46; }
  else if (t < tJetzt - 0.05) { scene = sv; const f = prog(t, tAm, tJetzt - tAm); const k = cl((t - W("vulcan") - 0.6) / 2.5); VU.g.position.set(0, 40 + k * 10, 0); VU.g.rotation.z = 0.3 + k * 0.4; VU.g.visible = k < 0.15; vx.visible = k === 0; vx.userData.mat.uniforms.t.value = t;
    if (k > 0) { boom.position.set(0, 80, 0); boom.material.opacity = Math.max(0, 1 - k * 0.7); boom.scale.setScalar(200 + k * 500); smk.forEach((s, i) => { const kk = ((i / smk.length) * 0.7 + k * 0.5) % 1; s.position.set(Math.sin(i * 7) * (10 + kk * 80), 80 + Math.cos(i) * kk * 80, Math.cos(i * 3) * (10 + kk * 80)); s.scale.setScalar(30 + kk * 100); s.material.opacity = 0.12 * (1 - kk); }); }
    pos = V(160, 50, 240); look = V(0, 60, 0); fov = 46; }
  else if (t < tAn - 0.05) { const f = prog(t, tJetzt, tAn - tJetzt); const a = 0.2 + f * 0.8; pos = V(Math.sin(a) * 110, lerp(8, 4, f), Math.cos(a) * 110); look = V(0, 42, 0); fov = 50; }
  else if (t < tGest - 0.05) { scene = so; stack.visible = true; stack.position.set(0, 0, 0); stack.rotation.set(0.3, t * 0.25, 0); EA.group.visible = false; const f = prog(t, tAn, tGest - tAn); pos = V(Math.sin(f) * 14, 6, 14); look = V(0, 0, 0); fov = 44; }
  else if (t < tFuer - 0.05) { const f = prog(t, tGest, tFuer - tGest); lamps.forEach((l) => (l.material.opacity = 0.85)); pos = V(lerp(-70, -40, f), 12, lerp(90, 70, f)); look = V(0, 38, 0); fov = 48; }
  else if (t < tAmz - 0.05) { const f = prog(t, tFuer, tAmz - tFuer); const a = 1.6 + f * 0.7; pos = V(Math.sin(a) * 70, 18, Math.cos(a) * 70); look = V(0, 22, 0); fov = 46; }
  else { scene = so; EA.group.visible = true; const f = prog(t, tAmz, END - tAmz); amzS.material.opacity = cl((t - tAmz - 0.3) / 0.8); slS.material.opacity = 0.7 * cl((t - W("starlink") + 0.2) / 0.8); const a = 0.5 + f * 0.5; pos = V(Math.sin(a) * 430, 110, Math.cos(a) * 430); look = V(0, 0, 0); fov = 42; }
  if (scene !== so) EA.group.visible = true;
  cam.fov = fov; cam.near = 0.1; cam.far = 80000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(W("vierzig") - 0.2, tJetzt - 0.1, "❌ 40 Satelliten verloren"); seg(W("sechsunddreißig") - 0.2, tGest - 0.1, logo("amazon.svg", 60) + "36 Satelliten");
  seg(W("stoppte") - 0.1, tNeu - 0.1, "⏸️ Countdown gestoppt"); seg(tNeu, tFuer - 0.1, "🕛 heute, kurz vor 12 Uhr"); seg(W("über", 57) - 0.1, tUnd - 0.1, "🟠 Amazon  vs.  🔵 Starlink");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
