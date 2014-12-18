import math, random, updater
from component import Thingy

# TODO implement me. just copied
class RandomPose(Thingy):

    def __init__(self, world_width, world_height, rate):
        Thingy.__init__(self)
        self.width = world_width
        self.height = world_height
        self.rate = rate

    def _new_pose(self):
        x = random.uniform(-self.width * 0.5, self.width * 0.5)
        y = random.uniform(-self.height * 0.5, self.height * 0.5)
        angle = random.uniform(0, 2 * math.pi)

        self.parent.pos = (x, y)
        self.parent.angle = angle

    def activate(self):
        Thingy.activate(self)
        self._new_pose()
        updater.add(self.update, self.rate)

    def deactivate(self):
        updater.remove(self.update)
        del self.parent.pos
        del self.parent.angle
        Thingy.deactivate(self)

    def update(self):
        self._new_pose()
        xprotocol.move_entity(self.parent.uid,
                              self.parent.pos[0],
                              self.parent.pos[1],
                              self.parent.angle) 