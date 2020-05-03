import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print(symbols)
    for command in commands:
        print(command)
        cmd = command['op']
        try:
            args = command['args']
        except:
            pass
        try:
            constants = command['constants']
        except:
            pass
            
        if cmd == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        
        elif cmd == 'pop':
            stack.pop()
            
        elif cmd == 'move':
            t = make_translate(args[0], args[1], args[2])
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        
        elif cmd == 'rotate':
            theta = args[1] * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        
        elif cmd == 'scale':
            t = make_scale(args[0], args[1], args[2])
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        
        elif cmd == 'box':
            add_box(coords,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], coords )
            draw_polygons(coords, screen, zbuffer, view, ambient, light, symbols, constants)
            coords = []
        
        elif cmd == 'sphere':
            add_sphere(coords,
                    args[0], args[1], args[2],
                    args[3], step_3d)
            matrix_mult( stack[-1], coords )
            draw_polygons(coords, screen, zbuffer, view, ambient, light, symbols, constants)
            coords = []
         
        elif cmd == 'torus':
            add_torus(coords,
                    args[0], args[1], args[2],
                    args[3], args[4], step_3d)
            matrix_mult( stack[-1], coords )
            draw_polygons(coords, screen, zbuffer, view, ambient, light, symbols, constants)
            coords = []
        
        elif cmd == 'line':
            add_edge( coordsl,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( stack[-1], edges )
            draw_lines(coordsl, screen, zbuffer, color)
            coordsl = []
        
        elif cmd == 'save':
            save_extension(screen, args[0])
        
        elif cmd == 'display':
            display(screen)
            
            
            
            
            
            
            
            
            
            
