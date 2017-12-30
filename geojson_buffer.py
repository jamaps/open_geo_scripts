# creates a polygonoal buffer in geojson format given ...
# xin,yin = centre point
# radius = buffer radius
# npoints = number of points (e.g. 3 for triangle, 6 for hex, Inf. for circle, etc.)

import math
import matplotlib.pyplot as plt

def buffer(xin,yin,radius,npoints):

    x = []
    y = []
    coords = []

    angle_int = 2 * math.pi / npoints
    theta = 0
    c = 0
    while c < npoints:
        xj = xin + math.sin(theta)
        yj = yin + math.cos(theta)
        x.append(xj)
        y.append(yj)
        xyj = [xj,yj]
        coords.append(xyj)
        theta = theta + angle_int
        c += 1
    coords.append(coords[0])

    # plot the buffer for checking, can comment out if needed
    plt.scatter(x, y)
    plt.show()

    out_geojson = {
            'type': 'FeatureCollection',
            'features': [
                {'geometry': {
                    'type': 'MultiPolygon',
                    'coordinates': [[coords]]
                 },
                  'properties': {
                        'time': radius
                  }}
            ]
        }

    return out_geojson

print buffer(50,50,1,24)
