# clips all .shps in folder to a boundary polygon

from subprocess import call
import os

# in dir of to be clipped shps and boundary file
shp_folder = "nrn_rrn_on_shp_en"
clip_poly = "clip_bound.shp"

# output dir
os.mkdir("clipped")

c = 0
for subdir, dirs, files in os.walk(shp_folder):
	for file in files:
	 	if file.endswith(('.shp')):
			print file
			call(["ogr2ogr", "-clipsrc", clip_poly, "clipped/" + file, shp_folder + '/' + file])
			c += 1
print c
