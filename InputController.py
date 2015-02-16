import GameManager
from vector import Vec2
import settings

def process_button(button, down):

    if button == 0:  # space
        if down:
            ship = GameManager.find("Ship1")  # todo crap string comparison
            if ship:
                ship.shoot_bullet()
    elif button == 1:  # return
        if down:
            ship = GameManager.find("Ship2")  # todo crap string comparison
            if ship:
                ship.shoot_missile()
    elif button == 2:  # ctrl left
        if down:
            ship = GameManager.find("Ship1")  # todo crap string comparison
            if ship:
                ship.shoot_missile()
    elif button == 3:  # ctrl right
        if down:
            ship = GameManager.find("Ship2")  # todo crap string comparison
            if ship:
                ship.shoot_bullet()


    else:
        print "button: " + str(button)


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
        ship = GameManager.find("Ship2")  # todo crap string comparison
        if ship:
            ship.steer(-value)
    elif axis == 1:
        ship = GameManager.find("Ship2")  # todo crap string comparison
        if ship:
            ship.accelerate(-value)

    elif axis == 2:
        ship = GameManager.find("Ship1")  # todo crap string comparison
        if ship:
            ship.steer(-value)
    elif axis == 3:
        ship = GameManager.find("Ship1")  # todo crap string comparison
        if ship:
            ship.accelerate(-value)


