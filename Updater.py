class Updater:

    counter = 0

    def __init__(self, uid, updatesPerSec, methodToCall):
        self.name = uid
        self.frequency = 1.0 / updatesPerSec
        self.methodToCall = methodToCall
        self.timer = 0.0

    def update(self, delta):
        self.timer += delta
        if (self.timer > self.frequency):
            self.timer -= self.frequency
            self.methodToCall()
            print "update", self.name, self.counter
            self.counter += 1
            
    def TimeTillNextCall(self):
        x = self.frequency - self.timer
        print "x:", x
        return max(0, x)

