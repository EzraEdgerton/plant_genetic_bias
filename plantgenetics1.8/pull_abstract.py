import os
import json
import string

readfile = open('writefile2.json', 'r')

json_data = json.load(readfile)

finalstring = ''

for d in json_data:
	s = d['abstracttext'].encode('utf-8').strip()
	print s.lower().translate(None, string.punctuation)
	finalstring = finalstring + ' ' + s.lower().translate(None, string.punctuation)


writefile = open('abstractsstripped.txt', 'w')

writefile.write(finalstring)
