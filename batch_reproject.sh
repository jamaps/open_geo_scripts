mkdir "out"
for i in *.shp
do
	# print info:
	echo "----------------------------"
	echo "$i"
	# gdalinfo "$i"
	echo "----------------------------"
	# copy filename without extension:
	f="${i%.*}"
	echo "$f"
	# assign new projection and put in output folder
	ogr2ogr out/"$f".shp -t_srs "EPSG:4269" "$i"
done
