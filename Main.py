from Components import *
from PongComponents import *
import PongComponents

import ComponentBuilder
import UpdaterManager
import settings


def main():

    # create timelines
    t_def = ComponentBuilder.build_timeline("DefaultTimeline", 60)
    t_slow = ComponentBuilder.build_timeline("Network", 5)
    t_slow.use_updater(t_def)
    time_physics = ComponentBuilder.build_timeline("Physics", 60)
    time_physics.use_updater(t_def)


    # create controller
    physics_controller = Component()
    physics_controller.add(Name("Physics Controller"))
    physics_controller.add(PhysicsController())
    physics_controller.activate()
    physics_controller.use_updater(time_physics)


    # network controller
    network = Component()
    network.add(Name("NetworkWrapper"))
    network.add(NetworkWrapper(3))
    network.activate()
    network.use_updater(t_slow)

    # create objects
    # world frame

    # leftwall = PongComponents.build_wall("Left Wall", 12, 7)

    wallwidth = 2
    leftwall = PongComponents.build_wall(
        "Left Wall",
        wallwidth,
        settings.worldWidth * settings.aspect - wallwidth)
    leftwall.pos.x = -(settings.worldWidth/2 - wallwidth/2)

    rightwall = PongComponents.build_wall(
        "Right Wall",
        wallwidth,
        settings.worldWidth * settings.aspect - wallwidth)
    rightwall.pos.x = settings.worldWidth/2 - wallwidth/2

    topwall = PongComponents.build_wall(
        "Top Wall",
        settings.worldWidth - wallwidth,
        wallwidth
    )
    topwall.pos.y = -(settings.worldWidth/2 * settings.aspect - wallwidth/2)


    bottomwall = PongComponents.build_wall(
        "Bottom Wall",
        settings.worldWidth - wallwidth,
        wallwidth
    )
    bottomwall.pos.y = settings.worldWidth/2 * settings.aspect - wallwidth/2


    # interactive stuff
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
