class GCodeGenerator:
    def __init__(self, layer_height=0.2, nozzle_diameter=0.4, filament_diameter=1.75):
        self.layer_height = layer_height
        self.nozzle_diameter = nozzle_diameter
        self.filament_area = math.pi * (filament_diameter / 2) ** 2
        self.gcode = []
        self.e_position = 0

    def add_header(self):
        self.gcode.extend([
            "G21 ; Set units to mm",
            "G90 ; Absolute positioning",
            "M104 S200 ; Set extruder temperature",
            "M109 S200 ; Wait for temperature",
            "M82 ; Extruder absolute mode",
            "G28 ; Home all axes",
            "G92 E0 ; Reset extrusion distance"
        ])

    def add_footer(self):
        self.gcode.extend([
            "M104 S0 ; Turn off extruder",
            "M140 S0 ; Turn off bed",
            "M84 ; Disable motors"
        ])

    def calculate_extrusion(self, distance):
        return round((distance * self.nozzle_diameter * self.layer_height) / self.filament_area, 5)

    def generate_layer(self, contours, z_height):
        self.gcode.append(f"G0 Z{z_height:.2f} F120 ;")
        current_z = 0; 
        for contour in contours:
            self.gcode.append(f"G0 X{contour[0][0]:.2f} Y{contour[0][1]:.2f} F3000 ;")
            for i in range(1, len(contour)):
                x1, y1 = contour[i - 1]
                x2, y2 = contour[i]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                e_value = self.calculate_extrusion(distance)
                self.e_position += e_value
                self.gcode.append(f"G1 X{x2:.2f} Y{y2:.2f} E{self.e_position:.5f} F1200 ;")

            self.gcode.append(f"G0 Z{current_z + self.layer_height:.2f} F120 ; Move up")
            self.gcode.append(f"G1 X{contour[0][0]:.2f} Y{contour[0][1]:.2f} E{self.e_position:.5f} ;")
            current_z += self.layer_height

    def generate_gcode(self, layers):
        self.add_header()
        z_height = self.layer_height
        for contours in layers:
            self.generate_layer(contours, z_height)
            z_height += self.layer_height
        self.add_footer()
        return "\n".join(self.gcode)