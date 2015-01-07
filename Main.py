from Managers import UpdaterManager

from Components.NetworkWrapper import NetworkWrapper
from Components.Component import Component
from Components.UpdateComponent import UpdateComponent


def main():
    network = NetworkWrapper("networkwrapper")
    #GameLoop.runGameLoop()

    parent = Component("parent")
    parent.addchildren(UpdateComponent("gameloop", 60))
    # parent.addchildren(UpdateComponent("network", 5)) # doesnt do anything
    # parent.addchildren(UpdateComponent("randPos", 0.5)) # doesnt do anything
    parent.addchildren(network)

    UpdaterManager.startLoop()

if __name__ == "__main__":
    main()
