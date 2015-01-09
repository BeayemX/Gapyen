import xprotocol
import random
import math

import GameManager
import UpdaterManager


class Component:
    def __init__(self):
        self.active = True
        self.parent = None
        self.children = []

        GameManager.register_entity(self)

    def __str__(self):
        return self.name

    def activate(self):
        self.active = True

        for child in self.children:
            child.activate()

    def deactivate(self):
        self.active = False

        for child in self.children:
            child.deactivate()

        GameManager.deregister_entity(self)

    def setparent(self, parent):
        if self.parent:
            self.parent.remove(self)

        self.parent = parent
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
        self.initPos = tuple(pos)
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
        GameManager.register_shape(self.parent.name, self.parent)

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


### until now everything is clean. --> .parent stuff...


class Timeline(Component):

    def __init__(self, updates_per_sec, paused=False, timescale=1.0):
        Component.__init__(self)
        self.paused = paused
        self.elapsedtime = 0.0
        self.timescale = timescale
        self.frequency = 1.0 / updates_per_sec
        self.timer = 0.0

    def activate(self):
        Component.activate(self)
        self.parent.paused = self.paused
        self.parent.elapsedtime = self.elapsedtime
        self.parent.frequency = self.frequency
        self.parent.timescale = self.timescale
        self.parent.elapse_time = self.elapse_time
        self.parent.pause = self.pause
        self.parent.unpause = self.unpause

    def deactivate(self):
        del self.parent.paused
        del self.parent.elapsedtime
        del self.parent.frequency
        del self.parent.timescale
        del self.parent.elapse_time
        del self.parent.pause
        del self.parent.unpause
        GameManager.deregister_timeline(self.parent.name)

    def pause(self):
        self.parent.paused = True

    def unpause(self):
        self.parent.paused = False

    def elapse_time(self, delta):
        self.parent.elapsedtime += delta * self.parent.timescale # todo not sure if correct / needed

        self.timer += delta
        # print self.name + "elapsed time: " + str(self.elapsedtime)

        if self.timer > self.parent.frequency:
            self.timer -= self.parent.frequency
            self.notify(self.parent.frequency)  # todo not sure if correct, maybe sth clock tick wise?

    def notify(self, delta):
        self.parent.update(delta)  # should call an updater component which calls all updateables

    def time_till_next_call(self):
        x = self.frequency - self.timer  # fixme this doesn't work with timescale, does it?
        return max(0, x)


class Updatable(Component):

    def __init__(self, updatesPerSec=1, timelinename="Default"):
        Component.__init__(self)
        self.timelinename = timelinename
        self.frequency = 1.0 / updatesPerSec

        #UpdaterManager.updatables.append(self)

    def update(self, delta):
        #delta = self.parent.timeline.elapsedtime - self.parent.elapsedTime
        self.parent.elapsedTime += delta
        #print "updatable.elapsedtime: " + str(self.parent.elapsedTime)

    def activate(self):
        Component.activate(self)

        self.parent.timeline = GameManager.timelines[self.timelinename]
        self.parent.elapsedTime = self.parent.timeline.elapsedtime  # todo not sure if correct
        self.parent.frequency = self.frequency

    def deactivate(self):

        del self.parent.timeline
        del self.parent.elapsedTime
        del self.parent.frequency

        Component.deactivate(self)


    # todo implement me
    """
    def TimeTillNextCall(self):
        x = self.frequency - self.timer
        return max(0, x)
    """


class NetworkWrapper(Component, Updatable):

    def __init__(self, timelinename):
        Updatable.__init__(self, 1, timelinename)
        self.worldWidth = 100
        self.triangleSize = 100
        self.objects = []

    def activate(self):
        Component.activate(self)
        self.start_server()
        #UpdaterManager.updaterList.append(Updater("network", 50, self.update))
        self.adjustView()
        self.parent.update = self.update


    def deactivate(self):
        self.stop_server()
        del self.parent.update
        Component.deactivate(self)

    def start_server(self):
        xprotocol.startup(1) # TODO make 1 variable?
        print "started server()"
        xprotocol.add_session_listener(self.connect)
        print "added listner"

    def stop_server(self):
        # TODO implement me. or already enough?
        xprotocol._stop_session()

    def connect(self, started):
        if started:
            print "session started"
            #spawnRandTri()
            self.adjustView()
            self.spawn()
        else:
            print "session ended"

    def spawn(self):
        for key in GameManager.shapes:
            shape = GameManager.shapes[key]
            xprotocol.spawn_entity(shape.name, shape.pos[0], shape.pos[1], shape.angle, shape.vertices)

    def update(self, delta):
        xprotocol.update()


    def adjustView(self):
        xprotocol.set_world_width(self.worldWidth)
        xprotocol.update()


    def spawnRandTri(self):
        name = "RandomTri" + str(len(self.objects))
        self.objects.append(name)
        xprotocol.spawn_entity(name, 0, 0, 0,
                               [(random.randint(-self.triangleSize, self.triangleSize), random.randint(-self.triangleSize, self.triangleSize)),
                                (random.randint(-self.triangleSize, self.triangleSize), random.randint(-self.triangleSize, self.triangleSize)),
                                (random.randint(-self.triangleSize, self.triangleSize), random.randint(-self.triangleSize, self.triangleSize))])


    def randomPos(self):
        x = random.randint(-self.worldWidth * 0.1, self.worldWidth * 0.1)
        y = random.randint(-self.worldWidth * 0.1, self.worldWidth * 0.1)
        return x, y


    def moveObjRandomly(self, name):
        randPos = self.randomPos()
        xprotocol.move_entity(name, randPos[0], randPos[1], 0)


    def randPosUpdate(self):
        self.spawnRandTri()
        for i in self.objects:
            self.moveObjRandomly(i)


class RandomPose(Updatable):

    def __init__(self, world_width, world_height):
        Updatable.__init__(self)
        #Component.__init__(self)
        self.width = world_width
        self.height = world_height

    def activate(self):
        Updatable.activate(self)
        self.parent.world_width = self.width
        self.parent.world_height = self.height
        self.parent.new_pose = self.new_pose
        self.parent.update = self.update

    def deactivate(self):
        del self.parent.pos
        del self.parent.angle
        del self.parent.new_pose

        Updatable.deactivate(self)

    def new_pose(self, delta):
        """
        x = random.uniform(-self.width * 0.5, self.width * 0.5)
        y = random.uniform(-self.height * 0.5, self.height * 0.5)
        angle = random.uniform(0, 2 * math.pi)

        self.parent.pos = [x, y]
        self.parent.angle = angle
        """
        degree_per_sec = 360
        self.parent.angle += degree_per_sec * delta / 360 * math.pi * 2
        print "parent.angle: " + str(self.parent.angle)
        print "delta: " + str(delta)

    def update(self, delta):

        # fixme shouldnt have to calculate by myself... should be forwarded: update(delta)
        #delta = self.parent.timeline.elapsedtime - self.parent.elapsedTime
        #self.parent.elapsedTime += delta

        self.parent.new_pose(delta)
        xprotocol.move_entity(self.parent.name,
                              self.parent.pos[0],
                              self.parent.pos[1],
                              self.parent.angle)


# todo xprotocol spawn von der anderen klasse weg
# todo noch nicht getestet
class LifeCycle(Component):

    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        GameManager.instance().spawn_entity(self.parent.uid,
                               self.parent.pos[0],
                               self.parent.pos[1],
                               self.parent.angle,
                               self.parent.vertices)

    def deactivate(self):
        GameManager.instance().destroy_entity(self.parent.uid)
        Component.deactivate(self)

"""
class TimeSource(Component):

    instance = None

    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.parent.elapsedtime = 0.0

    def deactivate(self):
        del self.parent.elapsedtime
        Component.deactivate(self)

    @staticmethod
    def get_instance():
        if not TimeSource.instance:
            TimeSource.instance = TimeSource()
        return TimeSource.instance

    def elapse_time(self, delta):
        self.parent.elapsedtime += delta
        print self.parent.elapsedtime
"""

class Updater(Component):

    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        self.parent.updatables = []
        self.parent.update = self.update
        self.parent.add_updatable = self.add_updatable

    def deactivate(self):
        del self.parent.updatables
        del self.parent.update
        del self.parent.add_updatable

        Component.deactivate(self)

    def update(self, delta):
        print "updating " + str(len(self.parent.updatables))
        for u in self.parent.updatables:
            u.update(delta)

    def add_updatable(self, updatable):
        self.parent.updatables.append(updatable)