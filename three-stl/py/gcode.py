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

        first_point = layer[0]
        gcode.append(f"G1 X{first_point[0]:.3f} Y{first_point[1]:.3f} F{feedrate}")  

        prev_x, prev_y = first_point
        extruder_position = 0  

        for x, y in layer[1:]:
            distance = math.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
            extrusion = distance * extrusion_multiplier

            extruder_position += extrusion
            gcode.append(f"G1 X{x:.3f} Y{y:.3f} E{extruder_position:.5f} F{feedrate}")

            prev_x, prev_y = x, y

        current_z += layer_height 

    # G-code Footer (TODO fix)
    gcode.append("G92 E0 ; ")
    gcode.append("M104 S0 ; ")
    gcode.append("M140 S0 ; ")
    gcode.append("M84 ; ")

    return "\n".join(gcode)