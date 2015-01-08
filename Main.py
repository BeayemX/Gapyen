from Components import *

import ComponentBuilder


def main():

    t_def = Component()
    t_def.add(Name("Default"))
    t_def.add(Timeline(t_def.name))

    t_slow = Component()
    t_slow.add(Name("Slow"))
    t_slow.add(Timeline(t_slow.name, timescale=0.5))


    GameManager.register_timeline(t_def.name, t_def) # todo name via uid componenet?
    GameManager.register_timeline(t_slow.name, t_slow) # todo name via uid componenet?

    t_def.activate()
    t_slow.activate()



    network = Component()
    network.add(NetworkWrapper("Default"))
    """
    triangle = ComponentBuilder.build_triangle("triangle1")
    triangle.add(RandomPose(100, 100))

    triangle2 = ComponentBuilder.build_triangle("trianlge2")
    triangle2.add(RandomPose(50, 0))
    triangle2.timeline = t_slow
    """


    size = 5
    t = Component()
    t.add(Name("tri1"))
    t.add(StaticTransform((0, 0, 0), 0))
    t.add(Shape([[-size, -size], [0, size], [size, -size]]))
    t.add(RandomPose(100, 100))

    size = 10
    t2 = Component()
    t2.add(Name("tri2"))
    t2.add(StaticTransform((0, 0, 0), 0))
    t2.add(Shape([[-size, -size], [0, size], [size, -size]]))
    t2.add(RandomPose(100, 100))
    t2.timeline = t_slow


    UpdaterManager.startLoop()


if __name__ == "__main__":
    main()
