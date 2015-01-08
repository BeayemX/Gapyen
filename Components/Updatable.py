from Managers import UpdaterManager
import TimelineManager
from Components.Component import Component


class Updateable(Component):

    def __init__(self, updatesPerSec = 1, timelinename = "Default"):
        Component.__init__(self)

        self.timeline = TimelineManager.timelines[timelinename]
        self.elapsedTime = self.timeline.elapsedtime
        self.frequency = 1.0 / updatesPerSec

        UpdaterManager.updatables.append(self)

    def update(self):
        delta = self.timeline.elapsedtime - self.parent.elapsedTime
        self.parent.elapsedTime += delta
        #print "updatable.elapsedtime: " + str(self.parent.elapsedTime)

    def activate(self):
        Component.activate(self)

        self.parent.timeline = self.timeline
        self.parent.elapsedTime = self.elapsedTime
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
