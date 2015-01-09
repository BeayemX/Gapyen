from Components import *

import ComponentBuilder


def main():

    t_def = Component()
    t_def.add(Name("Default"))
    t_def.add(Updater())
    t_def.add(Timeline(20))

    t_slow = Component()
    t_slow.add(Name("Slow"))
    t_slow.add(Updater())
    t_slow.add(Timeline(5))
    t_slow.add(TimelineUpdater())


    GameManager.register_timeline(t_def)  # todo init swhere
    GameManager.register_timeline(t_slow)
    # GameManager.register_timeline(t_slow)

    t_def.activate()
    t_slow.activate()

    """
    timesource = Component()
    timesource.add(TimeSource.get_instance())
    timesource.add(Name("Default"))
    GameManager.register_timeline(timesource)
    """

    network = Component()
    network.add(NetworkWrapper("Default"))

    size = 5
    t = Component()
    t.add(Name("tri1"))
    t.add(StaticTransform((0, 0, 0), 0))
    t.add(Shape([[0, 0], [size, 0], [0, size/2]]))
    t.add(RandomPose(100, 100))



    t_def.add_updatable(t_slow)
    t_def.add_updatable(t)

    t_slow.add_updatable(network)




    """
    size = 10
    t2 = Component()
    t2.add(Name("tri2"))
    t2.add(StaticTransform((0, 0, 0), 0))
    t2.add(Shape([[-size, -size], [0, size], [size, -size]]))
    t2.add(RandomPose(100, 100))
    t2.timeline = t_slow
    """
    UpdaterManager.startLoop()


if __name__ == "__main__":
    main()
