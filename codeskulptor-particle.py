import simplegui
import math

# global variables for frame

WIDTH = 800
HEIGHT = 500

# point list

point1 = (0, HEIGHT / 2 + 10)
point2 = (0, HEIGHT / 2 - 10)
point3 = (50, point2[1])
point4 = (50, point1[1])
point_list = [point1, point2, point3, point4]

midpoint = (0, HEIGHT / 2)

magnet_point = (600, 250)

# global variables
particle_group = set([])
xy_group = [midpoint]
xy_group_group = []

init_vel = [1.0, 0.0]
part_mass = 50.0
part_charge = 1.0

#part_mass_m = 1.0
part_charge_m = 1.0

# Particle class
class Particle:
    
    def __init__(self, pos, vel, accel, charge, mass, magn, magn_bool):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.accel = [accel[0], accel[1]]
        self.charge = charge
        self.mass = mass
        self.magn = magn
        self.magn_bool = False
        
    def update_old(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.vel[0] += self.accel[0]
        self.vel[1] += self.accel[1]
        
    def update(self):
        r = point_dist(self.pos, magnet_point)
        B = (self.magn / (r ** 3)) * 10 ** 6
        
        qbm = ((self.charge * B) / self.mass)
        
        
        self.vel[0] += self.vel[1] * qbm #+ self.accel[0]
        self.vel[1] += -1.0 * self.vel[0] * qbm #+ self.accel[1]
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
    def draw(self, canvas):
        canvas.draw_circle(self.pos, 5, 2, "Black")
        
    def line_d(self, canvas):
        global xy_group_group, xy_group, particle_group

        if self.pos[0] <= WIDTH and self.pos[1] <= HEIGHT:
            xy_group.append(tuple(self.pos))
            #canvas.draw_polyline(xy_group, 5, "Red")
            for pos in xy_group:
                canvas.draw_circle(pos, 1, 1, "Black", "Black")

        else:
            if len(xy_group) > 1:
                xy_group_group.append(list(xy_group)) 
                xy_group = []
                particle_group.pop(0)
                
            
# draw handler for canvas
def draw(canvas):
    #TEST
    canvas.draw_circle(magnet_point, 3, 2, "Blue")
    
    #if len(xy_group_group) > 0:
    #    print len(xy_group_group)
    
    # draw rectangle
    canvas.draw_polygon(point_list, 10, "Red", "Red")
    
    # draw particles
    part_draw(canvas, particle_group)
    
    # draw lines
    for part in particle_group:
        part.line_d(canvas)
        
    line_draw(canvas, xy_group_group)


# helper functions
def part_draw(canvas, group):
    for particle in group:
        particle.update()
        particle.draw(canvas)

def line_draw(canvas, group):
    for line in group:
        #canvas.draw_polyline(line, 5, "Purple")
        for pos in line:
            canvas.draw_circle(pos, 1, 1, "Purple", "Purple")
        
def part_var_update():
    global part
    part = Particle(midpoint, [2.0 * init_vel[0], init_vel[1]], [0.0, 0.1], part_charge, part_mass, 1.0, True)

def key_down(key):
    global part
    if key == simplegui.KEY_MAP['space']:
        particle_group.add(part)
        
def vel_inph_x(text_input):
    global init_vel
    
    init_vel[0] = float(text_input)
    
    part_var_update()
    
def vel_inph_y(text_input):
    global init_vel
    
    init_vel[1] = float(text_input)
    
    part_var_update()
    
def part_m(text_input):
    global part_mass, part
    
    part_mass_m = float(text_input)
    
    part_mass = part_mass * part_mass_m
    
    part_var_update()    
            
def part_ch(text_input):  
    global part_charge
    
    part_charge_m = float(text_input)
    
    part_charge = part_charge * part_charge_m
    
    part_var_update()
    
def point_dist(point1, point2):
    #distance = math.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))
    #test for x only
    distance = math.sqrt((point2[0] - point1[0]) ** 2)
    return distance

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_canvas_background("White")
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.add_input("init vel X", vel_inph_x, 50)
frame.add_input("init vel Y", vel_inph_y, 50)
frame.add_input("particle mass", part_m, 50)
frame.add_input("particle charge", part_ch, 50)

# particle list
part = Particle(midpoint, [2.0 * init_vel[0], init_vel[1]], [0.0, 0.1], part_charge, part_mass, 1.0, True)

# Start the frame animation
frame.start()