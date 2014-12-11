import xprotocol
import random
import time

from Clock import Clock
from Updater import Updater

worldWidth = 20
triangleSize = 4
maxSleepTime = 1
clock = Clock()
objects = []
updaters = []

def startServer():
    xprotocol.startup(1)
    print "started server()"
    xprotocol.add_session_listener(connect)
    print "added listner"

def connect(started):
    if started:
        print "session started"        
        spawnRandTri()
        adjustView()
    else:
        print "session ended"

def spawnRandTri():
    name = "RandomTri"+str(len(objects))
    objects.append(name)
    xprotocol.spawn_entity(name, 0, 0, 0, [(random.randint(-triangleSize, triangleSize),random.randint(-triangleSize, triangleSize)),(random.randint(-triangleSize, triangleSize),random.randint(-triangleSize, triangleSize)),(random.randint(-triangleSize, triangleSize),random.randint(-triangleSize, triangleSize))])
    
def adjustView():
    xprotocol.set_world_width(worldWidth);

def randomPos():
    x = random.randint(-worldWidth * 0.1, worldWidth * 0.1)
    y = random.randint(-worldWidth * 0.1, worldWidth * 0.1)
    return (x,y)

def moveObjRandomly(name):
    randPos = randomPos()
    xprotocol.move_entity(name, randPos[0], randPos[1], 0)

def networkUpdate():
    xprotocol.update()

def update():
    pass

def randPosUpdate():
    spawnRandTri()
    for i in objects:
        moveObjRandomly(i)

def runGameLoop():

    print "running game loop"
    print "waiting for client(s) to connect..."

    updaters.append(Updater("gameloop", 0.3, update))
    updaters.append(Updater("network", 1.0, networkUpdate))
    updaters.append(Updater("randPos", 0.5, randPosUpdate))
    while True:
        
        sleepTime = maxSleepTime
        delta = clock.tick()
        
        for updater in updaters:
            updater.update(delta)
            sleepTime = min(sleepTime, updater.TimeTillNextCall())
            print updater.name, "nextCall:", updater.TimeTillNextCall()
            
        print "sleepTime:", sleepTime
        time.sleep(sleepTime)
