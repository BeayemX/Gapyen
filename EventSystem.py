from Components import *


instance = None  # singleton

class EventSystem(TimeUpdatable):
    def __init__(self):
        TimeUpdatable.__init__(self)

        self.events = {}
        self.event_queue = []
        self.waiting_event_queue = []
        self.elapsedtime = 0.0

        messages = ["P1LostLife", "P2LostLife"]

        for msg in messages:
            self.events[msg] = []

    def activate(self):
        TimeUpdatable.activate(self)
        self.gameobject.send_event = self.send_event
        self.gameobject.send_event_after_sec = self.send_event_after_sec
        self.gameobject.trigger_event = self.trigger_event
        self.gameobject.register_event_listener = self.register_event_listener
        self.gameobject.deregister_event_listener = self.deregister_event_listener

    def deactivate(self):
        del self.gameobject.send_event
        del self.gameobject.send_event_after_sec
        del self.gameobject.trigger_event
        del self.gameobject.register_event_listener
        del self.gameobject.deregister_event_listener
        TimeUpdatable.deactivate(self)

    def update(self, delta):
        self.elapsedtime += delta
        self.work_queue()

    def work_queue(self):
        # check if waiting events should be triggered
        waiting_queue = list(self.waiting_event_queue)
        for waitingevent in waiting_queue:
            if self.elapsedtime > waitingevent[1]:
                self.send_event(waitingevent[0])
                self.waiting_event_queue.remove(waitingevent)

        working_queue = list(self.event_queue)
        self.event_queue = []
        for eventtype in working_queue:
            self.trigger_event(eventtype)

    def send_event(self, event):
        self.event_queue.append(event)

    def trigger_event(self, eventtype):
        for method in self.events[eventtype]:
            method()

    def register_event_listener(self, eventtype, listener):
        self.events[eventtype].append(listener)

    def deregister_event_listener(self, eventtype, listener):
        self.events[eventtype].remove(listener)

    def send_event_after_sec(self, eventtype, time):
        self.waiting_event_queue.append([eventtype, self.elapsedtime + time])