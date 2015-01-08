import time


class Clock:    
    def __init__(self):
        self.prevTime = 0.0
        self.currTime = 0.0

    def tick(self):
        self.prevTime = self.currTime
        self.currTime = time.clock()
        return self.currTime - self.prevTime
