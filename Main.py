from Components import *
from PongComponents import *
import PongComponents

import ComponentBuilder
import UpdaterManager


def main():

    # create timelines
    t_def = ComponentBuilder.build_timeline("Default", 60)
    t_slow = ComponentBuilder.build_timeline("Network", 5)
    time_physics = ComponentBuilder.build_timeline("Physics", 60)

    # create controller
    physics_controller = Component()
    physics_controller.add(Name("Physics Controller"))
    physics_controller.add(PhysicsController())
    physics_controller.activate()
    # fixme shouldnt add updatable to timeline. should call updatable.usetimeline("aasdf")
    time_physics.register_updatable(physics_controller)


    # network controller
    network = Component()
    network.add(Name("NetworkWrapper"))
    network.add(NetworkWrapper(3))
    network.activate()

    # add stuff to timelines
    # fixme super annoying to add all timelines to default timeline manually
    t_def.register_updatable(t_slow)
    t_def.register_updatable(time_physics)
    t_slow.register_updatable(network)

    # create objects
    ball = PongComponents.build_ball()
    paddle0 = PongComponents.build_paddle("paddle0")
    paddle0.pos.x = -40

    paddle1 = PongComponents.build_paddle("paddle1")
    paddle1.pos.x = 40

    t_def.register_updatable(ball)
    t_def.register_updatable(paddle0)
    t_def.register_updatable(paddle1)

    # start game
    UpdaterManager.start_loop()


if __name__ == "__main__":
    main()
