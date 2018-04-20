# subsets a csv with XY coords using a buffer area from a point

import csv

# centre point
point = [-79.1857,43.78423]

ymax = point[1] + 1
ymin = point[1] - 1
xmax = point[0] + 1
xmin = point[0] - 1

print xmin, xmax
print ymin, ymax

plaus_ldu = [['LDU','X','Y']]
with open("ldu_coords.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        X = float(row['X'])
        Y = float(row['Y'])
        if (X > xmin and X < xmax) and (Y > ymin and Y < ymax):
            out_row = [row['LDU'],X,Y]
            plaus_ldu.append(out_row)

print len(plaus_ldu)

with open("ldu_coords_subset.csv", 'r') as csvfile:
    writer = csv.wrieter(csvfile)
    for row in plaus_ldu:
        writer.writerow(row)
