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

import socket, select

BUFFER_SIZE = 1024

_received = []
_to_send = []
_sockets = []
_read = []
_write = []

def send_message(msg):
    """Sends the given message.
    Message must be a tuple in the form of (message_data, client_addr).
    
    Messages will be queued and send as soon as possible, but not before
    the next update cycle.
    """
    msg_data = msg[0]
    addr = msg[1]
    _to_send.append((msg_data, addr))

def fire_message(msg):
    """Sends the given message immediatly without queueing it.
    Message must be a tuple in the form of (message_data, client_addr).
    """
    assert len(_write) <= 1, 'only one outgoing socket supported'
    data = msg[0]
    addr = msg[1]
    for sock in _write:
        sock.sendto(data, addr)

def get_messages():
    result = list(_received)
    _received[:] = []
    return result

def startup(server_name = '', port = 12345):
    assert(len(_sockets) == 0)
    #initialize
    main_socket = socket.socket(type=socket.SOCK_DGRAM)
    main_socket.bind((server_name, port))
    
    _sockets.append(main_socket)
    _read.append(main_socket)
    _write.append(main_socket)

def shutdown():
    #cleanup
    
    for s in _sockets:
        s.close()
    _sockets[:] = []
    _read[:] = []
    _write[:] = []
    
    _received[:] = []
    _to_send[:] = []

def _process_exceptions(exceptional):
    if exceptional:
        # TODO figure out what the problem was and produce proper exception
        raise Exception('socket error')
        
def _process_readable(readable):
    try:
        for s in readable:
            _received.append(s.recvfrom(BUFFER_SIZE))
    except socket.error:
        # TODO more details error handling
        pass

def _process_writeable(writeable):
    assert(len(writeable) <= 1)

    if not writeable or not _to_send:
        # nothing to do
        return

    msg = _to_send.pop(0)
    msg_data = msg[0]
    addr = msg[1]
    for s in writeable:
        s.sendto(msg_data, addr)
        
def update():
    r, w, e = select.select(_read, _write, _sockets, 0)
    while e or r or (w and _to_send):
        _process_exceptions(e)
        _process_readable(r)
        _process_writeable(w)
        r, w, e = select.select(_read, _write, _sockets, 0)


if __name__ == '__main__':
    import time
    print "starting test echo server"
    startup()

    try:
        while True:
            update()
            for msg in get_messages():
                print 'received message from %s:%s' % msg[1]
                print 'message data: %s' % msg[0]
                send_message(msg)
                
            time.sleep(0.5)
    except KeyboardInterrupt:
        print "shuting down echo server"
        shutdown()
