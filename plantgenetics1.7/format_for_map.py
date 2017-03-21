"""
For creating node and links for map visualization

First input is readfile name, created from running new_extract.py

Second input is field you wish to create nodes and links file for,
either:
	'authors'
	'firstauthor'
	'lastauthor'
	'funding'
	'focalspecies'

focalspecies will take a while to run

It will store the new files in .json files of the field name in the plantgenmap folder

"""

import os
import sys
import csv
import json
import re


def search(values, searchFor):
	searchFor = searchFor.lower()
	for k in values:
		if k['properties']['name'].lower() == searchFor:
			return k["index"]
		if k['properties']['nameofficial'].lower() == searchFor:
			return k["index"]
	return -1

def separate(string, field):
	if field == 'focalspeciesCOO':
		string2 = []
		for item in string:
			string2 = string2 + item
		string = string2

	
	split_vals = string
	try:
		split_vals.remove(" ")
	except ValueError:
		return split_vals
	try:
		split_vals.remove("")
	except ValueError:
		return split_vals
	return split_vals

def search_cities(searchFor, values):
	searchFor = searchFor.lower()
	for k in values:
		if k['properties']['name'].lower() == searchFor:
			return k["index"]
		if k['properties']['nameofficial'].lower() == searchFor:
			return k["index"]
	return -1

def search_links(links, val_1, val_2):
	for l in range(0, len(links)):
		if links[l]['source'] == val_1 and links[l]['target'] == val_2:
			return l
		elif links[l]['source'] == val_2 and links[l]['target'] == val_1:
			return l
	return -1

def search_links_directed(links, val_1, val_2):
	for l in range(0, len(links)):
		if links[l]['source'] == val_1 and links[l]['target'] == val_2:
			return l
	return -1

def format_country_location(country_info, id_num, data, dummy=1):

	return {
		"type": "Feature",
		"id": id_num,
		"index" : id_num,
		"geometry": {
			"type": "Point",
			"coordinates": [float(country_info["longitude"]), float(country_info["latitude"])]
			},
		"properties": {
			"name": country_info["name"],
			"nameofficial": country_info['name_official']
			},
		"score": dummy#,
		#"data": data
		}

readfilename = sys.argv[1]

#writefilename = sys.argv[2]


field = sys.argv[2]
writefilename = 'plantgenmap/' + field + '.json'

order = -1

if field == 'authors':
	field = 'authorsCOO'
	order = -1
if field == 'firstauthor':
	field = 'authorsCOO'
	order = 1
if field == 'lastauthor':
	field = 'authorsCOO'
	order = 2
if field == 'focalspecies':
	field = 'focalspeciesCOO'
if field == 'funding':
	field = 'fundingCOO'



json_data = open(readfilename, 'r')
plant_data = json.load(json_data)

writefile = open(writefilename, 'w')



def format_cities(data, field_of_interest, order):
	country_locations =  open('plantgenmap/data/country-locations.json', 'rb') 
	country_locations_json = json.load(country_locations)
	country_data = { 
				"type":"FeatureCollection",
				"cities": []
						}
	pre_links = []
	id_number = 0

	for d in data:
		field_separated = separate(d[field_of_interest], field_of_interest)
		print field_separated
		other_fields = []
		for val in field_separated:
			other_fields.append(val)

		if len(field_separated) > 0:
			if field_of_interest == "authorsCOO":
				if order == 1:
					field_separated = [field_separated[0]]
				if order == 2:
					field_separated = [field_separated[len(field_separated) - 1]]
			else:
				field_separated = separate(d[field_of_interest], field_of_interest)
		#remove trailing and heading whitespace
		for val in field_separated:
			if len(val) > 0:
				if val[0] == " ":
					val = val[1: len(val)]
			city_index = search_cities(val, country_data["cities"])
			if city_index != -1:
				country_to_alter = country_data["cities"][city_index]
				country_to_alter["score"] = country_to_alter["score"] + 1


			else:
				val_lower = val.lower()
				for country_location in country_locations_json:
					if country_location['name'].lower() == val.lower() or country_location['name_official'].lower() == val.lower():
						location_data = format_country_location(country_location, id_number, d)
						id_number = id_number + 1
						country_data['cities'].append(location_data)
		
		for val in field_separated:
			#print other_fields
			#print val
			val =  val.strip()
			other_fields.remove(val)
			index = search(country_data['cities'], val)

			for other in other_fields:
				index2 = search(country_data['cities'], other)
		
				if index2 == -1:
					for country_location in country_locations_json:
							if country_location['name'].lower() == other.lower() or country_location['name_official'].lower() == other.lower():
								location_data = format_country_location(country_location, id_number, d, 0)
								index2 = id_number
								id_number = id_number + 1
								country_data['cities'].append(location_data)
				if order != -1:
					link_index =  search_links_directed(pre_links, index, index2)
				else:
					link_index =  search_links(pre_links, index, index2)
				if link_index != -1:
					pre_links[link_index]["value"] = pre_links[link_index]["value"] + 1
				else:
					pre_links.append({
						"source": index,
						"target": index2,
						"value": 1
						})

	return [country_data, {'links': pre_links}]

json.dump(format_cities(plant_data, field, order), writefile, indent=4)
writefile.close()
json_data.close()





