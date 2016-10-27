# geocoding with geopy
# from address field in one csv into new csv with X,Y fields
# also outputs table of any records that failed

import csv
import os
import time
from geopy.geocoders import GoogleV3

# input csv dir/name.csv
csv_in = 'path/in.csv'

# output csv dir/name.csv
csv_out = 'path/geocoded.csv'
csv_out_fail = 'path/fail.csv'


# name of geocoding service
geolocator = GoogleV3()

# outputs
out_table = []
fail_table = []

with open(csv_in, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        header = row
        break
    counter = 0
    for row in reader:
        if row != header:
            try:
                address = row[2] + ", " + row[3] + ", " + row[15] # will be different for each csv - choose wisely
                print address
                time.sleep(1)
                location = geolocator.geocode(address, timeout=60)
                if location is None:
                    location = geolocator.geocode(row[15], timeout=60) # just geocode postal code
                lat = location.latitude
                lon = location.longitude
                print lon, lat

                out_row = row + [lon,lat]

                out_table.append(out_row)

            except:
                print 'FAIL'
                fail_table.append(row)

            counter += 1

# write outputs to file

with open(csv_out, 'w') as csvw:
    writer = csv.writer(csvw)
    for row in out_table:
        writer.writerow(row)


with open(csv_out_fail, 'w') as csvw:
    writer = csv.writer(csvw)
    for row in fail_table:
        writer.writerow(row)

# print those that fail
print len(fail_table)
