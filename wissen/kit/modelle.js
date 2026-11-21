// ===== Modelle (Nutzer 19.11.: „schönere 3D-Modelle“, keine echten Fotos) =====
// In szene.js eine Zeile "// @modelle" -> sauber_bau.py setzt diesen Code ein. Braucht THREE, E (Renderer), K.
// MO.vulcan(), MO.ariane6(), MO.falcon9(), MO.longMarch2F(), MO.pad(), MO.tiangong(), MO.shenzhou(), MO.iss(), MO.hayabusa2(), MO.asteroid({r,seed,top,stretch}), MO.flagTex('cn'|'pk'), MO.bepi(), MO.jwst(), MO.exhaust(len, rad, col), MO.smoke(scene, n), MO.kuiper(), MO.panelTex(...)
const MO = {};
{
  const { RoomEnvironment } = await import("three/addons/environments/RoomEnvironment.js");
  const pmM = new THREE.PMREMGenerator(E.R); MO.env = pmM.fromScene(new RoomEnvironment(), 0.04).texture;
  // Kiste mit abgerundeten Kanten (Extrude mit Fase)
  const RoundedBoxGeometry = function (w, h, d, _s = 2, r = 0.02) { const sh = new THREE.Shape(), x = -w / 2 + r, y = -h / 2 + r, W2 = w - 2 * r, H2 = h - 2 * r; sh.moveTo(x, y); sh.lineTo(x + W2, y); sh.lineTo(x + W2, y + H2); sh.lineTo(x, y + H2); sh.lineTo(x, y);
    const g = new THREE.ExtrudeGeometry(sh, { depth: Math.max(0.001, d - 2 * r), bevelEnabled: true, bevelThickness: r, bevelSize: r, bevelSegments: 3, curveSegments: 4 }); g.translate(0, 0, -(d - 2 * r) / 2); g.computeVertexNormals(); return g; };
  MO.RBox = RoundedBoxGeometry;
  let sd = 7; const rr = () => ((sd = (sd * 16807) % 2147483647) / 2147483647);
  // Fläche mit Rauschen, Nähten, Schrift -> {map, bump}
  MO.panelTex = (o = {}) => {
    const w = o.w ?? 1024, h = o.h ?? 2048, cv = document.createElement("canvas"); cv.width = w; cv.height = h; const g = cv.getContext("2d");
    const bv = document.createElement("canvas"); bv.width = w; bv.height = h; const b = bv.getContext("2d");
    g.fillStyle = o.base ?? "#c9ccd1"; g.fillRect(0, 0, w, h); b.fillStyle = "#808080"; b.fillRect(0, 0, w, h);
    // Fleckiges Rauschen (Schaum / Lack)
    const n = o.mottle ?? 0.05; for (let i = 0; i < (o.spots ?? 3500); i++) { const x = rr() * w, y = rr() * h, r = 2 + rr() * (o.spotR ?? 14), v = rr() < 0.5 ? 0 : 255;
      g.fillStyle = `rgba(${v},${v},${v},${n * rr()})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); b.fillStyle = `rgba(${v},${v},${v},${0.25 * rr()})`; b.beginPath(); b.arc(x, y, r * 0.6, 0, 7); b.fill(); }
    // Nähte
    g.strokeStyle = o.seam ?? "rgba(0,0,0,.22)"; b.strokeStyle = "#3a3a3a";
    for (const y of o.rings ?? []) { const yy = h - y * h; g.lineWidth = 3; g.beginPath(); g.moveTo(0, yy); g.lineTo(w, yy); g.stroke(); b.lineWidth = 4; b.beginPath(); b.moveTo(0, yy); b.lineTo(w, yy); b.stroke(); }
    for (let i = 0; i < (o.vseams ?? 0); i++) { const x = (i + 0.5) / o.vseams * w; g.lineWidth = 2; g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); b.lineWidth = 3; b.beginPath(); b.moveTo(x, 0); b.lineTo(x, h); b.stroke(); }
    // Rippen (Zwischenstufe)
    if (o.ribs) for (let i = 0; i < o.ribs; i++) { const x = (i / o.ribs) * w; g.fillStyle = "rgba(255,255,255,.05)"; g.fillRect(x, 0, w / o.ribs * 0.35, h); b.fillStyle = "#b0b0b0"; b.fillRect(x, 0, w / o.ribs * 0.35, h); }
    // Bänder
    for (const [y0, y1, col] of o.bands ?? []) { g.fillStyle = col; g.fillRect(0, h - y1 * h, w, (y1 - y0) * h); }
    // Senkrechte Schrift (u = Position um den Umfang 0..1, v = Höhe 0..1)
    for (const L of o.text ?? []) { g.save(); g.translate(L.u * w, h - L.v * h); g.rotate(-Math.PI / 2); g.fillStyle = L.col ?? "#fff"; g.font = `900 ${L.size}px "Inter Display", Inter, sans-serif`; g.textAlign = "center"; g.textBaseline = "middle";
      if (L.spacing) g.letterSpacing = L.spacing + "px"; g.fillText(L.s, 0, 0); g.restore(); }
    // Flaggen
    for (const F of o.flags ?? []) { const fw = F.w * w, fh = F.h * h, x0 = F.u * w - fw / 2, y0 = h - F.v * h - fh / 2; g.save(); g.translate(x0 + fw / 2, y0 + fh / 2); g.rotate(-Math.PI / 2); const W2 = fh, H2 = fw;
      if (F.k === "us") { for (let i = 0; i < 13; i++) { g.fillStyle = i % 2 ? "#fff" : "#b22234"; g.fillRect(-W2 / 2, -H2 / 2 + (i * H2) / 13, W2, H2 / 13 + 1); } g.fillStyle = "#3c3b6e"; g.fillRect(-W2 / 2, -H2 / 2, W2 * 0.4, H2 * 7 / 13); }
      if (F.k === "eu") { g.fillStyle = "#003399"; g.fillRect(-W2 / 2, -H2 / 2, W2, H2); g.fillStyle = "#ffcc00"; for (let i = 0; i < 12; i++) { const a = (i / 12) * 6.283; g.beginPath(); g.arc(Math.cos(a) * H2 * 0.33, Math.sin(a) * H2 * 0.33, H2 * 0.04, 0, 7); g.fill(); } }
      g.restore(); }
    // Schmutz unten (Ruß)
    if (o.soot) { const gr = g.createLinearGradient(0, h, 0, h - o.soot * h); gr.addColorStop(0, "rgba(30,20,15,.55)"); gr.addColorStop(1, "rgba(30,20,15,0)"); g.fillStyle = gr; g.fillRect(0, h - o.soot * h, w, o.soot * h); }
    const map = new THREE.CanvasTexture(cv); map.colorSpace = THREE.SRGBColorSpace; map.anisotropy = 8; const bump = new THREE.CanvasTexture(bv); return { map, bump };
  };
  MO.mat = (tex, o = {}) => new THREE.MeshStandardMaterial({ map: tex?.map, bumpMap: tex?.bump, bumpScale: o.bumpScale ?? 0.6, color: o.color ?? 0xffffff, metalness: o.metal ?? 0.05, roughness: o.rough ?? 0.55, envMap: MO.env, envMapIntensity: o.ei ?? 0.35, side: o.side ?? THREE.FrontSide, ...(o.extra ?? {}) });
  MO.plain = (col, metal = 0.2, rough = 0.5, ei = 0.4, extra = {}) => new THREE.MeshStandardMaterial({ color: col, metalness: metal, roughness: rough, envMap: MO.env, envMapIntensity: ei, ...extra });
  const SEG = 96;
  const cyl = (r, h, mat, y, open = false) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, SEG, 1, open), mat); m.position.y = y + h / 2; return m; };
  // Ogive (Spitze): Profilpunkte von r bis 0 über Höhe h
  const ogive = (r, h, n = 40, blunt = 0.06) => { const pts = []; for (let i = 0; i <= n; i++) { const f = i / n; const rad = r * Math.sqrt(Math.max(0, 1 - Math.pow(f, 1.9))) * (1 - blunt) + r * blunt * (1 - f); pts.push(new THREE.Vector2(Math.max(0.001, rad * (f < 1 ? 1 : 0)), f * h)); } return pts; };
  const lathe = (pts, mat, phi0 = 0, phi = Math.PI * 2) => new THREE.Mesh(new THREE.LatheGeometry(pts, SEG, phi0, phi), mat);
  // Düse (Glocke)
  MO.nozzle = (r0, r1, h, mat) => { const pts = []; for (let i = 0; i <= 20; i++) { const f = i / 20; pts.push(new THREE.Vector2(r0 + (r1 - r0) * Math.pow(f, 0.6), -f * h)); } const m = lathe(pts, mat); m.material.side = THREE.DoubleSide; return m; };
  const nozM = () => MO.plain(0x3a3330, 0.85, 0.38, 0.6, { side: THREE.DoubleSide });
  // ---------- Abgasstrahl (Shader) ----------
  MO.exhaust = (len, rad, hot = [1, 0.95, 0.85], warm = [1, 0.55, 0.18]) => {
    const geo = new THREE.CylinderGeometry(rad * 0.55, rad * 1.6, len, 48, 24, true); geo.translate(0, -len / 2, 0);
    const mat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false,
      uniforms: { t: { value: 0 }, power: { value: 1 }, len: { value: len }, hot: { value: new THREE.Vector3(...hot) }, warm: { value: new THREE.Vector3(...warm) } },
      vertexShader: `varying vec2 vU; varying vec3 vN; varying vec3 vV; void main(){ vU = uv; vec4 mv = modelViewMatrix * vec4(position,1.); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
      fragmentShader: `uniform float t; uniform float power; uniform vec3 hot; uniform vec3 warm; varying vec2 vU; varying vec3 vN; varying vec3 vV;
        float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898,78.233)))*43758.5453); }
        float n(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x), mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x), f.y); }
        void main(){ float y = 1.-vU.y; float rim = abs(dot(vN, vV)); float core = pow(rim, 1.1);
          float fl = n(vec2(vU.x*12., y*8. - t*22.)) * .5 + n(vec2(vU.x*30., y*20. - t*40.)) * .5;
          float diam = .75 + .25*sin(y*60. - t*3.);
          float fade = pow(1.-y, 1.4) * smoothstep(0., .04, y + .02);
          vec3 c = mix(warm, hot, pow(core, 4.) * pow(1.-y, 3.));
          float a = core * fade * (0.55 + .45*fl) * diam * power;
          gl_FragColor = vec4(c * a * 1.9, a); }` });
    const m = new THREE.Mesh(geo, mat); m.renderOrder = 5; m.userData.mat = mat; return m;
  };
  // ---------- Rauch (weiche Wolken) ----------
  const smokeTexC = (() => { const s = 256, c = document.createElement("canvas"); c.width = c.height = s; const g = c.getContext("2d"); for (let i = 0; i < 26; i++) { const x = s / 2 + (rr() - 0.5) * s * 0.45, y = s / 2 + (rr() - 0.5) * s * 0.45, r = s * (0.12 + rr() * 0.2); const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, "rgba(255,255,255,.35)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, s, s); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  MO.smoke = (scene, n, col = 0xc9ccd4) => { const list = []; for (let i = 0; i < n; i++) { const m = new THREE.SpriteMaterial({ map: smokeTexC, color: col, transparent: true, depthWrite: false, opacity: 0 }); m.rotation = rr() * 6.28; const s = new THREE.Sprite(m); scene.add(s); list.push(s); } return list; };
  MO.glow = (col) => K.glowTex(col);

  // ================= VULCAN =================
  MO.vulcan = () => {
    const g = new THREE.Group(), boost = new THREE.Group(), up = new THREE.Group(); g.add(boost); g.add(up);
    const foam = MO.panelTex({ base: "#c8773e", mottle: 0.18, spots: 9000, spotR: 10, rings: [0.12, 0.33, 0.55, 0.78, 0.96], vseams: 4, seam: "rgba(90,40,10,.35)", soot: 0.1,
      text: [{ s: "ULA", u: 0.25, v: 0.62, size: 210, col: "rgba(255,255,255,.92)", spacing: 30 }, { s: "VULCAN", u: 0.75, v: 0.5, size: 120, col: "rgba(255,255,255,.85)", spacing: 24 }],
      flags: [{ k: "us", u: 0.25, v: 0.86, w: 0.07, h: 0.07 }] });
    const bm = MO.mat(foam, { rough: 0.78, ei: 0.25, bumpScale: 1.2 });
    boost.add(cyl(2.7, 33, bm, 0));
    const aft = cyl(2.75, 2.2, MO.plain(0x2a2b2f, 0.5, 0.5, 0.4), -0.6); boost.add(aft);
    const isTex = MO.panelTex({ base: "#1c1d21", mottle: 0.06, ribs: 64, rings: [0.1, 0.9] }); boost.add(cyl(2.72, 3, MO.mat(isTex, { metal: 0.45, rough: 0.45, ei: 0.5 }), 33));
    // BE-4 Triebwerke
    for (const s of [-1, 1]) { const nz = MO.nozzle(0.55, 1.15, 2.6, nozM()); nz.position.set(s * 1.2, -0.6, 0); boost.add(nz); }
    // 6 Booster GEM 63XL
    const srbT = MO.panelTex({ base: "#cfd2d6", mottle: 0.05, rings: [0.25, 0.5, 0.75], soot: 0.08, bands: [[0, 0.05, "#2a2b2f"]] });
    const srbM = MO.mat(srbT, { rough: 0.5 });
    const srbs = []; for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2 + Math.PI / 6; const sg = new THREE.Group(); sg.position.set(Math.cos(a) * 3.55, 0, Math.sin(a) * 3.55);
      sg.add(cyl(0.82, 20, srbM, 0)); const nose = lathe(ogive(0.82, 2.6), MO.plain(0xcfd2d6, 0.05, 0.45, 0.35)); nose.position.y = 20; sg.add(nose);
      const nz = MO.nozzle(0.4, 0.62, 1.1, nozM()); nz.position.y = 0; nz.rotation.z = 0; sg.add(nz);
      for (const y of [3, 17]) { const st = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1.0, 8), MO.plain(0x8a8d94, 0.8, 0.35)); st.position.set(-Math.cos(a) * 0.95, y, -Math.sin(a) * 0.95); st.rotation.z = Math.PI / 2; st.rotation.y = -a; sg.add(st); }
      boost.add(sg); srbs.push(sg); }
    // Oberstufe + Verkleidung
    const cenT = MO.panelTex({ base: "#c6c9ce", mottle: 0.04, rings: [0.5] }); up.add(cyl(2.7, 12, MO.mat(cenT, { metal: 0.15, rough: 0.4 }), 36));
    const fair = new THREE.Group(); fair.position.y = 48; up.add(fair);
    const fT = MO.panelTex({ base: "#d3d6da", mottle: 0.035, rings: [0.35], text: [{ s: "ULA", u: 0.25, v: 0.45, size: 260, col: "#1f4aa8", spacing: 20 }], flags: [{ k: "us", u: 0.75, v: 0.45, w: 0.09, h: 0.12 }] });
    const fM = MO.mat(fT, { rough: 0.38, ei: 0.4, side: THREE.DoubleSide });
    const halves = [0, 1].map((k) => { const h = new THREE.Group(); const c = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.7, 10, SEG / 2, 1, true, k * Math.PI, Math.PI), fM); c.position.y = 5; h.add(c);
      const tip = lathe(ogive(2.7, 9), MO.plain(0xd3d6da, 0.05, 0.38, 0.4, { side: THREE.DoubleSide }), k * Math.PI, Math.PI); tip.position.y = 10; h.add(tip); fair.add(h); return h; });
    const seamR = new THREE.Mesh(new THREE.TorusGeometry(2.71, 0.03, 6, SEG), MO.plain(0x9a9ca2, 0.6, 0.4)); seamR.rotation.x = Math.PI / 2; seamR.position.y = 48; up.add(seamR);
    // 40 Satelliten (im Fairing)
    const sats = new THREE.Group(); fair.add(sats);
    const disp = cyl(0.7, 13, MO.plain(0x50545c, 0.7, 0.4), 0); sats.add(disp);
    for (let lv = 0; lv < 10; lv++) for (let s = 0; s < 4; s++) { const a = (s / 4) * Math.PI * 2 + 0.785; const k = MO.kuiperFlat(); k.position.set(Math.cos(a) * 1.55, 0.7 + lv * 1.2, Math.sin(a) * 1.55); k.rotation.y = -a + Math.PI / 2; sats.add(k); }
    sats.visible = false;
    return { g, boost, up, halves, sats, srbs };
  };
  // Flacher Satellit (gestapelt)
  const cellT = (() => { const c = document.createElement("canvas"); c.width = 512; c.height = 256; const g = c.getContext("2d"); g.fillStyle = "#0d1630"; g.fillRect(0, 0, 512, 256); for (let y = 0; y < 256; y += 32) for (let x = 0; x < 512; x += 32) { g.fillStyle = `rgb(${20 + rr() * 10},${35 + rr() * 15},${80 + rr() * 30})`; g.fillRect(x + 2, y + 2, 28, 28); } g.strokeStyle = "rgba(200,210,230,.35)"; g.lineWidth = 1; for (let x = 0; x < 512; x += 32) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 256); g.stroke(); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  MO.cellM = () => new THREE.MeshStandardMaterial({ map: cellT, metalness: 0.6, roughness: 0.22, envMap: MO.env, envMapIntensity: 1.0 });
  const mliT = (() => { const c = document.createElement("canvas"); c.width = c.height = 512; const g = c.getContext("2d"); g.fillStyle = "#b58a34"; g.fillRect(0, 0, 512, 512); for (let i = 0; i < 900; i++) { const x = rr() * 512, y = rr() * 512; g.strokeStyle = `rgba(${rr() < 0.5 ? "255,240,190" : "90,60,10"},${0.15 + rr() * 0.3})`; g.lineWidth = 1 + rr() * 3; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rr() - 0.5) * 80, y + (rr() - 0.5) * 80); g.stroke(); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  MO.mliM = () => new THREE.MeshStandardMaterial({ map: mliT, bumpMap: mliT, bumpScale: 2, metalness: 0.95, roughness: 0.28, envMap: MO.env, envMapIntensity: 1.3 });
  MO.kuiperFlat = () => { const g = new THREE.Group(); const b = new THREE.Mesh(RoundedBoxGeometry(1.45, 1.0, 0.32, 2, 0.03), MO.plain(0x2c3038, 0.55, 0.45, 0.6)); g.add(b);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(1.35, 0.9), MO.cellM()); p.position.z = 0.165; g.add(p); const m = new THREE.Mesh(new THREE.PlaneGeometry(1.35, 0.9), MO.mliM()); m.position.z = -0.165; m.rotation.y = Math.PI; g.add(m); return g; };

  // ================= ARIANE 6 =================
  MO.ariane6 = () => {
    const g = new THREE.Group();
    const coreT = MO.panelTex({ base: "#cfd2d6", mottle: 0.04, rings: [0.2, 0.45, 0.7, 0.92], soot: 0.06, text: [{ s: "ARIANE 6", u: 0.25, v: 0.55, size: 150, col: "#1b2a4a", spacing: 18 }], flags: [{ k: "eu", u: 0.25, v: 0.85, w: 0.08, h: 0.06 }] });
    g.add(cyl(2.7, 30, MO.mat(coreT, { rough: 0.5 }), 0));
    g.add(cyl(2.72, 1.4, MO.plain(0x1e2230, 0.4, 0.5), 30));
    g.add(cyl(2.7, 6, MO.mat(MO.panelTex({ base: "#cbced2", mottle: 0.04 }), { rough: 0.45 }), 31.4));
    const fT = MO.panelTex({ base: "#d4d7db", mottle: 0.03, rings: [0.4], text: [{ s: "esa", u: 0.25, v: 0.45, size: 240, col: "#003247" }] });
    g.add(cyl(2.7, 10, MO.mat(fT, { rough: 0.38 }), 37.4)); const tip = lathe(ogive(2.7, 9), MO.plain(0xd4d7db, 0.05, 0.38, 0.4)); tip.position.y = 47.4; g.add(tip);
    const nz = MO.nozzle(0.8, 1.35, 2.4, nozM()); nz.position.y = 0; g.add(nz);
    const bT = MO.panelTex({ base: "#c8cbd0", mottle: 0.05, rings: [0.3, 0.6], soot: 0.08 });
    const boosters = []; for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2 + 0.785; const sg = new THREE.Group(); sg.position.set(Math.cos(a) * 4.25, 0, Math.sin(a) * 4.25);
      sg.add(cyl(1.5, 15, MO.mat(bT, { rough: 0.5 }), 0)); const n = lathe(ogive(1.5, 4.2), MO.plain(0xc8cbd0, 0.05, 0.45, 0.35)); n.position.y = 15; sg.add(n);
      const z = MO.nozzle(0.6, 1.05, 1.8, nozM()); sg.add(z); g.add(sg); boosters.push(sg); }
    return { g, boosters };
  };

  // ================= FALCON 9 =================
  MO.falcon9 = () => {
    const g = new THREE.Group(); const R = 1.85;
    const s1T = MO.panelTex({ base: "#d0d3d7", mottle: 0.04, rings: [0.15, 0.35, 0.55, 0.75, 0.93], soot: 0.22, text: [{ s: "SPACEX", u: 0.25, v: 0.55, size: 150, col: "#15171c", spacing: 26 }] });
    g.add(cyl(R, 42, MO.mat(s1T, { rough: 0.5 }), 0));
    for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2 + 0.785; const leg = new THREE.Mesh(new THREE.BoxGeometry(0.5, 9, 0.18), MO.plain(0x24262b, 0.4, 0.55)); leg.position.set(Math.cos(a) * (R + 0.08), 4.5, Math.sin(a) * (R + 0.08)); leg.rotation.y = -a + Math.PI / 2; g.add(leg); }
    g.add(cyl(R + 0.01, 4.5, MO.plain(0x141518, 0.45, 0.4, 0.5), 42));
    for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2; const fin = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.8, 0.12), MO.plain(0x3a3c42, 0.8, 0.35)); fin.position.set(Math.cos(a) * (R + 0.45), 45.5, Math.sin(a) * (R + 0.45)); fin.rotation.y = -a + Math.PI / 2; g.add(fin); }
    g.add(cyl(R, 9, MO.mat(MO.panelTex({ base: "#cdd0d4", mottle: 0.04 }), { rough: 0.45 }), 46.5));
    const fa = new THREE.Mesh(new THREE.CylinderGeometry(2.6, R, 2.5, SEG), MO.plain(0xd4d7db, 0.05, 0.4, 0.4)); fa.position.y = 56.75; g.add(fa);
    g.add(cyl(2.6, 6.5, MO.mat(MO.panelTex({ base: "#d4d7db", mottle: 0.03 }), { rough: 0.38 }), 58)); const tip = lathe(ogive(2.6, 6.2), MO.plain(0xd4d7db, 0.05, 0.38, 0.4)); tip.position.y = 64.5; g.add(tip);
    for (let i = 0; i < 9; i++) { const a = (i / 8) * Math.PI * 2, r = i === 8 ? 0 : 1.2; const nz = MO.nozzle(0.22, 0.42, 1.1, nozM()); nz.position.set(Math.cos(a) * r, 0, Math.sin(a) * r); g.add(nz); }
    return { g };
  };
  // ================= Flaggen-Textur (cn, pk) =================
  MO.flagTex = (k) => { const c = document.createElement("canvas"); c.width = 600; c.height = 400; const g = c.getContext("2d");
    const star = (x, y, r, rot = 0) => { g.beginPath(); for (let i = 0; i < 10; i++) { const a = rot - Math.PI / 2 + (i * Math.PI) / 5, rr2 = i % 2 ? r * 0.38 : r; g.lineTo(x + Math.cos(a) * rr2, y + Math.sin(a) * rr2); } g.closePath(); g.fill(); };
    if (k === "cn") { g.fillStyle = "#de2910"; g.fillRect(0, 0, 600, 400); g.fillStyle = "#ffde00"; star(100, 100, 60); [[200, 40], [240, 80], [240, 140], [200, 180]].forEach(([x, y]) => star(x, y, 20, 0.5)); }
    if (k === "pk") { g.fillStyle = "#fff"; g.fillRect(0, 0, 150, 400); g.fillStyle = "#01411c"; g.fillRect(150, 0, 450, 400); g.fillStyle = "#fff"; g.beginPath(); g.arc(375, 200, 120, 0, 7); g.fill(); g.fillStyle = "#01411c"; g.beginPath(); g.arc(405, 170, 105, 0, 7); g.fill(); g.fillStyle = "#fff"; star(430, 160, 40, 0.6); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
  const white = () => MO.plain(0xc9ccd1, 0.1, 0.5, 0.45);
  const wing = (w, h, mat, frame = 0x8a8f99, back = null) => { const g = new THREE.Group(); const p = new THREE.Mesh(new THREE.BoxGeometry(w, 0.06, h), [MO.plain(frame, 0.6, 0.4), MO.plain(frame, 0.6, 0.4), mat, back ?? MO.plain(0x30343c, 0.5, 0.5), MO.plain(frame, 0.6, 0.4), MO.plain(frame, 0.6, 0.4)]); g.add(p); return g; };

  // ================= LANGER MARSCH 2F (Einheit Meter) =================
  MO.longMarch2F = () => {
    const g = new THREE.Group(); const R = 1.675;
    const s1 = MO.panelTex({ base: "#d6d8da", mottle: 0.035, rings: [0.12, 0.45, 0.8], soot: 0.12, text: [{ s: "中国航天", u: 0.25, v: 0.6, size: 170, col: "#c8102e", spacing: 30 }], flags: [] });
    g.add(cyl(R, 28.5, MO.mat(s1, { rough: 0.5 }), 0));
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 2.4), new THREE.MeshStandardMaterial({ map: MO.flagTex("cn"), roughness: 0.6 })); fl.position.set(0, 21, R + 0.01); g.add(fl);
    g.add(cyl(R + 0.01, 1.2, MO.plain(0x3a3d44, 0.4, 0.5), 28.5));
    g.add(cyl(R, 12, MO.mat(MO.panelTex({ base: "#d6d8da", mottle: 0.03, rings: [0.5] }), { rough: 0.5 }), 29.7));
    const fa = new THREE.Mesh(new THREE.CylinderGeometry(1.9, R, 1.2, SEG), white()); fa.position.y = 42.3; g.add(fa);
    g.add(cyl(1.9, 7.5, MO.mat(MO.panelTex({ base: "#dadcdf", mottle: 0.03, vseams: 2 }), { rough: 0.42 }), 42.9));
    const tip = lathe(ogive(1.9, 4.2, 40, 0.15), white()); tip.position.y = 50.4; g.add(tip);
    for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2 + 0.4; const gf = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.1, 0.12), MO.plain(0x8b9099, 0.7, 0.35)); gf.position.set(Math.cos(a) * 2.35, 45.5, Math.sin(a) * 2.35); gf.rotation.y = -a + Math.PI / 2; g.add(gf); }
    const tower = new THREE.Group(); tower.position.y = 54.3; g.add(tower); tower.add(cyl(0.38, 6.5, white(), 0)); const tt = lathe(ogive(0.38, 1.3), white()); tt.position.y = 6.5; tower.add(tt);
    for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2; const nz = MO.nozzle(0.1, 0.22, 0.5, nozM()); nz.position.set(Math.cos(a) * 0.38, 1.0, Math.sin(a) * 0.38); nz.rotation.z = Math.cos(a) * 0.9; nz.rotation.x = -Math.sin(a) * 0.9; tower.add(nz); }
    const boosters = [];
    for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2 + Math.PI / 4; const b = new THREE.Group(); b.position.set(Math.cos(a) * (R + 1.15), 0, Math.sin(a) * (R + 1.15)); g.add(b);
      b.add(cyl(1.125, 13.5, MO.mat(MO.panelTex({ base: "#d4d6d9", mottle: 0.035, rings: [0.5], soot: 0.15 }), { rough: 0.5 }), 0));
      const c = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 1.125, 2.6, SEG), white()); c.position.y = 14.8; b.add(c);
      const fin = new THREE.Mesh(new THREE.BoxGeometry(0.1, 2.2, 1.5), MO.plain(0xbfc3c8, 0.3, 0.5)); fin.position.set(Math.cos(a) * 1.4, 1.2, Math.sin(a) * 1.4); fin.rotation.y = -a; b.add(fin);
      const nz = MO.nozzle(0.35, 0.6, 1.3, nozM()); b.add(nz); boosters.push(b); }
    for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2; const nz = MO.nozzle(0.35, 0.6, 1.3, nozM()); nz.position.set(Math.cos(a) * 0.8, 0, Math.sin(a) * 0.8); g.add(nz); }
    return { g, tower, boosters };
  };
  // ================= Startturm =================
  MO.pad = () => { const g = new THREE.Group(); const m = MO.plain(0x6e3b2a, 0.5, 0.6, 0.4), w = MO.plain(0x9aa0a8, 0.6, 0.5);
    const base = new THREE.Mesh(new THREE.BoxGeometry(30, 4, 30), MO.plain(0x5a5c60, 0.1, 0.9, 0.2)); base.position.y = -2; g.add(base);
    for (const [x, z] of [[-9, -4], [-9, 4], [-15, -4], [-15, 4]]) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.6, 70, 0.6), m); c.position.set(x, 35, z); g.add(c); }
    for (let y = 4; y < 70; y += 5) { const b = new THREE.Mesh(new THREE.BoxGeometry(7, 0.5, 9), m); b.position.set(-12, y, 0); g.add(b); }
    for (const y of [20, 34, 46]) { const arm = new THREE.Mesh(new THREE.BoxGeometry(6, 0.8, 2), w); arm.position.set(-6, y, 0); g.add(arm); }
    return g; };

  // ================= TIANGONG (Einheit Meter) =================
  MO.tiangong = () => { const g = new THREE.Group(); const hullT = MO.panelTex({ base: "#cfd2d6", mottle: 0.05, spots: 5000, vseams: 8, rings: [0.2, 0.4, 0.6, 0.8], w: 1024, h: 1024 });
    const hull = MO.mat(hullT, { rough: 0.55, bumpScale: 1 }), dark = MO.plain(0x3a3e46, 0.6, 0.4), gold = MO.mliM(); const cell = MO.cellM();
    const mod = (r, L, mat) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, SEG), mat); m.rotation.z = Math.PI / 2; return m; };
    const core = new THREE.Group(); g.add(core); const tc = mod(2.1, 13, hull); tc.position.x = -6.5; core.add(tc); const tn = mod(1.4, 3, hull); tn.position.x = 1.5; core.add(tn);
    const node = new THREE.Mesh(new THREE.SphereGeometry(1.5, 48, 32), hull); node.position.x = 3.6; core.add(node);
    const aft = mod(1.6, 1.5, gold); aft.position.x = -13.7; core.add(aft);
    for (const s of [-1, 1]) { const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 4, 12), dark); arm.position.set(-6, 0, s * 4); arm.rotation.x = Math.PI / 2; core.add(arm);
      const w = wing(4, 12, cell); w.position.set(-6, 0, s * 12); core.add(w); }
    const labs = [];
    for (const s of [-1, 1]) { const lab = new THREE.Group(); lab.position.set(3.6, 0, s * 1.4); lab.rotation.y = s * Math.PI / 2; g.add(lab);
      const lm = mod(2.1, 13, hull); lm.position.x = 8.5; lab.add(lm); const lc = mod(1.4, 2, hull); lc.position.x = 1; lab.add(lc); const back = mod(2.0, 3, gold); back.position.x = 16.5; lab.add(back);
      const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 8, 12), dark); mast.position.set(15.5, 4, 0); lab.add(mast);
      for (const z of [-1, 1]) { const w = wing(3.6, 26, cell); w.position.set(15.5, 8, z * 14); lab.add(w); }
      labs.push(lab); }
    const port = new THREE.Object3D(); port.position.set(5.1, 0, 0); g.add(port);
    return { g, port }; };

  // ================= SHENZHOU (Einheit Meter, Nase +x) =================
  MO.shenzhou = () => { const g = new THREE.Group(); const hull = MO.mat(MO.panelTex({ base: "#c4c7cc", mottle: 0.05, w: 512, h: 512 }), { rough: 0.55 });
    const om = new THREE.Mesh(new THREE.SphereGeometry(1.1, 40, 28), hull); om.scale.set(1.3, 1, 1); om.position.x = 2.6; g.add(om);
    const dock = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.6, 0.6, 32), MO.plain(0x8a8f99, 0.7, 0.35)); dock.rotation.z = Math.PI / 2; dock.position.x = 4.2; g.add(dock);
    const dm = lathe([[0.5, 0], [1.25, 1.1], [1.25, 2.0]].map(([r, y]) => new THREE.Vector2(r, y)), MO.plain(0x6b5b48, 0.4, 0.6)); dm.rotation.z = -Math.PI / 2; dm.position.x = 1.1; g.add(dm);
    const sm = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 2.9, SEG), MO.mliM()); sm.rotation.z = Math.PI / 2; sm.position.x = -2.4; g.add(sm);
    for (const s of [-1, 1]) { const w = wing(1.8, 7.2, MO.cellM()); w.position.set(-2.4, 0, s * 5.2); g.add(w); }
    const nz = MO.nozzle(0.3, 0.55, 0.8, nozM()); nz.rotation.z = Math.PI / 2; nz.position.x = -3.85; g.add(nz);
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.6), new THREE.MeshStandardMaterial({ map: MO.flagTex("cn"), roughness: 0.6 })); fl.position.set(-2.4, 0.4, 1.42); g.add(fl);
    return { g }; };

  // ================= ISS (Einheit Meter) =================
  MO.iss = () => { const g = new THREE.Group(); const hull = MO.mat(MO.panelTex({ base: "#cfd2d6", mottle: 0.05, vseams: 6, w: 512, h: 512 }), { rough: 0.55 }); const tr = MO.plain(0x9aa0a8, 0.7, 0.4);
    const truss = new THREE.Mesh(new THREE.BoxGeometry(100, 2.5, 2.5), tr); g.add(truss);
    const cellO = new THREE.MeshStandardMaterial({ color: 0x8a6a3a, metalness: 0.6, roughness: 0.35, envMap: MO.env, envMapIntensity: 0.6 });
    for (const x of [-44, -32, 32, 44]) for (const s of [-1, 1]) { const w = wing(11, 34, cellO, 0x6a6e76); w.position.set(x, 0, s * 19); w.rotation.z = 0.2; g.add(w); }
    for (const x of [-16, 16]) { const r = wing(4, 12, MO.plain(0xe8e8e8, 0.1, 0.6)); r.position.set(x, -3, 0); r.rotation.x = Math.PI / 2; g.add(r); }
    const mods = [[0, -4, 0, 2.2, 30, "z"], [0, -4, -18, 2.2, 10, "x"], [6, -4, -12, 2.2, 10, "x"], [-6, -4, -12, 2.2, 8, "x"]];
    for (const [x, y, z, r, L, ax] of mods) { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 48), hull); if (ax === "z") m.rotation.x = Math.PI / 2; else m.rotation.z = Math.PI / 2; m.position.set(x, y, z); g.add(m); }
    return { g }; };

  // ================= HAYABUSA2 (Einheit Meter) =================
  MO.hayabusa2 = () => { const g = new THREE.Group(); const gold = MO.mliM(), dark = MO.plain(0x2c3038, 0.6, 0.4), alu = MO.plain(0xb9bdc4, 0.9, 0.28, 1.1);
    const body = new THREE.Mesh(RoundedBoxGeometry(1.6, 1.25, 1.0, 2, 0.03), gold); g.add(body);
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.64, 0.04, 1.04), MO.plain(0xe0e2e6, 0.2, 0.5)); top.position.y = 0.64; g.add(top);
    for (const s of [-1, 1]) { const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.4, 10), alu); arm.rotation.x = Math.PI / 2; arm.position.set(0, 0.2, s * 0.7); g.add(arm);
      for (let i = 0; i < 3; i++) { const w = wing(1.15, 0.95, MO.cellM(), 0x50545c, MO.cellM()); w.rotation.x = Math.PI / 2; w.position.set(0, 0.2, s * (1.4 + i * 0.98)); g.add(w); } }
    const hga = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.05, 48), MO.plain(0xd8dadd, 0.3, 0.4)); hga.position.set(0.25, 0.75, 0); g.add(hga);
    const ka = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.05, 0.16, 32, 1, true), MO.plain(0xe8e8ea, 0.3, 0.4, 0.4, { side: THREE.DoubleSide })); ka.position.set(-0.45, 0.78, 0.2); g.add(ka);
    const horn = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.16, 1.0, 24), alu); horn.position.set(0.3, -1.1, 0); g.add(horn);
    const ip = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.7, 0.7), dark); ip.position.set(-0.84, -0.05, 0); g.add(ip);
    const engines = []; [[-0.18, -0.18], [-0.18, 0.18], [0.18, -0.18], [0.18, 0.18]].forEach(([y, z]) => { const e = new THREE.Group(); e.position.set(-0.9, y - 0.05, z); g.add(e);
      const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.06, 32), alu); ring.rotation.z = Math.PI / 2; e.add(ring);
      const grid = new THREE.Mesh(new THREE.CircleGeometry(0.1, 32), new THREE.MeshBasicMaterial({ color: 0x1b2a55, toneMapped: false })); grid.rotation.y = -Math.PI / 2; grid.position.x = -0.035; e.add(grid);
      const ex = MO.exhaust(3.5, 0.1, [0.75, 0.88, 1], [0.25, 0.4, 1]); ex.rotation.z = -Math.PI / 2; ex.position.x = -0.04; e.add(ex); e.userData = { grid, ex }; engines.push(e); });
    return { g, engines }; };

  // ================= ASTEROIDEN =================
  MO.asteroid = (o = {}) => { const r = o.r ?? 1; let s = o.seed ?? 3; const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647);
    const geo = new THREE.SphereGeometry(1, 220, 150); const p = geo.attributes.position; const v = new THREE.Vector3();
    const craters = []; for (let i = 0; i < (o.craters ?? 40); i++) craters.push([new THREE.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).normalize(), 0.05 + rnd() * 0.25, 0.02 + rnd() * 0.05]);
    const boulders = []; for (let i = 0; i < 260; i++) boulders.push([new THREE.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).normalize(), 0.015 + rnd() * 0.05, 0.01 + rnd() * 0.03]);
    const waves = []; for (let i = 0; i < 14; i++) waves.push([new THREE.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).normalize(), 2 + rnd() * 9, rnd() * 6.28, 0.035 / (1 + i * 0.35)]);
    const col = []; for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i).normalize(); let d = 1;
      if (o.top) d *= 0.78 + 0.32 * Math.pow(1 - Math.abs(v.y), 1.6) - 0.05 * Math.abs(v.y);
      for (const [dx, f, ph, am] of waves) d += am * Math.sin(v.dot(dx) * f + ph);
      for (const [c, cr, dp] of craters) { const a = v.angleTo(c); if (a < cr) d -= dp * (1 - (a / cr) ** 2); else if (a < cr * 1.3) d += dp * 0.3 * (1 - (a - cr) / (cr * 0.3)); }
      for (const [c, br, h] of boulders) { const a = v.angleTo(c); if (a < br) d += h * Math.cos((a / br) * Math.PI / 2); }
      v.multiplyScalar(d); if (o.stretch) v.multiply(o.stretch); p.setXYZ(i, v.x, v.y, v.z); const k = 0.88 + 0.12 * Math.sin(v.x * 9 + v.z * 5) * Math.cos(v.y * 7) + 0.04 * rnd(); col.push(0.32 * k, 0.3 * k, 0.28 * k); }
    geo.setAttribute("color", new THREE.Float32BufferAttribute(col, 3)); geo.computeVertexNormals();
    const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, metalness: 0, flatShading: false })); m.scale.setScalar(r); return m; };
  // ================= BEPICOLOMBO (MPO + Sonnenschild + Mio, Einheit Meter, Flugrichtung +y) =================
  MO.bepi = () => { const g = new THREE.Group(); const mli = MO.mliM(), white = MO.plain(0xd9dbde, 0.1, 0.45, 0.5), dark = MO.plain(0x2c3038, 0.6, 0.4), alu = MO.plain(0xb9bdc4, 0.9, 0.28, 1.1);
    const mliW = new THREE.MeshStandardMaterial({ color: 0xa8a497, metalness: 0.5, roughness: 0.4, envMap: MO.env, envMapIntensity: 0.45, bumpMap: MO.mliM().map, bumpScale: 1.2 });
    const mpo = new THREE.Group(); g.add(mpo); const body = new THREE.Mesh(RoundedBoxGeometry(2.4, 1.7, 2.2, 2, 0.04), mliW); mpo.add(body);
    const rad = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.05, 2.4), new THREE.MeshStandardMaterial({ color: 0xf2f2f0, metalness: 0.9, roughness: 0.15, envMap: MO.env, envMapIntensity: 1.4 })); rad.position.y = -0.9; mpo.add(rad);
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.4, 12), alu); arm.rotation.z = Math.PI / 2; arm.position.set(1.9, 0.2, 0); mpo.add(arm);
    const sw = new THREE.Group(); sw.position.set(2.6, 0.2, 0); mpo.add(sw); for (let i = 0; i < 3; i++) { const w = wing(2.4, 1.55, MO.cellM(), 0x50545c, MO.plain(0x30343c, 0.5, 0.5)); w.rotation.x = Math.PI / 2 - 0.3; w.position.x = 1.25 + i * 2.5; sw.add(w); }
    const hga = new THREE.Mesh(new THREE.SphereGeometry(0.75, 32, 12, 0, Math.PI * 2, 0, 0.6), MO.plain(0xe8e8ea, 0.3, 0.4, 0.4, { side: THREE.DoubleSide })); hga.rotation.x = Math.PI; hga.position.set(-1.3, 0.4, 0.9); mpo.add(hga);
    const mag = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.8, 8), alu); mag.rotation.z = Math.PI / 2; mag.position.set(-2.6, -0.4, -0.6); mpo.add(mag);
    const nz = []; for (const [x, z] of [[-0.8, -0.8], [0.8, -0.8], [-0.8, 0.8], [0.8, 0.8]]) { const n = MO.nozzle(0.08, 0.16, 0.3, nozM()); n.rotation.x = Math.PI; n.position.set(x, 0.85 + 0.3, z); mpo.add(n); const ex = MO.exhaust(3, 0.12); ex.rotation.x = Math.PI; ex.position.set(x, 1.15, z); ex.visible = false; mpo.add(ex); nz.push(ex); }
    const shield = new THREE.Group(); shield.position.y = 1.4; g.add(shield); const sh = new THREE.Mesh(new THREE.CylinderGeometry(1.7, 1.25, 1.6, 8), mliW); sh.position.y = 0.8; shield.add(sh);
    const mio = new THREE.Group(); mio.position.y = 3.3; g.add(mio); const mb = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 0.9, 8), [MO.cellM(), white, dark]); mio.add(mb);
    const mt = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 0.06, 8), white); mt.position.y = 0.47; mio.add(mt); const mm = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 2.2, 6), alu); mm.position.set(0, 0, 0); mm.rotation.z = Math.PI / 2; mio.add(mm);
    return { g, mpo, mio, shield, nz }; };
  // ================= JAMES WEBB (Einheit Meter) =================
  MO.jwst = () => { const g = new THREE.Group(); const goldM = new THREE.MeshStandardMaterial({ color: 0xd99a2b, metalness: 1, roughness: 0.18, envMap: MO.env, envMapIntensity: 1.0 });
    const hex = new THREE.CylinderGeometry(0.66, 0.66, 0.08, 6); const mir = new THREE.Group(); mir.position.set(0, 3.2, 0.5); mir.rotation.x = -0.25; g.add(mir);
    const s3 = Math.sqrt(3) * 0.66; const cells = [[0, 0]]; for (let i = 0; i < 6; i++) { const a = (i / 6) * 6.283 + Math.PI / 6; cells.push([Math.cos(a) * s3, Math.sin(a) * s3]); } for (let i = 0; i < 12; i++) { const a = (i / 12) * 6.283 + Math.PI / 6; const r = i % 2 ? 2 * s3 * Math.cos(Math.PI / 6) : 2 * s3; cells.push([Math.cos(a) * r, Math.sin(a) * r]); }
    cells.slice(1).forEach(([x, y]) => { const h = new THREE.Mesh(hex, goldM); h.rotation.x = Math.PI / 2; h.rotation.y = Math.PI / 6; h.position.set(x, y, 0); mir.add(h); });
    const strutM = MO.plain(0x2a2d33, 0.6, 0.4); for (const a of [0, 2.1, 4.2]) { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 3.4, 8), strutM); const p = V(Math.cos(a) * 2.2, Math.sin(a) * 2.2, 1.6); s.position.copy(p.clone().multiplyScalar(0.5)); s.lookAt(0, 0, 3.2); s.rotateX(Math.PI / 2); mir.add(s); }
    const sec = new THREE.Mesh(new THREE.CylinderGeometry(0.37, 0.37, 0.08, 24), goldM); sec.rotation.x = Math.PI / 2; sec.position.z = 3.2; mir.add(sec);
    const shield = new THREE.Group(); g.add(shield); const kite = new THREE.Shape(); kite.moveTo(-10.5, 0); kite.lineTo(-4, 3.6); kite.lineTo(4, 3.6); kite.lineTo(10.5, 0); kite.lineTo(4, -3.6); kite.lineTo(-4, -3.6); kite.closePath();
    for (let i = 0; i < 5; i++) { const m = new THREE.Mesh(new THREE.ShapeGeometry(kite), new THREE.MeshStandardMaterial({ color: i === 0 ? 0x9a8cae : 0x8a7d9e, metalness: 0.8, roughness: 0.3, envMap: MO.env, envMapIntensity: 0.5, side: THREE.DoubleSide, transparent: true, opacity: 0.96 })); m.rotation.x = -Math.PI / 2; m.position.y = -0.3 - i * 0.28; m.scale.setScalar(1 - i * 0.03); shield.add(m); }
    const bus = new THREE.Mesh(RoundedBoxGeometry(2, 1, 2, 2, 0.04), MO.plain(0x3a3e46, 0.6, 0.4)); bus.position.y = -2; g.add(bus); const sp = wing(2.4, 5, MO.cellM()); sp.position.set(0, -2.4, -3.2); sp.rotation.x = 0.4; g.add(sp);
    return { g, mir }; };
}
