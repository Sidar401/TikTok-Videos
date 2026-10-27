"""3D-Testszene (Blender/bpy, CPU-Cycles): Spielzeug-Figur „Max“ fährt im Sparschwein-Auto an Geldstapeln vorbei.

  python3 scripts/blender_test.py <ausgabe-ordner> [start end]   → PNG-Frames (540×960, 24 fps)
Danach: ffmpeg -framerate 24 -i <ordner>/f%04d.png -vf scale=1080:1920:flags=lanczos … .mp4
"""
import math
import sys

import bpy

out = sys.argv[1]
f0, f1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, 120)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = 540, 960
sc.render.fps = 24
sc.frame_start, sc.frame_end = 1, 120
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 16
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Punchy"

world = bpy.data.worlds.new("W")
sc.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.45, 0.68, 1.0, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9


def mat(name, rgb, rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


M = {k: mat(k, *v) for k, v in {
    "asphalt": ((0.06, 0.06, 0.07), 0.9), "gras": ((0.18, 0.5, 0.12), 0.9), "weiss": ((0.9, 0.9, 0.9), 0.6),
    "geh": ((0.55, 0.55, 0.55), 0.8), "pink": ((1.0, 0.45, 0.55), 0.35), "pinkd": ((0.85, 0.3, 0.42), 0.4),
    "schwarz": ((0.02, 0.02, 0.02), 0.3), "gold": ((1.0, 0.62, 0.12), 0.22, 1.0), "haut": ((0.95, 0.68, 0.52), 0.5),
    "orange": ((0.95, 0.42, 0.08), 0.6), "blau": ((0.08, 0.3, 0.9), 0.25), "jeans": ((0.15, 0.25, 0.55), 0.7),
    "geld": ((0.45, 0.72, 0.42), 0.6), "band": ((0.95, 0.55, 0.1), 0.5), "wand1": ((0.95, 0.88, 0.7), 0.8),
    "wand2": ((0.75, 0.82, 0.9), 0.8), "dach": ((0.75, 0.25, 0.15), 0.7), "stamm": ((0.4, 0.25, 0.12), 0.8),
    "laub": ((0.2, 0.55, 0.18), 0.8), "fenster": ((0.2, 0.45, 0.8), 0.1), "reifen": ((0.03, 0.03, 0.03), 0.8),
}.items()}


def obj(op, m, loc=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), smooth=True, bevel=0.0, parent=None, **kw):
    op(location=loc, rotation=rot, **kw)
    o = bpy.context.object
    o.scale = scale
    o.data.materials.append(M[m])
    if smooth:
        bpy.ops.object.shade_smooth()
    if bevel:
        mod = o.modifiers.new("b", "BEVEL")
        mod.width, mod.segments = bevel, 3
    if parent:
        o.parent = parent
    return o


cube = bpy.ops.mesh.primitive_cube_add
sph = bpy.ops.mesh.primitive_uv_sphere_add
cyl = bpy.ops.mesh.primitive_cylinder_add
cone = bpy.ops.mesh.primitive_cone_add

# ---- Straße & Umgebung ----
obj(cube, "asphalt", (0, 0, -0.05), (40, 2.2, 0.05), smooth=False)
for x in range(-20, 21, 3):
    obj(cube, "weiss", (x, 0, 0.002), (0.7, 0.06, 0.01), smooth=False)
obj(cube, "geh", (0, 2.9, 0.0), (40, 0.7, 0.08), smooth=False, bevel=0.03)
obj(cube, "geh", (0, -2.9, 0.0), (40, 0.7, 0.08), smooth=False, bevel=0.03)
obj(cube, "gras", (0, 12, -0.06), (40, 8.4, 0.05), smooth=False)
obj(cube, "gras", (0, -12, -0.06), (40, 8.4, 0.05), smooth=False)

for i, x in enumerate(range(-16, 20, 6)):
    w = "wand1" if i % 2 else "wand2"
    obj(cube, w, (x, 7, 1.6), (1.8, 1.6, 1.6), smooth=False, bevel=0.05)
    r = obj(cone, "dach", (x, 7, 4.0), (2.55, 2.3, 0.9), (0, 0, math.radians(45)), smooth=False, vertices=4)
    for fx in (-0.8, 0.8):
        obj(cube, "fenster", (x + fx, 5.38, 1.9), (0.35, 0.03, 0.4), smooth=False)
    obj(cube, "dach", (x, 5.38, 0.6), (0.35, 0.03, 0.6), smooth=False)
for x in range(-17, 20, 4):
    obj(cyl, "stamm", (x + 1.5, 4.2, 0.6), (0.12, 0.12, 0.6), vertices=16)
    obj(sph, "laub", (x + 1.5, 4.2, 1.6), (0.75, 0.75, 0.8), segments=24, ring_count=12)


# ---- Geldstapel am Straßenrand ----
def buendel_stapel(x, y, n):
    for k in range(n):
        obj(cube, "geld", (x, y, 0.08 + k * 0.13), (0.42, 0.2, 0.06), (0, 0, math.radians((k % 3 - 1) * 4)), smooth=False, bevel=0.01)
        obj(cube, "band", (x, y, 0.08 + k * 0.13), (0.07, 0.205, 0.065), (0, 0, math.radians((k % 3 - 1) * 4)), smooth=False)


def muenz_stapel(x, y, n):
    for k in range(n):
        obj(cyl, "gold", (x + (k % 2) * 0.01, y, 0.06 + k * 0.07), (0.28, 0.28, 0.03), vertices=48)


for x, n in [(-9, 6), (-5, 9), (-1, 12), (3, 16), (7, 20), (11, 26)]:
    buendel_stapel(x, 3.3, n)
    muenz_stapel(x + 1.1, 3.3, max(4, n // 2))

# ---- Sparschwein-Auto mit Max ----
car = bpy.data.objects.new("Auto", None)
sc.collection.objects.link(car)
obj(sph, "pink", (0, 0, 0.75), (1.15, 0.62, 0.55), segments=48, ring_count=24, parent=car)
obj(cyl, "pinkd", (1.15, 0, 0.78), (0.22, 0.22, 0.12), (0, math.radians(90), 0), vertices=32, parent=car)
for yy in (-0.07, 0.07):
    obj(sph, "schwarz", (1.28, yy, 0.8), (0.04, 0.04, 0.05), segments=16, ring_count=8, parent=car)
    obj(sph, "schwarz", (0.85, yy * 4.2, 1.05), (0.06, 0.06, 0.06), segments=16, ring_count=8, parent=car)
    obj(cone, "pinkd", (0.55, yy * 3.6, 1.3), (0.14, 0.12, 0.2), (0, math.radians(-15), 0), vertices=24, parent=car)
obj(cube, "schwarz", (-0.25, 0, 1.29), (0.25, 0.04, 0.02), smooth=False, parent=car)
wheels = []
for wx in (-0.65, 0.65):
    for wy in (-0.55, 0.55):
        w = obj(cyl, "reifen", (wx, wy, 0.32), (0.32, 0.32, 0.12), (math.radians(90), 0, 0), vertices=32, parent=car)
        obj(cyl, "gold", (wx, wy * 1.02, 0.32), (0.14, 0.14, 0.13), (math.radians(90), 0, 0), vertices=24, parent=car)
        wheels.append(w)
obj(bpy.ops.mesh.primitive_torus_add, "schwarz", (0.42, 0, 1.45), (1, 1, 1), (0, math.radians(-60), 0), major_radius=0.17, minor_radius=0.025, parent=car)

maxi = bpy.data.objects.new("Max", None)
sc.collection.objects.link(maxi)
maxi.parent = car
maxi.location = (-0.15, 0, 1.25)
obj(sph, "orange", (0, 0, 0.35), (0.33, 0.3, 0.42), segments=32, ring_count=16, parent=maxi)
kopf = bpy.data.objects.new("Kopf", None)
sc.collection.objects.link(kopf)
kopf.parent = maxi
kopf.location = (0.02, 0, 0.98)
obj(sph, "haut", (0, 0, 0), (0.3, 0.3, 0.3), segments=40, ring_count=20, parent=kopf)
obj(sph, "blau", (-0.06, 0, 0.1), (0.33, 0.33, 0.29), segments=40, ring_count=20, parent=kopf)
obj(cube, "blau", (0.2, 0, 0.19), (0.12, 0.26, 0.02), (0, math.radians(-12), 0), smooth=False, bevel=0.02, parent=kopf)
for yy in (-0.1, 0.1):
    obj(sph, "schwarz", (0.27, yy, 0.0), (0.035, 0.035, 0.045), segments=16, ring_count=8, parent=kopf)
obj(bpy.ops.mesh.primitive_torus_add, "schwarz", (0.27, 0, -0.1), (0.6, 1, 0.5), (0, math.radians(90), 0), major_radius=0.09, minor_radius=0.015, parent=kopf)
for yy in (-0.22, 0.22):
    obj(cyl, "orange", (0.3, yy, 0.42), (0.07, 0.07, 0.3), (0, math.radians(70), 0), vertices=16, parent=maxi)
    obj(sph, "haut", (0.58, yy * 0.7, 0.32), (0.08, 0.08, 0.08), segments=16, ring_count=8, parent=maxi)

# ---- Licht & Kamera ----
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), math.radians(10), math.radians(-40)))
bpy.context.object.data.energy = 4.0
bpy.context.object.data.angle = math.radians(8)
bpy.ops.object.camera_add()
cam = bpy.context.object
cam.data.lens = 26
sc.camera = cam
ziel = bpy.data.objects.new("Ziel", None)
sc.collection.objects.link(ziel)
ziel.parent = car
ziel.location = (0.2, 0, 1.1)
tc = cam.constraints.new("TRACK_TO")
tc.target, tc.track_axis, tc.up_axis = ziel, "TRACK_NEGATIVE_Z", "UP_Y"

# ---- Animation ----
def key(o, path, frame, val):
    setattr(o, path, val)
    o.keyframe_insert(data_path=path, frame=frame)


key(car, "location", 1, (-8, -0.9, 0))
key(car, "location", 120, (8, -0.9, 0))
key(cam, "location", 1, (-4.2, -5.2, 1.6))
key(cam, "location", 120, (9.5, -3.6, 2.4))
for f in range(1, 121, 6):
    key(maxi, "location", f, (-0.15, 0, 1.25 + (0.04 if (f // 6) % 2 else 0)))
    key(car, "rotation_euler", f, (math.radians(1.5 if (f // 6) % 2 else -1.5), 0, 0))
key(kopf, "rotation_euler", 1, (0, 0, 0))
key(kopf, "rotation_euler", 40, (0, 0, 0))
key(kopf, "rotation_euler", 60, (0, 0, math.radians(-55)))
key(kopf, "rotation_euler", 90, (0, 0, math.radians(-55)))
key(kopf, "rotation_euler", 108, (0, 0, 0))
for w in wheels:
    key(w, "rotation_euler", 1, (math.radians(90), 0, 0))
    key(w, "rotation_euler", 120, (math.radians(90), math.radians(16 / 0.32 * 57.3), 0))
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action:
        for fc in getattr(o.animation_data.action, "fcurves", []):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR" if o in wheels or (o == car and fc.data_path == "location") else "BEZIER"

for f in range(f0, f1 + 1):
    sc.frame_set(f)
    sc.render.filepath = f"{out}/f{f:04d}.png"
    bpy.ops.render.render(write_still=True)
