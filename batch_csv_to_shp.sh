for i in *.csv
do
	echo "----------------------------"
	echo "$i"
	f="${i%.*}"
	echo "$f"
	# using WGS84 :)
	ogr2ogr "$f".shp "$i" -dialect sqlite -sql "SELECT MakePoint(CAST(X as REAL), CAST(Y as REAL), 4326) Geometry, * FROM '$f'"
done
echo "----------------------------"
