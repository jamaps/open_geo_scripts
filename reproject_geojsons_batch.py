# run with shell ogr2ogr commands installed

import os
import time
from subprocess import call

start_time = time.time()

geojsons_in_folder = "geojsons"
geojsons_out_folder = "geojsons_nad83"
slash = "//"

for root, dirs, files in os.walk(geojsons_in_folder):
    for gj in files:
        if gj.endswith(".geojson"):
            print("gj")
            call(["ogr2ogr", "-f", "GeoJSON", geojsons_out_folder + slash + "nad83_%s" %gj,"-t_srs", "EPSG:4269", geojsons_in_folder + slash + gj])

print("--- %s seconds ---" % (time.time() - start_time))
