import time

from Utilities.Clock import Clock


maxSleepTime = 1
updaterList = []
clock = Clock()

def updateAllUpdaters():
    sleeptime = maxSleepTime
    delta = clock.tick()

    for updater in updaterList:
        if not updater.paused:
            updater.update(delta)
            sleeptime = min(sleeptime, updater.TimeTillNextCall())
            print updater.name, "nextCall:", updater.TimeTillNextCall()

    print "sleepTime:", sleeptime
    time.sleep(sleeptime)


def startLoop():
    while True:
        updateAllUpdaters()
