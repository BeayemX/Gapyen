scopes = []
tags = {}
shapes = {}
timelines = {}


def register_entity(component):
    if not scopes:
        push_scope()

    #component.activate()
    scopes[-1].append(component)

# TODO should the children of the component also be removed?
def deregister_entity(component):
    component.deactivate()
    scopes[-1].remove(component) # todo not sure if this works, what if componenet is not in the last scope?


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


def register_timeline(name, timeline):
    timelines[name] = timeline

def deregister_timeline(name):
    del timelines[name]


def register_shape(name, shape):
    shapes[name] = shape

def unregister_shape(name):
    del shapes[name]