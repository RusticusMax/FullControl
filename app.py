# Using FullControL.
# This is a simple example of how to use FullControl to generate a design and export it to gcode.
# FullControl is a free, open-source, 3D printing design and gcode generation tool.
# FullControl is available at https://github.com/FullControlXYZ/fullcontrol
# or pip install git+https://github.com/FullControlXYZ/fullcontrol
# or clone the repo and run pip install for the directory
# Models at https://fullcontrol.xyz/#/models

import fullcontrol as fc
import math

# printer/gcode parameters

design_name = 'my_design'
nozzle_temp = 220
bed_temp = 60
print_speed = 1000
printer_name= 'ender_3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0 / prusa_i3

# design parameters

EW = 0.4 # extrusion width
EH = 0.3 # extrusion height (and layer height)
initial_z = EH*0.3 # initial nozzle position is set to 0.6x the extrusion height to get a bit of 'squish' for good bed adhesion
layers = 100 # number of layers]
wall_cnt = 1 # number of walls
spin = 0.02 # angle of rotation of the design
steps = []

# centre_point = fc.Point(x=10, y=10, z=0)
enclosing_radius = 10
start_angle = 0
sides = 6
center_x = 75
center_y = 75
clockwise = True
for layer in range(layers):
  for wall in range(wall_cnt):
    for point in fc.polygonXY(fc.Point(x=center_x, y=center_y, z=initial_z+EH*layer), enclosing_radius+EW*wall, start_angle+layer*spin, sides, clockwise):
      steps.append(point)
  # steps.append(fc.PlotAnnotation(point=steps[-1], label="start/end"))
  # steps.append(fc.PlotAnnotation(point=steps[1], label="first point after start"))
  # steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
plot_data = fc.transform(steps, 'plot') # , fc.PlotControls(color_type='print_sequence'))


# steps.append(fc.Point(x=75, y=75, z=initial_z))
# steps.append(fc.Point(x=100, y=75, z=initial_z))
# steps.append(fc.Point(x=100, y=100, z=initial_z))
# steps.append(fc.Point(x=75, y=100, z=initial_z))
# for layer in range(layers):
#   for wall in range(4):
#     steps.append(fc.Point(x=75-wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
#     steps.append(fc.Point(x=75-wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
#     steps.append(fc.Point(x=100+wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
#     steps.append(fc.Point(x=100+wall*EW, y=100+wall*EW, z=initial_z+layer*EH))
#     steps.append(fc.Point(x=75-wall*EW, y=100+wall*EW, z=initial_z+layer*EH))
#     steps.append(fc.Point(x=75-wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
  
# instead of the above for-loop code, you can create the exact same design using built-in FullControl functions (uncomment the next two lines):
# rectangle_steps = fc.rectangleXY(fc.Point(x=75, y=75, z=initial_z), 75, 75)
# steps = fc.move(rectangle_steps, fc.Vector(z=EH), copy=True, copy_quantity=layers)
# preview the design

# plot_data = fc.transform(steps, 'plot')
# # uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
# # fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True)) 

# create and download gcode for the design
gcode_controls = fc.GcodeControls(
    printer_name = printer_name, 
    save_as = design_name,
    initialization_data={
    'primer': 'front_lines_then_y', 
    'print_speed': print_speed,
    "nozzle_temp": nozzle_temp,
    "bed_temp": bed_temp,
    "extrusion_width": EW,
    "extrusion_height": EH})
gcode = fc.transform(steps, 'gcode', gcode_controls)


## These functions are untested and some un finished.   I need to look deeper inyto full control to see how to use it.
def makespiral(steps, layer, EW, EH, initial_z, steps_per_layer, radius, angle) -> list():
  for step in range(steps_per_layer):
    steps.append(fc.Point(x=radius*math.cos(angle), y=radius*math.sin(angle), z=initial_z+layer*EH))
    angle += 2*math.pi/steps_per_layer
    radius += EW
  return steps

def make_square(steps, len_top, len_side, lower_left, num_layers, num_walls, EW, EH, initial_z) -> list():
  ''' return a Square of num_layers layers, each layer is num_walls walls thick, EW is the extrusion width, EH is the extrusion height, 
      and initial_z is the initial z position.  len_top is the length of the top and bottom, len_side is the length of the sides.
      lower_left is the lower left corner of the square.
  '''

  for layer in range(num_layers):
    for wall in range(num_walls):
      steps.append(fc.Point(x=lower_left-wall*EW, y=lower_left-wall*EW, z=initial_z+layer*EH))
      steps.append(fc.Point(x=lower_left-wall*EW, y=lower_left-wall*EW, z=initial_z+layer*EH))
      steps.append(fc.Point(x=lower_left+len_top+wall*EW, y=lower_left-wall*EW, z=initial_z+layer*EH))
      steps.append(fc.Point(x=lower_left+len_top+wall*EW, y=lower_left+len_side+wall*EW, z=initial_z+layer*EH))
      steps.append(fc.Point(x=lower_left-wall*EW, y=100+wall*EW, z=initial_z+layer*EH))
      steps.append(fc.Point(x=lower_left-wall*EW, y=lower_left-wall*EW, z=initial_z+layer*EH))
  return steps

def make_polygon(points: list(), num_layers, num_walls, EW, EH, initial_z) -> list():
  ''' return a Polygon of num_layers layers, each layer is num_walls walls thick, EW is the extrusion width, EH is the extrusion height, 
      and initial_z is the initial z position.  radius is the radius of the polygon, and lower_left is the lower left corner of the polygon.
  '''
  steps = []

  for layer in range(num_layers):
    for wall in range(num_walls):
      for x1, y1 in points:
        steps.append(fc.Point(x=radius*math.cos(angle)+lower_left, y=radius*math.sin(angle)+lower_left, z=initial_z+layer*EH))
  return steps

def is_point_inside_polygon(point, polygon):
    """
    Written by ChatGPT (4/2/23) 
    Check if a point is inside a polygon.

    Parameters:
    - point: a tuple or list of two numbers representing the (x, y) coordinates of the point.
    - polygon: a list of tuples or lists of two numbers representing the (x, y) coordinates of the vertices of the polygon, in order.

    Returns:
    - True if the point is inside the polygon, False otherwise.
    """
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if point[1] > min(p1y, p2y):
            if point[1] <= max(p1y, p2y):
                if point[0] <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (point[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or point[0] <= xinters:
                            inside = not inside
        p1x, p1y = p2x, p2y

    return inside