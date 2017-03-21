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

The extracted data will be stored in the new file in the format similar to the extractedstuff.json example data. 


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
	'funding'
	'focalspecies'

focalspecies will take a while to run

It will store the new files in .json files of the field name in the plantgenmap folder

run this script for each of the five fields.

FORMATTING COUNTRIES FOR SIDE GRAPHS

Once those field files have been have been created, navigate to the plantgenmap folder.

At the moment, you must have a json file with each of the field names in the plantgenmap folder for this script to run.

run [python country_force_format.py]

This will loop through the fields and store each country data in the country_force folder or, if the field is focalspecies it will store it in the spec_country_force folder.

REMEMBER:
If you are rerunning this script, delete the previous country files from the country folders, otherwise the new data will be appended to the old data and the old data will continue to be visualized.



VIEWING VISUALIZATION:

In the plantgenmap, run 
python -m SimpleHTTPServer 
and navigate to http://localhost:8000/map.html to view the complete visualization


 After that move the generated files into the plantgenmap folder and follow the same steps for running a server. If you navigate to http://localhost:8000/map.html you should see the visualization.



