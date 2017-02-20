import os
import sys
import csv
import json
import re
import untangle

obj = untangle.parse('')


"""
filename = sys.argv[1]
writefilename = sys.argv[2]
readfile = open(filename)
writefile = open(writefilename, 'w')

data = []


with open('plant_genera_new.csv', 'rb') as plant_terms:
	with open('genetic_tools.csv', 'rb') as genetic_terms:
		with open('countries.csv', 'rb') as countries:

			text =  readfile.read()


			plant_reader = csv.reader(plant_terms)
			genetic_tool_reader = csv.reader(genetic_terms)
			country_reader = csv.reader(countries)

				
			plant_terms = []
			tool_terms = []
			country_terms = []
			for row in plant_reader:
				if row[0] != 'Genus':
					plant_terms.append(row)
			for row in genetic_tool_reader:
				tool_terms.append(row)
			for row in country_reader:
				country_terms.append(row)

			firstindex = text.find('Journal')

			def inner_extractor(start):
				if start == -1:
					return ['', -1]
				startindex = text.find('{{', start)
				endindex = text.find('}}', start)
				return [text[startindex + 2 : endindex], endindex]

			def plant_inner_term_extractor(planttext):
				text_to_search = ' ' + planttext.lower()
				search_result = ''

				for row in plant_terms:	
					#first try to recognize genus
					subsearch_result = text_to_search.find(' ' + row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result = search_result + row[0] + ' ' + row[1] + ','
					#if there is no recognized genus, search in family
					if search_result == '':
						subsearch_result = text_to_search.find(' ' + row[1] + ' ')
						if subsearch_result != -1:
							search_result = search_result + row[1] + ','
				return search_result

			def tool_inner_term_extractor(tooltext):
				text_to_search = tooltext.lower()
				search_result = ''

				for row in tool_terms:
					subsearch_result = text_to_search.find(' ' +row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result = search_result + row[0] + ','

				return search_result

			def country_inner_term_extractor(text):
				text_to_search = text.lower()
				search_result = ''

				for row in country_terms:
					subsearch_result = text_to_search.find(' ' +row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result = search_result + row[0] + ','

				return search_result


			def extractor(textindex):
				index = textindex

				title_index = text.find('Title', index, len(text))
				title = inner_extractor(title_index)
				title_text = title[0]
				index = title[1]

				journal_index = text.find('Journal ', index)
				journal = inner_extractor(journal_index)
				journal_text = journal[0]
				
				index = journal[1]

				year_index = text.find('Year', index)
				year = inner_extractor(year_index)
				year_text = year[0]
				
				index = year[1]

				abstract_index = text.find('Abstract', index)
				abstract = inner_extractor(abstract_index)
				abstract_text = abstract[0]
				
				index = abstract[1]

				affiliation_index = text.find('Affiliation', index)
				affiliation = inner_extractor(affiliation_index)
				affiliation_text = affiliation[0]
				
				index = affiliation[1]

				keywords_index = text.find('Keywords', index)
				keywords = inner_extractor(keywords_index)
				keywords_text = keywords[0]
				
				index = keywords[1]

				keywords_plus_index = text.find('Keywords-Plus', index)
				keywords_plus = inner_extractor(keywords_plus_index)
				keywords_plus_text = keywords_plus[0]
				
				index = keywords_plus[1]

				funding_index = text.find('Funding-Acknowledgement', index)
				funding = inner_extractor(funding_index)
				funding_text = funding[0]
				
				index = funding[1]

				term_search_string = title_text + ' ' + abstract_text + ' ' +  keywords_text + ' ' + keywords_plus_text

				term_search_string = re.sub(r'[^\w\s]',' ',term_search_string) 
				#print term_search_string
				focal_species =  plant_inner_term_extractor(term_search_string)
				genetic_tool =  tool_inner_term_extractor(term_search_string)
				countries =  country_inner_term_extractor(term_search_string)

				author_coo_group = affiliation_text.split('.\n')
				authors_coo = ''
				for author in author_coo_group:
					text_to_search = author.lower()
					if text_to_search.find('reprint author') != -1:
						authors_coo = authors_coo + ' Reprint Author '
					for row in country_terms:
						if text_to_search.find(row[0].lower()) != -1:
							authors_coo = authors_coo + row[0] + ', '






				if title_text != '':
					data.append({ 'focal-species' : focal_species, 'focal-species-COO' : countries, 'year' : year_text, 'journal' : journal_text, 'genetic-tool' : genetic_tool, 'authors COO(in order)' : authors_coo, 'funding-organization' : funding_text})# \n {} \n {} \n {} \n {} \n {} \n {} \n \n'.format(focal_species, countries, year_text, journal_text, genetic_tool, authors_coo, funding_text))

				return index


			total_index = 0
			while total_index >= 0:
				total_index = extractor(total_index)
				print total_index

			json.dump(data, writefile, indent=4)


			readfile.close()
			writefile.close()

"""