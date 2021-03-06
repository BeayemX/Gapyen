import math
import uuid
import sys

import xprotocol
import GameManager
import InputController
import settings

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
            #self.gameobject = self  # TODO should .gameobject be None or self

        for component in self.components:
            component.activate()

    def deactivate(self):
        self.active = False

        for component in reversed(self.components):
            component.deactivate()

        if not self.gameobject:
            GameManager.deregister_gameobject(self)

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
        return component

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

    def __init__(self, pos=None, angle=0):
        Component.__init__(self)
        if not pos:
            pos = Vec2(0, 0)
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

    def move_by(self, delta_pos):
        self.gameobject.pos += delta_pos

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
        xprotocol.spawn_entity(self.gameobject.name, self.gameobject.pos.x, self.gameobject.pos.y, self.gameobject.angle, self.vertices)

    def deactivate(self):
        del self.gameobject.vertices
        GameManager.deregister_shape(self.gameobject)
        xprotocol.destroy_entity(self.gameobject.name)
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


class Updatable(Component):
    def __init__(self, updater=None):
        Component.__init__(self)
        #if not updater:
        #    updater = GameManager.timelines["DefaultTimeline"]
        # todo add to gameobject?
        # todo maybe a list?
        #self.updater = updater

    def activate(self):
        Component.activate(self)
        self.gameobject.update = self.update
        self.gameobject.use_updater = self.use_updater
        #self.use_updater(self.updater)

    def deactivate(self):
        del self.gameobject.update
        del self.gameobject.use_updater
        Component.deactivate(self)

    # todo shouldn't we be able to select which method to inject, because its \
    # a problem if we want to listen to 2 updaters and execute differnt methods
    def update(self):
        pass

    # todo maybe make usable if not activated. just set self.updater and onactivate --> updater.register...?
    def use_updater(self, updater):
        # todo should i deregister from old upddater?
        # todo maybe only deregister if timline? because normal updater could be multiple...
        updater.register_updatable(self.gameobject)


class TimeUpdatable(Updatable):

    def __init__(self):
        Updatable.__init__(self)

    def activate(self):
        Updatable.activate(self)
        self.gameobject.update = self.update

    def deactivate(self):
        self.gameobject.update = Updatable.update(self)
        Updatable.deactivate(self)

    def update(self, delta):
        pass


class NetworkWrapper(TimeUpdatable):

    def __init__(self, numusers):
        TimeUpdatable.__init__(self)
        self.worldWidth = settings.worldWidth
        self.objects = []
        self.numusers = numusers

    def activate(self):
        TimeUpdatable.activate(self)
        self.start_server()
        self.adjust_view()

    def deactivate(self):
        self.stop_server()
        TimeUpdatable.deactivate(self)

    def update(self, delta):
        TimeUpdatable.update(self, delta)
        xprotocol.update()

    def start_server(self):
        xprotocol.startup(self.numusers)
        print "started server()"
        xprotocol.add_connection_listener(self.connect)
        print "added listner"

        xprotocol.add_button_listener(self.button_listener)
        xprotocol.add_axis_listener(self.axis_listener)

    def stop_server(self):
        # TODO implement me. or already enough?
        xprotocol._stop_session()

    def connect(self, address, started):
        if started:
            print "user connected"
            self.adjust_view()
            self.spawn_objects()
        else:
            print "user disconnected"

    def spawn_objects(self):
        for shape in GameManager.shapes:
            xprotocol.spawn_entity(shape.name, shape.pos[0], shape.pos[1], shape.angle, shape.vertices)

    def adjust_view(self):
        xprotocol.set_world_width(self.worldWidth)

    def button_listener(self, address, button, down):
        InputController.process_button(button, down)

    def axis_listener(self, address, axis, value):
        InputController.process_axis(axis, value)


class PoseTransmitter(TimeUpdatable):  # todo crappy name

    def __init__(self):
        TimeUpdatable.__init__(self)

    def activate(self):
        TimeUpdatable.activate(self)

    def deactivate(self):
        TimeUpdatable.deactivate(self)

    def update(self, delta):
        TimeUpdatable.update(self, delta)
        self.update_entity_transforms()  # TODO better name
        xprotocol.update()

    def update_entity_transforms(self):
        # todo use list instead of dict for shapes?
        for shape in GameManager.shapes:
            xprotocol.move_entity(shape.name, shape.pos[0], shape.pos[1],
                                  shape.angle)


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
        self.gameobject.register_updatable = self.register_updatable
        self.gameobject.deregister_updatable = self.deregister_updatable

    def deactivate(self):
        del self.gameobject.updatables
        del self.gameobject.register_updatable
        del self.gameobject.deregister_updatable

        Component.deactivate(self)

    def send_update(self):
        for u in self.gameobject.updatables:
            u.update()

    def register_updatable(self, updatable):
        self.gameobject.updatables.append(updatable)

    def deregister_updatable(self, updatable):
        self.gameobject.updatables.remove(updatable)


class Timeline(Updater):

    def __init__(self, updates_per_sec, timescale=1.0, paused=False):
        Updater.__init__(self)
        self.paused = paused
        self.elapsedtime = 0.0
        self.timescale = timescale
        self.frequency = 1.0 / updates_per_sec  # todo is frequency correct?
        self.timer = 0.0
        self.last_notify_timestamp = 0.0

    def activate(self):
        Updater.activate(self)
        self.gameobject.paused = self.paused
        self.gameobject.elapsedtime = self.elapsedtime
        self.gameobject.frequency = self.frequency
        self.gameobject.timescale = self.timescale
        self.gameobject.elapse_time = self.elapse_time
        self.gameobject.pause = self.pause
        self.gameobject.unpause = self.unpause
        self.gameobject.time_till_next_call = self.time_till_next_call
        self.gameobject.reset_timeline = self.reset

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
        del self.gameobject.reset_timeline
        GameManager.deregister_timeline(self.gameobject.name)
        Updater.deactivate(self)

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
        self.send_update(send_delta)

    def send_update(self, delta):
        for u in self.gameobject.updatables:
            u.update(delta)

    def time_till_next_call(self):
        x = (self.gameobject.frequency - self.timer)
        return max(0, x / self.gameobject.timescale)

    def reset(self):
        self.gameobject.elapsedtime = 0.0
        self.gameobject.timer = 0.0


# todo also inherit timeline?
class TimelineTimeUpdatable(TimeUpdatable):

    def __init__(self):
        TimeUpdatable.__init__(self)

    def activate(self):
        TimeUpdatable.activate(self)

    def deactivate(self):
        TimeUpdatable.deactivate(self)

    def update(self, delta):
        TimeUpdatable.update(self, delta)
        self.gameobject.elapse_time(delta)


# todo make a collider componenet and inherit
class Collider(Component):
    def __init__(self, trigger=False):
        Component.__init__(self)
        # todo use for physics
        self.is_trigger = trigger

    def activate(self):
        Component.activate(self)
        self.gameobject.is_trigger = self.is_trigger
        self.gameobject.is_colliding = self.is_colliding

    def deactivate(self):
        del self.gameobject.is_trigger
        del self.gameobject.is_colliding
        Component.deactivate(self)

    def is_colliding(self, other):
        pass


class AABB(Collider):
    def __init__(self, trigger=False):
        Collider.__init__(self, trigger)

    def activate(self):
        Collider.activate(self)
        GameManager.register_collider(self.gameobject)
        # todo maybe inject only .collider not .aabb?
        self.gameobject.aabb = self.calculate_aabb()
        self.gameobject.calculate_aabb = self.calculate_aabb
        self.gameobject.get_overlapping_rect = self.get_overlapping_rect

    def deactivate(self):
        del self.gameobject.aabb
        del self.gameobject.calculate_aabb
        del self.gameobject.get_overlapping_rect

        GameManager.deregister_collider(self.gameobject)
        Collider.deactivate(self)

    # todo re-inject into .aabb
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

    # todo how to check if colliding with non-aabb?
    def is_colliding(self, other):
        # todo better check?
        if self.gameobject == other:
            print "self collision"
            return False

        a = self.gameobject.aabb + self.gameobject.pos
        b = other.aabb + other.pos

        if abs(a.center[0] - b.center[0]) > (a.radius[0] + b.radius[0]):
            return False
        if abs(a.center[1] - b.center[1]) > (a.radius[1] + b.radius[1]):
            return False
        return True

    # todo how to make sure that 'other' is also aabb?
    def get_overlapping_rect(self, other):
        a = self.gameobject.aabb + self.gameobject.pos
        b = other.aabb + other.pos

        diff_centerx = abs(a.center.x - b.center.x)
        diff_radiusy = a.radius.x + b.radius.x
        width = max(0, diff_radiusy - diff_centerx)

        diff_centery = abs(a.center.y - b.center.y)
        diff_radiusy = a.radius.y + b.radius.y
        height = max(0, diff_radiusy - diff_centery)
        return Rectangle(0, 0, width/2, height/2)


# todo move class because its not a componenet
class Rectangle:

    # todo center is (0|0) not .pos. is this a problem
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

    def __init__(self, velocity=None, acceleration=None, mass=1.0, linear_damping=1):
        Component.__init__(self)
        if not velocity:
            velocity = Vec2(0, 0)

        if not acceleration:
            acceleration = Vec2(0, 0)

        self.velocity = velocity
        self.ang_velocity = 0
        self.acceleration = acceleration
        self.ang_acc = 0
        self.mass = mass
        self.moi = 0.5  # moment of inertia
        self.linear_damping = linear_damping
        self.ang_damping = 0.1
        self.force = Vec2(0, 0)
        self.torque = 0.0

    def activate(self):
        Component.activate(self)

        self.gameobject.mass = self.mass
        self.gameobject.velocity = self.velocity
        self.gameobject.ang_velocity = self.ang_velocity
        self.gameobject.acceleration = self.acceleration
        self.gameobject.ang_acc = self.ang_acc

        self.gameobject.linear_damping = self.linear_damping
        self.gameobject.ang_damping = self.ang_damping

        self.gameobject.add_force = self.add_force
        self.gameobject.add_torque = self.add_torque
        self.gameobject.clear_forces = self.clear_forces

        self.gameobject.physics_timestep = self.physics_timestep

        GameManager.register_body(self.gameobject)

    def deactivate(self):
        del self.gameobject.mass
        del self.gameobject.velocity
        del self.gameobject.ang_velocity
        del self.gameobject.acceleration
        del self.gameobject.ang_acc
        del self.gameobject.linear_damping
        del self.gameobject.ang_damping

        del self.gameobject.add_force
        del self.gameobject.add_torque
        del self.gameobject.clear_forces
        del self.gameobject.physics_timestep

        GameManager.deregister_body(self.gameobject)
        Component.deactivate(self)

    def add_force(self, force):
        self.force += force

    def add_torque(self, torque):
        self.torque += torque

    def clear_forces(self):
        self.force[0] = 0
        self.force[1] = 0
        self.torque = 0

    # FIXME crappy method name
    def physics_timestep(self, delta):
        # linear damping
        self.gameobject.add_force(self.gameobject.velocity * -self.gameobject.linear_damping)
        self.gameobject.add_torque(-self.gameobject.ang_velocity * self.gameobject.ang_damping)

        # calculate accelerations
        self.gameobject.acceleration = self.force * (1.0 / self.gameobject.mass)  # vec2 has no '/'
        self.gameobject.ang_acc = self.torque / self.moi

        # euler step
        self.gameobject.velocity += self.gameobject.acceleration * delta
        self.gameobject.pos += self.gameobject.velocity * delta

        self.gameobject.move_by(self.gameobject.velocity * delta)

        self.clear_forces()

class PhysicsController(TimeUpdatable):
    def __init__(self):
        TimeUpdatable.__init__(self)

    def activate(self):
        TimeUpdatable.activate(self)

    def deactivate(self):
        TimeUpdatable.deactivate(self)

    def update(self, delta):
        TimeUpdatable.update(self, delta)
        self.move_bodies(delta)
        self.check_collisions()

    def move_bodies(self, delta):
        for body in GameManager.bodies:
            body.physics_timestep(delta)

    def check_collisions(self):
        collided_objects = set([])
        for i in range(len(GameManager.colliders)):
            for j in range(i+1, len(GameManager.colliders)):
                if GameManager.colliders[i].is_colliding(GameManager.colliders[j]):
                    GameManager.colliders[i].handle_collision(GameManager.colliders[j])
                    GameManager.colliders[j].handle_collision(GameManager.colliders[i])
                    collided_objects.add(GameManager.colliders[i])
                    collided_objects.add(GameManager.colliders[j])

        for col in collided_objects:
            col.handle_collided()


# todo unify with Collider class?
class CollisionHandler(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.gameobject.handle_collision = self.handle_collision
        self.gameobject.handle_collided = self.handle_collided

    def deactivate(self):
        del self.gameobject.handle_collision
        del self.gameobject.handle_collided
        Component.deactivate(self)

    def handle_collision(self, other):
        # pong
        """
        if other.tag == "Ball":  # hack implement layer mask stuff
            return
        """
        if not self.gameobject.is_trigger and not other.is_trigger:
            try:
                # todo what if 2 moving objects collide, one is already moved out
                # so the second one doesnt have a collision any more
                # maye solve in physic step, event-queue-like??
                overlap = self.gameobject.get_overlapping_rect(other)
                length = min(overlap.radius.x, overlap.radius.y)
                offset = length * self.gameobject.velocity.normalized() * -1
                self.gameobject.move_by(offset)
            except AttributeError:
                #print "Attribute error / Collision Handler"
                pass
            except ZeroDivisionError:
                # todo exception handling
                #print "Zero Division Error / Collision Handler, name=" + self.gameobject.name
                pass

    def handle_collided(self):
        pass