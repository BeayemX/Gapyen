# Network Module
#
# Copyright (c) 2014 Roman Divotkey, Univ. of Applied Sciences Upper Austria. 
# All rights reserved.
#
# This file is subject to the terms and conditions defined in file
# 'LICENSE', which is part of this source code package.
#
# THIS CODE IS PROVIDED AS EDUCATIONAL MATERIAL AND NOT INTENDED TO ADDRESS
# ALL REAL WORLD PROBLEMS AND ISSUES IN DETAIL.

"""Provides a basic implementation of the protocol used by the Game Terminal.
This is the server side implementation of the protocol. This module uses
the network module for communication.
"""

__VERSION__ = '1.0.0'

import network

_clients = []
_num_clients = None
_session_listener = []
_session_started = False

__version__ = '1.0.0'

def add_session_listener(listener):
    """Adds the given session listener.
    Session listener must accept an boolean argument indicating if the
    session has been started or stopped.
    Example:
    --------
    def my_session_listener(started):
        if started:
            print 'session has been started'
        else:
            print 'session has been stopped'
    xprotocol.add_session_listener(my_session_listener)
    """
    _session_listener.append(listener)

def remove_session_listener(listener):
    """Removes the given session listener."""
    _session_listener.removeg(listener)

def set_world_width(width):
    """Sets the with of the game world to be displayed."""
    data = "worldwidth:%f" % width
    for client in _clients:
        network.send_message((data, client))

def destroy_entity(entity_id):
    """Destroys the entity representation with the specified id."""
    data = "destroy:%s" % entity_id
    for client in _clients:
        network.send_message((data, client))

def spawn_entity(entity_id, x, y, angle, vertices):
    """Spans a new entity representation.
    Required arguments are:
    
    - id of the entity (typically a string),
    - the position within the game world (x, y),
    - the orientation (angle)
    - a list of vertices (to be rendered as polygon).
    """
    
    data = "spawn:%s:%f:%f:%f" % (entity_id, x, y, angle)
    data += ":%d" % len(vertices)

    for vertex in vertices:
        data += ":%f:%f" % (vertex[0], vertex[1])

    for client in _clients:
        network.send_message((data, client))

def move_entity(entity_id, x, y, angle):
    """Moves the entity representation to the specified position."""
    data = "move:%s:%f:%f:%f" % (entity_id, x, y, angle)

    for client in _clients:
        network.send_message((data, client))

def _start_session():
    global _session_started
    assert(not _session_started)
    _session_started = True
    
    for listener in _session_listener:
        listener(True)

def _stop_session():
    global _session_started
    assert(_session_started)
    _session_started = False

    _session_started = False
    for listener in _session_listener:
        listener(False)

def disconnect():
    """Disconnects all client and terminates an active session."""
    data = 'disconnect'
    for client in _clients:
        network.fire_message((data, client))

    if _session_started:
        _stop_session()
        
    _clients[:] = []


def startup(num_clients = 1):
    """Initializes the network and protocol."""
    global _num_clients
    assert not _num_clients, 'network already started'
    network.startup()   
    _num_clients = num_clients

def shutdown():
    """Shuts the nerwork down and disconnects from clients."""
    global _num_clients
    assert _num_clients, 'network not started'
    disconnect()
    _num_clients = False
    network.shutdown()

def _process(msg):
    data = msg[0]
    client = msg[1]
    params = data.split(':')

    if params[0] == 'connect' and not client in _clients:
        if not _session_started:
            network.send_message(('welcome', client))
            _clients.append(client)
        else:
            network.send_message(('goaway', client))
    elif params[0] == 'disconnect' and client in _clients:
         _clients.remove(client)

    if _session_started and len(_clients) < _num_clients:
        _stop_session()
    elif not _session_started and len(_clients) >= _num_clients:
        _start_session()
            
def update():
    """Call this method within your game loop."""
    network.update()

    messages = network.get_messages()
    for msg in messages:
        _process(msg)

# example usage
if __name__ == '__main__':

    import time
    
    num_players = 2
    pos_x = 5

    def run_idle():
        pass
    
    def run_demo():
        global pos_x
        move_entity('foo', pos_x, 0, 0)
        pos_x *= -1

    def on_session(started):
        global worker
        if started:
            print 'session has started'
            set_world_width(50)
            vertices = []
            vertices.append((-1, -1))
            vertices.append((1, -1))
            vertices.append((0, 1))
            spawn_entity("foo", 0, 0, 0, vertices)
            worker = run_demo
        else:
            print 'session has stopped'
            print "wating for %d players to connect" %  num_players
            worker = run_idle

    add_session_listener(on_session)
    worker = run_idle

    print "starting test game server"
    print "wating for %d player(s) to connect" %  num_players  
    startup(num_players)
    try:
        while True:
            update()
            worker()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print "shuting down test game server"
        shutdown()
