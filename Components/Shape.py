from Components.Component import Component
from Utilities import xprotocol

class Shape(Component):
    def __init__(self, vertices):
        Component.__init__(self)
        self._vertices = vertices
    
    def activate(self):
        Component.activate(self)
        self.parent.vertices = self._vertices
        xprotocol.spawn_entity("tri", self.parent.pos[0], self.parent.pos[1], self.parent.angle, self.parent.vertices)

    def deactivate(self):
        del self.parent.vertices
        Component.deactivate(self)