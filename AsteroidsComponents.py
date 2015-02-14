from Components import *
import time

def build_ship(name):
    c = Component()

    c.add(Name(name))
    c.add(Tag("Ship"))
    c.add(Transform())
    c.add(Shape([[0, 0], [-1, 1], [2, 0], [-1, -1]]))
    c.add(AABB())
    c.add(Body())
    c.add(Ship())

    c.activate()
    return c

def build_asteroid():
    pass

def build_bullet(pos, direction):

    c = Component()

    c.add(Name("Bullet" + str(time.time()))) # fixme crap to add timestamp to make bullet names unique for xprotocol spawn which uses go.name
    c.add(Tag("Bullet"))
    c.add(Transform(pos))
    size = 0.1
    c.add(Shape([
        [-size, -size],
        [-size, size],
        [size, size],
        [size, -size]
    ]))
    c.add(AABB(trigger=True))
    c.add(Body(linear_damping=0))
    c.add(Bullet(direction))

    c.activate()
    return c

def build_missile():
    pass

class Ship(TimeUpdatable, CollisionHandler):
    def __init__(self):
        TimeUpdatable.__init__(self)
        CollisionHandler.__init__(self)
        self.speed = 1500
        self.handling = 5

        self.accelerating = False
        self.steering = 0

    def activate(self):
        TimeUpdatable.activate(self)
        CollisionHandler.activate(self)
        self.gameobject.accelerate = self.accelerate
        self.gameobject.steer = self.steer
        self.gameobject.shoot_bullet = self.shoot_bullet
        self.gameobject.shoot_missile = self.shoot_missile

    def deactivate(self):
        del self.gameobject.accelerate
        del self.gameobject.steer
        del self.gameobject.shoot_bullet
        del self.gameobject.shoot_missile
        CollisionHandler.deactivate(self)
        TimeUpdatable.deactivate(self)

    def accelerate(self, value):
        self.accelerating = value

    def add_acceleration_force(self, delta):
        x = math.cos(self.gameobject.angle)
        y = math.sin(self.gameobject.angle)

        force = Vec2(x, y) * self.accelerating * self.speed * delta
        self.gameobject.add_force(force)

    def steer(self, value):
        self.steering = value

    def update(self, delta):
        if self.steering:
            self.gameobject.angle += self.steering * self.handling * delta
        if self.accelerating > 0:
            self.add_acceleration_force(delta)

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)

    def shoot_bullet(self):
        x = math.cos(self.gameobject.angle)
        y = math.sin(self.gameobject.angle)
        bullet = build_bullet(self.gameobject.pos, Vec2(x, y))

    def shoot_missile(self):
        pass



class Asteroid(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)

    def deactivate(self):
        Component.deactivate(self)


class Bullet(CollisionHandler):
    def __init__(self, direction):
        CollisionHandler.__init__(self)
        self.direction = direction

        self.speed = 25

    def activate(self):
        CollisionHandler.activate(self)
        self.gameobject.velocity = self.direction * self.speed

    def deactivate(self):
        CollisionHandler.deactivate(self)

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)

        #if other != self.gameobject:
        print "coll with: " + other.name
        #self.gameobject.deactivate()

class Missile(Bullet):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)

    def deactivate(self):
        Component.deactivate(self)