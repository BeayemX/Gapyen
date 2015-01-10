scopes = []
tags = {}
shapes = {}
timelines = {}


def register_entity(component):
    if not scopes:
        push_scope()

    #component.activate()
    scopes[-1].append(component)


def deregister_entity(component):
    component.deactivate()
    # todo not sure if this works, what if componenet is not in the last scope?
    scopes[-1].remove(component)


def push_scope():
    scopes.append([])


def pop_scope():
    scope = scopes.pop()
    for component in scope:
        component.deactivate()


# todo not tested yet
def register_tag(tag, entity):
    for key in tags:
        if key == tag:
            tags[tag].append(entity)
            return

    tags[tag] = []
    tags[tag].append(entity)


def deregister_tag(tag, entity):
    tags[tag].remove(entity)


def register_timeline(timeline):
    timelines[timeline.name] = timeline


def deregister_timeline(name):  # todo make call possible via name or GO.
    del timelines[name]


def register_shape(shape):
    shapes[shape.name] = shape


def deregister_shape(name):  # todo make call possible via name or GO
    del shapes[name]