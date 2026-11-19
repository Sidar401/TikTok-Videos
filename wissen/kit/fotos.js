// Foto-Ebene (Nutzer 19.11.: echte Fotos statt selbstgebauter 3D-Raketen/Roboter).
// In szene.js eine Zeile "// @fotos" -> sauber_bau.py setzt diesen Code dort ein.
// Nutzung: await fotosInit({ v1: "assets/foto/v1.jpg" });  in renderAt: fotos(t, [[t0, t1, "v1", { z0, z1, x0, x1, y0, y1, pos, dim, cr }], ...]);
const FL = document.createElement("div"); FL.id = "fotos"; FL.style.cssText = "position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;pointer-events:none;isolation:isolate"; document.getElementById("stage").after(FL);
const FOT = {}; let FOTN = 0;
const FSH = document.createElement("div"); FSH.style.cssText = "position:absolute;inset:0;z-index:50;background:linear-gradient(180deg,rgba(0,0,0,.6) 0%,rgba(0,0,0,0) 20%,rgba(0,0,0,0) 50%,rgba(0,0,0,.8) 100%);opacity:0";
const FCR = document.createElement("div"); FCR.style.cssText = "position:absolute;left:0;right:0;top:196px;z-index:51;text-align:center;font:600 24px Inter,sans-serif;letter-spacing:2px;color:rgba(255,255,255,.55);opacity:0";
async function fotosInit(map) {
  for (const k in map) { const d = document.createElement("div"); d.style.cssText = "position:absolute;inset:0;opacity:0;overflow:hidden"; const im = new Image(); im.src = map[k]; im.style.cssText = "position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;transform-origin:50% 50%"; d.appendChild(im); FL.appendChild(d); FOT[k] = { d, im }; }
  FL.appendChild(FSH); FL.appendChild(FCR); await Promise.all(Object.values(FOT).map((f) => f.im.decode().catch(() => {})));
}
function fotos(t, shots, dark = 0) {
  for (const k in FOT) FOT[k].d.style.opacity = 0; let any = 0, cr = "";
  shots.forEach(([a, b, k, o = {}], i) => {
    if (t < a - 0.3 || t >= b + 0.3) return; const F = FOT[k]; const fin = Math.min(1, Math.max(0, (t - a + 0.3) / 0.3));
    const fout = i === shots.length - 1 || shots[i + 1][0] > b + 0.05 ? 1 - Math.min(1, Math.max(0, (t - b) / 0.3)) : 1;
    const al = Math.min(fin, fout); const f = Math.min(1, Math.max(0, (t - a) / (b - a)));
    F.d.style.zIndex = i; F.d.style.opacity = al; F.im.style.objectPosition = o.pos ?? "50% 50%";
    const z = (o.z0 ?? 1.04) + ((o.z1 ?? 1.14) - (o.z0 ?? 1.04)) * f, x = (o.x0 ?? 0) + ((o.x1 ?? 0) - (o.x0 ?? 0)) * f, y = (o.y0 ?? 0) + ((o.y1 ?? 0) - (o.y0 ?? 0)) * f;
    F.im.style.transform = `translate(${x}px,${y}px) scale(${z})`; F.im.style.filter = o.dim ? `brightness(${1 - o.dim})` : "";
    if (al > any) { any = al; cr = o.cr ?? "FOTO: NASA"; }
  });
  FSH.style.opacity = any; FCR.style.opacity = any; FCR.textContent = cr; return any;
}
