// Titelbild (Thumbnail) aus einem sauberen 3D-Bild des Videos + großer Titel.
// Aufruf: node wissen/kit/thumb.js videos/<name> <sekunde> "<Titel mit <y>Wort</y>>" [ausgabe.png]
// Blendet Untertitel/Beschriftungen aus, rendert die Szene bei <sekunde>, legt den Titel darüber.
const { chromium } = require("playwright");
const http = require("http"), fs = require("fs"), path = require("path");
const [dir, sec, title, outArg] = process.argv.slice(2);
const root = path.resolve(dir);
const out = path.resolve(outArg || path.join("renders", path.basename(root) + "-thumbnail.png"));
const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".jpg": "image/jpeg", ".png": "image/png", ".otf": "font/otf", ".wav": "audio/wav", ".woff2": "font/woff2", ".svg": "image/svg+xml" };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split("?")[0])); if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { "Content-Type": types[path.extname(f)] || "application/octet-stream" }); fs.createReadStream(f).pipe(r); });
srv.listen(0, async () => {
  const port = srv.address().port;
  const b = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on("pageerror", (e) => console.log("ERR", e.message));
  await p.goto(`http://localhost:${port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.scene);
  await p.evaluate(() => window.__hf.buildReady.scene);
  const t = parseFloat(sec);
  await p.evaluate((t) => { window.dispatchEvent(new CustomEvent("hf-seek", { detail: { time: t, waitUntil() {} } })); }, t);
  await p.evaluate((s) => (window.__TS = s), parseInt(process.env.SIZE || "150"));
  await p.evaluate((l) => (window.__LOGO = l), process.env.LOGO || "");
  await p.evaluate((title) => {
    document.querySelectorAll(".line, .bar, .hookdim, .share, #flash, .pin, .an, .an-svg").forEach((e) => (e.style.display = "none"));
    const s = document.createElement("style");
    s.textContent = `#th{position:absolute;inset:0;z-index:99;font-family:"Inter Display","Inter",sans-serif}
      #th .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.75) 0%,rgba(0,0,0,.15) 30%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)}
      #th .t{position:absolute;left:50px;right:50px;top:330px;text-align:center;color:#fff;font-weight:900;font-size:${window.__TS||150}px;line-height:1.02;letter-spacing:-2px;text-shadow:0 8px 40px rgba(0,0,0,.9),0 0 4px #000}
      #th .t y{display:inline-block;background:#ffd23f;color:#111;padding:0 26px 10px;border-radius:24px;transform:rotate(-2deg);text-shadow:none;box-shadow:0 14px 50px rgba(255,210,63,.5)}
      #th .brand{position:absolute;left:0;right:0;bottom:120px;text-align:center;color:rgba(255,255,255,.9);font-weight:900;font-size:56px;letter-spacing:14px;text-shadow:0 4px 20px rgba(0,0,0,.9)}`;
    document.head.appendChild(s);
    const d = document.createElement("div"); d.id = "th";
    d.innerHTML = `<div class="shade"></div><div class="t">${title}</div><div class="brand">NOVARO</div>` + (window.__LOGO ? `<div style="position:absolute;left:330px;top:1180px;width:420px;height:170px;background:#fff;border-radius:28px;display:flex;align-items:center;justify-content:center;padding:26px 34px;box-sizing:border-box;box-shadow:0 0 60px rgba(255,154,60,.45),0 20px 40px rgba(0,0,0,.6)"><img src="${window.__LOGO}" style="width:100%;height:100%;object-fit:contain"></div>` : "");
    document.getElementById("root").appendChild(d);
  }, title);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({ path: out });
  console.log("Thumbnail:", out);
  await b.close(); srv.close();
});
