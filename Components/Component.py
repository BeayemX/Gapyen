from Managers import GameManager


class Component:
    #def __init__(self, name, parent=None, active=False):
    def __init__(self):
        #self.name = name
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
        if self.parent:
            self.parent.remove(self)

        self.parent = parent
        self.activate()

    def add(self, child):
        if child.parent:
            child.parent.remove(child)

        self.children.append(child)
        child.setparent(self)

    def remove(self, child):
        self.children.remove(child)