# freitag
#   ball outside screen
#   reset ball
#   score in output?
#   movement not so crappy
#   acc?

# screen: game settings class?: aspect ration

# physics
#   acceleration
# dead reckoning
#   new game terminal
#       buttons
#
# pose transimitter
# vel transmitter?
# acc transmitter?
"""
gravity / acceleration
"""

# game states

# todo now
"""
timeline adding more practical
it works with use_updater but its strange if i don't know the timelines...?
use_updater on gameobject or not?...
updater in .gameobject needed?

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

# todo OLD STUFF
# todo game terminals working over network?