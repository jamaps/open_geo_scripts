# converts pairs of points in csv row into geojson line segments

# e.g. if there is a row with [xi,yi,xj,yj] it converts it to a line segment of i to j

# it was built to map varying map mapmatching

import csv
import json

points = []
with open("translate_table.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            points.append([row['cma'],float(row['xi']),float(row['yi']),float(row['xg']),float(row['yg'])])
        except:
            None

# empty features list for geojson
features_list = []

for pt in points:

    # could add something about the angle !

    ft = { "type": "Feature",
        "geometry": {
        "type": "LineString",
        "coordinates": [[pt[1], pt[2]],[pt[3],pt[4]]]
        },
        "properties": {"cma": pt[0]}
        }
    features_list.append(ft)


# setting up the output geojson file
out_geojson = {"type":"FeatureCollection",
    "features": features_list
}

with open("translate_lines.geojson", 'w') as fp:
    json.dump(out_geojson, fp)
