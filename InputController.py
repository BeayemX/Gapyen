import GameManager
from vector import Vec2
import settings

def process_button(button, down):

    if button == 0:
        print "space"
    if button == 1:
        print "enter"
    elif button == 2:
        print "Ctrl-L"
    elif button == 3:
        print "Ctrl-R"
    else:
        print button


def process_axis(axis, value):

    if axis == 0:
        pass
    elif axis == 1:
        paddle = GameManager.find("paddle1")  # todo crap string comparison
        paddle.velocity = Vec2(0, -settings.paddlespeed * value)
    elif axis == 2:
        pass
    elif axis == 3:
        paddle = GameManager.find("paddle0")
        paddle.velocity = Vec2(0, -settings.paddlespeed * value)
    else:
        raise Exception("Wrong Axis?")