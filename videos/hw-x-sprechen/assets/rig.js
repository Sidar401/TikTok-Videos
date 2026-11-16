// HundeWissenTv – „Rig“: bewegt einzelne Körperteile eines freigestellten Posen-Bildes (WebGL-Bildverformung).
// Nutzung:
//   const r = Rig(canvas, img, { pad: 80, scale: 2, uniforms: ["aTail"], glsl: `q = rot(q, vec2(150.,215.), -aTail*box(p, vec4(0.,170.,0.,300.), 20.));` });
//   r.ready.then(...); r.draw({ aTail: 0.2 });
// Im GLSL: p = Pixel im Originalbild (0..W, 0..H), q = wohin gelesen wird (startet = p).
// Helfer: rot(p,c,a)  blob(p,c,r)  box(p, vec4(x0,x1,y0,y1), weich)  squashY(q,p,c,r,k) (Augen schließen)
(function () {
  const VS = "attribute vec2 a; varying vec2 v; void main(){ v = vec2(a.x*0.5+0.5, 0.5-a.y*0.5); gl_Position = vec4(a,0.,1.); }";
  const HEAD = `precision highp float;
    uniform sampler2D tex; uniform vec2 csize; uniform float pad, scl;
    varying vec2 v;
    vec2 rot(vec2 p, vec2 c, float a){ float s=sin(a), k=cos(a); p-=c; return c+vec2(k*p.x-s*p.y, s*p.x+k*p.y); }
    float blob(vec2 p, vec2 c, vec2 r){ vec2 d=(p-c)/r; return exp(-dot(d,d)); }
    float box(vec2 p, vec4 b, float w){ return smoothstep(b.x-w,b.x+w,p.x)*(1.0-smoothstep(b.y-w,b.y+w,p.x))*smoothstep(b.z-w,b.z+w,p.y)*(1.0-smoothstep(b.w-w,b.w+w,p.y)); }
    `;
  window.Rig = function (canvas, img, o) {
    const pad = o.pad ?? 80, scl = o.scale ?? 2;
    const gl = canvas.getContext("webgl", { premultipliedAlpha: true, preserveDrawingBuffer: true, alpha: true });
    const names = o.uniforms || [];
    const FS = HEAD + names.map((n) => `uniform float ${n};`).join("\n") + `
      void main(){
        vec2 p = v*csize/scl - pad; vec2 q = p;
        ${o.glsl}
        gl_FragColor = texture2D(tex, (q+pad)*scl/csize);
      }`;
    const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) console.error(gl.getShaderInfoLog(x)); return x; };
    const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const U = {}; let ok = false;
    const ready = new Promise((res) => {
      const go = () => {
        const W = img.naturalWidth, H = img.naturalHeight;
        canvas.width = (W + 2 * pad) * scl; canvas.height = (H + 2 * pad) * scl;
        gl.viewport(0, 0, canvas.width, canvas.height);
        const c = document.createElement("canvas"); c.width = canvas.width; c.height = canvas.height;
        const g = c.getContext("2d"); g.imageSmoothingQuality = "high"; g.drawImage(img, pad * scl, pad * scl, W * scl, H * scl);
        gl.useProgram(pr);
        const loc = gl.getAttribLocation(pr, "a"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
        const tx = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tx);
        gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, c);
        for (const [k, val] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, val);
        gl.uniform2f(gl.getUniformLocation(pr, "csize"), canvas.width, canvas.height);
        gl.uniform1f(gl.getUniformLocation(pr, "pad"), pad); gl.uniform1f(gl.getUniformLocation(pr, "scl"), scl);
        gl.uniform1i(gl.getUniformLocation(pr, "tex"), 0);
        names.forEach((n) => (U[n] = gl.getUniformLocation(pr, n)));
        ok = true; res();
      };
      img.complete && img.naturalWidth ? go() : img.addEventListener("load", go);
    });
    return {
      ready,
      draw(vals) {
        if (!ok) return;
        gl.useProgram(pr);
        names.forEach((n) => gl.uniform1f(U[n], vals[n] || 0));
        gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      },
    };
  };
  // Hilfen für Zeitkurven
  window.RZ = {
    S: (a, b, x) => { const k = Math.max(0, Math.min(1, (x - a) / (b - a))); return k * k * (3 - 2 * k); },
    TAU: Math.PI * 2,
    // Sprech-Rhythmus: deterministische „Silben“ (0..1)
    talk: (t, seed = 1) => { const k = Math.floor(t * 7.5); const f = t * 7.5 - k; const r = Math.abs(Math.sin(k * 12.9898 * seed + 4.1)) ; return r > 0.25 ? Math.sin(f * Math.PI) * (0.5 + 0.5 * r) : 0; },
    blink: (t, at) => at.reduce((m, b) => Math.max(m, 1 - Math.min(1, Math.abs(t - b) / 0.09)), 0),
  };
})();
