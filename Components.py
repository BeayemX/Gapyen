import math
import uuid
import sys

import xprotocol
import GameManager
import InputController

from vector import Vec2


class Component:
    def __init__(self):
        self.active = False
        self.gameobject = None
        self.components = []

        # todo do i need this? every (sub) component inside scope?
        GameManager.register_entity(self)

    def activate(self):
        self.active = True
        if not self.gameobject:
            GameManager.register_gameobject(self)

        for component in self.components:
            component.activate()

    def deactivate(self):
        self.active = False

        for component in reversed(self.components):
            component.deactivate()

        if not self.gameobject:
            GameManager.deregister_gameobject()

        GameManager.deregister_entity(self)

    def setgameobject(self, gameobject):
        if self.gameobject:
            self.gameobject.remove(self)

        self.gameobject = gameobject
        if gameobject.active:
            self.activate()

    def add(self, component):
        if component.gameobject:
            component.gameobject.remove(component)

        self.components.append(component)
        component.setgameobject(self)

    def remove(self, component):
        self.components.remove(component)


# TODO not tested yet
# TODO if gameobject is moved, children have to be moved also!!!
class Hierarchy(Component):

    def __init__(self):
        Component.__init__(self)
        self.children = []

    def activate(self):
        Component.activate(self)

        self.gameobject.children = self.children
        self.gameobject.add_child = self.add_child
        self.gameobject.remove_child = self.remove_child

    def deactivate(self):
        del self.gameobject.children
        del self.gameobject.add_child
        del self.gameobject.add_remove

        Component.deactivate(self)

    def add_child(self, child):
        self.gameobject.children.append(child)

    def remove_child(self, child):
        self.gameobject.children.remove(child)


class Transform(Component):

    def __init__(self, pos=Vec2(0, 0), angle=0):
        Component.__init__(self)
        self.initPos = Vec2(pos[0], pos[1])
        self.initAngle = angle

    def activate(self):
        Component.activate(self)
        self.gameobject.pos = self.initPos
        self.gameobject.angle = self.initAngle
        self.gameobject.move_by = self.move_by
        self.gameobject.move_to = self.move_to
        self.gameobject.rotate_by = self.rotate_by
        self.gameobject.rotate_to = self.rotate_to

    def deactivate(self):
        del self.gameobject.pos
        del self.gameobject.angle
        del self.gameobject.move_by
        del self.gameobject.move_to
        del self.gameobject.rotate_by
        del self.gameobject.rotate_to
        Component.deactivate(self)

    def move_by(self, delta):
        self.gameobject.pos += delta #Vec2(self.gameobject.pos.x + delta.x, self.gameobject.pos.y + delta.y)

    # todo rename to set_pos?
    def move_to(self, x, y):
        self.gameobject.pos = Vec2(self.gameobject.pos.x + x, self.gameobject.pos.y + y)

    def rotate_by(self, deltaangle):
        self.gameobject.angle = self.gameobject.angle + deltaangle

    # todo rename to set_angle?
    def rotate_to(self, angle):
        self.gameobject.angle = angle


class Shape(Component):
    def __init__(self, vertices):
        Component.__init__(self)
        self.vertices = vertices

    def activate(self):
        Component.activate(self)
        self.gameobject.vertices = self.vertices
        GameManager.register_shape(self.gameobject)

    def deactivate(self):
        del self.gameobject.vertices
        GameManager.deregister_shape(self.gameobject.name)
        Component.deactivate(self)


# object should be able to have multiple tags
class Tag(Component):

    def __init__(self, tag):
        Component.__init__(self)
        self._tag = tag

    def activate(self):
        Component.activate(self)
        self.gameobject.tag = self._tag
        GameManager.register_tag(self._tag, self.gameobject)

    def deactivate(self):
        GameManager.deregister_tag(self._tag, self.gameobject)
        del self.gameobject.tag
        Component.deactivate(self)


class UID(Component):

    def __init__(self):
        Component.__init__(self)
        self.uid = uuid.uuid4()

    def activate(self):
        Component.activate(self)
        self.gameobject.uid = self.uid

    def deactivate(self):
        del self.gameobject.uid
        Component.deactivate(self)


class Name(Component):

    def __init__(self, name):
        Component.__init__(self)
        self.name = name

    def activate(self):
        Component.activate(self)
        self.gameobject.name = self.name

    def deactivate(self):
        del self.gameobject.name
        Component.deactivate(self)


# todo make ElapsedTime-Component and inherit?
class Timeline(Component):

    def __init__(self, updates_per_sec, timescale=1.0, paused=False):
        Component.__init__(self)
        self.paused = paused
        self.elapsedtime = 0.0
        self.timescale = timescale
        self.frequency = 1.0 / updates_per_sec  # todo is frequency correct?
        self.timer = 0.0
        self.last_notify_timestamp = 0.0

    def activate(self):
        Component.activate(self)
        self.gameobject.paused = self.paused
        self.gameobject.elapsedtime = self.elapsedtime
        self.gameobject.frequency = self.frequency
        self.gameobject.timescale = self.timescale
        self.gameobject.elapse_time = self.elapse_time
        self.gameobject.pause = self.pause
        self.gameobject.unpause = self.unpause
        self.gameobject.time_till_next_call = self.time_till_next_call

        GameManager.register_timeline(self.gameobject)

    def deactivate(self):
        del self.gameobject.paused
        del self.gameobject.elapsedtime
        del self.gameobject.frequency
        del self.gameobject.timescale
        del self.gameobject.elapse_time
        del self.gameobject.pause
        del self.gameobject.unpause
        del self.gameobject.time_till_next_call
        GameManager.deregister_timeline(self.gameobject.name)

    def pause(self):
        self.gameobject.paused = True

    def unpause(self):
        self.gameobject.paused = False

    def elapse_time(self, delta):
        if not self.paused:
            self.gameobject.elapsedtime += delta * self.gameobject.timescale # todo not sure if correct / needed

            self.timer += delta * self.gameobject.timescale
            # print self.name + "elapsed time: " + str(self.elapsedtime)

            if self.timer >= self.gameobject.frequency:
                self.timer -= self.gameobject.frequency
                self.notify()

    def notify(self):
        send_delta = self.gameobject.elapsedtime - self.last_notify_timestamp
        self.last_notify_timestamp = self.gameobject.elapsedtime
        self.gameobject.send_update(send_delta)

    def time_till_next_call(self):
        x = (self.gameobject.frequency - self.timer)
        return max(0, x / self.gameobject.timescale)


class Updatable(Component):

    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.gameobject.update = self.update

    def deactivate(self):
        del self.gameobject.update
        Component.deactivate(self)

    def update(self, delta):
        pass

class NetworkWrapper(Updatable):

    def __init__(self, numusers):
        Updatable.__init__(self)
        self.worldWidth = 100  # todo save externally?
        self.triangleSize = 100  # todo save externally
        self.objects = []
        self.numusers = numusers

    def activate(self):
        Updatable.activate(self)
        self.start_server()
        self.adjust_view()

    def deactivate(self):
        self.stop_server()
        # del self.gameobject.update
        Updatable.deactivate(self)

    def update(self, delta):
        Updatable.update(self, delta)
        self.update_entity_transforms()  # TODO better name
        xprotocol.update()

    def start_server(self):
        xprotocol.startup(self.numusers)
        print "started server()"
        #xprotocol.add_session_listener(self.connect)
        xprotocol.add_connection_listener(self.connect)
        print "added listner"

        xprotocol.add_button_listener(self.button_listener)
        xprotocol.add_axis_listener(self.axis_listener)

    def stop_server(self):
        # TODO implement me. or already enough?
        xprotocol._stop_session()

    def connect(self, adress, started):
        if started:
            print "user connected"
            self.adjust_view()
            self.spawn_objects()
        else:
            print "user disconnected"

    def spawn_objects(self):
        for key in GameManager.shapes:
            shape = GameManager.shapes[key]
            xprotocol.spawn_entity(shape.name, shape.pos[0], shape.pos[1], shape.angle, shape.vertices)

    def adjust_view(self):
        xprotocol.set_world_width(self.worldWidth)

    def button_listener(self, button):
        print button

    def axis_listener(self, address, axis, value):
        print address, axis, value
        InputController.move_paddle(axis, value)

    def update_entity_transforms(self):
        # todo use list instead of dict for shapes?
        for key in GameManager.shapes:
            shape = GameManager.shapes[key]
            xprotocol.move_entity(shape.name, shape.pos[0], shape.pos[1], shape.angle)


class RandomPose(Updatable):

    def __init__(self, world_width, world_height):
        Updatable.__init__(self)
        self.width = world_width  # todo also used in network... save externally
        self.height = world_height  # todo also used in network... save externally
        self.delta_counter = 0

    def activate(self):
        Updatable.activate(self)

    def deactivate(self):
        Updatable.deactivate(self)

    def update(self, delta):
        Updatable.update(self, delta)
        self.new_pose(delta)

    def new_pose(self, delta):
        self.delta_counter += delta
        y = math.sin(self.delta_counter) * 10
        self.gameobject.pos.y = y


# todo wip
# todo not tested yet
# todo use this class to call xprotocol.spawn
class LifeCycle(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        GameManager.spawn_entity(self.gameobject.uid,
                                 self.gameobject.pos[0],
                                 self.gameobject.pos[1],
                                 self.gameobject.angle,
                                 self.gameobject.vertices)

    def deactivate(self):
        GameManager.destroy_entity(self.gameobject.uid)
        Component.deactivate(self)


class Updater(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.gameobject.updatables = []
        self.gameobject.send_update = self.send_update
        self.gameobject.add_updatable = self.add_updatable

    def deactivate(self):
        del self.gameobject.updatables
        del self.gameobject.send_update
        del self.gameobject.add_updatable

        Component.deactivate(self)

    def send_update(self, delta):
        for u in self.gameobject.updatables:
            u.update(delta)

    def add_updatable(self, updatable):
        self.gameobject.updatables.append(updatable)


class TimelineUpdatable(Updatable):

    def __init__(self):
        Updatable.__init__(self)

    def activate(self):
        Updatable.activate(self)

    def deactivate(self):
        Updatable.deactivate(self)

    def update(self, delta):
        Updatable.update(self, delta)
        self.gameobject.elapse_time(delta)


# todo make a collider componenet and inherit
class AABB(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        GameManager.register_collider(self.gameobject)
        self.gameobject.aabb = self.calculate_aabb()
        self.gameobject.calculate_aabb = self.calculate_aabb
        self.gameobject.is_colliding = self.is_colliding

    def deactivate(self):
        del self.gameobject.AABB
        del self.gameobject.calculate_aabb
        del self.gameobject.is_colliding

        GameManager.deregister_collider(self.gameobject)
        Component.deactivate(self)

    def calculate_aabb(self):
        minx = sys.maxint
        miny = sys.maxint
        maxx = -sys.maxint - 1
        maxy = -sys.maxint - 1

        # todo vertices should use vec2
        for v in self.gameobject.vertices:
            minx = min(minx, v[0])
            miny = min(miny, v[1])
            maxx = max(maxx, v[0])
            maxy = max(maxy, v[1])

        return Rectangle((minx+maxx)/2,
                         (miny+maxy)/2,
                         (maxx-minx)/2,
                         (maxy-miny)/2)

    def is_colliding(self, other):
        # todo better check?
        if self.gameobject == other:
            return False

        a = self.gameobject.aabb + self.gameobject.pos
        b = other.aabb + other.pos

        if abs(a.center[0] - b.center[0]) > (a.radius[0] + b.radius[0]):
            return False
        if abs(a.center[1] - b.center[1]) > (a.radius[1] + b.radius[1]):
            return False
        return True


# todo move class because its not a componenet
class Rectangle:

    # todo negative size?
    def __init__(self, center_x, center_y, radius_x, radius_y):
        self.radius = Vec2(radius_x, radius_y)
        self.center = Vec2(center_x, center_y)

    def __add__(self, other):
        center = Vec2(self.center.x, self.center.y)
        center.x += other.x
        center.y += other.y
        return Rectangle(center.x, center.y, self.radius.x, self.radius.y)

    def __str__(self):
        text = ""
        text += "Center: "
        text += str(self.center)
        text += ", Radius: "
        text += str(self.radius)
        return text


class Body(Component):

    def __init__(self, velocity=Vec2(0, 0), mass=1):
        Component.__init__(self)
        self.velocity = velocity
        self.mass = mass

    def activate(self):
        Component.activate(self)

        self.gameobject.mass = self.mass
        self.gameobject.velocity = self.velocity

        GameManager.register_body(self.gameobject)

    def deactivate(self):
        del self.gameobject.mass
        del self.gameobject.velocity

        GameManager.deregister_body(self.gameobject)
        Component.deactivate(self)


class PhysicsController(Updatable):

    def __init__(self):
        Updatable.__init__(self)

    def activate(self):
        Updatable.activate(self)

    def deactivate(self):
        Updatable.deactivate(self)

    def update(self, delta):
        Updatable.update(self, delta)
        self.move_bodies(delta)
        self.check_collisions()

    def check_collisions(self):
        for collider1 in GameManager.colliders:
            for collider2 in GameManager.colliders:
                if collider1 != collider2:
                    if collider1.is_colliding(collider2):
                        # TODO also call for collider2? because what if handling oves collider1 out of collider2?
                        collider1.handle_collision(collider2)

    def move_bodies(self, delta):
        for body in GameManager.bodies:
            body.move_by(body.velocity * delta)


class CollisionHandler(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.gameobject.handle_collision = self.handle_collision

    def deactivate(self):
        del self.gameobject.handle_collision
        Component.deactivate(self)

    def handle_collision(self, other):
        # TODO move body out of collision? parent-CollisionHandler so alle children do it?
        pass
