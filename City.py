import random
import uuid


class City:
    def __init__(self):
        position = self.generatePosition()
        self.name = uuid.uuid4().hex
        self.x = position[0]
        self.y = position[1]

    def generatePosition(self):
        return random.randint(0, 1000), random.randint(0, 1000)
