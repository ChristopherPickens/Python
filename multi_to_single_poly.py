'''
GEOJSON FILE STRUCTURE
{	type
	features	[{	type
					properties	{	CUSTOM		}
					geometry	{	type
									coordinates	[	region		[	shape		[	coordinates	[
]]]]}}]}

This script converts multipolygon geojson into polygon geojson, by removing the region from the record, and changing the geometry type to "Polygon"
'''

import json
import os
import sys

# DEFINE OUTPUT VARIABLE
new_dict = {"type":"FeatureCollection","features":[]}

# ENSURE SCRIPT IS CALLED CORRECTLY
if len(sys.argv) < 2:
	print("ERROR - Usage: multi_to_single_poly.py input_file [output_file]")
	sys.exit(-1)
# ENSURE FILE EXISTS
elif not os.path.isfile(sys.argv[1]):
	print("ERROR - File does not exist")
	sys.exit(-1)
# ENSURE FILE IS JSON LOADABLE
else:
	try:
		python_obj = json.loads(open(sys.argv[1],"r").read())
	except ValueError as e:
		print("ERROR - File format: file is not JSON loadable")
		sys.exit(-1)
	# DEFINE THE OUTPUT GEOJSON FILE, USE DEFAULT IF NONE DEFINED
	if len(sys.argv) >= 3:
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

output.write(json.dumps(new_dict))
