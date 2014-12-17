import GameManager
from Component import Component

GameManager.push_scope()

p = Component("Player")
p.addchildren(Component("InputProcessor"))
p.addchildren(Component("Health"))
p.addchildren(Component("Movement"))
p.addchildren(Component("Inventory"))

d = Component("Enemy")
d.addchildren(Component("Movement"))
d.addchildren(Component("Health"))

GameManager.remove_entity(p)

pass