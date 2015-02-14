scopes = []
bodies = []
colliders = []
gameobjects = []  # todo not sure if necessary
shapes = []

tags = {}
timelines = {}


def register_entity(component):
    if not scopes:
        push_scope()

    #component.activate()
    scopes[-1].append(component)


def deregister_entity(component):
    for scope in scopes:
        for comp in scope:
            if comp == component:
                scope.remove(comp)


def push_scope():
    scopes.append([])


def pop_scope():
    scope = scopes.pop()
    for component in scope:
        component.deactivate()


def register_body(body):
    bodies.append(body)


def deregister_body(body):
    bodies.remove(body)


def register_collider(collider):
    colliders.append(collider)


def deregister_collider(collider):
    colliders.remove(collider)


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
    # todo remove me when using .uid instead of .name
    for s in shapes:
        if s.name == shape.name:
            raise Exception("Using existing name '" + s.name + "'! Will lead to problems with "
                            "xprotocol.spawn_entity()")
    shapes.append(shape)


def deregister_shape(shape):
    shapes.remove(shape)


def find(name):
    for GO in gameobjects:
        if GO.name == name:
            return GO


def register_gameobject(go):
    gameobjects.append(go)


def deregister_gameobject(go):
    gameobjects.remove(go)