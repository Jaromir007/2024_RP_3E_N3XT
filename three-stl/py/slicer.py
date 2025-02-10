import json
import time

class Slicer:
    def __init__(self):
        self.triangles = []
        self.layers = []
        self.layer_height = 0.2
        

    def _slice_model(self):
        z_min = min(v[2] for tri in self.triangles for v in tri)

        if z_min < 0:
            for tri in self.triangles:
                for v in tri:
                    v[2] -= z_min  
            z_min = 0  

        z_max = max(v[2] for tri in self.triangles for v in tri)

        z = z_min
        while z <= z_max:
            layer = self._slice_at_z(z)
            if layer:
                self.layers.append(layer)
            z += self.layer_height


        return self.layers

    def _slice_at_z(self, z):
        intersections = []
        for tri in self.triangles:
            points = self._intersect_triangle(tri, z)
            if points:
                intersections.append(points)
        return intersections if intersections else None

    def _intersect_triangle(self, tri, z):
        edges = [(tri[i], tri[(i + 1) % 3]) for i in range(3)]
        points = []

        for v1, v2 in edges:
            z1, z2 = v1[2], v2[2]

            if (z1 <= z <= z2) or (z2 <= z <= z1):
                if z1 != z2:  
                    t = (z - z1) / (z2 - z1)
                    x = v1[0] + t * (v2[0] - v1[0])
                    y = v1[1] + t * (v2[1] - v1[1])
                    points.append((x, y))
                else:  
                    points.append((v1[0], v1[1]))  

        return points if len(points) == 2 else None

    def set_leayer_height(self, height):
        self.layer_height = height

    def slice(self, triangles):
        start_time = time.time()
        self.triangles = triangles
        layers = self._slice_model()
        print(f"[TIMING] Slicing took: {time.time() - start_time:.4f}s")

        return layers
