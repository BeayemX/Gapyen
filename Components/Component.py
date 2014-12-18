from Managers import GameManager


class Component:
    #def __init__(self, name, parent=None, active=False):
    def __init__(self, name):
        self.name = name
        self.active = True
        self.parent = None
        self.children = []

        GameManager.add_entity(self)

    def __str__(self):
        return self.name

    def activate(self):
        self.active = True

        for child in self.children:
            child.activate()

    def deactivate(self):
        self.active = False

        for child in self.children:
            child.deactivate()

    def setparent(self, parent):
        if self.parent != None: # TODO use 'if not self.parent' ?
            self.parent.removechildren(self)

        self.parent = parent
        self.activate()

    def addchildren(self, child):
        if child.parent != None:
            child.parent.removechildren(child)

        self.children.append(child)
        child.setparent(self)

    def removechildren(self, child):
        self.children.remove(child)