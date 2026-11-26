// Prüft ein HundeWissenTv-Video: Texte komplett im Bild (innerhalb Rahmen) und keine Überdeckung von Bildern.
// Aufruf: node hundewissen/pruefen.js videos/<name>
const { chromium } = require("playwright");
const path = require("path");
(async () => {
  const dir = path.resolve(process.argv[2]);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto("file://" + dir + "/index.html"); await p.waitForTimeout(800);
  const fehler = await p.evaluate(() => {
    gsap.set(".info, .chip, .call, .shopk, .pose, .x, .scene, .h, #co, #co-bn, #teilen", { clearProps: "transform,opacity" });
    const R = (e) => e.getBoundingClientRect(), out = [];
    const innen = (r) => r.left >= 30 && r.right <= 1050 && r.top >= 30 && r.bottom <= 1890;
    const schnitt = (a, c) => { const x = Math.max(0, Math.min(a.right, c.right) - Math.max(a.left, c.left)), y = Math.max(0, Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top)); return x * y; };
    document.querySelectorAll(".scene").forEach((s) => {
      const texte = [...s.querySelectorAll(".info, .chip, .call, .shopk, .h, .src")];
      const bilder = [...s.querySelectorAll("img.pose")];
      texte.forEach((t) => {
        const r = R(t); const name = (t.textContent || "").trim().slice(0, 30);
        if (!innen(r)) out.push(`${s.id}: "${name}" ragt aus dem Bild`);
        // Text darf nicht über Bild liegen (Bild-Rahmen 8 % eingerückt)
        bilder.forEach((im) => { const q = R(im), dx = q.width * 0.08, dy = q.height * 0.08;
          const k = { left: q.left + dx, right: q.right - dx, top: q.top + dy, bottom: q.bottom - dy };
          if (schnitt(r, k) > 400) out.push(`${s.id}: "${name}" verdeckt Bild ${im.getAttribute("src").split("/").pop()}`); });
      });
      bilder.forEach((im) => { if (!innen(R(im))) out.push(`${s.id}: Bild ${im.getAttribute("src").split("/").pop()} ragt aus dem Bild`); });
    });
    return out;
  });
  await b.close();
  if (fehler.length) { console.log("FEHLER:\n" + fehler.join("\n")); process.exit(1); } else console.log("Prüfung ok: alles im Bild, nichts verdeckt.");
})();
