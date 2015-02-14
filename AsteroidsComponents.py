from Components import *

def build_ship(name):
    c = Component()
    c.add(Name(name))
    c.add(Tag("Ship"))
    c.add(Transform())
    c.add(Shape([[0, 0], [-1, 1], [2, 0], [-1, -1]]))
    c.add(Body())
    c.add(Ship())
    c.activate()
    return c

def build_asteroid():
    pass
def build_bullet():
    pass
def build_missile():
    pass

class Ship(TimeUpdatable):
    def __init__(self):
        TimeUpdatable.__init__(self)
        self.speed = 1500
        self.handling = 5

        self.accelerating = False
        self.steering = 0

    def activate(self):
        TimeUpdatable.activate(self)
        self.gameobject.accelerate = self.accelerate
        self.gameobject.steer = self.steer

    def deactivate(self):
        del self.gameobject.accelerate
        del self.gameobject.steer
        TimeUpdatable.deactivate(self)

    def accelerate(self, value):
        self.accelerating = value
        print str(self.accelerating)

    def add_acceleration_force(self, delta):
        x = math.cos(self.gameobject.angle)
        y = math.sin(self.gameobject.angle)

        force = Vec2(x, y) * self.accelerating * self.speed * delta
        self.gameobject.add_force(force)

    def steer(self, value):
        self.steering = value
        print str(self.steering)

    def update(self, delta):
        if self.steering:
            self.gameobject.angle += self.steering * self.handling * delta
        if self.accelerating > 0:
            self.add_acceleration_force(delta)




class Asteroid(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)

    def deactivate(self):
        Component.deactivate(self)

class Bullet(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)

    def deactivate(self):
        Component.deactivate(self)

class Missile(Bullet):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)

    def deactivate(self):
        Component.deactivate(self)