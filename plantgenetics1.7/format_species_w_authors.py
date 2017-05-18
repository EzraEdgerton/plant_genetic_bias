"""
For creating linked map files for focalspecies based on authors, either first, last or all.

First input is readfile name, created from running new_extract.py

Second input is field you wish to create nodes and links file for,
either:
	'all'
	'first'
	'last'


It will store the new files in .json files of the country's name in the plantgenmap folder
in either species_all_auth, species_first_auth, or species_last_auth folders

"""

import os
import sys
import csv
import json
import re


readfilename = sys.argv[1]
author_field = sys.argv[2]

json_data = open(readfilename, 'r')
plant_data = json.load(json_data)

directory = 'species_all_auth'

if author_field == 'first':
	directory = 'species_first_auth'
if author_field == 'last':
	directory = 'species_last_auth'
if author_field == 'all':
	directory = 'species_all_auth'

country_locations =  open('plantgenmap/data/country-locations.json', 'rb')
country_locations_json = json.load(country_locations)
country_array = []
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

country_dict = dict(country_array)

"""
tup = ('coo1', 'coo2')
tup2 = ( 1, 3)

testdict = dict([[tup, 1],[tup2,2]])

if (1, 3) in testdict:
	print testdict"""

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

def format_nodes(species_info, species_countries):
	for species in species_info:
		for coo in species:
			if coo in species_countries:
				species_countries[coo]['score'] += 1
			else:
				species_countries[coo] = format_country_location(country_dict[coo.title()])
	#print species_countries
	return species_countries

def format_links(species_info, country_links):
	for species in species_info:
		for coo1 in species:
			coo1_id = country_dict[coo1.title()]['id']
			for coo2 in species:
				coo2_id = country_dict[coo2.title()]['id']
				tup = str(coo1_id) + ';' + str(coo2_id)
				tup_undirected = str(coo2_id) + ';' + str(coo1_id)
				#tup = (coo1_id, coo2_id)
				if tup in country_links:
					country_links[tup] += 1
				elif tup_undirected in country_links:
					country_links[tup_undirected] += 1
				else:
					country_links[tup] = 1
	return country_links

def fix_country_names(country):
	if country == 'Usa':
		return 'United States'
	else:
		return country


def format_fields(data, auth_type):
	
	countries_map_data = dict()
	count = 0
	for d in data:
		print 'article count ' + str(count)
		auth_countries = []
		article_species_coo = d['focalspeciesCOO']
		if len(d['authorsCOO']) > 0:
			if auth_type == 'first':
				auth_countries.append(fix_country_names(d['authorsCOO'][0].title()))
			elif auth_type == 'last':
				auth_countries.append(fix_country_names(d['authorsCOO'][len(d['authorsCOO']) - 1].title()))
			else:
				for auth in d['authorsCOO']:
					auth_countries.append(fix_country_names(auth.title()))

		for auth_country in auth_countries:
			if auth_country in countries_map_data:
				old_nodes = countries_map_data[auth_country]['nodes']
				old_links = countries_map_data[auth_country]['links']
				new_nodes = format_nodes(article_species_coo, old_nodes)
				new_links = format_links(article_species_coo, old_links)
				countries_map_data[auth_country] = {'nodes': new_nodes, 'links': new_links}
			else:
				nodes = format_nodes(article_species_coo, dict())
				links = format_links(article_species_coo, dict())
				countries_map_data[auth_country] = {'nodes': nodes, 'links': links}
		count += 1
	return countries_map_data


def contains(nodes, filter):
	list_len = len(nodes)
	for x in range(0, list_len):
		if filter(nodes[x]):
			return x
    	return False

		

def format_and_write(data):
	for d in data:
		country_name = d.replace(' ', '_')
		print country_name
		country_file = open('plantgenmap/' + directory + '/' + country_name + '.json', 'w')
		nodes = data[d]['nodes']
		formatted_nodes = []
		countries_length = len(country_locations_json)
		for n in nodes: 
			formatted_nodes.append(nodes[n])
		formatted_nodes = sorted(formatted_nodes, key=lambda node: node['index'])

		formatted_links = []
		links = data[d]['links']

		for l in links:
			link_indexes = l.split(';')
			
			source = contains(formatted_nodes, lambda n: n['index'] == int(link_indexes[0]))
			target = contains(formatted_nodes, lambda n: n['index'] == int(link_indexes[1]))

			formatted_links.append({'source' : source,
									'target' : target,
									'score' : links[l]})

		json.dump({'field' : directory, 'nodes' : formatted_nodes, 'links' : formatted_links}, country_file, indent=4 )
		
		country_file.close()

countries_data = format_fields(plant_data, author_field)

format_and_write(countries_data)

