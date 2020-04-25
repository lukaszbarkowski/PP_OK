import random
import uuid


class City:
    def __init__(self,x,y):
       #position = self.generatePosition()
        self.name = uuid.uuid4().hex
        self.x = x
        self.y = y
       #self.x = position[0]
       #self.y = position[1]

    def generatePosition(self):
        return random.randint(0, 1000), random.randint(0, 1000)
