const W = (w, ab = 0) => { const x = WORDS.find((q) => q.s >= ab - 0.01 && q.w.toLowerCase().replace(/[^a-zäöüß0-9]/g, "").startsWith(w)); return x ? x.s : ab; };
// @fotos
await fotosInit({ r1: "assets/foto/r1.jpg", r2: "assets/foto/r2.jpg", r3: "assets/foto/r3.jpg", r4: "assets/foto/r4.jpg", r5: "assets/foto/r5.jpg", r6: "assets/foto/r6.jpg", r7: "assets/foto/r7.jpg", r8: "assets/foto/r8.jpg", r9: "assets/foto/r9.jpg" });
const tZum = W("zum"), tOhne = W("ohne"), tUnd = W("und", 8), tFolg = W("folg"), tDer = W("der", 13.4), tGeb = W("gebaut"), tBez = W("bezahlt"), tIm = W("im", 22), tAstra = W("astra", 25), tDarin = W("darin"), tArm = W("der", 33.5), tStueck = W("stück"), tDas = W("das", 38.8), tElf = W("elf"), tZwei = W("zwei", 44), tDritte = W("das", 46.8), tGanz = W("ganz", 49.5), tDrei = W("drei", 51.3), tKontakt = W("kontakt"), tFertig = W("fertig"), tWarum = W("warum"), tRiesig = W("riesige"), tIn = W("in", 67.2), END = 72.0;
const SY = "FOTO: NASA · SYMBOLBILD";
const SHOTS = [
  [0, tZum, "r1", { z0: 1.0, z1: 1.1, cr: "FOTO: NASA / ISS" }],
  [tZum, tUnd, "r2", { z0: 1.05, z1: 1.2, x0: 20, x1: -20, cr: "FOTO: NASA / ISS" }],
  [tUnd, tDer, "r3", { z0: 1.05, z1: 1.18, cr: "FOTO: NASA / ISS" }],
  [tDer, tIm, "r4", { z0: 1.05, z1: 1.15, pos: "35% 50%", cr: SY }],
  [tIm, tAstra, "r5", { z0: 1.05, z1: 1.2, y0: 30, y1: -30, cr: "FOTO: NASA · SPACEX-START (SYMBOLBILD)" }],
  [tAstra, tArm, "r9", { z0: 1.1, z1: 1.2, dim: 0.6, cr: "GRAFIK · FOTO: NASA / ISS" }],
  [tArm, tDas, "r2", { z0: 1.5, z1: 1.3, pos: "60% 40%", cr: SY }],
  [tDas, tGanz, "r9", { z0: 1.2, z1: 1.3, dim: 0.62, cr: "GRAFIK · FOTO: NASA / ISS" }],
  [tGanz, tKontakt, "r4", { z0: 1.25, z1: 1.1, pos: "70% 50%", cr: SY }],
  [tKontakt, tFertig, "r6", { z0: 1.05, z1: 1.15, cr: "FOTO: NASA/JPL · SYMBOLBILD" }],
  [tFertig, tWarum, "r7", { z0: 1.05, z1: 1.15, cr: "FOTO: NASA / ISS" }],
  [tWarum, tIn, "r8", { z0: 1.05, z1: 1.18, cr: "FOTO: NASA · WEBB-TELESKOP" }],
  [tIn, END + 1, "r1", { z0: 1.15, z1: 1.3, cr: "FOTO: NASA / ISS" }],
];
// ---- klare Grafiken (Kiste + Ring) ----
const DIA = document.createElement("div"); DIA.style.cssText = "position:absolute;inset:0;z-index:52;opacity:0"; FL.appendChild(DIA);
const G = "#ffd23f", WH = "rgba(255,255,255,.92)";
// Würfel (isometrisch), Mitte 540/820
const P = (x, y, z) => [540 + (x - z) * 270, 800 + (x + z) * 156 - y * 320];
const C = [[0,0,0],[1,0,0],[1,0,1],[0,0,1],[0,1,0],[1,1,0],[1,1,1],[0,1,1]].map(([x,y,z]) => P(x - .5, y - .5, z - .5));
const ED = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
const cubeSvg = `<svg id="cube" width="1080" height="1920" style="position:absolute;inset:0">${ED.map(([a,b],i)=>`<line class="ce" x1="${C[a][0]}" y1="${C[a][1]}" x2="${C[b][0]}" y2="${C[b][1]}" stroke="${G}" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>`).join("")}
 <g id="cubeL" font-family="Inter Display" font-weight="800" font-size="54" fill="#fff" text-anchor="middle" opacity="0">
  <text x="${(C[2][0]+C[1][0])/2+90}" y="${(C[2][1]+C[1][1])/2+60}">1 m</text><text x="${(C[2][0]+C[3][0])/2-90}" y="${(C[2][1]+C[3][1])/2+60}">1 m</text><text x="${C[3][0]-90}" y="${(C[3][1]+C[7][1])/2+18}">1 m</text></g>
 <g id="cubeIn" opacity="0" stroke="${WH}" stroke-width="6" stroke-linecap="round" fill="none"><path d="M470 1000 L470 780 L630 700 L690 760"/><circle cx="470" cy="1000" r="16" fill="${WH}"/><circle cx="470" cy="780" r="12" fill="${WH}"/><circle cx="630" cy="700" r="12" fill="${WH}"/>
  ${[0,1,2,3,4].map(i=>`<line x1="${600+i*28}" y1="${930+i*12}" x2="${600+i*28}" y2="${1050+i*12}" stroke-width="5"/>`).join("")}</g></svg>`;
// Ring aus 11 Stücken, Mitte 540/860, r 300
const RC = [540, 860], RR = 300, segs = [];
for (let i = 0; i < 11; i++) { const a0 = -Math.PI / 2 + i * 2 * Math.PI / 11 + 0.03, a1 = a0 + 2 * Math.PI / 11 - 0.06; segs.push(`M${RC[0]+Math.cos(a0)*RR} ${RC[1]+Math.sin(a0)*RR} A${RR} ${RR} 0 0 1 ${RC[0]+Math.cos(a1)*RR} ${RC[1]+Math.sin(a1)*RR}`); }
const ringSvg = `<svg id="ring" width="1080" height="1920" style="position:absolute;inset:0">${segs.map((d,i)=>`<path class="rs" id="rs${i}" d="${d}" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="34" stroke-linecap="butt" stroke-dasharray="10 8"/>`).join("")}
 <g font-family="Inter Display" font-weight="800" font-size="46" text-anchor="middle"><text id="rd" x="540" y="875" fill="#fff" opacity="0">1,4 m</text><line id="rdl" x1="${540-RR+30}" y1="905" x2="${540+RR-30}" y2="905" stroke="#fff" stroke-width="4" opacity="0"/></g></svg>`;
DIA.innerHTML = cubeSvg + ringSvg;
const CE = [...DIA.querySelectorAll(".ce")], RS = [...DIA.querySelectorAll(".rs")], CUBE = DIA.querySelector("#cube"), RING = DIA.querySelector("#ring");
const logo = (f, h = 110) => `<div style="display:inline-block;background:#fff;border-radius:22px;padding:14px 28px;margin-bottom:16px"><img src='assets/logos/${f}' style='height:${h}px;display:block'></div><br>`;
const WORDEL = document.getElementById("word");
renderAt = (t) => {
  fotos(t, SHOTS);
  const cubeOn = t >= tAstra - 0.1 && t < tArm, ringOn = t >= tDas - 0.1 && t < tGanz;
  DIA.style.opacity = cubeOn ? Math.min(cl((t - tAstra + 0.1) / 0.4), 1 - cl((t - tArm + 0.3) / 0.3)) : ringOn ? Math.min(cl((t - tDas + 0.1) / 0.4), 1 - cl((t - tGanz + 0.3) / 0.3)) : 0;
  CUBE.style.display = cubeOn ? "" : "none"; RING.style.display = ringOn ? "" : "none";
  CE.forEach((e, i) => e.setAttribute("stroke-dashoffset", String(1 - cl((t - tAstra - 0.2 - i * 0.12) / 0.35))));
  DIA.querySelector("#cubeL").setAttribute("opacity", String(cl((t - tAstra - 1.8) / 0.4) * (1 - cl((t - tDarin + 0.2) / 0.3))));
  DIA.querySelector("#cubeIn").setAttribute("opacity", String(cl((t - tDarin) / 0.4)));
  RS.forEach((e, i) => { const show = cl((t - tDas - 0.1 - i * 0.08) / 0.25); e.style.opacity = show; let st = "rgba(255,255,255,.28)", da = "10 8";
    if (t >= tZwei && i < 2) { st = "#fff"; da = "none"; } if (t >= tDritte && i === 2) { st = G; da = "none"; e.style.opacity = 0.75 + 0.25 * Math.sin(t * 6); }
    e.setAttribute("stroke", st); e.setAttribute("stroke-dasharray", da); });
  const rdA = String(cl((t - tDas - 1.5) / 0.4) * (1 - cl((t - tElf + 0.2) / 0.3))); DIA.querySelector("#rd").setAttribute("opacity", rdA); DIA.querySelector("#rdl").setAttribute("opacity", rdA);
  let wh = "", wa = 0; const seg = (a, b, h) => { if (t >= a && t < b) { wh = h; wa = cl((t - a) / 0.3) * (1 - cl((t - b + 0.4) / 0.3)); } };
  seg(tZum + 0.2, tOhne - 0.1, "Zum ersten Mal"); seg(tOhne - 0.1, tUnd - 0.1, "ohne Astronauten");
  seg(tUnd + 0.2, tFolg - 0.1, "Bauen im All");
  seg(tDer, tGeb - 0.1, "Roboter „Astra“"); seg(tGeb, tBez - 0.1, logo("caltech.svg", 70) + "<div class='sub'>Uni in Kalifornien</div>"); seg(tBez, tIm - 0.1, "DARPA<div class='sub'>Forschung des US-Militärs</div>");
  seg(tIm, tAstra - 0.1, logo("spacex.svg", 50) + "März");
  seg(tAstra + 0.3, tDarin - 0.1, "eine Kiste, 1 m groß"); seg(tDarin, tArm - 0.1, "Greifarm + Stangen");
  seg(tArm, tDas - 0.1, "Stück für Stück");
  seg(tDas, tElf - 0.1, "Rahmen einer Antenne"); seg(tElf, tZwei - 0.1, "11 Teilstücke");
  seg(tZwei, tDritte - 0.1, "2 auf der Erde gebaut"); seg(tDritte, tGanz - 0.1, "<span class='y'>Nr. 3 im All gebaut</span>");
  seg(tDrei, tKontakt - 0.1, "3 Forscher<div class='sub'>Befehle & Fotos</div>"); seg(tKontakt, tFertig - 0.1, "ein paar Mal am Tag<div class='sub'>je ≈ 15 Minuten</div>");
  seg(tFertig, tWarum - 0.1, "nicht fertig<div class='sub'>Mission endet im Dezember</div>");
  seg(tRiesig, tIn - 0.1, "zu groß für jede Rakete"); seg(tIn, END, "Roboter bauen oben");
  WORDEL.style.top = (t >= tFolg - 0.1 && t < tGeb) || cubeOn || ringOn ? (cubeOn || ringOn ? "1340px" : "300px") : "";
  word(wh, wa); cap(t);
};
