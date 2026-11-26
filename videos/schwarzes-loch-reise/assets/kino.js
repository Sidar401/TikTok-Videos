// Novaro Kino-Baukasten (three.js + Nachbearbeitung). Nutzung in videos/<name>/index.html:
//   <script type="importmap">{"imports":{"three":"./assets/three/build/three.module.js","three/addons/":"./assets/three/jsm/"}}</script>
//   import * as K from "./assets/kino.js";
// Alles deterministisch: Zufall nur über K.rnd() mit festem Startwert.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
export { THREE };

let seed = 11;
export const reseed = (s) => (seed = s);
export const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
export const V = (x, y, z) => new THREE.Vector3(x, y, z);
export const cl = (x) => Math.max(0, Math.min(1, x));
export const lerp = (a, b, f) => a + (b - a) * f;
export const eio = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
export const eout = (x) => 1 - Math.pow(1 - x, 3);
export const prog = (t, s, d) => cl((t - s) / d);
export const de = (n) => n.toLocaleString("de-DE");

// ---------- Renderer + Kino-Nachbearbeitung ----------
const Grade = {
  uniforms: { tDiffuse: { value: null }, tint: { value: new THREE.Vector3(1, 1, 1) }, lift: { value: new THREE.Vector3(0, 0, 0) }, seed: { value: 1 }, vig: { value: 0.55 }, flash: { value: 0 } },
  vertexShader: `varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `uniform sampler2D tDiffuse;uniform vec3 tint,lift;uniform float seed,vig,flash;varying vec2 vUv;
    float r(vec2 c){return fract(sin(dot(c,vec2(12.9898,78.233))+seed)*43758.5453);}
    void main(){vec2 d=vUv-.5;float ca=.0036*length(d);vec3 c;c.r=texture2D(tDiffuse,vUv+d*ca).r;c.g=texture2D(tDiffuse,vUv).g;c.b=texture2D(tDiffuse,vUv-d*ca).b;
    c=c*tint+lift*(1.-c);float v=smoothstep(.95,.25,length(d*vec2(1.,.8)));c*=mix(vig,1.,v);c+=(r(vUv*vec2(1080.,1920.))-.5)*.045;c=mix(c,vec3(1.),flash);gl_FragColor=vec4(c,1.);}`,
};
export function setup(canvas) {
  const R = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  R.setSize(1080, 1920, false); R.toneMapping = THREE.ACESFilmicToneMapping; R.outputColorSpace = THREE.SRGBColorSpace;
  const cam = new THREE.PerspectiveCamera(40, 1080 / 1920, 0.1, 60000);
  const comp = new EffectComposer(R);
  const pass = new RenderPass(new THREE.Scene(), cam); comp.addPass(pass);
  const bloom = new UnrealBloomPass(new THREE.Vector2(540, 960), 0.8, 0.55, 0.8); comp.addPass(bloom);
  const grade = new ShaderPass(Grade); comp.addPass(grade); comp.addPass(new OutputPass());
  return { R, cam, comp, pass, bloom, grade,
    render(scene, t) { pass.scene = scene; grade.uniforms.seed.value = Math.floor(t * 30) * 1.37; comp.render(); },
    look(tint, lift, bloomS, bloomT) { grade.uniforms.tint.value.set(...tint); grade.uniforms.lift.value.set(...lift); bloom.strength = bloomS; bloom.threshold = bloomT; } };
}

// ---------- Texturen ----------
export function noiseCanvas(w, h, scale, oct, cover, soft) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d"); const im = g.createImageData(w, h);
  const G = 64, grid = []; for (let i = 0; i < G * G; i++) grid.push(rnd());
  const at = (x, y) => grid[((y % G + G) % G) * G + ((x % G + G) % G)];
  const vn = (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi; const s = (t) => t * t * (3 - 2 * t);
    const a = at(xi, yi), b = at(xi + 1, yi), c2 = at(xi, yi + 1), d = at(xi + 1, yi + 1); return a + (b - a) * s(xf) + (c2 - a) * s(yf) + (a - b - c2 + d) * s(xf) * s(yf); };
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let v = 0, amp = 0.5, f = scale; for (let o = 0; o < oct; o++) { v += amp * vn(x * f / w * G / 8, y * f / h * G / 8); amp *= 0.5; f *= 2; }
    const a = cl((v - cover) / soft); const i = (y * w + x) * 4; im.data[i] = im.data[i + 1] = im.data[i + 2] = 255; im.data[i + 3] = a * 255; }
  g.putImageData(im, 0, 0); return c;
}
export function windowsTex(lit, warm) {
  const c = document.createElement("canvas"); c.width = 128; c.height = 512; const g = c.getContext("2d"); g.fillStyle = "#06080e"; g.fillRect(0, 0, 128, 512);
  for (let y = 6; y < 512; y += 14) for (let x = 6; x < 128; x += 12) if (rnd() < lit) { const k = 0.55 + rnd() * 0.45; g.fillStyle = warm ? `rgba(255,${190 + rnd() * 40},${110 + rnd() * 50},${k})` : `rgba(170,200,255,${k * 0.6})`; g.fillRect(x, y, 6, 8); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}
export function moonTex() {
  const c = document.createElement("canvas"); c.width = 2048; c.height = 1024; const g = c.getContext("2d");
  const base = noiseCanvas(512, 256, 1.5, 6, 0.0, 1.0); g.fillStyle = "#c4beb2"; g.fillRect(0, 0, 2048, 1024);
  const mare = noiseCanvas(512, 256, 1.2, 5, 0.5, 0.18); g.globalCompositeOperation = "multiply"; g.globalAlpha = 0.55; g.filter = "brightness(0.45)"; g.drawImage(mare, 0, 0, 2048, 1024); g.filter = "none";
  g.globalAlpha = 0.35; g.drawImage(base, 0, 0, 2048, 1024); g.globalCompositeOperation = "source-over"; g.globalAlpha = 1;
  for (let i = 0; i < 900; i++) { const x = rnd() * 2048, y = rnd() * 1024, rr = Math.pow(rnd(), 4) * 30 + 1.5; const gr = g.createRadialGradient(x - rr * 0.2, y - rr * 0.2, 0, x, y, rr);
    gr.addColorStop(0, "rgba(60,56,50,.35)"); gr.addColorStop(0.75, "rgba(80,76,70,.18)"); gr.addColorStop(0.9, "rgba(235,230,220,.22)"); gr.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = gr; g.fillRect(x - rr, y - rr, rr * 2, rr * 2); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
export function glowTex(col) { const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d"); const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, col); gr.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c); }

// ---------- Bausteine ----------
export function sky(scene, top, mid, hor, r = 3000) {
  const u = { t: { value: new THREE.Color(top) }, m: { value: new THREE.Color(mid) }, h: { value: new THREE.Color(hor) } };
  const m = new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false, uniforms: u,
    vertexShader: `varying vec3 vP;void main(){vP=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader: `uniform vec3 t,m,h;varying vec3 vP;void main(){float y=vP.y;vec3 c=mix(h,m,smoothstep(-.02,.18,y));c=mix(c,t,smoothstep(.18,.6,y));gl_FragColor=vec4(c,1.);}` });
  const s = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 24), m); scene.add(s); return s;
}
export function stars(scene, n, minY, r = 2800, size = 3) {
  const p = []; for (let i = 0; i < n; i++) { const a = rnd() * 6.283, u = minY + rnd() * (1 - minY); p.push(Math.cos(a) * Math.sqrt(1 - u * u) * r, u * r, Math.sin(a) * Math.sqrt(1 - u * u) * r); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
  const pts = new THREE.Points(g, new THREE.PointsMaterial({ color: 0xdfe8ff, size, sizeAttenuation: false, transparent: true, opacity: 0.8, fog: false })); scene.add(pts); return pts;
}
export function city(scene, o) {
  const { n, rMin, rMax, arc, lit = 0.15, warm = true, hMax = 80, hMin = 10, base = -2, center = 0, colors = [0x0b0e16], glowI = 1.2, rough = 0.8, metal = 0.2, w0 = 6, w1 = 14 } = o;
  const g = new THREE.Group(); const list = [];
  for (let i = 0; i < n; i++) { const a = center + (rnd() - 0.5) * arc, r = rMin + rnd() * (rMax - rMin); const w = w0 + rnd() * (w1 - w0), d = w0 + rnd() * (w1 - w0), h = hMin + Math.pow(rnd(), 2.2) * hMax;
    const tx = windowsTex(lit, warm); tx.repeat.set(w / 12, h / 40);
    const m = new THREE.MeshStandardMaterial({ color: colors[i % colors.length], roughness: rough, metalness: metal, emissiveMap: tx, emissive: 0xffffff, emissiveIntensity: glowI });
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); b.position.set(Math.sin(a) * r, base + h / 2, -Math.cos(a) * r); b.rotation.y = -a; g.add(b); list.push(b);
    if (rnd() < 0.2) { const ant = new THREE.Mesh(new THREE.SphereGeometry(0.6, 8, 8), new THREE.MeshBasicMaterial({ color: 0xff3030 })); ant.position.set(b.position.x, base + h + 1, b.position.z); g.add(ant); } }
  scene.add(g); return { group: g, list };
}
export function sprite(scene, tex, size, pos, op = 1) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false, opacity: op, fog: false })); s.scale.setScalar(size); s.position.copy(pos); scene.add(s); return s;
}
export function water(scene, y, deep, skyCol, glint, glintDir) {
  const u = { deep: { value: new THREE.Color(deep) }, skyc: { value: new THREE.Color(skyCol) }, gl: { value: new THREE.Color(glint) }, gd: { value: glintDir.clone() }, time: { value: 0 }, fogD: { value: 0.004 } };
  const m = new THREE.ShaderMaterial({ uniforms: u,
    vertexShader: `varying vec3 vW;void main(){vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}`,
    fragmentShader: `uniform vec3 deep,skyc,gl,gd;uniform float time,fogD;varying vec3 vW;
      float h(vec2 p){float s=0.;float a=.5;mat2 m=mat2(.8,.6,-.6,.8);for(int i=0;i<6;i++){s+=a*sin(p.x*.4+time*(.6+float(i)*.2)+sin(p.y*.31+float(i))*1.7)*cos(p.y*.37+float(i)*1.3-time*.4);p=m*p*1.9;a*=.5;}return s;}
      void main(){vec2 p=vW.xz;float e=.15;vec3 n=normalize(vec3(h(p-vec2(e,0))-h(p+vec2(e,0)),2.2,h(p-vec2(0,e))-h(p+vec2(0,e))));
      vec3 v=normalize(cameraPosition-vW);float fr=pow(1.-max(dot(n,v),0.),4.);vec3 c=mix(deep,skyc,.15+.85*fr);
      vec3 r=reflect(-v,n);float s=pow(max(dot(r,normalize(gd)),0.),180.)*1.6+pow(max(dot(r,normalize(gd)),0.),18.)*.25;c+=gl*s;
      float fog=1.-exp(-length(cameraPosition-vW)*fogD);c=mix(c,skyc,fog*.7);gl_FragColor=vec4(c,1.);}` });
  const w = new THREE.Mesh(new THREE.PlaneGeometry(12000, 12000), m); w.rotation.x = -Math.PI / 2; w.position.y = y; scene.add(w); return { mesh: w, u };
}
export function moon(scene, r, pos, emissive = 0.06) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 128), new THREE.MeshStandardMaterial({ map: moonTex(), roughness: 1, emissive: 0xffcf90, emissiveIntensity: emissive }));
  m.position.copy(pos); scene.add(m); return m;
}
export function clouds(scene, list, color = 0x8a7a90) {
  const tex = new THREE.CanvasTexture(noiseCanvas(512, 256, 2.5, 5, 0.55, 0.25)); tex.colorSpace = THREE.SRGBColorSpace;
  return list.map(([x, y, z, w, h, o]) => { const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: o, color, depthWrite: false, fog: false })); p.position.set(x, y, z); scene.add(p); return p; });
}
// Erde mit Tag/Nacht, Wolken, Eis-Abschmelzen (ice: 1 = heute, 0 = weg) und Überflutung (flood: 0..1 über Höhenkarte)
export function earth(scene, imgs, radius = 2.6) {
  const mk = (im, srgb = true) => { const t = new THREE.Texture(im); if (srgb) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.needsUpdate = true; return t; };
  const U = { d: { value: mk(imgs.day) }, n: { value: mk(imgs.night) }, topo: { value: imgs.topo ? mk(imgs.topo, false) : null }, sun: { value: V(-0.6, 0.35, 0.75).normalize() }, ice: { value: 1 }, flood: { value: 0 } };
  const m = new THREE.ShaderMaterial({ uniforms: U,
    vertexShader: `varying vec2 vUv;varying vec3 vN;varying vec3 vV;varying vec3 vL;void main(){vUv=uv;vL=normal;vN=normalize(mat3(modelMatrix)*normal);vec4 w=modelMatrix*vec4(position,1.);vV=normalize(cameraPosition-w.xyz);gl_Position=projectionMatrix*viewMatrix*w;}`,
    fragmentShader: `uniform sampler2D d,n,topo;uniform vec3 sun;uniform float ice,flood;varying vec2 vUv;varying vec3 vN;varying vec3 vV;varying vec3 vL;
      void main(){float l=dot(vN,sun);float k=smoothstep(-.15,.25,l);vec3 dt=texture2D(d,vUv).rgb;
      float water=smoothstep(.0,.03,dt.b-dt.r)*(1.-step(.3,dt.r));
      float white=smoothstep(.55,.75,min(dt.r,min(dt.g,dt.b)));float lat=abs(vL.y);
      float isIce=white*smoothstep(.62,.8,lat);
      dt=mix(dt,mix(vec3(.05,.15,.32),dt*.6,.2),isIce*(1.-ice));
      float hgt=texture2D(topo,vUv).r;float sunk=(1.-water)*(1.-step(flood*.0098+.0001,hgt))*step(.001,flood);
      dt=mix(dt,vec3(.04,.2,.42),sunk*.92);water=max(water,sunk);
      dt+=water*vec3(.015,.04,.08);
      vec3 dc=dt*(.12+1.25*max(l,0.));vec3 nc=texture2D(n,vUv).rgb*vec3(1.4,1.05,.65)*1.8*(1.-sunk);vec3 c=mix(nc,dc,k);
      float f=pow(1.-clamp(dot(vN,vV),0.,1.),3.);c+=vec3(.3,.6,1.)*f*(.2+k);c+=pow(max(dot(reflect(-sun,vN),vV),0.),60.)*.15*k*water;gl_FragColor=vec4(c,1.);}` });
  const g = new THREE.Group(); const e = new THREE.Mesh(new THREE.SphereGeometry(radius, 160, 160), m); g.add(e);
  const cl = new THREE.CanvasTexture(noiseCanvas(1024, 512, 3.5, 6, 0.5, 0.22));
  const cloudsM = new THREE.Mesh(new THREE.SphereGeometry(radius * 1.012, 128, 128), new THREE.MeshStandardMaterial({ map: cl, transparent: true, opacity: 0.75, depthWrite: false }));
  g.add(cloudsM);
  const atm = new THREE.Mesh(new THREE.SphereGeometry(radius * 1.17, 96, 96), new THREE.ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, side: THREE.BackSide, depthWrite: false, uniforms: { sun: U.sun },
    vertexShader: `varying vec3 vN;varying vec3 vW;void main(){vN=normalize(mat3(modelMatrix)*normal);vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}`,
    fragmentShader: `uniform vec3 sun;varying vec3 vN;varying vec3 vW;void main(){vec3 v=normalize(cameraPosition-vW);float i=pow(max(.72-dot(vN,v),0.),4.);float l=smoothstep(-.4,.6,dot(vN,sun));gl_FragColor=vec4(vec3(.35,.65,1.)*i*(.3+1.5*l),1.);}` }));
  g.add(atm); scene.add(g);
  const ll = (lat, lon, r = radius) => { g.updateMatrixWorld(true); const la = (lat * Math.PI) / 180, lo = (lon * Math.PI) / 180; return e.localToWorld(V(Math.cos(la) * Math.cos(lo) * r, Math.sin(la) * r, -Math.cos(la) * Math.sin(lo) * r)); };
  return { group: g, mesh: e, clouds: cloudsM, U, ll };
}

// ---------- Untertitel Wort für Wort ----------
export function captions(words, chunks, el, startAt, fix = {}) {
  words = words.map((w) => ({ ...w, w: fix[w.w] ?? w.w }));
  const groups = []; let wi = 0;
  chunks.forEach(([a, b]) => { const ws = []; while (wi < words.length && words[wi].s < b + 0.01) ws.push(words[wi++]); let cur = [];
    ws.forEach((w) => { const len = cur.map((x) => x.w).join(" ").length + w.w.length; if (cur.length && (cur.length >= 3 || len > 16 || /[.?!]$/.test(cur[cur.length - 1].w))) { groups.push(cur); cur = []; } cur.push(w); });
    if (cur.length) groups.push(cur); });
  groups.forEach((g, i) => { g.s = g[0].s; g.e = i + 1 < groups.length ? groups[i + 1][0].s : 99; });
  let last = "";
  return (t) => { let h = ""; const g = groups.find((g) => t >= g.s - 0.05 && t < g.e);
    if (g && t >= startAt) h = g.filter((w) => w.w !== "").map((w) => `<span class="w${t >= w.s - 0.04 && t < w.e + 0.02 ? " on" : ""}">${w.w.replace(/[,.:]$/, "")}</span>`).join("");
    if (h !== last) { el.innerHTML = h; last = h; } };
}
export function labeler(el) { let last = ""; return (h) => { if (h !== last) { el.innerHTML = h; last = h; } }; }
