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


4. Now we must run the python script to reformat that data into a nodes and links json file that the javascript vis can recognize. the format_for_linking.py file takes as input the input file, what we created in the previous step, and fields to search the data (any number of authors, funding, species, speciesCOO, or tool). It will output json files of the name of the field you input. 

	python format_for_linking.py [combined_data.json] [field][field2][field3]

	e.g. If I wanted to create a file to visualize the author COO and tool used from combined.json I would run

	python format_for_linking combined.json authors tool

	and that data will be stored in authors.json and tool.json

5. Move those output files from the previous step into the plantgenetics_graph_proto folder. Do not rename the files unless you want to edit the file path in the index.html file(also an option)

6. Next, navigate to the plantgenetics_graph_proto folder and run a simple server.
	Create the simple server by running:
	python -m SimpleHTTPServer

7. Open your browser and go to http://localhost:8000/. It will work for each of the fields you created and moved into the plantgenetics_graph_proto folder.



