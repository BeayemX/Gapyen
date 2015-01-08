from Components import ComponentBuilder

from Managers import UpdaterManager
import TimelineManager
from Components.NetworkWrapper import NetworkWrapper
from Components.Component import Component
from Components.UpdateComponent import UpdateComponent
from Timeline import Timeline
from Components.Updatable import Updateable
from Components.StaticPose import StaticTransform
from Components.NetworkWrapper import NetworkWrapper
from Components.Shape import Shape
from Components.randompose import RandomPose

def main():
    """
    #GameLoop.runGameLoop()

    parent = Component("parent")
    parent.addchildren(UpdateComponent("gameloop", 60))
    # parent.addchildren(UpdateComponent("network", 5)) # doesnt do anything
    # parent.addchildren(UpdateComponent("randPos", 0.5)) # doesnt do anything
    parent.addchildren(network)

    UpdaterManager.startLoop()
    """


    timeline_slow = Timeline("Slow")
    timeline_slow.timescale = 0.5


    network = Component()
    network.add(NetworkWrapper("Default"))

    c1 = ComponentBuilder.build_triangle()

    updatable = Component()
    updatable.add(Updateable(2, "Slow"))
    updatable.add(StaticTransform((-10, 0), 0))

    triangle = ComponentBuilder.build_triangle()
    triangle.add(RandomPose(10, 10))


    UpdaterManager.startLoop()



if __name__ == "__main__":
    main()
