# geocodes addresses in a csv file and outputs them to a Shapefile

import csv
import os
import time
from geopy.geocoders import Nominatim
from shapely.geometry import Point, mapping
from fiona import collection
from fiona.crs import from_epsg
from collections import Counter

start_time = time.ctime()

# address field called 'Address' and includes a property field titled "Date"
in_table = "PATH.csv"
out_geocoded_file = "PATH.shp"

geolocator = Nominatim

print ("--------------------------------")

geocode_list = []
fail_list = []

add_count = success_count = fail_count = 0
with open(in_table) as csv_table:
    reader = csv.DictReader(csv_table, delimiter=',')
    for row in reader:
        if row['Address'] != '':
            x = (str(row['Address']))
            time.sleep(1)
            location = geolocator.geocode(x, timeout=60)
            print x
            try:
                print((location.latitude, location.longitude))
                success_count += 1
                geocode_list.append((row['Address'],row['Date'],location.longitude,location.latitude))
            except:
                fail_list.append(x)
                print("Geocode FAIL")
                fail_count += 1
            add_count += 1
            print add_count
            print ("--------------------------------")

geo_format="ESRI Shapefile"
epsg = from_epsg(4326)

geo_schema = { 'geometry': 'Point',
                'properties': {
                        'address':'str',
                        'year':'str',
                        'X':'float',
                        'Y':'float'
                    } }

with collection (out_geocoded_file, "w", driver=geo_format, crs=epsg, schema=geo_schema) as output:
    for x in geocode_list:
        print (x[0], x[1], x[2], x[3])
        print ("--------------------------------")

        point = Point(float(x[2]), float(x[3]))

        output.write({
            'properties': {
                'address':x[0],
                'year': x[1],
                'X': x[2],
                'Y': x[3]
            },
            'geometry': mapping(point)
        })


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("those that failed...")
for f in fail_list:
    print f
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print add_count
print success_count
print fail_count
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
end_time = time.ctime()
print start_time
print end_time
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
