from Components.Component import Component


class StaticTransform(Component):

    def __init__(self, pos, angle):
        Component.__init__(self)
        self.initPos = tuple(pos)
        self.initAngle = angle

    def activate(self):
        Component.activate(self)
        self.parent.pos = self.initPos
        self.parent.angle = self.initAngle

    def deactivate(self):
        del self.parent.pos
        del self.parent.angle
        Component.deactivate(self)
