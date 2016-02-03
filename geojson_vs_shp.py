# compares the sizes of geojsons to shps for the same spatial features

import os
import matplotlib.pyplot as plt
import numpy as np
import shutil
import time
from osgeo import ogr
from subprocess import call

# temp directory for converted files
os.mkdir("test_output")

# shell script for shp to geojson
def to_geojson(shp):
    name = shp.split('.')[0]
    call(["ogr2ogr","-f", "GeoJSON", "test_output/%s.geojson" %name, shp])

# shell script for geojson to shp
def to_shp(geojson):
    name = geojson.split('.')[0]
    call(["ogr2ogr","-f", "ESRI Shapefile", "test_output/%s.shp" %name, geojson])

geojson_list = []
shp_list = []

# loop through shps in directory, converting using functions and storing file sizes
for f in os.listdir('.'):
     if os.path.isfile(f) and f.endswith(('.shp')):
         print f
         print f.split('.')[0]
         to_geojson(f)
         g = "%s" %f
         to_shp(g)
         shp_size = (os.stat('test_output/%s.shp' %f.split('.')[0])).st_size
         dbf_size = (os.stat('test_output/%s.dbf' %f.split('.')[0])).st_size
         shx_size = (os.stat('test_output/%s.shx' %f.split('.')[0])).st_size
         geojson_size = (os.stat('test_output/%s.geojson' %f.split('.')[0])).st_size
         shapefile_size = shp_size + dbf_size + shx_size
         geojson_list.append(float(geojson_size)/1000000)
         shp_list.append(float(shapefile_size)/1000000)

shutil.rmtree("test_output")

print "---------"

# plot results with pyplot
print geojson_list
print shp_list
plt.plot(geojson_list,shp_list,'ro')
plt.plot([0,20],[0,20])
plt.axis([0, 20, 0, 20])
plt.show()
