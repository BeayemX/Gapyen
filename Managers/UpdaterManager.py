import time

import TimelineManager
from Utilities.Clock import Clock


maxSleepTime = 1
updaterList = []
updatables = []
timelines = []
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


    for key in TimelineManager.timelines:
        if not TimelineManager.timelines[key].paused:
            TimelineManager.timelines[key].elapsetime(delta)

    for u in updatables:
        u.update()
        #sleeptime = min(sleeptime, u.TimeTillNextCall())


    # time.sleep(sleeptime)  # todo implement me
    time.sleep(1.0 / 60.0)  # todo implement me


def startLoop():
    while True:
        updateAllUpdaters()
