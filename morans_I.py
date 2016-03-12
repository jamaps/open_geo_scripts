# loops through all fields in a shp/dbf and outputs moran's I, z-score, and p-value of each to a csv table

import os
import pysal
import csv
import time
import numpy as np
from osgeo import ogr

begin_time = time.clock()

#open shp
shp = "PATH.shp"

#gdal layer reader
driver = ogr.GetDriverByName('ESRI Shapefile')
dataSource = driver.Open(shp, 0) # 0 means read-only. 1 means writeable.
layer = dataSource.GetLayer()
layerDefinition = layer.GetLayerDefn()

#open dbf
dbf = pysal.open('PATH.dbf','r')

# create spatial weight matrix
w = pysal.queen_from_shapefile(shp)

# csv write setup
out_table = r"PATH.csv"
writer = csv.writer(open(out_table, 'a'))

for i in range(layerDefinition.GetFieldCount()):
     fieldName =  layerDefinition.GetFieldDefn(i).GetName()
     fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
     fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
     fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
     GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
     print fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision)
     print "_______"
     y = np.array(dbf.by_col[fieldName])
     mi = pysal.Moran(y, w, two_tailed=False)
     print "I = %f" %mi.I
     print "Z-score = %f" %mi.z_norm
     print "p-value = %f" %mi.p_norm
     I = mi.I
     Z = mi.z_norm
     P = mi.p_norm
     row = [fieldName, I, Z, P]
     writer.writerow(row)
     print "_______"
     print "_______"

end_time = time.clock()

print (end_time - begin_time)
