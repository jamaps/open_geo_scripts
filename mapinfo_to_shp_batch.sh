mkdir "shp_outs"
for i in *.tab
do
	# print info:
	echo "----------------------------"
	echo "$i"
	# copy filename without extension:
	f="${i%.*}"
	echo "$f"
	# convert to shp into output folder
	ogr2ogr -f "ESRI Shapefile" shp_outs/"$f".tab "$i"
  echo "----------------------------"
done
