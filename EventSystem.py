class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise Exception("EventType doesn't exist!")

EventType = Enum(["ResetGame", "WallCollision"])

events = {}

for key in EventType:
    events[key] = []


def add_eventlistener(eventtype, method):
    events[eventtype].append(method)


def remove_eventlistener(eventtype, method):
    events[eventtype].remove(method)


def trigger_event(eventtype):
    for method in events[eventtype]:
        method()