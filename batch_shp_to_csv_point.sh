# converts points to XY columns

cd in_folder
mkdir out_folder

for i in *.shp
do
  echo "----------------------------"
  echo i
  f="${i%.*}"
  echo "$f"
  ogr2ogr -f CSV out_folder/"$f".csv "$i" -lco GEOMETRY=AS_XY
done
