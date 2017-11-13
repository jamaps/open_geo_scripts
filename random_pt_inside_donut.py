# simple functionf for computing a random point inside a "donut" (between two buffer rings)

# r1 = radius of inner buffer
# r2 = radius of outer buffer
# x1, y1 = centre coordinate

import math
import random

def random_point_inside_donut(r1,r2,x1,y1):
    h = random.random()
    h = r1 + h * (r2 - r1)
    angle = random.random() * 2 * math.pi
    y2 = h * math.sin(angle) + float(y1)
    x2 = h * math.cos(angle) + float(x1)
    return([x2,y2])
