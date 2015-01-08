from Components import *

def build_triangle(name):
    c = Component()
    c.add(Name(name))
    c.add(StaticTransform((0, 0, 0), 0))
    c.add(Shape([[-1, -1], [1, -1], [0, 1]]))
    return c