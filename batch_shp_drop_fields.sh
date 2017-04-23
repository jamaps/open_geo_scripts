# drop same field from a group of shps

for i in *.shp
do
	echo "----------------------------"
	echo "$i"
  f="${i%.*}"
	ogrinfo "$f".shp -sql "ALTER TABLE "$f" DROP COLUMN the_field_to_drop"
done
