const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
const lerpLog = (a, b, f) => Math.exp(lerp(Math.log(a), Math.log(b), f));
K.reseed(41);
// @modelle
const sunT = await tex("sun.jpg"), merT = await tex("mercury.jpg");
// ================= Merkur-Nähe: Sonde, Merkur, Sonne =================
const sc = new THREE.Scene(); K.stars(sc, 9000, -1, 60000, 1.7).material.opacity = 0.7; sc.add(new THREE.AmbientLight(0x2c3040, 0.6));
const sunL = new THREE.DirectionalLight(0xfff0dc, 2.4); sunL.position.set(-1, 0.25, 0.35); sc.add(sunL);
const RM = 120; const MER = new THREE.Mesh(new THREE.SphereGeometry(RM, 160, 120), new THREE.MeshStandardMaterial({ map: merT, roughness: 1 })); sc.add(MER);
const heat = new THREE.Mesh(new THREE.SphereGeometry(RM * 1.004, 96, 64), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { sun: { value: V(-1, 0.25, 0.35).normalize() }, hot: { value: 0 }, cold: { value: 0 } },
  vertexShader: `varying vec3 vN;void main(){vN=normalize((modelMatrix*vec4(normal,0.)).xyz);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform vec3 sun;uniform float hot,cold;varying vec3 vN;void main(){float d=dot(vN,sun);vec3 c=vec3(1.,.35,.05)*hot*smoothstep(.0,.9,d)*.9+vec3(.25,.55,1.)*cold*smoothstep(.05,-.6,d)*.05;gl_FragColor=vec4(c,1.);}` })); sc.add(heat);
const sunS = K.sprite(sc, K.glowTex("rgba(255,230,180,1)"), 5200, V(-9000, 2250, 3150), 1);
const BC = MO.bepi(); sc.add(BC.g); const bcO = new THREE.Object3D(); BC.g.add(bcO); bcO.position.set(0, 5, 0);
const orb = new THREE.Mesh(new THREE.TorusGeometry(RM * 1.9, 0.5, 8, 256), new THREE.MeshBasicMaterial({ color: 0x7fd0ff, transparent: true, opacity: 0, toneMapped: false })); orb.rotation.x = Math.PI / 2 - 0.25; sc.add(orb);
const orb2 = new THREE.Mesh(new THREE.TorusGeometry(RM * 3.2, 0.6, 8, 256), new THREE.MeshBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); orb2.rotation.x = Math.PI / 2 - 0.25; sc.add(orb2);
// Magnetfeld-Linien
const field = new THREE.Group(); sc.add(field); for (let i = 0; i < 10; i++) { const pts = []; const L = 1.6 + (i % 5) * 0.45; for (let k = 0; k <= 80; k++) { const th = (k / 80) * Math.PI; const r = RM * L * Math.sin(th) ** 2; if (r < RM * 1.02 && k > 2 && k < 78) continue; pts.push(V(r * Math.sin(th), r * Math.cos(th) + RM * 0.2, 0)); }
  const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0x9fd8ff, transparent: true, opacity: 0, toneMapped: false })); l.rotation.y = (i / 10) * Math.PI * 2; field.add(l); }
// ================= Sonnensystem-Schema =================
const ss = new THREE.Scene(); K.stars(ss, 6000, -1, 60000, 1.6).material.opacity = 0.5;
const sun2 = new THREE.Mesh(new THREE.SphereGeometry(14, 96, 64), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(1.3, 1.0, 0.72), toneMapped: false })); ss.add(sun2); K.sprite(ss, K.glowTex("rgba(255,170,70,.6)"), 70, V(0, 0, 0), 0.8);
const ring = (r, col, th = 0.35) => { const m = new THREE.Mesh(new THREE.TorusGeometry(r, th, 8, 256), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, toneMapped: false })); m.rotation.x = Math.PI / 2; ss.add(m); return m; };
const PL = [["Merkur", 39, 0xb8b8b8, "rgba(210,210,210,1)"], ["Venus", 72, 0xffd9a0, "rgba(255,220,170,1)"], ["Erde", 100, 0x7fd0ff, "rgba(120,200,255,1)"]].map(([n, r, c, g], i) => { const o = ring(r, c); const d = K.sprite(ss, K.glowTex(g), 9, V(r, 0, 0), 0); const O = new THREE.Object3D(); ss.add(O); return { n, r, o, d, O, a: 1 + i * 2 }; });
const pluto = ring(3950, 0xc8a8ff, 4); const plD = K.sprite(ss, K.glowTex("rgba(200,170,255,1)"), 60, V(0, 0, 3950), 0); const plO = new THREE.Object3D(); plO.position.set(0, 0, 3950); ss.add(plO);
const path = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0, toneMapped: false })); ss.add(path);
const spiral = []; for (let k = 0; k <= 600; k++) { const f = k / 600; const a = f * Math.PI * 2 * 4.5; const r = lerp(100, 39, Math.pow(f, 0.8)) * (1 + 0.12 * Math.sin(a * 0.5)); spiral.push(V(Math.cos(a) * r, 0, Math.sin(a) * r)); }
const probe2 = K.sprite(ss, K.glowTex("rgba(255,240,200,1)"), 7, V(0, 0, 0), 0);
const flyTxt = []; [[0.03, "Erde"], [0.18, "Venus"], [0.3, "Venus"], [0.45, "Merkur"], [0.55, "Merkur"], [0.65, "Merkur"], [0.75, "Merkur"], [0.85, "Merkur"], [0.95, "Merkur"]].forEach(([f]) => flyTxt.push(f));
// ===== Zeiten =====
const tDie = W("die", 3.5), tUnd = W("und", 10), tGeb = W("gebaut"), tGest = W("gestartet"), tProb = W("das", 21.3), tSonde = W("die", 26), tDafuer = W("dafür", 29.5), tEig = W("eigentlich"), tDoch = W("doch"), tMer = W("merkur", 44.3), tNacht = W("nachts"), tDez = W("im", 51.8), tApr = W("ab", 58), tZum = W("zum", 62.2), END = 66.8;
const KARTE = 14.25;
label("BepiColombo", bcO, 3, { t0: tDie + 0.5, t1: tUnd - 0.1, size: 54, gap: 22 }); label("Merkur", MER, RM, { t0: 4.5, t1: tUnd - 0.1, size: 56, gap: 24 });
PL.forEach((p) => label(p.n, p.O, 4, { t0: tUnd + 0.3, t1: tUnd + 1.4, size: 46, gap: 16 })); label("Pluto", plO, 40, { t0: tUnd + 1.6, t1: tGeb - 0.1, size: 50, gap: 18 });
const mpoO = new THREE.Object3D(); BC.mpo.add(mpoO); mpoO.position.set(0, -1.5, 0); const mioO = new THREE.Object3D(); BC.mio.add(mioO); mioO.position.set(0, 1, 0);
label("🇪🇺 MPO", mpoO, 1, { t0: W("einen", 54.5) + 0.2, t1: tApr - 0.1, size: 48, gap: 16 }); label("🇯🇵 Mio", mioO, 1, { t0: W("japanischen") - 0.2, t1: tApr - 0.1, size: 48, gap: 16 });
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
const nzOn = (p, t) => BC.nz.forEach((e) => { e.visible = p > 0.02; e.userData.mat.uniforms.t.value = t; e.userData.mat.uniforms.power.value = p; });
renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.3, 0.86);
  let scene = sc, pos = V(0, 0, 400), look = V(0, 0, 0), fov = 40; MER.rotation.y = t * 0.01; heat.material.uniforms.hot.value = 0; heat.material.uniforms.cold.value = 0;
  BC.g.position.set(0, 0, 0); BC.g.rotation.set(0, 0, 0); BC.mio.position.set(0, 3.3, 0); BC.shield.visible = true; nzOn(0, t); orb.material.opacity = 0; orb2.material.opacity = 0; field.children.forEach((l) => (l.material.opacity = 0));
  const onOrbit = (a, R, incl = 0.25) => V(Math.cos(a) * R, Math.sin(a) * R * Math.sin(incl) * 0, Math.sin(a) * R).applyAxisAngle(V(1, 0, 0), -incl);
  if (t < tDie - 0.05) { const f = prog(t, 0, tDie); BC.g.position.set(lerp(-60, -20, f), lerp(40, 10, f), RM * 2.4); BC.g.rotation.set(0.2, 0.6 + f * 0.3, -0.3); pos = BC.g.position.clone().add(V(lerp(11, 8, f), 2, lerp(10, 7, f))); look = BC.g.position.clone().add(V(-30, -20, -RM)); fov = 46; }
  else if (t < tUnd - 0.05) { const f = prog(t, tDie, tUnd - tDie); const a = lerp(2.6, 3.6, f); const p = onOrbit(a, RM * 1.9); BC.g.position.copy(p); BC.g.lookAt(onOrbit(a - 0.1, RM * 1.9)); BC.g.rotateX(Math.PI / 2); nzOn(f < 0.7 ? 1 : 0, t);
    orb.material.opacity = 0.7 * cl((t - tDie - 1) / 1); const c = p.clone().multiplyScalar(1.9); pos = c.add(V(0, 70, 0)); look = V(0, 0, 0); fov = 44; }
  else if (t < tGeb - 0.05) { scene = ss; const f = prog(t, tUnd, tGeb - tUnd); PL.forEach((p, i) => { p.o.material.opacity = 0.8; const a = p.a + t * 0.1 / (i + 1); const v = V(Math.cos(a) * p.r, 0, Math.sin(a) * p.r); p.d.position.copy(v); p.O.position.copy(v); p.d.material.opacity = 1; });
    pluto.material.opacity = 0.8 * cl((t - tUnd - 1.2) / 0.6); plD.material.opacity = pluto.material.opacity; const d = lerpLog(380, 12500, K.eio(cl((t - tUnd - 1) / 2.5))); pos = V(0, d * 0.95, d * 0.25); look = V(0, 0, 0); fov = 44; plD.scale.setScalar(Math.max(60, d * 0.03)); }
  else if (t < tProb - 0.05) { const f = prog(t, tGeb, tProb - tGeb); BC.g.position.set(0, 0, RM * 4); BC.g.rotation.set(0.3, t * 0.25, 0.2); pos = BC.g.position.clone().add(V(Math.sin(f) * 14, 4, 14)); look = BC.g.position.clone().add(V(0, 1.5, 0)); fov = 42; }
  else if (t < tDafuer - 0.05) { const f = prog(t, tProb, tDafuer - tProb); BC.g.position.set(lerp(300, 120, f), 20, RM * 3); BC.g.rotation.set(0, 0, Math.PI / 2 + 0.2); if (t > tSonde) nzOn(1, t);
    pos = BC.g.position.clone().add(V(13, 4, 16)); look = BC.g.position.clone().add(V(-6, 0, -3)); fov = 46; }
  else if (t < tEig - 0.05) { scene = ss; const f = prog(t, tDafuer, tEig - tDafuer - 0.3); PL.forEach((p, i) => { p.o.material.opacity = 0.7; const a = p.a + t * 0.1 / (i + 1); const v = V(Math.cos(a) * p.r, 0, Math.sin(a) * p.r); p.d.position.copy(v); p.O.position.copy(v); p.d.material.opacity = 1; });
    const n = Math.max(2, Math.floor(cl(f) * spiral.length)); path.geometry.setFromPoints(spiral.slice(0, n)); path.material.opacity = 0.95; probe2.position.copy(spiral[n - 1]); probe2.material.opacity = 1; pos = V(0, 260, 140); look = V(0, 0, 0); fov = 44; }
  else if (t < tMer - 0.05) { const f = prog(t, tEig, tMer - tEig); BC.g.position.set(0, 0, RM * 4); BC.g.rotation.set(0.2, 2 + t * 0.15, 0.4); if (t > tDoch) nzOn(Math.sin(t * 31) > 0.3 ? 0.4 : 0.05, t); pos = BC.g.position.clone().add(V(10, -4, 12)); look = BC.g.position.clone(); fov = 42; }
  else if (t < tDez - 0.05) { const f = prog(t, tMer, tDez - tMer); heat.material.uniforms.hot.value = 0.45 * cl((t - W("tagsüber") + 0.2) / 0.6); heat.material.uniforms.cold.value = cl((t - tNacht + 0.2) / 0.6); const day = t < tNacht - 0.3; const g = K.eio(cl((t - tNacht + 0.3) / 1.4)); pos = V(lerp(-RM * 1.6, RM * 2.4, g), 30, lerp(RM * 2.6, RM * 1.9, g)); look = V(0, 0, 0); fov = 44; if (day) pos = V(-RM * 1.6 - f * 30, 30, RM * 2.6); }
  else if (t < tApr - 0.05) { const f = prog(t, tDez, tApr - tDez); const k = K.eio(cl((t - W("teilt") - 0.3) / 2.5)); BC.g.position.set(0, 0, RM * 3); BC.g.rotation.set(0.15, 0.6, 0.1); BC.mio.position.y = 3.3 + k * 9; BC.shield.position.y = 1.4 + k * 4; pos = BC.g.position.clone().add(V(lerp(16, 22, f), 6, lerp(16, 22, f))); look = BC.g.position.clone().add(V(0, 5, 0)); fov = 44; }
  else { const f = prog(t, tApr, END - tApr); orb.material.opacity = 0.6; orb2.material.opacity = 0.6; const a1 = t * 0.5, a2 = t * 0.25 + 2; BC.shield.visible = false; BC.g.position.copy(onOrbit(a1, RM * 1.9)); BC.mio.position.copy(onOrbit(a2, RM * 3.2).sub(BC.g.position));
    if (t > tZum) field.children.forEach((l, i) => (l.material.opacity = 0.55 * cl((t - tZum - i * 0.08) / 0.6))); const d = lerp(720, 860, f); const a = 0.6 + f * 0.4; pos = V(Math.sin(a) * d, 160, Math.cos(a) * d); look = V(0, 0, 0); fov = 44; }
  cam.fov = fov; cam.near = 0.1; cam.far = 200000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(scene, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  const sub = (s) => `<div class='sub'>${s}</div>`;
  seg(tGeb, tGest - 0.1, logo("esa.svg", 70) + "+ Japan 🇯🇵");
  seg(W("einmal", 32.5) - 0.1, tEig - 0.1, "9 Vorbeiflüge" + sub("1× Erde · 2× Venus · 6× Merkur"));
  seg(W("tagsüber") - 0.1, tNacht - 0.1, "☀️ über 400 °C"); seg(tNacht, tDez - 0.1, "🌙 −180 °C");
  WORDEL.style.top = t >= KARTE && t < KARTE + 5.4 ? "300px" : "";
  word(wh, wa); cap(t);
};
