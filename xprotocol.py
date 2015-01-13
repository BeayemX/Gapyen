# Game Architecture Network Layer (ganet)
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

import network, message

_num_clients = None
_session_listener = []
_session_started = False
_decoder = message.MessageDecoder()
_peers = {}

_connection_listeners = set()
_axis_listeners = set()
_button_listeners = set()


class Peer(object):

    def __init__(self, addr, encoder):
        self.addr = addr
        self.encoder = encoder

    def accept(self):
        self.encoder.reset()
        self.encoder.write_string('welcome')
        network.send_message((self.encoder.get_message(), self.addr))

    def refuse(self):
        self.encoder.reset()
        self.encoder.write_string('goaway')
        network.send_message((self.encoder.get_message(), self.addr))

    def disconnect(self, instant = False):
        self.encoder.reset()
        self.encoder.write_string('disconnect')
        if instant:
            network.fire_message((self.encoder.get_message(), self.addr))
        else:
            network.send_message((self.encoder.get_message(), self.addr))

    def destroy_entity(self, entity_id):
        self.encoder.reset()
        self.encoder.write_string('destroy')
        self.encoder.write_string(entity_id)
        network.send_message((self.encoder.get_message(), self.addr))

    def set_world_width(self, width):
        self.encoder.reset()
        self.encoder.write_string('worldwidth')
        self.encoder.write_float(width)
        network.send_message((self.encoder.get_message(), self.addr))

    def spawn_entity(self, entity_id, x, y, angle, vertices):
        self.encoder.reset()
        self.encoder.write_string('spawn')
        self.encoder.write_string(entity_id)
        self.encoder.write_float(x)
        self.encoder.write_float(y)
        self.encoder.write_float(angle)
        self.encoder.write_int(len(vertices))

        for vertex in vertices:
            self.encoder.write_float(vertex[0])
            self.encoder.write_float(vertex[1])
        
        network.send_message((self.encoder.get_message(), self.addr))

    def move_entity(self, entity_id, x, y, angle):
        self.encoder.reset()
        self.encoder.write_string('move')
        self.encoder.write_string(entity_id)
        self.encoder.write_float(x)
        self.encoder.write_float(y)
        self.encoder.write_float(angle)
        
        network.send_message((self.encoder.get_message(), self.addr))

def add_connection_listener(listener):
    """Adds the given connection listener.
    connection listener must have the following signature:
      listener(peer, connected)
    - peer: the client that has connected or disconnected.
    - connected: True if the client has connected, False
                 if the client has disconnected.
    """
    _connection_listeners.add(listener)

def remove_connection_listener(listener):
    """Removes the specified connection listener."""
    _connection_listeners.remove(listener)

def add_axis_listener(listener):
    """Adds the given axis listener.
    Axis listener must have the following signature:
      listener(peer, axis_number, axis_value)
    - peer: the client that is the origin of the message
    - axis_number: integer value >0 that identifies the axis.
    - axis_value: float value between -1.0 and 1.0. Specified
                  the new position of the axis.
    """
    _axis_listeners.add(listener)
    
def remove_axis_listener(listener):
    """Removes the specified axis listener."""
    _axis_listeners.discard(listener)

def add_button_listener(listener):
    """Adds the given button listener.
    button listener must have the following signature:
      listener(peer, button_number, pressed)
    - peer: the client that is the origin of the message
    
    - button_number: integer value >0 that identifies the button.
    - pressed: True if the button has been pressed, False if
               the button has been released.
    """

    _button_listeners.add(listener)
    
def remove_button_listener(listener):
    """Removes the specified button listener."""
    _button_listeners.discard(listener)

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
    _session_listener.remove(listener)

def set_world_width(width):
    """Sets the with of the game world to be displayed."""

    for peer in _peers.itervalues():
        peer.set_world_width(width)

def destroy_entity(entity_id):
    """Destroys the entity representation with the specified id."""

    for peer in _peers.itervalues():
        peer.destroy_entity(entity_id)
        
def spawn_entity(entity_id, x, y, angle, vertices):
    """Spans a new entity representation.
    Required arguments are:
    
    - id of the entity (typically a string),
    - the position within the game world (x, y),
    - the orientation (angle)
    - a list of vertices (to be rendered as polygon).
    """

    for peer in _peers.itervalues():
        peer.spawn_entity(entity_id, x, y, angle, vertices)
    

def move_entity(entity_id, x, y, angle):
    """Moves the entity representation to the specified position."""

    for peer in _peers.itervalues():
        peer.move_entity(entity_id, x, y, angle)
    
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
    """Disconnects all client and terminates active session."""
    for peer in _peers.itervalues():
        peer.disconnect(True)
        
    if _session_started:
        _stop_session()

    _peers.clear()


def startup(num_clients = 1, port = 12345):
    """Initializes the network and protocol."""
    global _num_clients
    
    assert not _num_clients, 'network already started'
    network.startup(port = port)   
    _num_clients = num_clients

    
def shutdown():
    """Shuts the nerwork down and disconnects from clients."""
    global _num_clients
    assert _num_clients, 'network not started'
    disconnect()
    _num_clients = False
    network.shutdown()

def _process(msg):
    _decoder.reset(msg[0])
    addr = msg[1]

    # get peer and decode message id (mid)
    peer = _peers.get(addr, None)
    mid = _decoder.read_string()

    if not peer:
        if mid == 'connect':
            peer = Peer(addr, _decoder.create_encoder())
            if not _session_started:
                _peers[addr] = peer
                peer.accept()
            else:
                peer.refuse()

            for listener in _connection_listeners:
                listener(peer.addr, True)
        else:
            # ignore messages if peer is not connected
            return

    if mid == 'disconnect':
        _peers.pop(addr)
        for listener in _connection_listeners:
            listener(peer.addr, False)
            
    elif mid == 'axis':
        axis = _decoder.read_int()
        value = _decoder.read_float()
        
        for listener in _axis_listeners:
            listener(peer.addr, axis, value)
            
    elif mid == 'button':
        button = _decoder.read_int()
        pressed = _decoder.read_bool()
        
        for listener in _button_listeners:
            listener(peer.addr, button, pressed)

    # maintain session state        
    if _session_started and len(_peers) < _num_clients:
        _stop_session()
    elif not _session_started and len(_peers) >= _num_clients:
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
    
    num_players = 1
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