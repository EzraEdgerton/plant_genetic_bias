This Folder is for creating and visualizing a worldmap of the locations of fields extracted from xml files:

run python map.py readfile.json writefile.json field

to get a formatted json file stored in readfile of the field's country locations.

Name the readfile.json file after the field you wish to filter by, for example:

python mapy.py example.json authors.json authors

will store the formatted data in authors.json.

The fields one can search are:

authors
firstauthor
lastauthor
speciesCOO
funding

To view the visualizations, run a simple python server from this folder( python -m SimpleHTTPServer) and navigate to:
localhost:8000/map.html