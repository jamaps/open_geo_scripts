# creating a network distance OD matrix using OSRM
# returns the distance in metres of the route with the shortest travel time for each OD pair 

import csv
import requests
import time
import json
# import polyline

start_time = time.time()

origins = []
dests = []
with open("TAZ_fixed_1.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    n = 0
    for row in reader:
        # print row
        origins.append([row['GTA06'],row['X'],row['Y']])
        dests.append([row['GTA06'],row['X'],row['Y']])
        n += 1


print(len(origins))
print(len(dests))


# get list of destination ids
dids = []
for row in dests:
    dids.append(row[0])



# function for one-to-many - input origin X, origin Y, and list of destinations
def row_request(ox,oy,destinations):

    # grab string of all the coordinates - for plugging into OSRM url
    coord_str = str(ox) + ',' + str(oy) + ';'
    for row in destinations:
        coord_str = coord_str + str(row[1]) + ',' + str(row[2]) + ';'
    coord_str = coord_str[:-1]

    # grab list of destinations IDs for URL string
    distr = ''
    di = 1
    while di <= len(destinations):
        distr = distr + str(di) + ';'
        di += 1
    distr = distr[:-1]

    # setting up the url to send
    url = 'http://localhost:5000/table/v1/driving/' + coord_str + '?sources=0&destinations=' + distr + '&annotations=duration,distance'


    # sending and recieving the data
    page = requests.get(url)
    data = json.loads(page.content)

    # print length for testing
    # print(len(data['distances'])) # should be 1
    # print(len(data['distances'][0])) # should be = len(destinations)

    # print(data)
    # return the data as a row
    return data['distances'][0]


# do this for a bunch of origins if needed = essentially an OD matrix
out_rows = [['OD'] + dids]
cou = 0
for person in origins:
    tt = row_request(person[1],person[2],dests)
    tt = [person[0]] + tt
    out_rows.append(tt)
    print("----------------------------")
    print(cou, time.time() - start_time)
    cou += 1

with open("TAZ_distance_matrix.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    for p in out_rows:
        writer.writerow(p)
