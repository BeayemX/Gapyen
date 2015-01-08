from Managers import GameManager
from Components.Component import Component
import Managers.GameManager


GameManager.push_scope()

p = Component("Player")
p.activate()
print p.active
p.add(Component("InputProcessor"))
p.add(Component("Health"))
p.add(Component("Movement"))
p.add(Component("Inventory"))

d = Component("Enemy")
d.add(Component("Movement"))
d.add(Component("Health"))

#GameManager.remove_entity(p)