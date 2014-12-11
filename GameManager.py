from Container import Container

class GameManager:

    containers = []
    
    def __init__(self):
        pass

    def addContainer(self, container):
        self.containers.append(container)

    def printOutline(self):
        print (str(self))

    def __str__(self):
        text = ""
        for cont in self.containers:
            text += (str(cont))
        return text
        
        
