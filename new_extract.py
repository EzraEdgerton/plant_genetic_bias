import os
import sys
import csv
import json
import re

filename = sys.argv[1]
writefilename = sys.argv[2]
readfile = open(filename)
writefile = open(writefilename, 'w')

data = []


with open('plant_genera_new.csv', 'rb') as plant_terms:
	with open('genetic_tools.csv', 'rb') as genetic_terms:
		with open('countries.csv', 'rb') as countries:


			def inner_extractor(start, sub_text):

				startindex = -1
				startindex = sub_text.find('= {', start)
				adder = 3
				subtractor = 1
				if startindex == -1:
					startindex = sub_text.find('={', start)
					adder = 2
					subtractor = 0

				endindex = sub_text.find('},', startindex)
				return sub_text[startindex + adder : endindex - subtractor]


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

			def country_inner_term_extractor(co_text):
				text_to_search = co_text.lower()
				search_result = ''

				for row in country_terms:
					subsearch_result = text_to_search.find(' ' +row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result = search_result + row[0] + ','
				return search_result


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

			text = text.lower()


			def extractor(entry_text):

				fields = [
						'\ntitle', 
						'\njournal',
						'\nyear', 
						'\nabstract', 
						'\naffiliation', 
						'\nkeywords', 
						'\nkeywords-plus', 
						'\nfunding-acknowledgement', 
						'\nauthor_keywords']

				title_text = ''
				journal_text = ''
				year_text = ''
				abstract_text = ''
				affiliation_text = ''
				keywords_text = ''
				keywords_plus_text = ''
				funding_text = ''
				author_keywords = ''
				results = [
						title_text, 
						journal_text, 
						year_text, 
						abstract_text, 
						affiliation_text, 
						keywords_text, 
						keywords_plus_text, 
						funding_text, 
						author_keywords]
				for i in range(0, len(fields)):
					field_index = entry_text.find(fields[i])
					if field_index != -1:
						results[i] = inner_extractor(field_index, entry_text)
				
				#title_text + ' ' + abstract_text + ' ' +  keywords_text + ' ' + keywords_plus_text
				term_search_string = results[0] + ' ' + results[3] + ' ' +  results[5] + ' ' + results[6]
				term_search_string = term_search_string.replace('{', ' ')
				term_search_string = term_search_string.replace('}', ' ')

				term_search_string = re.sub(r'[^\w\s]',' ',term_search_string)
			
				focal_species =  plant_inner_term_extractor(term_search_string)
				genetic_tool =  tool_inner_term_extractor(term_search_string)
				countries =  country_inner_term_extractor(term_search_string)

				author_coo_group = results[4].split('.\n')
				authors_coo = ''
				for author in author_coo_group:
					text_to_search = author.lower()
					if text_to_search.find('reprint author') != -1:
						authors_coo = authors_coo + ' Reprint Author '
					for row in country_terms:
						if text_to_search.find(row[0].lower()) != -1:
							authors_coo = authors_coo + row[0] + ', '

				year_text = results[2]
				journal_text = results[1]
				funding_text = results[7]
				

				#remove ugly characters
				year_text = year_text.replace('{', '')
				year_text = year_text.replace('}', '')
				year_text = year_text.replace('\n', '')
				journal_text = journal_text.replace('{', '')
				journal_text = journal_text.replace('}', '')
				journal_text = journal_text.replace('\n', '')
				funding_text = funding_text.replace('{',' ')
				funding_text = funding_text.replace('}',' ')
				funding_text = funding_text.replace('\n',' ')
				funding_coo = funding_text
				funding_coo = re.sub(r'[^\w\s]',' ',funding_text)

				funding_coo = country_inner_term_extractor(funding_coo)

				print funding_coo
				
				data.append({ 
					'focalspecies' : focal_species.encode('utf-8').strip(),
					'focalspeciesCOO' : countries.encode('utf-8').strip(), 
					'year' : year_text.encode('utf-8').strip(), 
					'journal' : journal_text.encode('utf-8').strip(),
					'genetictool' : genetic_tool.encode('utf-8').strip(), 
					'authorsCOO' : authors_coo.encode('utf-8').strip(), 
					'fundingorganization' : funding_text.encode('utf-8').strip(),
					'fundingCOO' : funding_coo.encode('utf-8').strip()
					})
				return 1
			index_start = text.find('@article')
			index_end = text.find('@article', index_start + 7)

			while 1:
				print index_start
				extractor(text[index_start: index_end])
				index_start = index_end + 8
				index_end = text.find('@article', index_start)
				if index_start == 7:
					break

			json.dump(data, writefile, indent=4)


			readfile.close()
			writefile.close()
			

