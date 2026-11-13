// Größenvergleich in echten Proportionen (Durchmesser in 1000 km → Radius in Einheiten)
const sc = new THREE.Scene();
const st = K.stars(sc, 3000, -1, 30000, 1.6); st.material.opacity = 0.45;
const Ld = V(1, 0.25, 0.85).normalize();
const sunL = new THREE.DirectionalLight(0xfff6ea, 3.4); sunL.position.copy(Ld.clone().multiplyScalar(100)); sc.add(sunL); sc.add(new THREE.AmbientLight(0x223040, 0.25));
const ball = async (f, r, x) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), new THREE.MeshStandardMaterial({ map: await tex(f), roughness: 1, metalness: 0 })); m.position.set(x, 0, 0); sc.add(m); return m; };
const R = { me: 2.44, ma: 3.39, ve: 6.05, er: 6.37, ju: 69.9, so: 695.7 };
const X = { me: 0 }; X.ma = X.me + R.me + 4 + R.ma; X.ve = X.ma + R.ma + 4 + R.ve; X.er = X.ve + R.ve + 4 + R.er; X.ju = X.er + R.er + 16 + R.ju; X.so = X.ju + R.ju + 60 + R.so;
const me = await ball("mercury.jpg", R.me, X.me), ma = await ball("mars.jpg", R.ma, X.ma), ve = await ball("venus_atmosphere.jpg", R.ve, X.ve), ju = await ball("jupiter.jpg", R.ju, X.ju);
const EA = K.earth(sc, { day, night, topo }, R.er); EA.group.position.set(X.er, 0, 0); EA.U.sun.value.copy(Ld); EA.group.children[EA.group.children.length - 1].scale.setScalar(0.93);
// Sonne: echte Textur, selbstleuchtend + Glühen
const sunT = await tex("sun.jpg");
const sun = new THREE.Mesh(new THREE.SphereGeometry(R.so, 128, 96), new THREE.MeshBasicMaterial({ map: sunT, color: new THREE.Color(1.6, 1.15, 0.8), toneMapped: false })); sun.position.set(X.so, 0, 0); sc.add(sun);
const g1 = K.sprite(sc, K.glowTex("rgba(255,140,40,.55)"), R.so * 3.0, sun.position.clone().add(V(0, 0, -60)), 0.9);
const g2 = K.sprite(sc, K.glowTex("rgba(255,200,120,.5)"), R.so * 2.3, sun.position.clone().add(V(0, 0, -30)), 0.8);
// Beschriftungen
label("Merkur", me, R.me, { t0: 0.4, t1: 3.4 }); label("Mars", ma, R.ma, { t0: 0.8, t1: 3.4 });
label("Venus", ve, R.ve, { t0: 3.9, t1: 6.8 }); label("Erde", EA.group, R.er, { t0: 4.3, t1: 6.8 });
label("Jupiter", ju, R.ju, { t0: 7.3, t1: 10.0 }); label("Sonne", sun, R.so, { t0: 11.0, t1: 99, size: 110 });
// Kamerastationen [Mitte x, Abstand]
const S = [[(X.me - R.me + X.ma + R.ma) / 2, 52], [(X.me - R.me + X.er + R.er) / 2, 148], [(X.me + X.ju + R.ju) / 2, 560], [(X.ju - R.ju + X.so + R.so) / 2 + 40, 4300]];
const T = [0, 3.2, 6.6, 10.2];
renderAt = (t) => {
  E.look([1.0, 1.0, 1.0], [0, 0, 0], t < 9.4 ? 0.22 : 0.5, t < 9.4 ? 0.95 : 0.85); E.grade.uniforms.flash.value = 0;
  let i = 0; while (i < 3 && t >= T[i + 1]) i++;
  const a = S[i], b = S[Math.min(i + 1, 3)]; const f = i < 3 ? K.eio(cl((t - T[i + 1] + 1.4) / 1.4)) : 0;
  const cx = lerp(a[0], b[0], f), d = lerp(a[1], b[1], f) * (1 + 0.04 * prog(t, T[i], 3.4));
  cam.fov = 40; cam.updateProjectionMatrix(); cam.position.set(cx + d * 0.05, d * 0.06, d); cam.lookAt(cx, -d * 0.05, 0);
  [me, ma, ve, ju].forEach((m, k) => (m.rotation.y = t * (0.12 + k * 0.03))); EA.mesh.rotation.y = t * 0.15; EA.clouds.rotation.y = t * 0.17; sun.rotation.y = t * 0.02;
  E.render(sc, t); updLabels(t);
  const w = cl((t - 12.2) / 0.5); word("1,3 Mio. × Erde<div style='font:600 40px Inter,sans-serif;color:rgba(255,255,255,.75);margin-top:10px'>passt in die Sonne</div>", w);
};
