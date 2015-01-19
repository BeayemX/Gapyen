import GameManager
from vector import Vec2


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
        paddle = GameManager.find("paddle1")
        paddle.move_by(Vec2(value, 0))
    elif axis == 1:
        paddle = GameManager.find("paddle1")
        paddle.move_by(Vec2(0, -value))
    elif axis == 2:
        paddle = GameManager.find("paddle0")
        paddle.move_by(Vec2(value, 0))
    elif axis == 3:
        paddle = GameManager.find("paddle0")
        paddle.move_by(Vec2(0, -value))

    else:
        print axis
        #raise Exception("Wrong Axis?")