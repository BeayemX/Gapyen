from Components import *

import ComponentBuilder
import UpdaterManager


def main():

    t_def = Component()
    t_def.add(Name("Default"))
    t_def.add(Updater())
    t_def.add(Timeline(60))

    t_slow = Component()
    t_slow.add(Name("Slow"))
    t_slow.add(Updater())
    t_slow.add(Timeline(60, 0.5))
    t_slow.add(TimelineUpdatable())

    GameManager.register_timeline(t_def)  # todo init swhere
    GameManager.register_timeline(t_slow)

    t_def.activate()
    t_slow.activate()

    network = Component()
    network.add(NetworkWrapper(3))

    t_def.add_updatable(t_slow)
    t_slow.add_updatable(network)

    for i in range(5):
        size = 5
        t = Component()
        t.add(Name("tri"+str(i)))
        t.add(StaticTransform((i * size * 2, 0, 0), 0))
        t.add(Shape([[0, 0], [size, 0], [0, size/2]]))
        t.add(RandomPose(100, 100))

        t_slow.add_updatable(t)

    """
    size = 10
    t2 = Component()
    t2.add(Name("tri2"))
    t2.add(StaticTransform((0, 0, 0), 0))
    t2.add(Shape([[-size, -size], [0, size], [size, -size]]))
    t2.add(RandomPose(100, 100))
    t2.timeline = t_slow
    """
    UpdaterManager.start_loop()


if __name__ == "__main__":
    main()
