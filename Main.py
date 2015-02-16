from eventsystem import EventSystem

import ComponentBuilder
import UpdaterManager

from AsteroidsComponents import *


def main():

    # create timelines
    timeline_default = ComponentBuilder.build_timeline("DefaultTimeline", 60)

    networkupdates = ComponentBuilder.build_timeline("NetworkUpdates", 60)
    networkupdates.use_updater(timeline_default)

    posetransmitterupdates = ComponentBuilder.build_timeline("posetransmitterupdates", 60)
    posetransmitterupdates.use_updater(timeline_default)

    timeline_physics = ComponentBuilder.build_timeline("Physics", 60)
    timeline_physics.use_updater(timeline_default)

    timeline_events = ComponentBuilder.build_timeline("EventTimeline", 60)
    timeline_events.use_updater(timeline_default)

    # create Event System
    eventSys = Component()
    eventSys.add(Name("Event System"))
    eventSys.add(EventSystem())
    eventSys.activate()
    eventSys.use_updater(timeline_events)
    eventsystem.instance = eventSys

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
    network.use_updater(networkupdates)

    posetransmitter = Component()
    posetransmitter.add(Name("PoseTransmitter"))
    posetransmitter.add(PoseTransmitter())
    posetransmitter.activate()
    posetransmitter.use_updater(posetransmitterupdates)

    """########## collider move out test
    width = 10
    halfwidth = width / 2
    a = Component()
    a.add(Name("box1"))
    a.add(Transform())
    a.add(Shape([[-halfwidth, - halfwidth], [-halfwidth, halfwidth], [halfwidth, halfwidth], [halfwidth, -halfwidth]]))
    a.add(Body())
    a.add(AABB())
    a.add(CollisionHandler(True))
    a.activate()

    b = Component()
    b.add(Name("box2"))
    b.add(Transform([0,0]))
    b.add(Shape([[-halfwidth, - halfwidth], [-halfwidth, halfwidth], [halfwidth, halfwidth], [halfwidth, -halfwidth]]))
    b.add(Body(Vec2(-1, -0.5)))
    b.add(AABB())
    b.add(CollisionHandler())
    b.activate()

    ########### collider test end"""


    """ pong
    # create objects
    # world frame
    wallwidth = 2
    leftwall = PongComponents.build_wall(
        "Left Wall",
        wallwidth,
        settings.worldWidth * settings.aspect - wallwidth,
        tag="DeathZone"
    )
    leftwall.pos.x = -(settings.worldWidth/2 - wallwidth/2)

    rightwall = PongComponents.build_wall(
        "Right Wall",
        wallwidth,
        settings.worldWidth * settings.aspect - wallwidth,
        tag="DeathZone"
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
    num = 1
    for i in range(num):
        alpha = 360.0 / num * i
        ball = PongComponents.build_ball("ball" + str(i))
        direction = Vec2(math.cos(alpha), math.sin(alpha))
        ball.acceleration = direction * settings.ballspeed

    #raise Exception("asdf")

    paddle0 = PongComponents.build_paddle("paddle0")
    paddle0.pos.x = -40

    paddle1 = PongComponents.build_paddle("paddle1")
    paddle1.pos.x = 40

    timeline_default.register_updatable(ball)
    timeline_default.register_updatable(paddle0)
    timeline_default.register_updatable(paddle1)
    #"""


    # asteroids
    build_ship("Ship1")
    build_ship("Ship2").pos += Vec2(10, 0)

    eventsystem.instance.send_event("LevelClear")
    build_gui()
    build_asteroid_spawn_controller()


    # start game
    UpdaterManager.start_loop()


if __name__ == "__main__":
    main()
