# downloads GBFS bikeshare stations and converts it to a geojson file
# this example is for Toronto

import requests
import json

# URL of Toronto bike share stations
url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

# downloading and converting to Python dictionary
response = requests.request("GET", url)
data = response.json()

# empty geojson file
geojson  = {
	"type": "FeatureCollection",
	"features": []
}

# loop over bike share stations, creating geojson features
for station in data["data"]["stations"]:
	feature = {
		"type": "Feature",
		"properties": {
			"station_id": station["station_id"],
			"name": station["name"],
			"address": station["address"],
			"capacity": station["capacity"],
			"rental_methods": station["rental_methods"],
			# optional items in Toronto's feed
			"physical_configuration": station["physical_configuration"],
			"altitude": station["altitude"],
			"groups": station["groups"],
			"obcn": station["obcn"],
			"nearby_distance": station["nearby_distance"]
		},
		"geometry": {
			"type": "Point",
			"coordinates": [float(station["lon"]),float(station["lat"])]
		}
	}
	geojson["features"].append(feature)

# write geojson to file
with open('bikeshare-stations.geojson', 'w') as file:
	file.write(json.dumps(geojson))
