import time
import GameManager
from Clock import Clock

maxSleepTime = 1
updaterList = []
updatables = []
clock = Clock()

def updateAllUpdaters():
    sleeptime = maxSleepTime
    delta = clock.tick()

    """
    for updater in updaterList:
        if not updater.paused:
            updater.update(delta)
            sleeptime = min(sleeptime, updater.TimeTillNextCall())
            print updater.name, "nextCall:", updater.TimeTillNextCall()
    """

    """ # should be handled by default timeline
    for key in GameManager.timelines:
        if not GameManager.timelines[key].paused:
            GameManager.timelines[key].elapse_time(delta)
    """
    """ should be handled by timeline manager
    for u in updatables:
        u.update()
        #sleeptime = min(sleeptime, u.TimeTillNextCall())
    """
    t = GameManager.timelines["Default"]
    t.elapse_time(delta)

    time.sleep(t.frequency)  # nothing can be updated faster than the time source


def startLoop():
    while True:
        updateAllUpdaters()
