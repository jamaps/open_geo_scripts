for i in coverage*
do
	echo "----------------------------"
	cd "$i"
	for f in *
		do
		echo "$f"
		ogr2ogr -f "ESRI Shapefile" "shp_$f" "$f"
	done
	cd ..
done
