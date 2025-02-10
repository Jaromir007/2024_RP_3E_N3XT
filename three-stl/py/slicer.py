import time

class Slicer:
    def __init__(self):
        self.triangles = []
        self.layers = []
        self.layer_height = 0.2
        self.triangle_bounds = []
        self.start_time = 0

    def _precompute_z_bounds(self):
        t = time.time()
        self.triangle_bounds = [(min(v[2] for v in tri), max(v[2] for v in tri)) for tri in self.triangles]
        print(f"[TIMING] _precompute_z_bounds: {time.time() - t:.4f}s")

    def _slice_model(self):
        t = time.time()
        z_min = min(z[0] for z in self.triangle_bounds)
        z_max = max(z[1] for z in self.triangle_bounds)

        print(f"[TIMING] Compute z_min and z_max: {time.time() - t:.4f}s")

        layers = []
        z = z_min
        while z <= z_max:
            layer = self._slice_at_z(z)
            if layer:
                layers.append(layer)
            z += self.layer_height

        self.layers = layers
        print(f"[TIMING] _slice_model: {time.time() - t:.4f}s")
        return self.layers

    def _slice_at_z(self, z):
        t = time.time()
        intersections = []
        
        for i in range(len(self.triangles)):
            z_min, z_max = self.triangle_bounds[i]

            if z_min <= z <= z_max:  
                points = self._intersect_triangle(self.triangles[i], z)
                if points:
                    intersections.append(points)

        print(f"[TIMING] _slice_at_z({z}): {time.time() - t:.4f}s")
        return intersections if intersections else None

    def _intersect_triangle(self, tri, z):
        edges = [(tri[i], tri[(i + 1) % 3]) for i in range(3)]
        points = []

        for v1, v2 in edges:
            z1, z2 = v1[2], v2[2]

            if (z1 < z < z2) or (z2 < z < z1):  
                inv_dz = 1.0 / (z2 - z1)  
                t = (z - z1) * inv_dz  
                x = v1[0] + t * (v2[0] - v1[0])
                y = v1[1] + t * (v2[1] - v1[1])
                points.append((x, y))

        return points if len(points) == 2 else None

    def _reset(self):
        self.triangles = []
        self.layers = []
        self.triangle_bounds = []

    def set_layer_height(self, height):
        self.layer_height = height

    def slice(self, triangles):
        self.start_time = time.time()
        self.triangles = triangles
        self._precompute_z_bounds()
        layers = self._slice_model()
        print(f"[TIMING] Slicing took: {time.time() - self.start_time:.4f}s")
        self._reset()
        return layers
