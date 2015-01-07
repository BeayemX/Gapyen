from Managers import GameManager
from Components.Component import Component
import Managers.GameManager


GameManager.push_scope()

p = Component("Player")
p.activate()
print p.active
p.addchildren(Component("InputProcessor"))
p.addchildren(Component("Health"))
p.addchildren(Component("Movement"))
p.addchildren(Component("Inventory"))

d = Component("Enemy")
d.addchildren(Component("Movement"))
d.addchildren(Component("Health"))

#GameManager.remove_entity(p)