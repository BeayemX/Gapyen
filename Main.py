from Components import *
from PongComponents import *
import PongComponents

import ComponentBuilder
import UpdaterManager
import settings


def main():

    # create timelines
    timeline_default = ComponentBuilder.build_timeline("DefaultTimeline", 60)

    timeline_network_updates = ComponentBuilder.build_timeline("NetworkUpdates", 60)
    timeline_network_updates.use_updater(timeline_default)

    timeline_network_gameobjects_transmitter = ComponentBuilder.build_timeline("NetworkGOTransmitter", 3)
    timeline_network_gameobjects_transmitter.use_updater(timeline_default)

    timeline_physics = ComponentBuilder.build_timeline("Physics", 60)
    timeline_physics.use_updater(timeline_default)


    # create controller
    physics_controller = Component()
    physics_controller.add(Name("Physics Controller"))
    physics_controller.add(PhysicsController())
    physics_controller.activate()
    physics_controller.use_updater(timeline_physics)


    # network controller
    network = Component()
    network.add(Name("NetworkWrapper"))
    network.add(NetworkWrapper(3))
    network.activate()
    network.use_updater(timeline_network_updates)

    posetransmitter = Component()
    posetransmitter.add(Name("PoseTransmitter"))
    posetransmitter.add(PoseTransmitter())
    posetransmitter.activate()
    posetransmitter.use_updater(timeline_network_gameobjects_transmitter)



    # create objects
    # world frame
    wallwidth = 2
    leftwall = PongComponents.build_wall(
        "Left Wall",
        wallwidth,
        settings.worldWidth * settings.aspect - wallwidth,
        "DeathZone"
    )
    leftwall.pos.x = -(settings.worldWidth/2 - wallwidth/2)

    rightwall = PongComponents.build_wall(
        "Right Wall",
        wallwidth,
        settings.worldWidth * settings.aspect - wallwidth,
        "DeathZone"
    )

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

    timeline_default.register_updatable(ball)
    timeline_default.register_updatable(paddle0)
    timeline_default.register_updatable(paddle1)

    # start game
    UpdaterManager.start_loop()


if __name__ == "__main__":
    main()
