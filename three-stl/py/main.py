import json
import struct
from slicer import Slicer
from gcode import generate_gcode


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



triangles = parseSTL("../models/3dbenchy.stl")

slicer = Slicer()
layers = slicer.slice(triangles)
gcode = generate_gcode(layers)

with open("../models/benchy-sliced.json", "w") as f:
    json.dump(layers, f, indent=2)

with open("../models/benchy-gcode.gcode", "w") as g:
    g.write(gcode)

print("Slicing complete!")
