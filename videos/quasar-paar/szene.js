const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
K.reseed(77);
const sc = new THREE.Scene(); K.stars(sc, 8000, -1, 30000, 1.7).material.opacity = 0.55;
// Quasar = Schwarzes Loch + glühende Gasscheibe + Kernlicht + Wirtsgalaxie
const diskMat = (hot) => new THREE.ShaderMaterial({ uniforms: { time: { value: 0 }, bright: { value: 1 }, hot: { value: hot } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec2 vP;void main(){vP=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform float time,bright,hot;varying vec2 vP;void main(){float r=length(vP);float a=atan(vP.y,vP.x);float k=(r-3.6)/9.4;
    float sw=.55+.45*sin(a*7.-r*1.7+time*2.2)*sin(a*3.+r*.9-time*1.3);vec3 c=mix(vec3(1.,.97,.92),mix(vec3(1.,.55,.2),vec3(.6,.75,1.),hot),smoothstep(0.,.45,k));c=mix(c,mix(vec3(.6,.12,.05),vec3(.25,.3,.8),hot),smoothstep(.45,1.,k));
    float al=(1.-smoothstep(.0,1.,k))*(.55+.45*sw)*smoothstep(0.,.04,k);gl_FragColor=vec4(c*al*bright*1.5,al);}` });
const galTex = K.glowTex("rgba(150,170,255,.5)");
function quasar(s, hot, seed) { const g = new THREE.Group();
  const bh = new THREE.Mesh(new THREE.SphereGeometry(3, 48, 32), new THREE.MeshBasicMaterial({ color: 0x000000 })); g.add(bh);
  const dm = diskMat(hot); const disk = new THREE.Mesh(new THREE.RingGeometry(3.6, 13, 160, 4), dm); disk.rotation.x = -1.2; g.add(disk);
  const core = K.sprite(g, K.glowTex("rgba(230,240,255,.95)"), 14, V(0, 0, 0), 0.7); const halo = K.sprite(g, K.glowTex("rgba(140,170,255,.35)"), 60, V(0, 0, 0), 0.35);
  K.reseed(seed); const pts = []; for (let i = 0; i < 9000; i++) { const arm = i % 2, r = Math.pow(K.rnd(), 0.6) * 90, a = r * 0.05 + arm * Math.PI + (K.rnd() - 0.5) * 0.9; pts.push(Math.cos(a) * r, (K.rnd() - 0.5) * 4, Math.sin(a) * r); }
  const gg = new THREE.BufferGeometry(); gg.setAttribute("position", new THREE.Float32BufferAttribute(pts, 3));
  const gal = new THREE.Points(gg, new THREE.PointsMaterial({ color: 0x9fb0ff, size: 1.5, sizeAttenuation: false, transparent: true, opacity: 0.35, blending: THREE.AdditiveBlending, depthWrite: false })); gal.rotation.x = -1.2; g.add(gal);
  g.scale.setScalar(s); sc.add(g); return { g, dm, core, halo, gal, disk }; }
const Q1 = quasar(1.0, 0.0, 3), Q2 = quasar(0.62, 0.5, 9);
const sep = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(1, 0, 0)]), new THREE.LineDashedMaterial({ color: 0xffffff, dashSize: 3, gapSize: 2.4, transparent: true, opacity: 0 })); sc.add(sep);
const flash = K.sprite(sc, K.glowTex("rgba(255,255,255,1)"), 70, V(0, 0, 0), 0);

const mid = new THREE.Object3D(); sc.add(mid);
const tEs = W("es", 9), tWir = W("wir", 13), tIhr = W("ihr", 18), tAelt = W("älteste"), tEnt = W("entdeckt", 26), tBeide = W("beide"), tSolche = W("solche"), tGr = W("größere"), tKl = W("kleinere"), tZw = W("zwischen"), tFuenf = W("fünftel"), tRaet = W("rätsel"), tUnd = W("und", 57.5), tWas = W("was", 60.8), tFolg = W("folg", 64);
label("2 Schwarze Löcher", mid, 0, { t0: tEs + 0.8, t1: tWir - 0.1, size: 60, gap: 150 });
label("1,5 Mrd. Sonnen", Q1.g, 14, { t0: tGr + 1.6, t1: tZw - 0.1, size: 60, gap: 20 }); label("400 Mio. Sonnen", Q2.g, 9, { t0: tKl + 0.7, t1: tZw - 0.1, size: 52, gap: 20 });
label("18.000 Lichtjahre", mid, 0, { t0: tZw + 1.2, t1: tRaet - 0.1, size: 56, gap: 30 });

renderAt = (t) => {
  E.grade.uniforms.flash.value = 0; E.look([1, 1, 1], [0, 0, 0], 0.35, 0.86); flash.material.opacity = 0; sep.material.opacity = 0;
  // Paar umkreist sich, am Ende Verschmelzung
  const merge = K.eio(prog(t, tUnd + 0.3, 2.6)); const half = lerp(30, 0.01, merge); const a = t * 0.08 + merge * 6;
  Q1.g.position.set(Math.cos(a) * half, 0, Math.sin(a) * half); Q2.g.position.set(-Math.cos(a) * half, 0, -Math.sin(a) * half);
  [Q1, Q2].forEach((q, i) => { q.dm.uniforms.time.value = t * (1 + i * 0.3); q.disk.rotation.z = t * 0.2; q.gal.rotation.y = t * 0.02; });
  if (t > tUnd + 2.7 && t < tUnd + 3.4) { const f = prog(t, tUnd + 2.7, 0.7); flash.material.opacity = 0.7 * Math.sin(f * Math.PI); }
  mid.position.copy(Q1.g.position).lerp(Q2.g.position, 0.5);
  let pos, look = V(0, 0, 0), fov = 40;
  if (t < tEs - 0.05) { const f = K.eio(prog(t, 0, tEs)); pos = V(lerp(40, 10, f), lerp(60, 25, f), lerp(420, 150, f)); }
  else if (t < tWir - 0.05) { const b = 0.3 + (t - tEs) * 0.05; pos = V(Math.sin(b) * 140, 30, Math.cos(b) * 140); }
  else if (t < tAelt - 0.05) { const f = K.eio(prog(t, tWir, 3)); pos = V(0, lerp(30, 120, f), lerp(140, 900, f)); }
  else if (t < tBeide - 0.05) { const b = 0.8 + (t - tAelt) * 0.04; pos = V(Math.sin(b) * 220, 60, Math.cos(b) * 220); }
  else if (t < tGr - 0.05) { const f = K.eio(prog(t, tBeide, 1.6)); const c = Q1.g.position; pos = c.clone().add(V(lerp(60, 18, f), lerp(40, 10, f), lerp(120, 42, f))); look = c.clone(); E.look([1, 1, 1], [0, 0, 0], 0.4, 0.86); }
  else if (t < tZw - 0.05) { const b = 0.2 + (t - tGr) * 0.05; pos = V(Math.sin(b) * 225, 50, Math.cos(b) * 225); }
  else if (t < tRaet - 0.05) { sep.material.opacity = 0.7 * cl((t - tZw - 0.3) / 0.5); const P = sep.geometry.attributes.position; P.setXYZ(0, ...Q1.g.position.toArray()); P.setXYZ(1, ...Q2.g.position.toArray()); P.needsUpdate = true; sep.computeLineDistances();
    pos = V(0, 150, 110); }
  else if (t < tUnd - 0.05) { const b = 1.2 + (t - tRaet) * 0.06; pos = V(Math.sin(b) * 170, 70, Math.cos(b) * 170); }
  else { const f = prog(t, tUnd, 7); pos = V(lerp(30, -20, f), lerp(60, 40, f), lerp(170, 230, f)); }
  cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(pos); cam.lookAt(look);
  E.render(sc, t); updLabels(t);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(W("neunhundert") - 0.2, tIhr - 0.1, "900 Mio. Jahre<div class='sub'>nach dem Urknall</div>");
  seg(W("dreizehn") - 0.2, tAelt - 0.1, "≈ 13 Mrd. Jahre<div class='sub'>war das Licht unterwegs</div>");
  seg(tAelt, tEnt - 0.1, "🏆 ältestes Paar");
  seg(tEnt, tBeide - 0.1, "<img src='assets/logos/nasa.svg' style='width:220px;height:110px;object-fit:contain;background:#fff;border-radius:18px;padding:12px 24px;vertical-align:middle'><div class='sub'>James Webb + Gemini (Hawaii)</div>");
  seg(tBeide + 1.2, tSolche - 0.1, "heller als<br>ganze Galaxien"); seg(tSolche, tGr - 0.1, "= Quasar");
  seg(tFuenf - 0.2, tRaet - 0.1, "= ⅕ Milchstraße"); seg(tRaet, tUnd - 0.1, "zu früh – zu groß?!"); seg(tUnd + 0.3, tWas - 0.1, "💥 Verschmelzung");
  word(wh, wa); cap(t);
};
