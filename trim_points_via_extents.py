# trims a point .csv file from using select extents

import csv

# function for trimming db by extents
def subset_points(db_table, xmax, xmin, ymax, ymin):
    out_points = []
    for row in db_table:
        x = float(row[0])
        y = float(row[1])
        if x > xmin and x < xmax and y > ymin and y < ymax:
            out_points.append(row)
    return out_points

# grabbing all blocks from csv and put into an array
all_db = []
with open("db_points.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        header = row
        break
    for row in reader:
        if row != header:
            all_db.append(row)

# printing length and header for reference
print len(all_db)
print header

# test toronto
toronto = subset_points(all_db,-78.78,-80.025,44.138,43.169)
print len(toronto)
