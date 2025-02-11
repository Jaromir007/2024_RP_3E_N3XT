import math

def generate_gcode(layers, layer_height=0.2, extrusion_multiplier=0.05, feedrate=1500):
    gcode = []
    
    # G-code Header (TODO fix)
    gcode.append("G21 ; ")
    gcode.append("G90 ; ")
    gcode.append("M82 ; ")
    gcode.append("G28 ; ")
    gcode.append("G92 E0 ;")

    current_z = 0.2  # Layer Z height
    for layer in layers:
        gcode.append(f"G1 Z{current_z:.2f} F{feedrate}")  
        
        if not layer:
            continue  

        p = layer[0]
        gcode.append(f"G1 X{p[0]:.3f} Y{p[1]:.3f} F{feedrate}")  

        x2, y2 = p
        extruder_position = 0  

        for x1, y1 in layer[1:]:
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            extrusion = distance * extrusion_multiplier

            extruder_position += extrusion
            gcode.append(f"G1 X{x1:.3f} Y{y1:.3f} E{extruder_position:.5f} F{feedrate}")

            x2, y2 = x1, y1

        current_z += layer_height 

    # G-code Footer (TODO fix)
    gcode.append("G92 E0 ; ")
    gcode.append("M104 S0 ; ")
    gcode.append("M140 S0 ; ")
    gcode.append("M84 ; ")

    return "\n".join(gcode)