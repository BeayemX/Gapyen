import GameManager
from vector import Vec2
import settings

def process_button(button, down):

    if button == 0:  # space
        if down:
            # todo make event system accessible through GameManager
            # GameManager.find("Event System").trigger_event("ResetGame")  # pong
            ship = GameManager.find("Ship1")  # todo crap string comparison
            ship.shoot_bullet()

    if button == 1:
        if down:
            ship = GameManager.find("Ship1")  # todo crap string comparison
            ship.shoot_missile()
    elif button == 2:
        print "Ctrl-L"
    elif button == 3:
        print "Ctrl-R"
    else:
        print button


def process_axis(axis, value):
    """
    pong
    if axis == 0:
        paddle = GameManager.find("paddle1")  # todo crap string comparison
        paddle.add_force(Vec2(settings.paddlespeed * value, 0))
    elif axis == 1:
        paddle = GameManager.find("paddle1")  # todo crap string comparison
        paddle.add_force(Vec2(0, -settings.paddlespeed * value))
    elif axis == 2:
        paddle = GameManager.find("paddle0")  # todo crap string comparison
        paddle.add_force(Vec2(settings.paddlespeed * value, 0))
    elif axis == 3:
        paddle = GameManager.find("paddle0")
        paddle.add_force(Vec2(0, -settings.paddlespeed * value))
    else:
        raise Exception("Wrong Axis?")
    """

    if axis == 0:
        ship = GameManager.find("Ship1")  # todo crap string comparison
        ship.steer(-value)
    elif axis == 1:
        ship = GameManager.find("Ship1")  # todo crap string comparison
        ship.accelerate(-value)

    elif axis == 2:
        ship = GameManager.find("Ship2")  # todo crap string comparison
        ship.steer(-value)
    elif axis == 3:
        ship = GameManager.find("Ship2")  # todo crap string comparison
        ship.accelerate(-value)


