from Components import *


def build_paddle(name):
    c = Component()
    c.add(Name(name))
    c.add(Transform())
    c.add(Shape([[-1, -10], [-1, 10], [1, 10], [1, -10]]))
    c.add(AABB())
    c.add(PaddleLogic())
    c.activate()
    return c


def build_ball():
    c = Component()
    c.add(Name("Ball"))
    c.add(Transform())
    c.add(Shape([[-1, 0], [0, 1], [1, 0], [0, -1]]))
    c.add(AABB())
    c.add(Body(Vec2(20, 0)))
    c.add(BallLogic())
    c.activate()
    return c


class PaddleLogic(CollisionHandler, Updatable):
    def __init__(self):
        CollisionHandler.__init__(self)
        Updatable.__init__(self)

    def activate(self):
        CollisionHandler.activate(self)
        Updatable.activate(self)  # todo does this write the self.update into the gameobject?

    def deactivate(self):
        CollisionHandler.deactivate(self)
        Updatable.deactivate(self)

    def update(self, delta):
        print delta

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)


class BallLogic(CollisionHandler, Updatable):
    def __init__(self):
        CollisionHandler.__init__(self)
        Updatable.__init__(self)

    def activate(self):
        CollisionHandler.activate(self)
        Updatable.activate(self)

        self.gameobject.handle_collision = self.handle_collision
        self.gameobject.update = self.update

    def deactivate(self):
        self.gameobject.handle_collision = CollisionHandler.handle_collision
        self.gameobject.update = Updatable.update
        Updatable.deactivate()
        CollisionHandler.deactivate(self)

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)
        self.gameobject.velocity.x = -self.gameobject.velocity.x

    def update(self, delta):
        Updatable.update(self, delta)
        self.gameobject.rotate_by(1 * delta)
