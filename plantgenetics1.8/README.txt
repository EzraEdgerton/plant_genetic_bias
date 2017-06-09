These are python scripts to extract the following information from .bib plant genetics study metadata:

	1)      Focal species
	2)      Focal species country of origin (CoO)
	3)      Year of publication
	4)      Journal published in 
	5)      Type of genetic marker/technique used 
	6)      First author affiliation CoO
	7)      Second author affiliation CoO
	8)      Third author affiliation CoO
	a.       … and so on for however many authors are on the paper
	9)      Funding agency
	10)   Funding agency CoO
	a.       (and additional funding agencies if present)


They will format the data properly and allow the user to view visualized node maps of some of these fields


TO USE:

1. In terminal navigate to the folder where the python script and data files(including .csv files) are stored.

2. for each of the files you would like to extract the data from run:

	 new_extract.py [extracted_data_file.json] [data.bib data2.bib data3.bib]

	e.g. if the data is stored in multiple files SampleDataset.bib, plantgen.bib, and scopus_plant_gen.bib and I want to store the extracted data in extractedstuff.json I would run:

		python new_extract.py extractedstuff.json SampleDataset.bib plantgen.bib scopus_plant_gen.bib

The extracted data will be stored in the new file in the format similar to the writefile.json example data. 


NOW EXTRA FORMATTING FOR VISUALIZING:
The visualization page is stored in the plantgenmap folder.
To format the inital data for the plantgenmap run 

FORMATTING NODE AND LINKS FOR MAPS

python format_for_map.py [file_you_just_created.json] [field]

First input is readfile name, created from running new_extract.py

Second input is field you wish to create nodes and links file for,
either:
	'authors'
	'firstauthor'
	'lastauthor'
	'focalspecies'


It will store the new files in .json files of the field name in the plantgenmap folder

run this script for each of the four fields.

CREATING SPECIES-AUTHOR COUNTRY FILES:

A new addition, for added species studies analysis, the script  format_species_with_authors.py creates species map data for each author in the extracted data's coo. It will create a file for each author coo and store the species data related to that coo in the plantgenmap/species_[all/first/last]_auth folder.

First input is readfile name, created from running new_extract.py

Second input is field you wish to create nodes and links file for,
either:
	'all'
	'first'
	'last'

Usage:

python format_species_w_authors.py [readfile] [field]

Run this script for each of the three fields to generte that data.

Finally, run spec_country_list.py to create an easy reference for each of those countries to be called in the select interaction in the visualization.




VIEWING VISUALIZATION:

In the plantgenmap, run 
python -m SimpleHTTPServer 
and navigate to http://localhost:8000/map.html to view the complete visualization


 After that move the generated files into the plantgenmap folder and follow the same steps for running a server. If you navigate to http://localhost:8000/map.html you should see the visualization.



