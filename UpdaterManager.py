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
    GameManager.timelines["Default"].elapse_time(delta)
    # time.sleep(sleeptime)  # todo implement me
    time.sleep(1.0 / 60.0)


def startLoop():
    while True:
        updateAllUpdaters()
