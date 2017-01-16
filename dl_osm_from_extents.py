import subprocess

def dl_osm_from_extents(xmax, xmin, ymax, ymin):

    # overpass url for grabbing data
    url = 'http://overpass-api.de/api/map?bbox=' + str(xmin) + ',' + str(ymin) + ',' + str(xmax) + ',' + str(ymax)

    # send the request
    subprocess.call(["wget", url])

    # temp name, since it returns it as this string
    temp_name = 'map?bbox=' + str(xmin) + ',' + str(ymin) + ',' + str(xmax) + ',' + str(ymax)

    # rename to map.osm.xml for future use!
    subprocess.call(["mv", temp_name, "map.osm.xml"])

# e.g.
dl_osm_from_extents(-77,-78,45,46)
