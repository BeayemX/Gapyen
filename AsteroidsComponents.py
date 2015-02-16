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
    c.add(Transform())
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
        [0 * size, 1 * size],
        [0.4 * size, 0.9 * size],
        [1 * size, 0.2 * size],
        [1 * size, 0 * size],
        [1 * size, -0.2 * size],
        [0.7 * size, -0.7 * size],
        [0 * size, -1 * size],
        [-0.5 * size, -0.5 * size],
        [-0.7 * size, 0.3 * size]
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


def build_gui_ship(name, pos):
    c = Component()

    c.add(Name(name))
    c.add(Transform(pos, angle=math.pi/2))
    c.add(Shape([[0, 0], [-1, 1], [2, 0], [-1, -1]]))


    c.activate()
    return c


def build_asteroid_spawn_controller():
    c = Component()
    c.add(Name("Asteroids Spawner"))
    c.add(AsteroidsSpawner())
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

        eventsystem.instance.register_event_listener("ResetGame", self.reset)

        t = GameManager.timelines["DefaultTimeline"]
        t.register_updatable(self.gameobject)

    def deactivate(self):
        t = GameManager.timelines["DefaultTimeline"]
        t.deregister_updatable(self.gameobject)

        eventsystem.instance.deregister_event_listener("ResetGame", self.reset)

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

        x = self.gameobject.pos.x
        y = self.gameobject.pos.y
        w = settings.worldWidth * 0.5
        h = settings.worldWidth * 0.5 * settings.aspect

        if x < -w or x > w or y < -h or y > h:
            self.lose_life = True
            self.handle_collided()
            print "outside"

    def handle_collision(self, other):
        CollisionHandler.handle_collision(self, other)
        if other.tag == "Asteroid":
            self.lose_life = True

    def handle_collided(self):

        if self.lose_life:
            self.lose_life = False
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

    def reset(self):
        self.lives = 3
        self.gameobject.pos = Vec2(0, 0)
        self.gameobject.velocity = Vec2(0, 0)
        self.gameobject.clear_forces()



class Asteroid(CollisionHandler):
    def __init__(self, size):
        CollisionHandler.__init__(self)

        # spawn random pos
        # random direction
        self.direction = Vec2(random.random() - 0.5, random.random() - 0.5).normalized()
        #self.direction = Vec2(1, 1).normalized()
        self.speed = 10 - size*2

        self.size = size
        self.should_explode = False

    def activate(self):
        CollisionHandler.activate(self)

        eventsystem.instance.register_event_listener("ResetGame", self.reset)

        self.gameobject.velocity = self.direction * self.speed

    def deactivate(self):

        eventsystem.instance.deregister_event_listener("ResetGame", self.reset)

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
        eventsystem.instance.send_event("AsteroidDestroyed")

        if self.size > 1:
            build_asteroid(self.gameobject.pos, self.size - 1)
            build_asteroid(self.gameobject.pos, self.size - 1)

        self.gameobject.deactivate()

    def reset(self):
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
        right_border = settings.worldWidth * 0.5
        top_border = settings.worldWidth * settings.aspect * 0.5

        if self.gameobject.pos.x > right_border:
            self.gameobject.pos.x = -right_border
        elif self.gameobject.pos.x < -right_border:
            self.gameobject.pos.x = right_border

        if self.gameobject.pos.y > top_border:
            self.gameobject.pos.y = -top_border
        elif self.gameobject.pos.y < -top_border:
            self.gameobject.pos.y = top_border


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

        eventsystem.instance.register_event_listener("ResetGame", self.reset)

        t = GameManager.timelines["DefaultTimeline"]
        t.register_updatable(self.gameobject)

        self.gameobject.velocity = self.direction * self.speed

    def deactivate(self):
        t = GameManager.timelines["DefaultTimeline"]
        t.deregister_updatable(self.gameobject)

        eventsystem.instance.deregister_event_listener("ResetGame", self.reset)

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

    def reset(self):
        self.destroy_itself()


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
            diff = target_angle - self.gameobject.angle

            if diff >= math.pi:
                self.gameobject.angle += math.pi * 2
            elif diff <= -math.pi:
                self.gameobject.angle -= math.pi * 2

            diff = target_angle - self.gameobject.angle

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
        self.p1_gui_lives = []
        self.p2_gui_lives = []

    def activate(self):
        Component.activate(self)

        eventsystem.instance.register_event_listener("ResetGame", self.reset)
        eventsystem.instance.register_event_listener("P1LostLife", self.p1LostLife)
        eventsystem.instance.register_event_listener("P2LostLife", self.p2LostLife)
        self.fill_gui()

    def deactivate(self):
        eventsystem.instance.deregister_event_listener("ResetGame", self.reset)
        eventsystem.instance.deregister_event_listener("P1LostLife", self.p1LostLife)
        eventsystem.instance.deregister_event_listener("P2LostLife", self.p2LostLife)

        self.clear_gui()

        Component.deactivate(self)

    def p1LostLife(self):
        self.p1_lives -= 1
        gui_ship = self.p1_gui_lives[-1]
        self.p1_gui_lives.remove(gui_ship)
        gui_ship.deactivate()
        self.check_game_over()

    def p2LostLife(self):
        self.p2_lives -= 1
        gui_ship = self.p2_gui_lives[-1]
        self.p2_gui_lives.remove(gui_ship)
        gui_ship.deactivate()
        self.check_game_over()

    def check_game_over(self):
        if self.p1_lives <= 0 and self.p2_lives <= 0:
            eventsystem.instance.send_event("ResetGame")
            print "reset"

    def reset(self):
        self.clear_gui()
        self.p1_lives = 3
        self.p2_lives = 3
        self.fill_gui()

        if not GameManager.find("Ship1"):  # todo crap string comparison
            build_ship("Ship1")
        if not GameManager.find("Ship2"):  # todo crap string comparison
            build_ship("Ship2")


    def fill_gui(self):
        space = 3
        topspacing = -1
        for i in range(self.p1_lives):

            x = -settings.worldWidth * 0.5 + space * (i+1)
            y = settings.worldWidth * 0.5 * settings.aspect - topspacing
            pos = Vec2(x, y)
            gui_ship = build_gui_ship("p1ship_" + str(i), pos)
            self.p1_gui_lives.append(gui_ship)

        for i in range(self.p2_lives):

            x = settings.worldWidth * 0.5 - space * (i+1)
            y = settings.worldWidth * 0.5 * settings.aspect - topspacing
            pos = Vec2(x, y)
            gui_ship = build_gui_ship("p2ship_" + str(i), pos)
            self.p2_gui_lives.append(gui_ship)

    def clear_gui(self):
        for gui_ship in self.p1_gui_lives:
            gui_ship.deactivate()
        self.p1_gui_lives = []
        for gui_ship in self.p2_gui_lives:
            gui_ship.deactivate()
        self.p2_gui_lives = []




class AsteroidsSpawner(Component):
    def __init__(self):
        Component.__init__(self)
        self.level = 0
        self.destroyed_asteroids = 0

    def activate(self):
        Component.activate(self)

        eventsystem.instance.register_event_listener("ResetGame", self.reset)
        eventsystem.instance.register_event_listener("LevelClear", self.next_level)
        eventsystem.instance.register_event_listener("AsteroidDestroyed", self.handle_asteroid_destroyed)

    def deactivate(self):

        eventsystem.instance.deregister_event_listener("ResetGame", self.reset)
        eventsystem.instance.deregister_event_listener("LevelClear", self.next_level)
        eventsystem.instance.deregister_event_listener("AsteroidDestroyed", self.handle_asteroid_destroyed)

        Component.deactivate(self)

    def next_level(self):
        self.destroyed_asteroids = 0
        self.level += 1
        for i in range(self.level):
            x = random.random() - 0.5 * settings.worldWidth
            y = random.random() - 0.5 * settings.worldWidth * settings.aspect
            randpos = Vec2(x, y)
            build_asteroid(randpos)

    def handle_asteroid_destroyed(self):
        self.destroyed_asteroids += 1
        if self.destroyed_asteroids >= self.level * 15: # fimxe magic number has to do with asteroids size and size decrease for children
            eventsystem.instance.send_event("LevelClear")

    def reset(self):
        self.level = 0
        self.destroyed_asteroids = 0
        eventsystem.instance.send_event("LevelClear")