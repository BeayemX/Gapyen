from Components.Component import Component
from Components.StaticPose import StaticTransform
from Components.Shape import Shape


def build_triangle():
    c = Component()
    c.add(StaticTransform((0, 0, 0), 0))
    c.add(Shape([[-1, -1], [1, -1], [0, 1]]))
    return c