# todo now
"""
timeline adding more practical
component.activate() somehow more practical?
"""

# todo [collision] vertices value ignore rotation

# todo when should components be activated? in constructor? method call? game manager?
# todo list for all physik obj to check collision against each other

# todo go through main.py and put stuff into activate(). like register_timeline etc.
# use component builder for more classes

# todo use uid instead of name?
# todo test pausing timelines
# todo should updatable have elapsed time? i.e. if entity is spawned later in game...?
# if so.... use Updatable[base class] to increase time and call Updatable.update() in inheritetd classes


# TODO PONG

# states
"""
IDLE
PLAYING
"""
"""
"""

"""
ball
    id
    poly
    body
    collision detection
    life cycle
    pos_transmitter
    balllogic

paddle
    id
    poly
    lifecycle
    body
    collision
    netgamepad
    paddlelogic!! not reusable, just for paddle
    pos_transmitter
"""


# todo assignment
"""
pausable, everybody can unpause
"""

# todo also implement modules as componeents so that there is one 'Game'-Root-Componeent and everything.
# singleton? or how access globally?
# is implemented inside that or hierarchically as children...
# todo timeline reset()

# todo OLD STUFF
# todo game terminals working over network?