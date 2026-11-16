const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(8);
const sc = new THREE.Scene(); const bgStars = K.stars(sc, 9000, -1, 30000, 1.7); bgStars.material.opacity = 0.6;
sc.add(new THREE.AmbientLight(0x30303a, 0.6)); const fill = new THREE.DirectionalLight(0xdfe6ff, 1.2); sc.add(fill);
const sunTex = await tex("sun.jpg");
// Sonnenähnlicher Begleitstern (Mittelpunkt)
const RC = 30; const comp = new THREE.Mesh(new THREE.SphereGeometry(RC, 128, 96), new THREE.MeshBasicMaterial({ map: sunTex, color: new THREE.Color(1.3, 1.0, 0.68), toneMapped: false })); sc.add(comp);
const cg = K.sprite(sc, K.glowTex("rgba(255,170,70,.5)"), RC * 4, V(0, 0, 0), 0.75); const cl2 = new THREE.PointLight(0xfff0d8, 3, 0, 0); sc.add(cl2);
// Weißer Zwerg (ca. erdgroß), kreist um den Begleiter
const wdC = K.noiseCanvas(1024, 512, 6, 6, 0.5, 0.6); const wdTex = new THREE.CanvasTexture(wdC); wdTex.wrapS = wdTex.wrapT = THREE.RepeatWrapping; wdTex.colorSpace = THREE.SRGBColorSpace; const RW = 2; const wd = new THREE.Group(); sc.add(wd);
const wdM = new THREE.Mesh(new THREE.SphereGeometry(RW, 96, 64), new THREE.ShaderMaterial({ uniforms: { n: { value: wdTex } }, toneMapped: false,
  vertexShader: `varying vec2 vU;varying vec3 vN;varying vec3 vV;void main(){vU=uv;vN=normalize(mat3(modelMatrix)*normal);vec4 w=modelMatrix*vec4(position,1.);vV=normalize(cameraPosition-w.xyz);gl_Position=projectionMatrix*viewMatrix*w;}`,
  fragmentShader: `uniform sampler2D n;varying vec2 vU;varying vec3 vN;varying vec3 vV;void main(){float g=texture2D(n,vU*vec2(2.,2.)).r;float mu=clamp(dot(vN,vV),0.,1.);vec3 c=mix(vec3(.62,.74,1.),vec3(1.,1.,1.),smoothstep(.2,.9,g));c*=.55+.6*pow(mu,.6);gl_FragColor=vec4(c*1.15,1.);}` })); wd.add(wdM);
const wg1 = K.sprite(wd, K.glowTex("rgba(170,200,255,.75)"), RW * 4, V(0, 0, 0), 0.8), wg2 = K.sprite(wd, K.glowTex("rgba(120,160,255,.3)"), RW * 9, V(0, 0, 0), 0.35);
const ORB = 140; const orbit = new THREE.Mesh(new THREE.RingGeometry(ORB - 0.35, ORB + 0.35, 512), new THREE.MeshBasicMaterial({ color: 0xaab4d0, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false })); orbit.rotation.x = -Math.PI / 2; sc.add(orbit);
// Erde zum Größenvergleich (klein, neben dem Zwerg)
const dayT = new THREE.Texture(day); dayT.colorSpace = THREE.SRGBColorSpace; dayT.needsUpdate = true;
const mini = new THREE.Mesh(new THREE.SphereGeometry(RW, 96, 64), new THREE.MeshStandardMaterial({ map: dayT, emissiveMap: dayT, emissive: 0xffffff, emissiveIntensity: 0.55, roughness: 1 })); sc.add(mini);
// Funkpulse (Ringe)
const rings = []; for (let i = 0; i < 5; i++) { const m = new THREE.Mesh(new THREE.RingGeometry(0.988, 1, 200), new THREE.MeshBasicMaterial({ color: 0x8fd8ff, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); sc.add(m); rings.push(m); }
// Magnetfeldlinien (Dipol) um den Zwerg
const FL = []; for (let i = 0; i < 12; i++) { const L = i < 6 ? 3.2 : 6; const ph = (i % 6) * (Math.PI / 3) + (i < 6 ? 0 : 0.5); const pts = []; for (let k = 0; k <= 80; k++) { const th = 0.12 + (k / 80) * (Math.PI - 0.24); const r = L * Math.sin(th) ** 2; if (r < RW * 0.98) continue; pts.push(V(r * Math.sin(th) * Math.cos(ph), r * Math.cos(th), r * Math.sin(th) * Math.sin(ph))); }
  const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, toneMapped: false })); wd.add(l); FL.push(l); }
// Ausbruch + Gasbogen auf dem Begleiter
const arc = new THREE.Mesh(new THREE.TorusGeometry(7, 1.3, 24, 96, Math.PI), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.6, 0.55, 0.18), toneMapped: false, transparent: true, opacity: 0, depthWrite: false })); sc.add(arc);
const arcG = K.sprite(sc, K.glowTex("rgba(255,110,40,.7)"), 40, V(0, 0, 0), 0); const flareG = K.sprite(sc, K.glowTex("rgba(255,240,200,1)"), 30, V(0, 0, 0), 0);
// Erde (Australien) weit weg
const EP = V(0, 0, 12000); const EA = K.earth(sc, { day, night, topo }, 10); EA.group.position.copy(EP); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93);
const mwa = K.sprite(sc, K.glowTex("rgba(255,210,80,1)"), 1.4, V(0, 0, 0), 0); const mwaO = new THREE.Object3D(); sc.add(mwaO);

// ===== Zeiten =====
const tEnt = W("entdeckt"), tDas = W("das", 13.5), tDie = W("die", 17.3), tEr = W("er", 21.8), tAberM = W("aber", 23.7), tEin = W("ein", 25.9), tUnd = W("und", 29), tSo = W("so", 34.4), tDieF = W("die", 39.9), tDabei = W("dabei"), tUnd2 = W("und", 46.7), tAber = W("aber", 50.4), tVerm = W("vermutlich"), tNein = W("und", 58.2), tDieS = W("die", 62), tWas = W("was", 65.8), tFolg = W("folg", 70.4);
label("Murchison Widefield Array<small>Westaustralien</small>", mwaO, 0, { t0: tEnt + 1.2, t1: tDas - 0.1, size: 52, gap: 40 });
label("Weißer Zwerg", wd, RW, { t0: tDie + 0.4, t1: tEin - 0.1, size: 58, gap: 30 }); label("Erde", mini, RW, { t0: tEr - 0.1, t1: tEin - 0.1, size: 58, gap: 30 });
label("Weißer Zwerg", wd, RW, { t0: tUnd + 0.8, t1: tSo - 0.1, size: 50, gap: 24 }); label("sonnenähnlicher Stern", comp, RC, { t0: W("kreist") + 0.2, t1: tSo - 0.1, size: 54, gap: 24 });
label("Gasbogen", arc, 8, { t0: W("bogen") - 0.3, t1: tAber - 0.1, size: 56, gap: 20 });

renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.45, 0.8);
  const wa = 0.6 + t * 0.012; wd.position.set(Math.cos(wa) * ORB, 0, Math.sin(wa) * ORB); wdM.rotation.y = t * 0.8; comp.rotation.y = t * 0.03;
  mini.visible = false; orbit.material.opacity = 0; FL.forEach((l) => (l.material.opacity = 0)); arc.material.opacity = 0; arcG.material.opacity = 0; flareG.material.opacity = 0; mwa.material.opacity = 0;
  const W0 = wd.position.clone(); const near = (t >= tDie - 0.05 && t < tUnd - 0.05) || (t >= tAber - 0.05 && t < tNein - 0.05) || t < tEnt - 0.05; if (near) E.look([1, 1, 1], [0, 0, 0], 0.22, 0.92); let pos, look = W0.clone(), fov = 40, rOn = 0, rMax = 40;
  if (t < tEnt - 0.05) { const f = K.eio(prog(t, 0, tEnt)); const a = 2.2 + t * 0.05; const d = lerp(70, 22, f); pos = W0.clone().add(V(Math.sin(a) * d, lerp(10, 3, f), Math.cos(a) * d)); rOn = 1; }
  else if (t < tDas - 0.05) { // Erde, Australien
    EA.group.rotation.y = 0; const site = EA.ll(-26.7, 116.7, 10); const n = site.clone().sub(EP).normalize(); EA.U.sun.value.copy(n).add(V(0.3, 0.4, 0)).normalize();
    mwa.position.copy(EP.clone().add(n.clone().multiplyScalar(10.2))); mwa.material.opacity = 0.6 + 0.4 * Math.sin(t * 6); mwaO.position.copy(mwa.position);
    const f = K.eio(prog(t, tEnt, tDas - tEnt)); pos = EP.clone().add(n.clone().multiplyScalar(lerp(48, 30, f))).add(V(0, lerp(-6, -2, f), 0)); look = EP.clone().add(n.clone().multiplyScalar(4)); }
  else if (t < tDie - 0.05) { const f = K.eio(prog(t, tDas, tDie - tDas)); const d = lerp(60, 5000, f); pos = W0.clone().add(V(d * 0.25, d * 0.15, d)); look = W0.clone().multiplyScalar(lerp(1, 0.5, f)); rOn = 1 - f; }
  else if (t < tEin - 0.05) { mini.visible = t > tEr - 0.2; mini.position.copy(W0).add(V(-5.5, 0, 1.5)); mini.rotation.y = t * 0.3; const f = K.eio(prog(t, tDie, 2)); const sh = K.eio(cl((t - tEr + 0.5) / 1)); pos = W0.clone().add(V(lerp(-6, -2.75, f) - 0 * sh, 1, lerp(30, 17, f) + 9 * sh)); look = W0.clone().add(V(-2.75 * sh, 0, 0)); }
  else if (t < tUnd - 0.05) { const f = prog(t, tEin, tUnd - tEin); const a = 0.4 + f * 0.5; pos = W0.clone().add(V(Math.sin(a) * lerp(11, 8.5, f), 1.2, Math.cos(a) * lerp(11, 8.5, f))); look = W0.clone().add(V(0, 0.6, 0)); }
  else if (t < tSo - 0.05) { orbit.material.opacity = 0.28 * cl((t - tUnd - 0.6) / 0.8); const f = K.eio(prog(t, tUnd, 3)); pos = W0.clone().multiplyScalar(lerp(1, 0.5, f)).add(V(lerp(20, 60, f), lerp(6, 210, f), lerp(30, 200, f))); look = W0.clone().multiplyScalar(lerp(1, 0.5, f)); }
  else if (t < tDieF - 0.05) { orbit.material.opacity = 0.2; rOn = 1; rMax = 120; const a = 0.9 + (t - tSo) * 0.05; pos = V(Math.sin(a) * 300, 90, Math.cos(a) * 300); look = W0.clone().multiplyScalar(0.55); }
  else if (t < tDabei - 0.05) { orbit.material.opacity = 0.15; rOn = 0.7; rMax = 90; const a = 1.25 + (t - tDieF) * 0.04; pos = V(Math.sin(a) * 260, 40, Math.cos(a) * 260); look = W0.clone().multiplyScalar(0.45); }
  else if (t < tAber - 0.05) { // Begleiter: Ausbrüche + Gasbogen
    const f = K.eio(prog(t, tDabei, 2)); const a = 0.3 + (t - tDabei) * 0.03; const d = lerp(190, 135, f); pos = V(Math.sin(a) * d, 20, Math.cos(a) * d); look = V(0, 8, 0);
    const cd = V(Math.sin(a), 0, Math.cos(a)); const side = V(Math.cos(a), 0, -Math.sin(a));
    const dir = side.clone().multiplyScalar(0.75).add(V(0, 0.55, 0)).add(cd.clone().multiplyScalar(0.25)).normalize(); const fx = prog(t, tDabei + 0.9, 0.9); flareG.position.copy(dir.clone().multiplyScalar(RC + 2)); flareG.material.opacity = Math.sin(Math.PI * fx) * 0.9; flareG.scale.setScalar(20 + 30 * fx);
    if (t > tDabei + 1.0 && t < tDabei + 1.25) E.grade.uniforms.flash.value = 0.18;
    const fa = K.eout(prog(t, tUnd2 + 0.4, 1.8)); const ad = side.clone().multiplyScalar(-0.35).add(V(0, 1, 0)).add(cd.clone().multiplyScalar(0.15)).normalize(); arc.position.copy(ad.clone().multiplyScalar(RC - 0.8)); arc.up.copy(ad); arc.lookAt(arc.position.clone().add(cd)); arc.scale.setScalar(0.3 + 1.0 * fa); arc.material.opacity = fa > 0 ? 1 : 0;
    arcG.position.copy(ad.clone().multiplyScalar(RC + 5)); arcG.material.opacity = fa * 0.5;
    E.look([1, 1, 1], [0, 0, 0], 0.35, 0.85); }
  else if (t < tNein - 0.05) { const on = cl((t - tVerm + 0.3) / 0.8); FL.forEach((l, i) => (l.material.opacity = on * (0.55 + 0.3 * Math.sin(t * 4 + i)))); rOn = 1; rMax = 30; const a = 1.0 + (t - tAber) * 0.06; const d = lerp(30, 20, K.eio(prog(t, tAber, 3))); pos = W0.clone().add(V(Math.sin(a) * d, 4, Math.cos(a) * d)); }
  else if (t < tWas - 0.05) { const f = prog(t, tNein, tWas - tNein); orbit.material.opacity = 0.15; const a = 1.8 + f * 0.3; pos = V(Math.sin(a) * 340, lerp(60, 120, f), Math.cos(a) * 340); look = W0.clone().multiplyScalar(0.5); rOn = 0.6; rMax = 100; }
  else { orbit.material.opacity = 0.2; rOn = 1; rMax = 120; const f = prog(t, tWas, 7); const a = 2.1 + f * 0.3; pos = V(Math.sin(a) * lerp(260, 380, f), lerp(70, 140, f), Math.cos(a) * lerp(260, 380, f)); look = W0.clone().multiplyScalar(0.5); }
  cam.fov = fov; cam.near = 0.05; cam.far = 60000; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look); fill.position.copy(cam.position);
  // Funkpulse vom Zwerg (Takt im Video stark verkürzt)
  rings.forEach((m, i) => { const ph = (t * 0.5 + i / rings.length) % 1; m.scale.setScalar(RW * 1.2 + ph * rMax); m.position.copy(W0); m.lookAt(cam.position); m.material.opacity = rOn * (1 - ph) * 0.6; });
  const beat = Math.pow(Math.max(0, Math.sin(t * Math.PI)), 12); wg1.material.opacity = 0.7 + 0.3 * beat; wg2.material.opacity = 0.25 + 0.25 * beat;
  arc.visible = arc.material.opacity > 0; E.render(sc, t); updLabels(t);
  let wh = "", wa2 = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa2 = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("fünftausend") - 0.2, tDie - 0.1, "> 5.000 Lichtjahre");
  seg(tDie + 0.2, tEr - 0.1, "ausgebrannter Stern"); seg(tEr + 0.3, tAberM - 0.1, "= so groß wie die Erde"); seg(tAberM, tEin - 0.1, "> ½ Sonnenmasse");
  seg(tEin, tUnd - 0.1, "🥄 1 Teelöffel<div class='sub'>≈ mehrere Tonnen</div>");
  seg(W("erste", 38) - 0.2, tDieF - 0.1, "das erste seiner Art"); seg(tDieF + 0.2, tDabei - 0.1, "> 100 Stunden<div class='sub'>Messdaten</div>");
  seg(W("ausbrüche") - 0.1, tUnd2 - 0.1, "Ausbrüche");
  seg(tAber + 0.3, tVerm - 0.1, "Warum? 🤔"); seg(tVerm, tNein - 0.1, "Magnetfelder?");
  seg(W("aliens") - 0.1, tDieS - 0.1, "👽 Aliens? Nein.<div class='sub'>natürliches Signal</div>");
  seg(tDieS + 0.2, tWas - 0.1, "Nature Astronomy<div class='sub'>Fachzeitschrift, Nov. 2026</div>");
  word(wh, wa2); cap(t);
};
