# Using FullControL.
# This is a simple example of how to use FullControl to generate a design and export it to gcode.
# FullControl is a free, open-source, 3D printing design and gcode generation tool.
# FullControl is available at https://github.com/FullControlXYZ/fullcontrol
# or pip install git+https://github.com/FullControlXYZ/fullcontrol
# or clone the repo and run pip install for the directory
# Models at https://fullcontrol.xyz/#/models

import fullcontrol as fc

# printer/gcode parameters

design_name = 'my_design'
nozzle_temp = 220
bed_temp = 40
print_speed = 1000
printer_name= 'ender_3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0 / prusa_i3

# design parameters

EW = 0.4 # extrusion width
EH = 0.3 # extrusion height (and layer height)
initial_z = EH*0.4 # initial nozzle position is set to 0.6x the extrusion height to get a bit of 'squish' for good bed adhesion
layers = 25 # number of layers


# MLW There has to be a way in fulcontrol to darw parmiter walls (similar to tge way fc.rectangleXY works, but increasing parameter size by EW each time)
# Here we have to just make sure we are subtracting EW from the lower cordinates and adding it to the higher cordinates
steps = []
# steps.append(fc.Point(x=75, y=75, z=initial_z))
# steps.append(fc.Point(x=100, y=75, z=initial_z))
# steps.append(fc.Point(x=100, y=100, z=initial_z))
# steps.append(fc.Point(x=75, y=100, z=initial_z))
for layer in range(1, layers):
  for wall in range(4):
    steps.append(fc.Point(x=75-wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
    steps.append(fc.Point(x=75-wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
    steps.append(fc.Point(x=100+wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
    steps.append(fc.Point(x=100+wall*EW, y=100+wall*EW, z=initial_z+layer*EH))
    steps.append(fc.Point(x=75-wall*EW, y=100+wall*EW, z=initial_z+layer*EH))
    steps.append(fc.Point(x=75-wall*EW, y=75-wall*EW, z=initial_z+layer*EH))
  
# instead of the above for-loop code, you can create the exact same design using built-in FullControl functions (uncomment the next two lines):
# rectangle_steps = fc.rectangleXY(fc.Point(x=75, y=75, z=initial_z), 75, 75)
# steps = fc.move(rectangle_steps, fc.Vector(z=EH), copy=True, copy_quantity=layers)
# preview the design

plot_data = fc.transform(steps, 'plot')
# uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
# fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True)) 

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