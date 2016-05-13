# batch converts Shapefiles to geojsons
mkdir "geojsons"
for i in *.shp
do
	# print info:
	echo "----------------------------"
	echo "$i"
	# copy filename without extension:
	f="${i%.*}"
	echo "$f"
	# convert to shp into output folder
	ogr2ogr -f "GeoJSON" "geojsons/$f.geojson" "$i"
  echo "----------------------------"
done
cd ..
