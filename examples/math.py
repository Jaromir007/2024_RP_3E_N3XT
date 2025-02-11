# Linear interpolation 

v1 = (1, 2, 3)
v2 = (4, 6, 9)

# formula: P = v1 + t(v2 - v1)
 
t = 0.5 # half way 

p_x = v1[0] + t*(v2[0] - v1[0])
p_y = v1[1] + t*(v2[1] - v1[1])
p_z = v1[2] + t*(v2[2] - v1[2])

p = (p_x, p_y, p_z)

# simplification: 

p = ()
for i in range(3): 
    p_i = v1[i] + t*(v2[i] - v1[i])
    p += (p_i,)


# more simplification 
p=[v1[i] + t*(v2[i] - v1[i]) for i in range(3)]

# Tuple for more efficiency

p = tuple(v1[i] + t * (v2[i] - v1[i]) for i in range(3))

# -------------------------------------------------------------------------------------#


# For slicing, we need t (since we already know the z, it's quite easy)

z = 0.2 # layer height 
z_p = 4 # 20th layer (průsečík)

# formula for t: 

t = (z_p - v1[2])/ (v2[2] - v1[2])

# print(t) # where are we on the distance between v1 and v2

# Now get the x_p and y_p
x_p = v1[0] + t * (v2[0] - v1[0])
y_p = v1[1] + t * (v2[1] - v1[1])


p = (x_p, y_p, z_p)
# print(p)

# v2[2] cant equal v1[2], to avoid division by 0

def find_intersection(v1, v2, z_p):
    if(v2[2] == v1[2]):
        print("no intersection, points are parallel")
        return 
    else:
        t = (z_p - v1[2]) / (v2[2] - v1[2])
        return tuple((v1[0] + t * (v2[0] - v1[0]), v1[1] + t * (v2[1] - v1[1]), z_p))

# print(find_intersection(v1, v2, z_p))

# add check if the plate intersect the line between v1 and v2 

def _find_intersection(v1, v2, z_p): 
    z1, z2 = v1[1], v2[2]
    if(z1 == z2):
        return 
    if not (min(z1, z2) <= z_p <= max(z1, z2)): 
        return 
    else: 
        return tuple((v1[0] + t * (v2[0] - v1[0]), v1[1] + t * (v2[1] - v1[1]), z_p))

# print(_find_intersection(v1, v2, z_p))

# find intersection in triangle 

tri = [
    (1, 2, 3), 
    (4, 5, 6), 
    (7, 8, 9)
]

edges = [tri[i] for i in range(3)]

v1 = edges[0]
v2 = edges[1]
v3 = edges[2]

# print(_find_intersection(v1, v2, z_p))
# print(_find_intersection(v1, v3, z_p))
# print(_find_intersection(v2, v3, z_p))


def _intersect_triangle(tri, z_p):
    edges = [(tri[i], tri[(i + 1) % 3]) for i in range(3)]
    points = []
    for v1, v2 in edges:
        p = _find_intersection(v1, v2, z_p)
        if p:
            points.append(p)
    return points
        

print(_intersect_triangle(tri, z_p))