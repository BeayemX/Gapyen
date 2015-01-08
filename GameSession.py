import xprotocol
from Components.Component import Component

class GameSession(Component):
    _instance = None
    
    def __init__(self):
        global _num_players, _network_ups, _world_width
        Component.__init__(self)
        self._num_players = _num_players
        self._rate = _network_ups
        self._world_width = _world_width

    def activate(self):
        Component.activate(self)
        self.parent.started = False
        
        self.parent.add_session_listener = xprotocol.add_session_listener
        self.parent.spawn_entity = xprotocol.spawn_entity
        self.parent.move_entity = xprotocol.move_entity
        self.parent.destroy_entity = xprotocol.destroy_entity
        
        xprotocol.startup(self._num_players)
        xprotocol.add_session_listener(self._onSession)
        updater.add(self.update, self._rate)
        print("GameSession activated")

    def deactivate(self):
        xprotocol.remove_session_listener(self._onSession)
        updater.remove(self.update)
        xprotocol.shutdown()
        del self.parent.started
        Thingy.deactivate(self)
        print("GameSession deactivated")

    def update(self):
        xprotocol.update()

    def _onSession(self, started):
        self.parent.started = started
        if(started):
            xprotocol.set_world_width(self._world_width)
            print("GameSession started")
        else:
            print("GameSession ended")

    def instance():
        if(GameSession._instance == None):
            GameSession._instance = GameSession()
        return GameSession._instance