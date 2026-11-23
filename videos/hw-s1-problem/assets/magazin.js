// Helfer für den Magazin-Stil. Erwartet globale Variable tl (GSAP-Timeline) und DUR.
const show = (s, a, b) => { tl.set(s, { opacity: 1 }, a); if (b !== undefined) tl.set(s, { opacity: 0 }, b); };
const up = (s, a, d = 0.5) => tl.fromTo(s, { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: d, ease: "power3.out" }, a);
const peek = (s, a, from = 520) => tl.fromTo(s, { y: from }, { y: 0, duration: 0.7, ease: "back.out(1.3)" }, a);
const note = (s, a) => tl.fromTo(s, { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, a);
const count = (id, to, a, d, fmt = (v) => Math.round(v)) => { const o = { v: 0 }; tl.to(o, { v: to, duration: d, ease: "power2.out", onUpdate: () => (document.getElementById(id).textContent = fmt(o.v)) }, a); };
// Szenenwechsel: alte Szene kurz nach oben weg, neue kommt
const scenes = (list) => list.forEach(([s, a, b], i) => {
  tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: i ? 0.2 : 0.01 }, a);
  if (b !== undefined) tl.to(s, { opacity: 0, y: -30, duration: 0.2, ease: "power2.in" }, b - 0.2);
  tl.fromTo(s, { scale: 1 }, { scale: 1.025, duration: (b ?? DUR) - a, ease: "none" }, a);
});
const kopf = () => {
  tl.fromTo("#logo", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, 0);
  tl.fromTo("#name", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.1);
  tl.to("#rule-in", { width: "100%", duration: DUR, ease: "none" }, 0);
};
const caps = (list) => list.forEach(([s, a, b]) => show(s, a, b));
const folgen = (a) => { tl.fromTo("#follow", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, a);
  tl.to("#follow span", { scale: 1.05, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, a + 0.5); };
// Kopf ohne Fortschrittsbalken (Nutzer 16.11.)
const kopf2 = () => {
  tl.fromTo("#logo", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.8)" }, 0);
  tl.fromTo("#name", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0.1);
};
// Schluss-Karte mit großem Logo
const schluss = (a) => {
  tl.fromTo("#cta", { opacity: 0 }, { opacity: 1, duration: 0.35 }, a);
  tl.fromTo("#cta .ring", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.7)" }, a + 0.1);
  tl.fromTo("#cta .n", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, a + 0.45);
  tl.fromTo("#cta .pill span", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.5)" }, a + 1.0);
  tl.to("#cta .pill span", { scale: 1.07, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }, a + 1.5);
};
// Kommentar-Aufruf: Fenster, Text tippt, Zeiger klickt „Kommentieren“. Gibt Tipp-/Klick-Zeiten zurück (für Sound).
const kommentar = (a, n) => {
  const step = 0.08;
  tl.fromTo("#co", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, a);
  tl.fromTo("#co-bn", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, a + 0.15);
  tl.to("#co .tz", { opacity: 1, duration: 0.01, stagger: step }, a + 0.5);
  tl.fromTo("#co-cur", { opacity: 1 }, { opacity: 0, duration: 0.3, repeat: 13, yoyo: true, ease: "steps(1)" }, a + 0.3);
  const k = a + 0.5 + n * step + 0.9;
  tl.fromTo("#co-z", { x: -200, y: 120, opacity: 0 }, { x: 260, y: -175, opacity: 1, duration: 0.8, ease: "power2.inOut" }, k - 0.85);
  tl.to("#co-z", { scale: 0.82, duration: 0.08, yoyo: true, repeat: 1 }, k);
  tl.to("#co-btn", { scale: 0.9, duration: 0.08, yoyo: true, repeat: 1 }, k);
  tl.to(["#co", "#co-bn", "#co-z"], { opacity: 0, duration: 0.3 }, k + 0.9);
};
