# takes all shps in a directory tree and copies them into a single folder

import os
from shutil import copyfile

in_dir = r"PATH"
out_dir =  r"PATH"

slash = "\\"

s = d = x = p =0

for root, dirs, files in os.walk(in_dir):
    for file in files:
        if file.endswith(".shp"):
			fp = (os.path.join(root, file))
			copyfile(fp, out_dir + slash + file)
			s += 1
for root, dirs, files in os.walk(in_dir):
    for file in files:
        if file.endswith(".dbf"):
			fp = (os.path.join(root, file))
			copyfile(fp, out_dir + slash + file)
			d += 1
for root, dirs, files in os.walk(in_dir):
    for file in files:
        if file.endswith(".shx"):
			fp = (os.path.join(root, file))
			copyfile(fp, out_dir + slash + file)
			x += 1
for root, dirs, files in os.walk(in_dir):
    for file in files:
        if file.endswith(".prj"):
			fp = (os.path.join(root, file))
			copyfile(fp, out_dir + slash + file)
			p += 1
			
print s
print d
print x
print p
