from Components import *

import ComponentBuilder
import UpdaterManager


def main():

    t_def = ComponentBuilder.build_timeline("Default", 60)
    t_slow = ComponentBuilder.build_timeline("Slow", 60, 0.5)

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

    UpdaterManager.start_loop()


if __name__ == "__main__":
    main()
