import xprotocol
import math
import GameManager
import uuid
import sys

from vector import Vec2


class Component:
    def __init__(self):
        self.active = False
        self.parent = None
        self.children = []

        GameManager.register_entity(self)
    """
    def __str__(self):
        return self.name
    """
    def activate(self):
        self.active = True
        if not self.parent:
            GameManager.register_gameobject(self)

        for child in self.children:
            child.activate()

    def deactivate(self):
        self.active = False

        for child in reversed(self.children):
            child.deactivate()

        if not self.parent:
            GameManager.deregister_gameobject()

        GameManager.deregister_entity(self)

    def setparent(self, parent):
        if self.parent:
            self.parent.remove(self)

        self.parent = parent
        if parent.active:
            self.activate()

    def add(self, component):
        if component.parent:
            component.parent.remove(component)

        self.children.append(component)
        component.setparent(self)

    def remove(self, child):
        self.children.remove(child)


class StaticTransform(Component):

    def __init__(self, pos, angle):
        Component.__init__(self)
        self.initPos = Vec2(pos[0], pos[1])
        self.initAngle = angle

    def activate(self):
        Component.activate(self)
        self.parent.pos = self.initPos
        self.parent.angle = self.initAngle

    def deactivate(self):
        del self.parent.pos
        del self.parent.angle
        Component.deactivate(self)


class Shape(Component):
    def __init__(self, vertices):
        Component.__init__(self)
        self.vertices = vertices

    def activate(self):
        Component.activate(self)
        self.parent.vertices = self.vertices
        GameManager.register_shape(self.parent)

    def deactivate(self):
        del self.parent.vertices
        GameManager.deregister_shape(self.parent.name)
        Component.deactivate(self)


class Tag(Component):

    def __init__(self, tag):
        Component.__init__(self)
        self._tag = tag

    def activate(self):
        Component.activate(self)
        self.parent.tag = self._tag
        GameManager.register_tag(self._tag, self.parent)

    def deactivate(self):
        GameManager.deregister_tag(self._tag, self.parent)
        del self.parent.tag
        Component.deactivate(self)


class UID(Component):

    def __init__(self):
        Component.__init__(self)
        self.uid = uuid.uuid4()

    def activate(self):
        Component.activate(self)
        self.parent.uid = self.uid

    def deactivate(self):
        del self.parent.uid
        Component.deactivate(self)


class Name(Component):

    def __init__(self, name):
        Component.__init__(self)
        self.name = name

    def activate(self):
        Component.activate(self)
        self.parent.name = self.name

    def deactivate(self):
        del self.parent.name
        Component.deactivate(self)


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
        self.parent.paused = self.paused
        self.parent.elapsedtime = self.elapsedtime
        self.parent.frequency = self.frequency
        self.parent.timescale = self.timescale
        self.parent.elapse_time = self.elapse_time
        self.parent.pause = self.pause
        self.parent.unpause = self.unpause
        self.parent.time_till_next_call = self.time_till_next_call

        GameManager.register_timeline(self.parent)

    def deactivate(self):
        del self.parent.paused
        del self.parent.elapsedtime
        del self.parent.frequency
        del self.parent.timescale
        del self.parent.elapse_time
        del self.parent.pause
        del self.parent.unpause
        del self.parent.time_till_next_call
        GameManager.deregister_timeline(self.parent.name)

    def pause(self):
        self.parent.paused = True

    def unpause(self):
        self.parent.paused = False

    def elapse_time(self, delta):
        if not self.paused:
            self.parent.elapsedtime += delta * self.parent.timescale # todo not sure if correct / needed

            self.timer += delta * self.parent.timescale
            # print self.name + "elapsed time: " + str(self.elapsedtime)

            if self.timer >= self.parent.frequency:
                self.timer -= self.parent.frequency
                self.notify()

    def notify(self):
        send_delta = self.parent.elapsedtime - self.last_notify_timestamp
        self.last_notify_timestamp = self.parent.elapsedtime
        self.parent.send_update(send_delta)

    def time_till_next_call(self):
        x = (self.parent.frequency - self.timer)
        return max(0, x / self.parent.timescale)


# class not really needed... maybe remove?
class Updatable(Component):

    def __init__(self, updatesPerSec=1, timelinename="Default"):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.parent.update = self.update

    def deactivate(self):
        del self.parent.update
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
        self.parent.update = self.update

    def deactivate(self):
        self.stop_server()
        # del self.parent.update
        self.parent.update = Updatable.update  # todo is this correct?
        Updatable.deactivate(self)

    def start_server(self):
        xprotocol.startup(self.numusers)
        print "started server()"
        #xprotocol.add_session_listener(self.connect)
        xprotocol.add_connection_listener(self.connect)
        print "added listner"

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

    def update(self, delta):
        xprotocol.update()

    def adjust_view(self):
        xprotocol.set_world_width(self.worldWidth)
        xprotocol.update()


class RandomPose(Updatable):

    def __init__(self, world_width, world_height):
        Updatable.__init__(self)
        self.width = world_width  # todo also used in network... save externally
        self.height = world_height  # todo also used in network... save externally
        self.delta_counter = 0

    def activate(self):
        Updatable.activate(self)
        #self.parent.world_width = self.width
        #self.parent.world_height = self.height
        #self.parent.new_pose = self.new_pose
        self.parent.update = self.update

    def deactivate(self):
        #del self.parent.pos
        #del self.parent.angle
        #del self.parent.new_pose
        self.parent.update = Updatable.update  # todo is this correct?

        Updatable.deactivate(self)

    def new_pose(self, delta):
        self.delta_counter += delta
        y = math.sin(self.delta_counter) * 10
        """
        x = random.uniform(-self.width * 0.5, self.width * 0.5)
        y = random.uniform(-self.height * 0.5, self.height * 0.5)
        angle = random.uniform(0, 2 * math.pi)

        self.parent.pos = [x, y]
        self.parent.angle = angle
        """
        self.parent.pos.y = y
        """
        degree_per_sec = 360
        self.parent.angle += degree_per_sec * delta / 360 * math.pi * 2
        """

    def update(self, delta):
        self.new_pose(delta)
        xprotocol.move_entity(self.parent.name,
                              self.parent.pos[0],
                              self.parent.pos[1],
                              self.parent.angle)
        self.parent.calculate_AABB()
        self.parent.is_colliding(GameManager.Find("tri1"))  # fixme supder duper ugly


# todo wip
# todo not tested yet
# todo use this class to call xprotocol.spawn
class LifeCycle(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        GameManager.spawn_entity(self.parent.uid,
                                 self.parent.pos[0],
                                 self.parent.pos[1],
                                 self.parent.angle,
                                 self.parent.vertices)

    def deactivate(self):
        GameManager.destroy_entity(self.parent.uid)
        Component.deactivate(self)


class Updater(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.parent.updatables = []
        self.parent.send_update = self.send_update
        self.parent.add_updatable = self.add_updatable

    def deactivate(self):
        del self.parent.updatables
        del self.parent.send_update
        del self.parent.add_updatable

        Component.deactivate(self)

    def send_update(self, delta):
        for u in self.parent.updatables:
            u.update(delta)

    def add_updatable(self, updatable):
        self.parent.updatables.append(updatable)


class TimelineUpdatable(Component):

    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.parent.update = self.update

    def deactivate(self):
        del self.parent.update
        Component.deactivate(self)

    def update(self, delta):
        self.parent.elapse_time(delta)


class AABB(Component):
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.parent.AABB = self.calculate_AABB()
        self.parent.calculate_AABB = self.calculate_AABB
        self.parent.is_colliding = self.is_colliding

    def deactivate(self):
        del self.parent.AABB
        del self.parent.calculate_AABB
        del self.parent.is_colliding
        Component.deactivate(self)

    def calculate_AABB(self):
        minX = sys.maxint
        minY = sys.maxint
        maxX = -sys.maxint - 1
        maxY = -sys.maxint - 1

        # todo vertices should use vec2
        for v in self.parent.vertices:
            minX = min(minX, v[0])
            minY = min(minY, v[1])
            maxX = max(maxX, v[0])
            maxY = max(maxY, v[1])

        return Rectangle((minX+maxX)/2,
                         (minY+maxY)/2,
                         (maxX-minX)/2,
                         (maxY-minY)/2)

    def is_colliding(self, otherAABB):
        if self.parent == otherAABB:
            return False

        a = self.parent.AABB + self.parent.pos
        b = otherAABB.AABB + otherAABB.pos

        if abs(a.center[0] - b.center[0]) > (a.radius[0] + b.radius[0]):
            return False
        if abs(a.center[1] - b.center[1]) > (a.radius[1] + b.radius[1]):
            return False

        return True


class Rectangle:

    # todo negative size?
    def __init__(self, centerX, centerY, radiusX, radiusY):
        self.radius = Vec2(radiusX, radiusY)
        self.center = Vec2(centerX, centerY)

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

    def __init__(self, mass=1, velocity=Vec2(0, 0)):
        Component.__init__(self)
        self.mass = mass
        self.velocity = velocity

    def activate(self):
        Component.activate(self)

        self.parent.mass = self.mass
        self.parent.velocity = self.velocity

        GameManager.register_body(self.parent)

    def deactivate(self):
        del self.parent.mass
        del self.parent.velocity

        GameManager.deregister_body(self.parent)
        Component.deactivate(self)