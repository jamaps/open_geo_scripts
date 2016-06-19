# clips all .shps in folder to a boundary polygon

# clips all .shps in folder

from subprocess import call
import os

# in dir of to be clipped shps
shp_folder = "nrn_rrn_on_shp_en"

# clip poly if this is your choice
clip_poly = "clip_bound_2.shp"

# clip bounds if this is your choice [N,S,E,W]
clip_bounds = [45,42.75,-77.85,-80.9]

# output dir name
# os.mkdir("clipped")

for subdir, dirs, files in os.walk(shp_folder):
    for file in files:
		if file.endswith(('.shp')):
			print file

			# for clipping by a boundary
			# call(["ogr2ogr", "-clipsrc", clip_poly, "clipped/" + file, shp_folder + '/' + file])

			# for clipping by an extent (much faster i hope)
			call(["ogr2ogr", "-f", "ESRI Shapefile", "clipped/" + file, shp_folder + '/' + file, "-clipsrc", clip_bounds[3], clip_bounds[1], clip_bounds[2], clip_bounds[0])
