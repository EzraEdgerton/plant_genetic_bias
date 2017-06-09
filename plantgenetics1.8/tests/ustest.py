import os
import sys
import json
import re

file = open('writefile.json', 'r')

file_json = json.load(file)
count1 = 0
count2 = 0
for d in file_json:
	for author in d['authorsCOO']:
		if author == 'USA':
			count = count+1
		if author == 'UNITED STATES':
			count2 = count2 + 1
print 'USA'
print count1
print 'UNITED STATES'
print count2
