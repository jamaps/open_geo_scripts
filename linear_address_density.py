# codes addresses to streets, calculating the number of addresses that fall on each street segment

# used in creation of this map: http://jamaps.github.io/maps/parking_ticket_density_2112x1367.png

import csv
import time
from collections import Counter

start = time.time()

in_parking_folder = "parking_tickets_2015"
slash = "//"
in_parking_csv = ["Parking_Tags_Data_2015_2.csv","Parking_Tags_Data_2015_3.csv","Parking_Tags_Data_2015_1.csv"]
in_centre_lines = "cl.csv" #exported from shp to csv with QGIS

# list of every street name
all_streets = []

# list of each street sgement with geoid and addresses
# only those with addresses
street_segments = []

# filling the lists
with open(in_centre_lines) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        segment = []
        street_name = row['LF_NAME'].upper()
        all_streets.append(street_name)
        if '-' in row['ADDRESS_L'] or '-' in row['ADDRESS_R']:
            segment.append(street_name)
            segment.append(row['GEO_ID'])
            if '-' in row['ADDRESS_L']:
                bl = int(row['ADDRESS_L'].split('-', 1)[0])
                al = int(row['ADDRESS_L'].split('-', 1)[1])
                segment.append(bl)
                segment.append(al)
            if '-' in row['ADDRESS_R']:
                br = int(row['ADDRESS_R'].split('-', 1)[0])
                ar = int(row['ADDRESS_R'].split('-', 1)[1])
                segment.append(br)
                segment.append(ar)
            street_segments.append(segment)
street_counts = Counter(all_streets)

# print street_segments
# print all_streets
# print street_counts
print len(street_segments)
print len(all_streets)



good_addresses = []
bad_addresses = []
# put each address into good or bad lists, based on whether
# they have address numbers
for csv_q in in_parking_csv:
    with open(in_parking_folder + slash + csv_q) as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            number = row['location2'].split(' ', 1)[0]
            try:
                address = []
                add_num = int(number)
                street = row['location2'].split(' ', 1)[1]
                address.append(add_num)
                address.append(street)
                good_addresses.append(address)
            except:
                bad_addresses.append(row['location2'])
            count +=1
            # if count == 35:
            #     break
        print ("addresses in file")
        print count
        print ("------------------")

    # print good_addresses
    # print bad_addresses

print ("addresses with numbers")
print len(good_addresses)
print ("------------------")
print ("addresses no numbers")
print len(bad_addresses)
print ("------------------")
print ("total addresses")
print (len(good_addresses) + len(bad_addresses))
print ("------------------")

count = 0
good_geo_id = []
not_coded_add = []
for addr in good_addresses:
    if addr[0] % 2 == 0:
        c = 1
        for streets in street_segments:
            if streets[0] == addr[1] and len(streets) == 4:
                if addr[0] <= (max(streets[2],streets[3])) and addr[0] >= min(streets[2],streets[3]):
                    good_geo_id.append(streets[1])
                    break
            if streets[0] == addr[1] and len(streets) == 6:
                if streets[2] % 2 == 0 and streets[3] % 2 == 0:
                    if addr[0] <= (max(streets[2],streets[3])) and addr[0] >= min(streets[2],streets[3]):
                        good_geo_id.append(streets[1])
                        break
                elif streets[5] % 2 == 0 and streets[4] % 2 == 0:
                    if addr[0] <= (max(streets[5],streets[4])) and addr[0] >= min(streets[4],streets[5]):
                        good_geo_id.append(streets[1])
                        break
                else:
                    if addr[0] <= (max(streets[3],streets[4],streets[5],streets[2])) and addr[0] >= min(streets[2],streets[3],streets[4],streets[5]):
                        good_geo_id.append(streets[1])
                        break
            if c == len(street_segments):
                not_coded_add.append(addr)
            c += 1
    if addr[0] % 2 != 0:
        c = 1
        for streets in street_segments:
            if streets[0] == addr[1] and len(streets) == 4:
                if addr[0] <= (max(streets[2],streets[3])) and addr[0] >= min(streets[2],streets[3]):
                    good_geo_id.append(streets[1])
                    break
            if streets[0] == addr[1] and len(streets) == 6:
                if streets[2] % 2 != 0 and streets[3] % 2 != 0:
                    if addr[0] <= (max(streets[2],streets[3])) and addr[0] >= min(streets[2],streets[3]):
                        good_geo_id.append(streets[1])
                        break
                elif streets[5] % 2 != 0 and streets[4] % 2 != 0:
                    if addr[0] <= (max(streets[5],streets[4])) and addr[0] >= min(streets[4],streets[5]):
                        good_geo_id.append(streets[1])
                        break
                else:
                    if addr[0] <= (max(streets[3],streets[4],streets[5],streets[2])) and addr[0] >= min(streets[2],streets[3],streets[4],streets[5]):
                        good_geo_id.append(streets[1])
                        break
            if c == len(street_segments):
                not_coded_add.append(addr)
            c += 1
    count += 1
    if count % 1000 == 0:
        print count
        print time.time() - start
        print ("==========")


print ("geocoded to streets properly")
print len(good_geo_id)
print ("------------------")
print ("not geocoded to streets properly")
print len(not_coded_add)
print ("------------------")

ticket_counts = Counter(good_geo_id)


# output coded and uncoded addresses to csvs

with open('geo_counts_2015.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in ticket_counts:
        csv_row = []
        csv_row.append(i)
        csv_row.append(ticket_counts[i])
        writer.writerow(csv_row)

with open('geo_counts_2015_no_number.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for badbad in bad_addresses:
        row = []
        row.append(badbad)
        writer.writerow(row)

with open('geo_counts_2015_nein_coded.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in not_coded_add:
        writer.writerow(row)


# for addr in bad_addresses:
end = time.time()
print("####################")
print(end - start)
