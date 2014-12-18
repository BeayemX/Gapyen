scopes = []


def add_entity(component):
    if not scopes:
        push_scope()

    #component.activate()
    scopes[-1].append(component)

# TODO should the children of the component also be removed?
def remove_entity(component):
    component.deactivate()
    scopes[-1].remove(component)


def push_scope():
    scopes.append([])


def pop_scope():
    scope = scopes.pop()
    for component in scope:
        component.deactivate()
