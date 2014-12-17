import GameManager

from Component import Component

"""
class Container(Component):
    
    def __init__(self, uid):
        Component.__init__(self, "Container")
        self.uid = uid
        GameManager.add_container(self)
        
    def add_component(self, comp):
        if Component.active:
            self.components.append(comp)
        else:
            print "not active"

    def activate(self):
        Component.activate(self)
        self.parent.components = []
        self.parent.add_component = self.add_component

    def deactivate(self):
        del self.parent.components
        del self.parent.add_component
        Component.deactivate(self)

"""