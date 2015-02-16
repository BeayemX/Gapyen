from Components import *
import uuid
import GameManager
import sys
import random
import eventsystem

def build_ship(name):
    c = Component()

    c.add(Name(name))
    c.add(Tag("Ship"))
    c.add(Transform(angle=math.pi))
    c.add(Shape([[0, 0], [-1, 1], [2, 0], [-1, -1]]))
    c.add(AABB(trigger=True))
    c.add(Body())
    c.add(Ship())

    c.activate()
    return c

def build_bullet(pos, direction):

    c = Component()

    c.add(Name("Bullet" + str(uuid.uuid4())))
    c.add(Tag("Bullet"))
    c.add(Transform(pos))
    size = 0.2
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

def build_missile(pos, angle):
    c = Component()

    c.add(Name("Missile" + str(uuid.uuid4())))
    c.add(Tag("Missile"))
    c.add(Transform(pos, angle=angle))
    size = 0.3
    c.add(Shape([
        [-size*4, -size],
        [-size*4, size],
        #[size*4, size],
        #[size*4, -size]
        [size*4, 0]
    ]))
    c.add(AABB(trigger=True))
    c.add(Body(linear_damping=0))
    c.add(Missile())

    c.activate()
    return c

def build_asteroid(pos, size=4):
    c = Component()

    c.add(Name("Asteroid" + str(uuid.uuid4())))
    c.add(Tag("Asteroid"))
    c.add(Transform(pos=pos))
    c.add(Shape([
        [-size, -size],
        [-size, size],
        [size, size],
        [size, -size]
    ]))
    c.add(AABB(trigger=True))
    c.add(Body(linear_damping=0))
    c.add(Asteroid(size))
    c.add(DoughnutUniverse())

    c.activate()
    return c

def build_gui():
    c = Component()
    c.add(Name("GUI"))
    c.add(GUI())
    c.activate()
    return c


class Ship(TimeUpdatable, CollisionHandler):
    def __init__(self):
        TimeUpdatable.__init__(self)
        CollisionHandler.__init__(self)
        self.speed = 1500
        self.handling = 5

        self.accelerating = False
        self.steering = 0
        self.lives = 3
        self.lose_life = False

    def activate(self):
        TimeUpdatable.activate(self)
        CollisionHandler.activate(self)
        self.gameobject.accelerate = self.accelerate
        self.gameobject.steer = self.steer
        self.gameobject.shoot_bullet = self.shoot_bullet
        self.gameobject.shoot_missile = self.shoot_missile

        t = GameManager.timelines["DefaultTimeline"]
        t.register_updatable(self.gameobject)

    def deactivate(self):
        t = GameManager.timelines["DefaultTimeline"]
        t.deregister_updatable(self.gameobject)

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
        if other.tag == "Asteroid":
            self.lose_life = True

    def handle_collided(self):

        if self.lose_life:
            self.lives -= 1

            if self.gameobject.name == "Ship1":
                eventsystem.instance.send_event("P1LostLife")
            else:
                eventsystem.instance.send_event("P2LostLife")

            self.gameobject.pos = Vec2(0, 0)
            self.gameobject.velocity = Vec2(0, 0)
            self.gameobject.clear_forces()

            if self.lives <= 0:
                self.gameobject.deactivate()

    def shoot_bullet(self):
        x = math.cos(self.gameobject.angle)
        y = math.sin(self.gameobject.angle)
        forward = Vec2(x, y)

        max = 2
        spread = math.pi / 8.0

        for i in range(-max+1, max):
            bullet = build_bullet(self.gameobject.pos, forward.rotated(i * spread))

    def shoot_missile(self):
        build_missile(self.gameobject.pos, self.gameobject.angle)


class Asteroid(CollisionHandler):
    def __init__(self, size):
        CollisionHandler.__init__(self)

        # spawn random pos
        # random direction
        self.direction = Vec2(random.random() - 0.5, random.random() - 0.5).normalized()
        #self.direction = Vec2(1, 1).normalized()
        self.speed = 5 - size

        self.size = size
        self.should_explode = False

    def activate(self):
        CollisionHandler.activate(self)
        self.gameobject.velocity = self.direction * self.speed

    def deactivate(self):
        CollisionHandler.deactivate(self)

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)
        if other.tag != self.gameobject.tag:
            self.should_explode = True

    def handle_collided(self):
        CollisionHandler.handle_collided(self)
        if self.should_explode:
            self.explode()

    def explode(self):
        if self.size > 1:
            build_asteroid(self.gameobject.pos, self.size - 1)
            build_asteroid(self.gameobject.pos, self.size - 1)

        self.gameobject.deactivate()


class DoughnutUniverse(TimeUpdatable):
    def __init__(self):
        TimeUpdatable.__init__(self)

    def activate(self):
        TimeUpdatable.activate(self)

        t = GameManager.timelines["DefaultTimeline"]
        t.register_updatable(self.gameobject)

    def deactivate(self):
        t = GameManager.timelines["DefaultTimeline"]
        t.deregister_updatable(self.gameobject)

        TimeUpdatable.deactivate(self)

    def update(self, delta):
        screen_w = settings.worldWidth * 0.5
        screen_h = settings.worldWidth * settings.aspect * 0.5

        if self.gameobject.pos.x > screen_w or self.gameobject.pos.x < -screen_w:
            self.gameobject.pos.x *= -0.95

        if self.gameobject.pos.y > screen_h or self.gameobject.pos.y < -screen_h:
            self.gameobject.pos.y *= -0.95


class Bullet(CollisionHandler, TimeUpdatable):
    def __init__(self, direction, lifetime=1):
        CollisionHandler.__init__(self)
        TimeUpdatable.__init__(self)

        self.direction = direction
        self.lifetime = lifetime

        self.speed = 25
        self.elapsed_time = 0
        self.collided = False

    def activate(self):
        CollisionHandler.activate(self)
        TimeUpdatable.activate(self)

        t = GameManager.timelines["DefaultTimeline"]
        t.register_updatable(self.gameobject)

        self.gameobject.velocity = self.direction * self.speed

    def deactivate(self):
        t = GameManager.timelines["DefaultTimeline"]
        t.deregister_updatable(self.gameobject)

        CollisionHandler.deactivate(self)
        TimeUpdatable.deactivate(self)

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)

        if other.tag != "Ship" and other.tag != "Bullet" and other.tag != "Missile":
            self.collided = True

    def handle_collided(self):
        CollisionHandler.handle_collided(self)
        if self.collided:
            self.destroy_itself()

    def update(self, delta):
        self.elapsed_time += delta

        if self.elapsed_time > self.lifetime:
            self.destroy_itself()

    def destroy_itself(self):
        self.gameobject.deactivate()


class Missile(Bullet):
    def __init__(self):
        Bullet.__init__(self, Vec2(0, 0), 5)
        self.speed /= 2.0
        self.handling = 3.0

    def activate(self):
        Bullet.activate(self)
        self.choose_target()

    def deactivate(self):
        Bullet.deactivate(self)

    def forward_direction(self):
        x = math.cos(self.gameobject.angle)
        y = math.sin(self.gameobject.angle)
        forward = Vec2(x, y)
        return forward

    def update(self, delta):
        self.choose_target()
        if self.target:
            target_pointing_vec2 = self.target.pos - self.gameobject.pos
            target_angle = math.atan2(target_pointing_vec2.y, target_pointing_vec2.x)
            diff = target_angle - self.gameobject.angle  #/ 180.0 * math.pi

            if diff >= math.pi:
                self.gameobject.angle += math.pi * 2
            elif diff <= -math.pi:
                self.gameobject.angle -= math.pi * 2

            diff = target_angle - self.gameobject.angle  # / 180.0 * math.pi

            sign = 1
            if diff < 0:
                sign = -1
            elif diff == 0:
                sign = 0

            self.gameobject.angle += sign * min(abs(diff), self.handling * delta)

        self.gameobject.velocity = self.speed * self.forward_direction()

        Bullet.update(self, delta)

    def choose_target(self):

        min_distance = sys.maxint
        self.target = None

        for a in GameManager.tags["Asteroid"]:
            dist = (a.pos - self.gameobject.pos).length_squared()
            if (dist < min_distance):
                min_distance = dist
                self.target = a


class GUI(Component):
    def __init__(self):
        Component.__init__(self)
        self.p1_lives = 3
        self.p2_lives = 3

    def activate(self):
        Component.activate(self)

        eventsystem.instance.register_event_listener("P1LostLife", self.p1LostLife)
        eventsystem.instance.register_event_listener("P2LostLife", self.p2LostLife)

    def deactivate(self):
        eventsystem.instance.deregister_event_listener("P1LostLife", self.p1LostLife)
        eventsystem.instance.deregister_event_listener("P2LostLife", self.p2LostLife)
        Component.deactivate(self)

    def p1LostLife(self):
        self.p1_lives -= 1
        print "p1 lives: " + str(self.p1_lives)

    def p2LostLife(self):
        self.p2_lives -= 1
        print "p2 lives: " + str(self.p2_lives)
