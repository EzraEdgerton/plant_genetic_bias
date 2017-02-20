import os
import sys
import json
import re


def search(values, searchFor):
    for k in values:
    	if k['name'] == searchFor:
    		return k["index"]
    return -1

def extract_index(json):
	return json['index']

def separate(string):
	
	#print string
	split_vals = string.split(",")
	for i in range(0, len(split_vals)):
		if split_vals[i][0:8] == " Reprint":
			split_vals[i] = ' ' + split_vals[i].split(' ', 3)[3]
		elif split_vals[i][0:9] == "  Reprint":
			split_vals[i] = ' ' + split_vals[i].split(' ', 4)[4]
	try:
		split_vals.remove(" ")
	except ValueError:
		return split_vals
	return split_vals

def search_links(links, val_1, val_2):
	for l in range(0, len(links)):
		if links[l]['source'] == val_1 and links[l]['target'] == val_2:
			return l
		elif links[l]['source'] == val_2 and links[l]['target'] == val_1:
			return l
	return -1





filename = sys.argv[1]


"""
One of:
      focal-species
      authors COO(in order)
      journal
      year
      focal-species-COO
      genetic-tool
      funding-organization
"""
#field = sys.argv[2]

fields = []

for x in range(2, len(sys.argv)):
	field = sys.argv[x]
	fields.append(field)

print fields



json_data = open(filename, 'r')
data = json.load(json_data)

for field in fields:



	
	writefilename = field + '.json'

	writefile = open(writefilename, 'w')
	

	if field == "authors":
		field = "authorsCOO"
	if field == "funding":
		field = "fundingCOO"
	if field == "species":
		field = "focalspecies"
	if field == "speciesCOO":
		field = "focalspeciesCOO"
	if field == "tool":
		field = "genetictool"


	pre_links = []
	pre_nodes = []

	node_track = 0

	#teststr= "microsatellite,microsatellites,"
	#teststr2 = "BOLIVIA,ECUADOR,MEXICO,PERU,"

	#test_links = [{"source": 3, "target": 6}, {"source": 0, "target": 2}, {"source": 2, "target": 8}]

	#print search_links(test_links, 2, 0)

	pre_nodes.append({
				"index": node_track,
				"name": "",
				"data": [],
				"group": 1, 
				"score": 0
				})

	node_track = node_track + 1


	for d in data:
		field_separated = separate(d[field])
		try:
			field_separated.remove("")
		except ValueError:
			field_separated = field_separated
		temp_field_sep = []
		for val in field_separated:
			temp_field_sep.append(val.strip())

		field_separated = temp_field_sep
		
		#create nodes
		for val in field_separated:
		
			

			print val
			index = search(pre_nodes, val)

			if index != -1:
				pre_nodes[index]["score"] = pre_nodes[index]["score"] + 1
				pre_nodes[index]["data"].append(d)
			else:
				pre_nodes.append({
					"index": node_track,
					"name": val,
					"data": [d],
					"group": 1, 
					"score": 1
					})
				node_track = node_track + 1
		#create links
		other_fields = field_separated
		#print '\n\n'
		#print other_fields
		for val in other_fields:
			val =  val.strip()
			other_fields.remove(val)
			index = search(pre_nodes, val)
			for other in other_fields:
				index2 = search(pre_nodes, other)
				link_index =  search_links(pre_links, index, index2)
				if link_index != -1:
					pre_links[link_index]["value"] = pre_links[link_index]["value"] + 1
				else:
					pre_links.append({
						"source": index,
						"target": index2,
						"value": 1
						})





	formatted_data = {
		'nodes': pre_nodes,
		'links': pre_links
	}


	json.dump(formatted_data, writefile, indent=4)

	writefile.close()

json_data.close()

