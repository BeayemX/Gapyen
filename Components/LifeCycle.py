from Components.Component import Component
from Managers import GameManager
from Utilities import xprotocol

class LifeCycle(Component):

    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        GameManager.instance().spawn_entity(self.parent.uid,
                               self.parent.pos[0],
                               self.parent.pos[1],
                               self.parent.angle,
                               self.parent.vertices)

    def deactivate(self):
        GameManager.instance().destroy_entity(self.parent.uid)
        Component.deactivate(self)
