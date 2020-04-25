import uuid

class City:
    def __init__(self, x, y):
        self.name = uuid.uuid4().hex
        self.x = x
        self.y = y
