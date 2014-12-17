import Updater
from Component import Component


class updaterComp (Component):

    def asdf(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        del self.parent.pos
        del self.parent.angle
        Component.deactivate(self)
