import os
from osgeo import ogr

ws = r"PATH"

ref_list_check = []
x = "filler"
count = 0
fail_list = []

for subdir, dirs, files in os.walk(ws):
    for file in files:
        #print file
        #print os.path.join(subdir, file)
        if file.endswith(('.shp')):
            print "______________________________"
            print file
            shp = os.path.join(subdir, file)
            driver = ogr.GetDriverByName('ESRI Shapefile')
            dataSource = driver.Open(shp, 0)
            if dataSource is None:
                fail_list.append(file)
            else:
                print shp
                layer = dataSource.GetLayer()
                featureCount = layer.GetFeatureCount()
                print featureCount
                spatialRef = layer.GetSpatialRef()
                print spatialRef
                if x != str(spatialRef):
                    ref_list_check.append(1)
                x = str(spatialRef)
                count = count + 1

print "total shps checked:"
print count
print "_"
if fail_list != []:
    print "failed"
    print fail_list
if ref_list_check != [1]:
    print "there are multiple spatial refs"
else:
    print "all have the same spatial ref:"
    print spatialRef
