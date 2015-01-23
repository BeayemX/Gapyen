# freitag
# wie genau die acceleration einbauen?
# wenn man posetransmitter nur 3x / sec aufruft weiss das terminal dann, dass
#   es die pos aendern soll?
#   --> dead reckoning? wie einbauen?


# todo QUEUE EVENTS
#   send event --> queue
#   fire event --> immediately
# copy list before iterating over it?
# delay for messages
# eventsystem should be timeupdatable. use tim1estamp for delayed msgs
# enum for event types?

# game states?

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

# todo go through main.py and put stuff into activate(). like register_timeline etc.
# use component builder for more classes

# todo use uid instead of name?
# todo test pausing timelines

# TODO states
"""
IDLE
PLAYING
"""

# todo pose transmitter not as timeline but instead on gameobject?
# todo input controller not as module but instead on gameobject?


# todo assignment
"""
pausable, everybody can unpause
"""

# TODO? only one 'Game'-Root-Component
# all modules as children of this component?
# because at the moment all components are just in the list but no hierarchy

# todo call xprotocol.destroy_entity somewhere?

# TODO cleanup
# import * --> bad
# split into mutliple files not one big componenet file?
# modules?