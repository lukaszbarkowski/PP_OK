import math
from City import City

def getDistanceBetweenTwoCities(a: City, b: City):
    x = pow((b.x - a.x), 2)
    y = pow((b.y - a.y), 2)
    return math.sqrt(x + y)
