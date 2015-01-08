import TimelineManager
from Components.Component import Component


class Timeline(Component):

    def __init__(self, name, paused=False, timescale=1.0):
        self.paused = paused
        self.elapsedtime = 0.0
        self.timescale = timescale
        self.name = name
        TimelineManager.timelines[name] = self

    def activate(self):
        print ("timeline activated")

    def deactivate(self):
        print ("timeline deactivated")

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def elapsetime(self, delta):
        self.elapsedtime += delta * self.timescale
        #print self.name + "elapsed time: " + str(self.elapsedtime)


"""
class BaseUpdater(object):

    def __init__(self, uid, updatesPerSec, methodToCall):
        self.startup timestamp = time.time
        self.name = uid
        self.frequency = 1.0 / updatesPerSec
        self.methodToCall = methodToCall
        self.timer = 0.0
        self.counter = 0
        self.paused = False
        UpdaterManager.updaterList.append(self)

    def update(self, delta):

        self.timer += delta

        if self.timer > self.frequency:
            self.timer -= self.frequency
            self.methodToCall()
            print "update", self.name, self.counter
            self.counter += 1

    def TimeTillNextCall(self):
        x = self.frequency - self.timer
        return max(0, x)

"""