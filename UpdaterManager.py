import time
import GameManager

from Clock import Clock

clock = Clock()


def start_loop():
    while True:
        delta = clock.tick()
        t = GameManager.timelines["Default"]
        t.elapse_time(delta)
        time.sleep(t.time_till_next_call())  # nothing can be updated faster than the time source