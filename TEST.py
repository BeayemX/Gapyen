from GameManager import GameManager
from Container import Container
from Component import Component

def comp(name):
    return Component(name)

def cont(name):
    return Container(name)

gm = GameManager()

c = cont("Player")
c.addComponent(comp("InputProcessor"))
c.addComponent(comp("Health"))
c.addComponent(comp("Movement"))
c.addComponent(comp("Inventory"))

d = cont("Enemy")
d.addComponent(comp("Movement"))
d.addComponent(comp("Health"))

gm.addContainer(c)
gm.addContainer(d)


