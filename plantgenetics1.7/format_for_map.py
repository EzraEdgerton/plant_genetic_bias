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



country_locations =  open('plantgenmap/data/country-locations.json', 'rb')
country_locations_json = json.load(country_locations)
ordered_country_locations = sorted(country_locations, key=lambda node: node['index'])
country_array = []
country_array_by_id = []
for loc in country_locations_json:
	
	country_array.append([loc['name'],
								{'name' : loc['name'],
								'name_official' : loc['name_official'],
								'latitude' : loc['latitude'],
								'longitude' : loc['longitude'],
								'id': loc['id']}])
	country_array.append([loc['name_official'],
								{'name' : loc['name'],
								'name_official' : loc['name_official'],
								'latitude' : loc['latitude'],
								'longitude' : loc['longitude'],
								'id' : loc['id']}])
	country_array_by_id.append([loc['id'],
								{'name' : loc['name'],
								'name_official' : loc['name_official'],
								'latitude' : loc['latitude'],
								'longitude' : loc['longitude'],
								'id': loc['id']}])


def fix_name(name):
	if name == 'Usa':
		return 'United States'
	if name == 'Korea':
		return 'South Korea'
	else:
		return name

country_dict = dict(country_array)

readfilename = sys.argv[1]

field = sys.argv[2]
writefilename = 'plantgenmap/' + field + '2.json'

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

def format_country_location(country_info):

	return {
		"type": "Feature",
		"id": int(country_info['id']),
		"index" : int(country_info['id']),
		"geometry": {
			"type": "Point",
			"coordinates": [float(country_info["longitude"]), float(country_info["latitude"])]
			},
		"properties": {
			"name": country_info["name"],
			"nameofficial": country_info['name_official']
			},
		"score": 1
		}

def make_links(field_data, country_links, directed):
	other_field_data = field_data
	if directed == 1:
		if len(field_data) != 0:
			field_data = [field_data[0]]
		else:
			field_data = []
	elif directed == 2:
		if len(field_data) != 0:
			field_data = [field_data[len(field_data) - 1]]
		else:
			field_data = [] 
	else:
		field_data = field_data

	for coo1 in field_data:
		other_field_data.remove(coo1)
		coo1_id = country_dict[fix_name(coo1.title())]['id']
		for coo2 in other_field_data:
			coo2_id = country_dict[fix_name(coo2.title())]['id']
			tup = str(coo1_id) + ';' + str(coo2_id)
			if directed > 0:
				if tup in country_links:
					country_links[tup] += 1
				else:
					country_links[tup] = 1
			else:
				tup_undirected = str(coo2_id) + ';' + str(coo1_id)
				if tup in country_links:
					country_links[tup] += 1
				elif tup_undirected in country_links:
					country_links[tup_undirected] += 1
				else:
					country_links[tup] = 1
		other_field_data = field_data

	return country_links

def contains(nodes, filter):
	list_len = len(nodes)
	for x in range(0, list_len):
		if filter(nodes[x]):
			return x
    	return False



def format_field(data, field_of_interest, order):

	nodes = dict()
	links = dict()
	#count = 0
	for d in data:
		#x = -1
		#y = -1
		"""
		for t in d['authorsCOO']:
			if t == 'united states':
				x = 1
		for t in d['authorsCOO']:
			if t == 'china':
				y = 1
		if x > 0 and y > 0:
			count += 1
			print d['authorsCOO']
		"""

		field_data = []
		if field == 'authorsCOO':
			if order == -1:
				field_data = d['authorsCOO']
			if order == 1:
				if len(d['authorsCOO']) != 0:
					field_data = [d['authorsCOO'][0]]
				else:
					field_data = []
			if order == 2:
				if len(d['authorsCOO']) != 0:
					field_data = [d['authorsCOO'][len(d['authorsCOO']) - 1]]
				else:
					field_data = [] 
		else:
			for spec in d['focalspeciesCOO']:
				field_data.extend(spec)

		for f in field_data:
			f = fix_name(f.title())
			if f in nodes:
				nodes[f]['score'] += 1
			else:
				nodes[f] = format_country_location(country_dict[f])
		if order == 1 or order == 2:
			if len(d['authorsCOO']) > 1:
				ugly_data = d['authorsCOO']
				ugly_data.remove(field_data[0])
				#print ugly_data
				for f in ugly_data:
					f = fix_name(f.title())
					if f in nodes:
						continue
					else:
						nodes[f] = format_country_location(country_dict[f])
						nodes[f]['score'] = 0


		if field == 'focalspeciesCOO':
			for spec in d['focalspeciesCOO']:
				new_links = make_links(spec, links, order)
				links = new_links
		else:
			#authors
			links = make_links(d['authorsCOO'], links, order)

	
	formatted_nodes = []
	nodes_by_index = []
	for n in nodes: 
		formatted_nodes.append(nodes[n])
	formatted_nodes = sorted(formatted_nodes, key=lambda node: node['index'])

	formatted_links = []
	for l in links:
		link_indexes = l.split(';')

		source = contains(formatted_nodes, lambda n: n['index'] == int(link_indexes[0]))
		target = contains(formatted_nodes, lambda n: n['index'] == int(link_indexes[1]))
		
		formatted_links.append({'source' : source,
								'target' : target,
								'score' : links[l]})
	
	return {'field': field,
			'nodes': formatted_nodes, 
			'links': formatted_links}

formatted_stuff = format_field(plant_data, field, order)

json.dump(formatted_stuff, writefile, indent=4)
writefile.close()
json_data.close()





