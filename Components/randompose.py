import math, random
from Utilities import  xprotocol
from Components.Component import Component
from Components.Updatable import Updateable

class RandomPose(Component, Updateable):

    def __init__(self, world_width, world_height):
        Updateable.__init__(self)
        #Component.__init__(self)
        self.width = world_width
        self.height = world_height

    def _new_pose(self):
        x = random.uniform(-self.width * 0.5, self.width * 0.5)
        y = random.uniform(-self.height * 0.5, self.height * 0.5)
        angle = random.uniform(0, 2 * math.pi)

        self.parent.pos = (x, y)
        self.parent.angle = angle

    def activate(self):
        Component.activate(self)
        self._new_pose()

    def deactivate(self):
        del self.parent.pos
        del self.parent.angle
        Component.deactivate(self)

    def update(self):
        self._new_pose()

        xprotocol.move_entity("tri",
                              self.parent.pos[0],
                              self.parent.pos[1],
                              self.parent.angle) 