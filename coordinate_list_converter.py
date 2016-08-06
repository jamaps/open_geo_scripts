# converts format of coordinate lists

def coord_list_convert(coord_list):
    print "meow"
    out_geo = []
    for xy in coord_list:
        lat = xy[0]
        lon = xy[1]
        out_geo.append([lon,lat])
    return out_geo

tuple_coords = [(43.68007, -79.34519), (43.68004, -79.34518), (43.67997, -79.34515), (43.67989, -79.34512), (43.67969, -79.34503), (43.67976, -79.3447), (43.67979, -79.34452)]

print tuple_coords

print "+" * 12

print coord_list_convert(tuple_coords)
