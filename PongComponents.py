import EventSystem

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


def build_ball():
    c = Component()
    c.add(Name("Ball"))
    c.add(Transform())
    c.add(Shape([[-1, 0], [0, 1], [1, 0], [0, -1]]))
    c.add(AABB())
    c.add(Body(Vec2(20, 20)))
    c.add(BallLogic())
    c.activate()
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
        TimeUpdatable.activate(self)  # todo does this write the self.update into the gameobject?

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

    def activate(self):
        CollisionHandler.activate(self)
        TimeUpdatable.activate(self)
        EventSystem.add_eventlistener("Restart", self.handle_restart)

    def deactivate(self):
        self.gameobject.handle_collision = CollisionHandler.handle_collision
        self.gameobject.update = TimeUpdatable.update
        TimeUpdatable.deactivate()
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

            self.gameobject.velocity.x = -self.gameobject.velocity.x

        if other.tag == "Wall":
            self.gameobject.velocity.y = -self.gameobject.velocity.y
        elif other.tag == "DeathZone":
            EventSystem.trigger_event("Restart")

    def handle_restart(self):
        self.gameobject.velocity.x = -self.gameobject.velocity.x
        self.gameobject.pos = Vec2(0, 0)

    def update(self, delta):
        TimeUpdatable.update(self, delta)
        #self.gameobject.rotate_by(1 * delta)
