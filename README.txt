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

	 new_extract.py [datafile.bib] [extracted_data_file.json]

	e.g. if the data is stored in SampleDataset.bib and I want to store the extracted data in extractedstuff.json I would run:

		python new_extract.py SampleDataset.bib extractedstuff.json

The extracted data will be stored in the new file in the format similar to the extractedstuff.json example data. 

3. After that, if you wish to combine the extracted data into one json file run:
		python combine.py [combined_data.json] [each of the extracted data file names from the previous step]

	e.g. If I am trying to combine the results stored in prelim0.json prelim1.json and 
	prelim2.json and store them in combined.json I would run:
	
		python combine.py combined.json prelim0.json prelim1.json prelim2.json

4. Now we must run the python script to reformat that data into a nodes and links json file that the javascript vis can recognize. the format_for_linking.py file takes as input the input file, what we created in the previous step, and a field to search the data (either authors, funding, species, speciesCOO, or tool). It will output a json file of the name of the field you input. 

	python format_for_linking.py [combined_data.json] [field]

	e.g. If I wanted to create a file to visualize the author COO from combined.json I 	would run

	python format_for_linking combined.json authors

	and that data will be stored in authors.json 

5. Move those output files from the previous step into the plantgenetics_graph_proto folder. Do not rename the files unless you want to edit the file path in the index.html file(also an option)

6. Next, navigate to the plantgenetics_graph_proto folder and run a simple server.
	Create the simple server by running:
	python -m SimpleHTTPServer

7. Open your browser and go to http://localhost:8000/. It will work for each of the fields you created and moved into the plantgenetics_graph_proto folder.



