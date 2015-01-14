from Components import *


def build_triangle(name, size):
    c = Component()

    c.add(Name(name))
    c.add(StaticTransform((size * 2, 0, 0), 0))
    c.add(Shape([[0, 0], [size, 0], [0, size/2]]))
    c.add(Updatable())
    #c.add(RandomPose(100, 100))
    c.add(AABB())
    c.add(Body())
    c.activate()
    return c


def build_timeline(name, updates_per_sec, timescale=1.0):
    c = Component()
    c.add(Name(name))
    c.add(Updater())
    c.add(Timeline(updates_per_sec, timescale))
    c.add(TimelineUpdatable())
    c.activate()
    return c
