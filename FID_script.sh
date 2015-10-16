############################
# shell script for batch renaming, reprojecting, and converting to GTiff
# works in GDAL version 1.11
############################

# start runtime
start=`date +%s`

# create output folder
mkdir "GTiff_output"

# loop through img files (various extensions)
for i in *.{jpg,JPG,tif,tiff,jp2} # add more ext HERE
do
	# print info:
	echo "----------------------------"
	echo "$i"
	gdalinfo "$i"
	echo "----------------------------"
	# copy filename without extension:
	f="${i%.*}"
	# convert to geotiff and put in output folder:
	gdal_translate -of "GTiff" "$i" GTiff_output/"$f".tif
done

# change working directory to output folder:
cd GTiff_output

# loop through output folder
for t in *.tif
do
	echo "$t"
	# new file name
	n=$(echo $t | tr ' ' '_' | tr '-' '_' )
	m="${n%.*}"
	# reproject to WGS84
	gdalwarp -srcnodata None -dstnodata None -dstalpha -t_srs "EPSG:4326" "$t" "$n.tif"
	# print info of reprojected raster
	echo "----------------------------"
	echo "$n"
	gdalinfo "$n.tif"
	echo "----------------------------"
	# remove unprojected raster
	rm "$t"
done

# remove extra ".tif" in name
for q in *.tif
do
	m="${q%.*}"
	mv "$q" "$m"
done
end=`date +%s`

# print results
echo "----------------------------"
echo "Converted to WGS84 GTiff:"
for z in *.tif
do
	echo "$z"
done
# end runtime and print
runtime=$((end-start))
echo "----------------------------"
echo "Elapsed Time:"
echo "$runtime seconds"
echo "----------------------------"
echo "----------------------------"
