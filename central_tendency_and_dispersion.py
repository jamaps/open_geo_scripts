# computes measures of central tendancy from a csv table
# table must be set up as 3 columns: x, y, weight

import csv

csv_path = 'x_y_w.csv'

# calculating the mean centre
with open(csv_path, 'rb') as f:
    reader = csv.reader(f)
    x_sum = 0
    y_sum = 0
    n = 0
    for row in reader:
        n = n + 1
        x_sum = x_sum + float(row[0])
        y_sum = y_sum + float(row[1])
    mean_x = x_sum / n
    mean_y = y_sum / n

# calculating the standard distance
with open(csv_path, 'rb') as f:
    reader = csv.reader(f)
    x_sq_dist = 0
    y_sq_dist = 0
    for row in reader:
        x_sq_dist = (float(row[0]) - mean_x)**2 + float(x_sq_dist)
        y_sq_dist = (float(row[1]) - mean_y)**2 + float(y_sq_dist)
    SD = float(((x_sq_dist + y_sq_dist) / n)**0.5)

# caclulating the weighted mean centre
with open(csv_path, 'rb') as f:
    reader = csv.reader(f)
    x_w_sum = 0
    y_w_sum = 0
    w_sum = 0
    for row in reader:
        w_sum = float(row[2]) + float(w_sum)
        x_w_sum = (float(row[0]) * float(row[2])) + float(x_w_sum)
        y_w_sum = (float(row[1]) * float(row[2])) + float(y_w_sum)
    w_mean_x = x_w_sum / w_sum
    w_mean_y = y_w_sum / w_sum

# caclulating the weighted standard distance
with open(csv_path, 'rb') as f:
    reader = csv.reader(f)
    x_sq_dist = 0
    y_sq_dist = 0
    w_x_sq_dist = 0
    w_y_sq_dist = 0
    for row in reader:
        w_x_sq_dist = float((float(row[0]) - float(w_mean_x))**2)*float(row[2]) + float(w_x_sq_dist)
        w_y_sq_dist = float((float(row[1]) - float(w_mean_y))**2)*float(row[2]) + float(w_y_sq_dist)
    WSD = ( ((w_x_sq_dist) + (w_y_sq_dist)) / w_sum ) ** 0.5

# print results
print "Count = %i" % (n)
print "Mean Centre = (%f, %f)" % (mean_x, mean_y)
print "Standard Distance = %f" % (SD)
print "Weighted Mean Centre = (%f, %f)" % (w_mean_x, w_mean_y)
print "Weighted Standard Distance = %f" % (WSD)
