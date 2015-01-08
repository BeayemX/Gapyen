from Components.Component import Component
#from Updater import Updater


class UpdateComponent(Component):

    def __init__(self, name, callsPerSec):
        Component.__init__(self, name)
        self.callsPerSec = callsPerSec

    def activate(self):
        Component.activate(self)
        self.parent.update = self.update
        self.parent.updater = Updater(self.parent.name+"Updater", self.callsPerSec, self.parent.update)

    def deactivate(self):
        del self.parent.updater
        Component.deactivate(self)

    def update(self):
        # TODO implement me
        print (self.parent.updater.name)