# -*- coding: cp1252 -*-
from Component import Component

class Container(Component):
    
    def __init__(self, uid):
        Component.__init__(self, "Container")
        self.uid = uid
        
    def addComponent(self, comp):
        if Component.active:
            self.components.append(comp)
        else:
            print "noe"
            
    """
    def __str__(self):
        text = "\n\nContainter: "
        text += str(self.id)
        text += "\n"
        text += "Components:"

        for comp in self.components:
            text += "\n\t"
            text += str(comp.name)
        return text

    def getStructureAsStringArray(self):
        return [str(comp) for comp in self.components]

    """


    def activate(self):
        Component.activate(self)
        self.parent.components = []
        self.parent.addComponent = self.addComponent

    def deactivate(self):
        del self.parent.components
        del self.parent.addComponent
        Component.deactivate(self)
