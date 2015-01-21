events = {"Restart": []}


def add_eventlistener(eventname, method):

    for key in events:
        if key == eventname:
            events[eventname].append(method)
            return

    events[eventname] = []
    events[eventname].append(method)


def trigger_event(eventname):
    for method in events[eventname]:
        method()