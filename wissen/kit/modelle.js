// ===== Modelle (Nutzer 19.11.: „schönere 3D-Modelle“, keine echten Fotos) =====
// In szene.js eine Zeile "// @modelle" -> sauber_bau.py setzt diesen Code ein. Braucht THREE, E (Renderer), K.
// MO.vulcan(), MO.ariane6(), MO.falcon9(), MO.exhaust(len, rad, col), MO.smoke(scene, n), MO.kuiper(), MO.panelTex(...)
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
}
