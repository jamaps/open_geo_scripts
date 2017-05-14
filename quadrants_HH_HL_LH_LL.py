# python3 for categorizing data into 4 quadrants from 2 numerical fields

# this case is for vis minoirty + avg income in Toronto census tracts

import csv
import statistics as st


# just the toronto cts
tor_cts = []
with open('ct_tor.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tor_cts.append(row['ctuid'])

var_1 = [] # avg inc
var_2 = [] # perc vis min
with open('in_inc_vis.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['ctuid'] in tor_cts:
            try:
                var_1.append(float(row['avg_inc']))
                perc_vis = float(row['vis_min_pop']) / float(row['total_pop'])
                var_2.append(perc_vis)
            except:
                print(row['ctuid'])

print(len(var_1))
print(len(var_2))
v1b=v2b=0
print("----------------------------------")
# for var 1
print("median", st.median(var_1))
print("mean", st.mean(var_1))
print("input break value:")
v1b = float(input())
# for var 2
print("----------------------------------")
print("median", st.median(var_2))
print("mean", st.mean(var_2))
print("input break value:")
v2b = float(input())

HHc = 0
HLc = 0
LHc = 0
LLc = 0
# break the data via the set breaks
with open('in_inc_vis.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['ctuid'] in tor_cts:
            try:
                perc_vis = float(row['vis_min_pop']) / float(row['total_pop'])
                inc = float(row['avg_inc'])

                # ye olde if statements
                if inc > v1b and perc_vis > v2b:
                    q = 'HH'
                    HHc += 1
                elif inc > v1b and perc_vis <= v2b:
                    q = 'HL'
                    HLc += 1
                elif inc <= v1b and perc_vis > v2b:
                    q = 'LH'
                    LHc += 1
                elif inc <= v1b and perc_vis <= v2b:
                    q = 'LL'
                    LLc += 1
                orow = [row['ctuid'],inc,perc_vis,q]
                #print(orow)
            except:
                #print(row['ctuid'])
                None

print("HH", HHc)
print("LH", LHc)
print("HL", HLc)
print("LL", LLc)
