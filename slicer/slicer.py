import time
import json
import struct
from gcode_generator import GCodeGenerator
from monotone_chain import MonotoneChain


class Slicer:
    def __init__(self):
        self.layer_height = 0.2

        self.triangles = []
        self.layers = []
        self.triangle_bins = {}
        self.z_values = []
        self.start_time = 0

    def _precompute_z_bounds(self):
        self.triangle_bins.clear()
        self.z_values.clear()
        
        for tri in self.triangles:
            z_min, z_max = min(v[2] for v in tri), max(v[2] for v in tri)
            self.triangle_bins.setdefault((z_min, z_max), []).append(tri)
            self.z_values.extend([z_min, z_max])
        
        self.z_values = sorted(set(self.z_values))

    def _slice_model(self):
        z_min, z_max = self.z_values[0], self.z_values[-1]
        layers = []
        
        z = z_min
        while z <= z_max:
            layer = self._slice_at_z(z)
            if layer:
                layers.append(layer)
            z = round(self.layer_height + z, 2)
        
        self.layers = layers
        return self.layers

    def _slice_at_z(self, z):
        intersections = []
        for (z_min, z_max), triangles in self.triangle_bins.items():
            if z_min <= z <= z_max:
                for tri in triangles:
                    points = self._intersect_triangle(tri, z)
                    if points:
                        intersections.extend(points)
        
        return intersections if intersections else None

    def _intersect_triangle(self, tri, z):
        vertices = [(tri[i], tri[(i + 1) % 3]) for i in range(3)]
        points = set()

        for v1, v2 in vertices:
            z1, z2 = v1[2], v2[2]
            if (z1 < z < z2) or (z2 < z < z1):
                t = (z - z1) / (z2 - z1)
                x = round(v1[0] + t * (v2[0] - v1[0]), 5)
                y = round(v1[1] + t * (v2[1] - v1[1]), 5)
                points.add((x, y))

        return points if points else None

    def _reset(self):
        self.triangles = []
        self.layers = []
        self.triangle_bins.clear()
        self.z_values.clear()

    def set_layer_height(self, height):
        self.layer_height = height

    def slice(self, triangles):
        self.start_time = time.time()
        self.triangles = triangles
        self._precompute_z_bounds()
        layers = self._slice_model()
        print(f"[INFO] Total points generated:", sum(len(layer) for layer in layers))
        print(f"[TIMING] Slicing took: {time.time() - self.start_time:.4f}s")
        self._reset()
        return layers



def parseSTL(fileIn):
    triangles = []
    with open(fileIn, "rb") as f:
        _ = f.read(80)
        num_triangles = struct.unpack("<I", f.read(4))[0]

        for _ in range(num_triangles):
            _ = struct.unpack("<3f", f.read(12))
            v1 = struct.unpack("<3f", f.read(12))
            v2 = struct.unpack("<3f", f.read(12))
            v3 = struct.unpack("<3f", f.read(12))
            f.read(2)
            triangles.append([v1, v2, v3])
    
    return triangles


import os

base_dir = os.path.dirname(os.path.abspath(__file__))

stl_path = os.path.join(base_dir, "../models/benchy.stl")
sliced_path = os.path.join(base_dir, "../models/benchy-sliced.json")
gcode_path = os.path.join(base_dir, "../models/benchy-gcode.gcode")


# stl_path = os.path.join(base_dir, "../models/cube.stl")
# sliced_path = os.path.join(base_dir, "../models/cube-sliced.json")
# gcode_path = os.path.join(base_dir, "../models/cube-gcode.gcode")

triangles = parseSTL(stl_path)

slicer = Slicer()
layers = slicer.slice(triangles)

with open(sliced_path, "w") as f:
    json.dump(layers, f, indent=2)

mc = MonotoneChain()
hull = []
for layer in layers:
    hull.append(mc.get_outline(layer))

gg = GCodeGenerator()
gcode = gg.generate_gcode([hull])

with open(gcode_path, "w") as f:
    f.write(gcode)

print("Slicing complete!")
