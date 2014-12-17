from Component import Component

#TODO should there always be a scope. because it is possible to try to add_entity without a pushed_scope to cause an error

scopes = []


def add_entity(component):
    component.activate()
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
