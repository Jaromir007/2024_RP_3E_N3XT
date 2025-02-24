import time

class GCodeGenerator:
    def __init__(self, layers, layer_height=0.2, extrusion_multiplier=0.05, speed=1500):
        self.layers = layers
        self.layer_height = layer_height
        self.extrusion_multiplier = extrusion_multiplier
        self.speed = speed
        self.e_value = 0 

    def distance(self, p1, p2):
        return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

    def generate_gcode(self):
        t = time.time()
        if not self.layers:
            return [";"]

        gcode = [
            "; START GCODE",
            "G21 ; Set units to millimeters",
            "G90 ; Absolute positioning",
            "M82 ; Absolute extrusion mode",
            "G28 ; Home all axes"
        ]

        for layer_index, layer in enumerate(self.layers):
            if not layer:
                continue

            z_height = self.layer_height * (layer_index + 1)
            gcode.append(f"G1 Z{z_height:.2f} F1200 ; Move to layer height {layer_index + 1}")

            start_x, start_y = layer[0]
            gcode.append(f"G0 X{start_x:.2f} Y{start_y:.2f} F3000 ; Move to start of layer {layer_index + 1}")

            for i in range(1, len(layer)):
                x, y = layer[i]
                e_increment = self.distance(layer[i - 1], (x, y)) * self.extrusion_multiplier
                self.e_value += e_increment
                gcode.append(f"G1 X{x:.2f} Y{y:.2f} E{self.e_value:.4f} F{self.speed}")

            e_increment = self.distance(layer[-1], layer[0]) * self.extrusion_multiplier
            self.e_value += e_increment
            gcode.append(f"G1 X{start_x:.2f} Y{start_y:.2f} E{self.e_value:.4f} F{self.speed}")

        gcode.extend([
            "G1 Z10 F1200 ; Lift nozzle",
            "G0 X0 Y0 ; Move to home",
            "M104 S0 ; Turn off extruder",
            "M140 S0 ; Turn off bed",
            "M107 ; Turn off fan",
            "M84 ; Disable motors",
            "; END GCODE"
        ])

        print(f"[INFO] Generated {len(gcode)} lines of G-code")
        print(f"[TIMING] GCode generation: {time.time() - t:.4f}s")
        return gcode
