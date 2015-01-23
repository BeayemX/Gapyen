from Components import *


instance = None  # singleton


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise Exception("EventType doesn't exist!")

EventType = Enum(["ResetGame", "WallCollision"])


class EventSystem(TimeUpdatable):
    def __init__(self):
        TimeUpdatable.__init__(self)

        self.events = {}
        self.event_queue = []

        for key in EventType:
            self.events[key] = []

    def activate(self):
        TimeUpdatable.activate(self)
        self.gameobject.send_event = self.send_event
        self.gameobject.trigger_event = self.trigger_event
        self.gameobject.register_event_listener = self.register_event_listener
        self.gameobject.deregister_event_listener = self.deregister_event_listener

    def deactivate(self):
        del self.gameobject.send_event
        del self.gameobject.trigger_event
        del self.gameobject.register_event_listener
        del self.gameobject.deregister_event_listener
        TimeUpdatable.deactivate(self)

    def update(self, delta):
        self.work_queue()

    def work_queue(self):
        working_queue = list(self.event_queue)
        self.event_queue = []
        for eventtype in working_queue:
            print "work " + eventtype
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