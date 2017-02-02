# using osrm to create a big dirty OD matrix

import csv
import requests
import polyline
import time
import json

db_points = []

# grab points from csv file - just grab, x, y, and a unique ID
# the headers may be different depending on your data!
with open("db.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    n = 0
    q = 0
    for row in reader:
        # limiting number of points for testing, may do all eventually!
        if n % 1 == 0:
            q += 1
            db_points.append([row['X'],row['Y'],row['dbuid']])
        n += 1

# split up into managable size - 2000 destinations seems managable
point_count = len(db_points)
points_split_list = []
single_list = []
i = 1
for row in db_points:
    single_list.append(row)
    if i % 3000 == 0:
        points_split_list.append(single_list)
        single_list = []
    if i == len(db_points):
        points_split_list.append(single_list)
    i += 1

# print lenghts of before and after
print len(db_points)
print len(points_split_list)
for x in points_split_list:
    print len(x)
# make sure these total!

# list of ids
dbuids = []
for row in db_points:
    dbuids.append(row[2])
print len(dbuids)


# set up that awesome marix were going to output!
the_matrix = []

# lets add in a header row!
the_matrix.append([''] + dbuids)
print len(the_matrix)
print len(the_matrix[0])

# the start time for time timing
start_time = time.time()


# loop over the origins
for origin in db_points:

    # the output row!
    out_row = [origin[2]]

    for points in points_split_list:

        polyline_list = []

        polyline_list.append((float(origin[1]),float(origin[0])))

        # grab x y for lists
        for row in points:

            dr_tuple = (float(row[1]),float(row[0]))
            polyline_list.append(dr_tuple)

        line = polyline.encode(polyline_list, 5)

        # what to send
        url = 'http://localhost:5000/table/v1/driving/polyline(' + line + ')?sources=0'

        # sending and recieving
        page = requests.get(url)
        data = json.loads(page.content)
        durs = data["durations"][0]
        del durs[0] # deleting initial 0
        out_row = out_row + durs

    the_matrix.append(out_row)

    # this break is for testing!
    break

print time.time() - start_time

for row in the_matrix:
    print len(row)
