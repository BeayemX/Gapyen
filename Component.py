class Component:        
    def __init__(self, name, parent = None, active = False):
        self.name = name
        self.active = active
        self.parent = parent
        
        if (self.active):
            activate();

    def __str__(self):
        return self.name

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def setParent(self, parent):
        self.parent = parent
