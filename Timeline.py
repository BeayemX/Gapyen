from Components.Component import Component


class Timeline(Component):

    def __init__(self):
        pass

    def activate(self):
        Component.active()

    def deactivate(self):
        Component.deactivate()