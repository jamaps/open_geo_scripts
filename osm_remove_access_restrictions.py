# removes access restriction tags in osm data

f = open('pre.osm.xml', 'r')

lines = f.readlines()

f.close()

q = open("post.osm.xml","w")

l = 0
x = 0
for line in lines:
    if r'<tag k="access"' in line:
        l += 1
        #new = r'  <tag k="access" v="yes"/>'
    else:
        q.write(line)
        x += 1

print "--------"
print l
print x
print x + l
