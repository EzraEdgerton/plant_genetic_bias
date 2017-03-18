import os
import json
import sys

openfiles = ['funding.json', 'authors.json', 'firstauthor.json', 'lastauthor.json', 'focalspecies.json']


def format_force_field(filename):
	file = open(filename, 'r')

	file_data = json.load(file)
	print file_data
	for country in file_data:
		print country



#for file in openfiles:
format_force_field('funding.json')