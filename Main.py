from Components import *
from PongComponents import *

import ComponentBuilder
import UpdaterManager


def main():

    t_def = ComponentBuilder.build_timeline("Default", 60)
    t_slow = ComponentBuilder.build_timeline("Slow", 60, 0.5)

    network = Component()
    network.add(Name("NetworkWrapper"))
    network.add(NetworkWrapper(3))
    network.activate()

    t_def.add_updatable(t_slow)
    t_slow.add_updatable(network)

    # collision test begin
    size = 10
    tri1 = ComponentBuilder.build_triangle("tri1", size)

    tri2 = ComponentBuilder.build_triangle("tri2", size)
    tri2.add(RandomPose(100, 100))
    tri2.pos.x += -7

    t_slow.add_updatable(tri1)
    t_slow.add_updatable(tri2)
    # collision test end

    UpdaterManager.start_loop()


if __name__ == "__main__":
    main()
