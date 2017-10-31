cd in_folder
mkdir out_folder

for i in *.dbf
do
	echo "----------------------------"
  echo i
  f="${i%.*}"
	echo "$f"
  ogr2ogr -f CSV out_folder/"$f".csv "$i"
done
