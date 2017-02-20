import os
import sys
import json

file_no = len(sys.argv)

files_to_open = []

writefilename = sys.argv[1]
writefile = open(writefilename, 'w')

for file_index in range(2, file_no):
	files_to_open.append(sys.argv[file_index])

files = []

finaljson = []

for file in files_to_open:
	print file
	openfile = open(file)

	text = openfile.read()
	text.replace('[', '')
	text.replace(']', '')
	text = json.loads(text)
	for entry in text:
		finaljson.append(entry)
	openfile.close()
json.dump(finaljson, writefile, indent=4)
writefile.close()


