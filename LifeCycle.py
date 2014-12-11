from Component import Component
#TODO WIP 
class LifeCycle(Component):
    
    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        xprotocol.spawn_entity(self.parent.uid,
                               self.parent.pos[0],
                               self.parent.pos[1],
                               self.parent.angle,
                               self.parent.vertices)

    def deactivate(self):
        xprotocol.destroy_entity(self.parent.uid)
        Component.deactivate(self)
