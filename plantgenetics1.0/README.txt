This is a python script to extract the following information from .bib plant genetics study metadata:

	1)      Focal species
	2)      Focal species country of origin (CoO)
	3)      Year of publication
	4)      Journal published in 
	5)      Type of genetic marker/technique used (we can talk more about this one later this week; we should probably come up with a list of names and acronyms to use in an OR search)
	6)      First author affiliation CoO
	7)      Second author affiliation CoO
	8)      Third author affiliation CoO
	a.       … and so on for however many authors are on the paper
	9)      Funding agency
	10)   Funding agency CoO
	a.       (and additional funding agencies if present)

TO USE:

1. In terminal navigate to the folder where the python script and data files(including .csv files) are stored.

2. run extract.py [datafile.bib] [extracted_data_file.json]

	e.g. if the data is stored in SampleDataset.bib and I want to store the extracted data in extractedstuff.json I would run:

		python extract.py SampleDataset.bib extractedstuff.json

That is all. The extracted data will be stored in the new file in the format similar to the extractedstuff.json example data. 

(NOTES: I added the term 'microsatellites' to the genetic tools csv. 
		I removed the leading 'x' from a number of terms in the plant genara csv. )

Created by Ezra Edgerton Nov 2016

