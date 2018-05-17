import mdl
from display import *
from matrix import *
from draw import *


def sanitize(c):

    if (c[0] == "rotate" or c[0] =="save" or c == "display"):
        return c

    retVal = [c[0]]
    x = 1

    while x < len(c):
        if isinstance(c[x], float):
            retVal.append(c[x])
        x = x + 1

    return tuple(retVal)

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    systems = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    polygons = []
    step_3d = 20
    edges = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
        for args in commands:
            args = sanitize(args)
            
            if args[0] == 'sphere':

                add_sphere(polygons,
                           float(args[1]), float(args[2]), float(args[3]),
                           float(args[4]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif args[0] == 'torus':

                add_torus(polygons,
                          float(args[1]), float(args[2]), float(args[3]),
                          float(args[4]), float(args[5]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
                
            elif args[0] == 'box':

                add_box(polygons,
                        float(args[1]), float(args[2]), float(args[3]),
                        float(args[4]), float(args[5]), float(args[6]))
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif args[0] == 'line':

                add_edge( edges,
                          float(args[1]), float(args[2]), float(args[3]),
                          float(args[4]), float(args[5]), float(args[6]) )
                matrix_mult( systems[-1], edges )
                draw_lines(eges, screen, zbuffer, color)
                edges = []
                
            elif args[0] == 'scale':
                
                t = make_scale(float(args[1]), float(args[2]), float(args[3]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
                
            elif args[0] == 'move':
                
                t = make_translate(float(args[1]), float(args[2]), float(args[3]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
                
            elif args[0] == 'rotate':

                theta = float(args[2]) * (math.pi / 180)
                if args[1] == 'x':
                    t = make_rotX(theta)
                elif args[1] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]

            elif args[0] == 'push':
                systems.append( [x[:] for x in systems[-1]] )

            elif args[0] == 'pop':
                systems.pop()

            elif args[0] == 'display':
                display(screen)

            elif args[0] == 'save':
                save_extension(screen, args[1]+args[2])

    else:
        print "Parsing failed."
        return
