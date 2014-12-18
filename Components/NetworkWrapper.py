import random

from Utilities import xprotocol
from Managers import UpdaterManager
from Updater import  Updater

from Components.Component import Component


class NetworkWrapper(Component):

    def __init__(self, name):
        Component.__init__(self, name)
        self.worldWidth = 1920
        self.triangleSize = 960
        self.objects = []

    def activate(self):
        Component.activate(self)
        self.start_server()
        UpdaterManager.updaterList.append(Updater("network", 50, self.update))


    def deactivate(self):
        self.stop_server()
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
        else:
            print "session ended"


    def update(self):
        xprotocol.update()
        self.spawnRandTri()


    def adjustView(self):
        xprotocol.set_world_width(self.worldWidth)


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
        return (x, y)


    def moveObjRandomly(self, name):
        randPos = self.randomPos()
        xprotocol.move_entity(name, randPos[0], randPos[1], 0)


    def randPosUpdate(self):
        self.spawnRandTri()
        for i in self.objects:
            self.moveObjRandomly(i)