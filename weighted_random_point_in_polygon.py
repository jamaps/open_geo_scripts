# computes a random point in a polygon by weighting probability 
# of location by population of a sub-polygon layer

import psycopg2
import random
import csv
import time

try:
    conn = psycopg2.connect("dbname='database' user='username' host='localhost' password='password' port='5432'")
except:
    print "connection fail :("

all_points_array = []

start = time.time()

with open('routing_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    q = 0
    for row in reader:
        print '--------------------'
        print row['HHKey_']
        CT_in = row['HmCTuid']

        q +=1
        # print q
        # if q == 5:
        #     break

        if CT_in != '':

            cur = conn.cursor()

            cur.execute("SELECT ctpop FROM c2011_ct WHERE ctuid = CAST(%s as text);" %CT_in)
            ct_pop = cur.fetchone()
            ct_pop = ct_pop[0]

            db_list = []
            cur.execute("SELECT dbuid, dbpop FROM c2011_block WHERE ctuid = CAST(%s as text);" %CT_in)
            for record in cur:
                db_list.append([record[0],record[1]])

            r = random.random() * ct_pop
            c = 0
            for block in db_list:
                block.append(c)
                c = c + block[1]
                block.append(c)
                if r >= block[2] and r <= block[3]:
                    out_block = block[0]
                    break

            print out_block

            cur.execute("SELECT ST_AsGeoJSON(randompointsinpolygon(geom, 1)) FROM c2011_block WHERE dbuid = CAST(%s as text);" %out_block)
            t = ((cur.fetchone()[0]).split('[')[1]).split(',')
            x = t[0]
            y = (t[1].split(',')[0]).split(']')[0]
            print x,y

            out_row = [row['HHKey_'],x,y]
            all_points_array.append(out_row)
            print time.time() - start

        else:
            x = 0
            y = 0
            out_row = [row['HHKey_'],x,y]
            all_points_array.append(out_row)


with open('coords.csv', 'w') as csvfile2:
    writer = csv.writer(csvfile2)
    for row in all_points_array:
        writer.writerow(row)
