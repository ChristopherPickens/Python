import json
import sys

'''
GEOJSON FILE STRUCTURE
{	type
	features	[{	type
					properties	{	CUSTOM ENTITY
								}
					geometry	{	type
									coordinates	[	region		[	shape		[	coordinates
}				]}				}				]				]				]

This script converts multipolygon geojson into polygon geojson, by removing the region from the record, and changing the geometry type to "Polygon"
'''

# LOAD GEOJSON FILE
python_obj = json.loads(open(sys.argv[1],"r").read())
# DEFINE OUTPUT VARIABLE
new_dict = {"type":"FeatureCollection","features":[]}

# DEFINE OUTPUT VARIABLE
output = open("upload_postcodes.geojson","w+")


if len(sys.argv) < 2:
	print("Usage: multi_to_single_poly.py input_file [output_file]")
	
	sys.exit(-1)
elif len(sys.argv) >= 2:
	print("Running with:", sys.argv[1])
	print("")
	python_obj = json.loads(open(sys.argv[1],"r").read())
	
	if len(sys.argv) == 3:
		print("Outputting to:", sys.argv[2])
		output = open(sys.argv[2],"w+")
	else:
		print("Outputting to: output.geojson")
		output = open("output.geojson","w+")


# FOR EACH RECORD
for i in python_obj['features']:
	# CHECK RECORD IS POLYGON
	if i['geometry']["type"] == 'Polygon':
		# ADD RECORD TO NEW_DICT VARIABLE, REMOVING REGION LAYER, AND SETTING GEOMETRY TYPE TO POLYGON
		new_dict['features'].append({'type':i['type'],'properties':i['properties'],'geometry':{'type':'Polygon','coordinates':i['geometry']['coordinates'][0]}})
	
	# IF THERES ONLY 1 REGION IN THE RECORD
	elif len(i['geometry']['coordinates']) <= 1:
		# FOR EACH SHAPE WITHIN THE REGION
		for j in i['geometry']['coordinates'][0]:
			# GET TO THE INDIVIDUAL POINT
			for k in j:
				# IF EXISTS, REMOVE 3RD VALUE
				if len(k) == 3:
					del k[2]
		# ADD RECORD TO NEW_DICT VARIABLE, REMOVING REGION LAYER, AND SETTING GEOMETRY TYPE TO POLYGON
		new_dict['features'].append({'type':i['type'],'properties':i['properties'],'geometry':{'type':'Polygon','coordinates':i['geometry']['coordinates'][0]}})
	
	# FOR RECORDS WITH MULTIPLE REGIONS
	else:
		# FOR EACH REGION IN THE RECORD
		for j in range(len(i['geometry']['coordinates'])):
			# FOR EACH SHAPE WITHIN THE REGION
			for k in i['geometry']['coordinates'][j]:
				# GET TO THE INDIVIDUAL POINT
				for l in k:
					# IF EXISTS, REMOVE 3RD VALUE
					if len(l) == 3:
						del l[2]
			# ADD RECORD TO NEW_DICT VARIABLE, REMOVING REGION LAYER, AND SETTING GEOMETRY TYPE TO POLYGON
			new_dict['features'].append({'type':i['type'],'properties':i['properties'],'geometry':{'type':'Polygon','coordinates':i['geometry']['coordinates'][j]}})
#

output.write(json.dumps(new_dict))