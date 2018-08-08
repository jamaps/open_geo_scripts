# converts shapes and stops in GTFS to mappable geojson format

import json, csv

# input gtfs folder name
gtfs_in = "GO_GTFS"


# converting stops.txt to a geojson object
def stops_to_geojson(gtfs_folder_name):

    out_geojson_stops = {
                'type': 'FeatureCollection',
                'features': [
                ]
    }

    with open(gtfs_folder_name + "/stops.txt","r") as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            feature = {
                "type": "Feature",
                "properties": {
                    "stop_id": row["stop_id"],
                    "stop_name": row["stop_name"]
                },
                "geometry": {
                    'type': 'Point',
                    'coordinates': [float(row["stop_lon"]),float(row["stop_lat"])]
                }
            }

            out_geojson_stops["features"].append(feature)

    return out_geojson_stops



# converting shapes.txt to a geojson object
def shapes_to_geojson(gtfs_folder_name):

    out_geojson_shapes = {
                'type': 'FeatureCollection',
                'features': [
                ]
    }

    with open(gtfs_folder_name + "/shapes.txt","r") as csvfile:
        reader = csv.DictReader(csvfile)

        c_shape_id = "0"

        c = 0

        coord_list = []

        for row in reader:

            if c_shape_id != row["shape_id"]:

                feature = {
                    "type": "Feature",
                    "properties": {
                        "shape_id": c_shape_id
                    },
                    "geometry": {
                        'type': 'LineString',
                        'coordinates': coord_list
                    }
                }

                out_geojson_shapes["features"].append(feature)

                c_shape_id = row["shape_id"]
                coord_list = []
                coord_list.append([float(row["shape_pt_lon"]),float(row["shape_pt_lat"])])
                c += 1

            else:

                coord_list.append([float(row["shape_pt_lon"]),float(row["shape_pt_lat"])])

            # if c > 5:
            #     break

    return out_geojson_shapes


# run and write the data

stops = stops_to_geojson(gtfs_in)
with open(gtfs_in + 'stops.geojson', 'w') as file:
     file.write(json.dumps(stops))


shapes = shapes_to_geojson(gtfs_in)
with open(gtfs_in + 'shapes.geojson', 'w') as file:
     file.write(json.dumps(shapes))

