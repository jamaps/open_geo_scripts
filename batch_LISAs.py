# writes LISAs (Local Moran's I and Getis Ord) to csv table for each field in a shapefile

import os
import pysal
from pysal.esda.getisord import G_Local
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

csv write setup
out_table = r"/PATH.csv"
writer = csv.writer(open(out_table, 'a'))

for i in range(layerDefinition.GetFieldCount()):
     fieldName =  layerDefinition.GetFieldDefn(i).GetName()
     fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
     fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
     fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
     GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
     print fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision)
     print "_______"
     if fieldName == "CTUID_1996":
         x = np.array(dbf.by_col[fieldName])
         writer.writerow(x)
     else:
         y = np.array(dbf.by_col[fieldName])
         lm = pysal.Moran_Local(y,w)
         I = lm.Is
         writer.writerow(I)
         Z = lm.z_sim
         writer.writerow(Z)
         P = lm.p_sim
         writer.writerow(P)
         Q = lm.q
         writer.writerow(Q)
         lgstar = G_Local(y, w, transform='R', star=True)
         GZ = lgstar.Zs
         writer.writerow(GZ)
         Gp = lgstar.p_norm * 2 #because two tailed
         writer.writerow(Gp)

end_time = time.clock()

print (end_time - begin_time)
