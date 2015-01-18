import time
import GameManager

from Clock import Clock

clock = Clock()


def start_loop():

    t = GameManager.timelines["DefaultTimeline"]

    while True:
        delta = clock.tick()
        t.elapse_time(delta)
        time.sleep(t.time_till_next_call())  # nothing can be updated faster than the time source