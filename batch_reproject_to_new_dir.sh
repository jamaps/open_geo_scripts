# loops through folders in a directory
# picks shps and copies file names to new folder in an out folder
# reprojects shps to NAD83 and puts them in the out folders with same folder structure

# creat out folder
mkdir "out"
# loop through directory
for d in */ ; do
  echo "$d"
  # loop through sub dirs
  for i in "$d"*.shp ; do
  	# print info:
  	echo "$i"
    echo "${d%?}"
    #echo "$x"
    # assign new projection and put in output folder
    pwd
    cd out
    pwd
    mkdir "$d"
    cd ..
    ogr2ogr out/"${d%?}"/"${d%?}".shp -t_srs "EPSG:4269" "$i"
  done
  echo "----------------------------"
done
