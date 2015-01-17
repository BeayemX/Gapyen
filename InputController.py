import GameManager
from vector import Vec2


def move_paddle(axis, delta):
    paddle = GameManager.find("paddle0")
    if axis == 0:
        paddle.move_by(Vec2(delta, 0))
    elif axis == 2:
        paddle.move_by(Vec2(0, -delta))
    else:
        raise Exception("Wrong Axis?")