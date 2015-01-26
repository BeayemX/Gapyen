import eventsystem

from Components import *


def build_paddle(name):
    c = Component()
    c.add(Name(name))
    c.add(Tag("Paddle"))
    c.add(Transform())
    c.add(Shape([[-1, -10], [-1, 10], [1, 10], [1, -10]]))
    c.add(AABB())
    c.add(Body())
    c.add(PaddleLogic())
    c.activate()
    return c


def build_ball(name):
    c = Component()
    c.add(Name(name))
    c.add(Tag("Ball"))
    c.add(Transform())
    c.add(Shape([[-1, -1], [-1, 1], [1, 1], [1, -1]]))
    c.add(AABB())
    c.add(Body(acceleration=Vec2(1, 1).normalized() * settings.ballspeed))
    c.add(BallLogic())
    c.activate()
    #c.acceleration = Vec2(1, 1) * settings.ballspeed
    return c


def build_wall(name, width, height, tag="Wall"):
    c = Component()
    c.add(Name(name))
    c.add(Tag(tag))
    c.add(Transform())
    c.add(Shape([[-width/2, -height/2], [-width/2, height/2],
                 [width/2, height/2], [width/2, -height/2]]))
    c.add(AABB())
    c.add(CollisionHandler())
    c.activate()
    return c


class PaddleLogic(CollisionHandler, TimeUpdatable):
    def __init__(self):
        CollisionHandler.__init__(self)
        TimeUpdatable.__init__(self)

    def activate(self):
        CollisionHandler.activate(self)
        TimeUpdatable.activate(self)

    def deactivate(self):
        CollisionHandler.deactivate(self)
        TimeUpdatable.deactivate(self)

    def update(self, delta):
        TimeUpdatable.update(self, delta)

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)


class BallLogic(CollisionHandler, TimeUpdatable):
    def __init__(self):
        CollisionHandler.__init__(self)
        TimeUpdatable.__init__(self)
        self.out_of_game = False

    def activate(self):
        CollisionHandler.activate(self)
        TimeUpdatable.activate(self)

        eventsystem.instance.register_event_listener(
            eventsystem.EventType.ResetGame,
            self.handle_restart)

    def deactivate(self):
        eventsystem.instance.add_eventlistener(
            eventsystem.EventType.ResetGame,
            self.handle_restart)

        TimeUpdatable.deactivate(self)
        CollisionHandler.deactivate(self)

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)
        if other.tag == "Paddle":
            if self.gameobject.velocity.x > 0:  # right paddle
                if self.gameobject.pos.x > other.pos.x - other.aabb.radius.x:
                    return
            else:  # left paddle
                if self.gameobject.pos.x < other.pos.x + other.aabb.radius.x:
                    return

            hitpoint_y = self.gameobject.pos.y - other.pos.y
            sign = self.gameobject.velocity.x / abs(self.gameobject.velocity.x)

            direction = Vec2(sign * -1 * other.aabb.radius.y, hitpoint_y)
            direction.normalize()

            self.gameobject.acceleration = direction * settings.ballspeed
            self.gameobject.velocity.x = -self.gameobject.velocity.x

        elif other.tag == "Wall":
            self.gameobject.acceleration.y = -self.gameobject.acceleration.y
            self.gameobject.velocity.y = -self.gameobject.velocity.y

        elif other.tag == "DeathZone":
            if not self.out_of_game:
                self.out_of_game = True
                eventsystem.instance.send_event_after_sec(eventsystem.EventType.ResetGame, 2)
                # self.gameobject.acceleration.x = -self.gameobject.acceleration.x

    def handle_restart(self):
        self.gameobject.acceleration.x = -self.gameobject.acceleration.x
        self.gameobject.velocity = Vec2(0, 0)
        self.gameobject.pos = Vec2(0, 0)
        self.out_of_game = False

    def update(self, delta):
        TimeUpdatable.update(self, delta)
        #self.gameobject.rotate_by(5 * delta)
