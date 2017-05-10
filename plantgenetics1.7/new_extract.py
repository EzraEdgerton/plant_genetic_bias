# -*- coding: utf-8 -*-
import os
import sys
import csv
import json
import re
import bibtexparser
import time


writefilename = sys.argv[1]
arg_num = len(sys.argv)

readfiles = []
#readfile = open(filename)
writefile = open(writefilename, 'w')

print writefilename

for i in range(2, arg_num):
	readfiles.append(sys.argv[i])

print readfiles




#with open('important_data/all_plantspecies_cc_dict.json', 'rb') as plant_terms:
with open('important_data/genetic_tools.csv', 'rb') as genetic_terms:
	with open('important_data/countries.csv', 'rb') as countries:
		with open('important_data/nationalities.csv', 'rb') as nationalities:

			plant_terms = open('important_data/all_plantspecies_cc_dict.json', 'r')

			plant_reader = json.load(plant_terms)
			genetic_tool_reader = csv.reader(genetic_terms)
			country_reader = csv.reader(countries)

			tool_terms = []
			country_terms = []
			#nationality_terms = []
			for row in genetic_tool_reader:
				tool_terms.append([row[0].lower(), 0])
			for row in country_reader:
				country_terms.append([row[0].lower(), 0])
			#added search coverage for nationalities (i.e. cuban etc) not included
			#for row in nationalities:
			#	nationality_terms.append(row)

			for term in plant_reader:
				term = term.lower()
				term = term.split(' ')
				term = term[0] + ' ' + term[1]

			
			tool_terms_dict = dict(tool_terms)
			country_terms_dict = dict(country_terms)
			plant_terms_dict = dict(plant_reader)

			def plant_inner_term_extractor(planttext):

				text_to_search = ' ' + planttext.lower()
				split_text = text_to_search.split(' ')
				search_result = set()
				split_len = len(split_text)
				no_count = 0
				#print text_to_search
				for i in range(0, split_len - 1):
					text_term = split_text[i].title() + ' ' + split_text[i + 1]
					try:
						plant_terms_dict[text_term]
						print text_term
						"""if len(search_result) > 0:
							for thing in search_result:
								if thing == text_term:
									no_count = 0
								else:
									search_result.append(text_term)
						else:"""
						search_result.add(text_term)
						
					except KeyError:
						#print ''
						no_count = 0
				"""text_to_search = ' ' + planttext.lower()
				search_result = []
				for item in plant_reader:
					subsearch_result = text_to_search.find(' ' + item.lower() + ' ')
					if subsearch_result != -1:
						if item != 'species':
							if item != '':
								search_result.append(item)"""
				print search_result
				return search_result


			def get_plant_countries(genii):
				genii_countries = []
				for genus in genii:
					genus_countries = []
					countries = plant_reader[genus]
					for country in countries:
						for row in country_terms:
							if country == row[1]:
								genus_countries.append(row[0])
					genii_countries.append(genus_countries)
				return genii_countries




			def tool_inner_term_extractor(tooltext):
				text_to_search = tooltext.lower()
				search_result = []

				for row in tool_terms:
					subsearch_result = text_to_search.find(' ' +row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result.append(row[0])
				return search_result

			def country_inner_term_extractor(co_text):
				text_to_search = co_text.lower()
				search_result = []
				for row in country_terms:
					subsearch_result = text_to_search.find(' ' +row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result.append(row[0])
				return search_result


			def get_author_countries(author_text):

				text_to_search = author_text.lower()
				auth_countries = []
				for country in country_terms:
					sub_text = text_to_search
					s_country = country[0].lower()
					search_index = sub_text.find(s_country)
					sub_index = search_index
					while search_index > -1:
						#get character to see if it is name of affiliation school or country name
						if len(sub_text) <= search_index + len(s_country):
							auth_char = ';'
						else:
							auth_char = sub_text[search_index + len(s_country)]
						if auth_char == '.' or auth_char == ';':
							auth_countries.append([country[0],sub_index])
						sub_text = sub_text[search_index + 1: len(text_to_search)]
						search_index = sub_text.find(s_country)
						sub_index = sub_index + search_index
				auth_countries = sorted(auth_countries, key=lambda co: co[1])
				return_val = []
				for c in auth_countries:
					return_val.append(c[0])
				#print return_val
				return return_val


			def extractor(entry_text):

				fields = [
						'title', 
						'journal',
						'year', 
						'abstract', 
						'affiliation', 
						'keywords', 
						'keywords-plus', 
						'funding-acknowledgement', 
						'author_keywords', 
						'funding_details']

				title_text = ''
				journal_text = ''
				year_text = ''
				abstract_text = ''
				affiliation_text = ''
				keywords_text = ''
				keywords_plus_text = ''
				funding_text = ''
				author_keywords = ''
				funding_details = ''
				results = [
						#0
						title_text, 
						#1
						journal_text, 
						#2
						year_text, 
						#3
						abstract_text, 
						#4
						affiliation_text, 
						#5
						keywords_text, 
						#6
						keywords_plus_text, 
						#7
						funding_text, 
						#8
						author_keywords,
						#9
						funding_details]
				for i in range(0, len(fields)):
					#print fields[i]
					try:
						#print entry_text[fields[i]]
						results[i] = entry_text[fields[i]].encode('utf-8').strip()
						
					except KeyError:
						print ''

				#title_text + ' ' + abstract_text + ' ' +  keywords_text + ' ' + keywords_plus_text
				term_search_string = results[0] + ' ' + results[3] + ' ' +  results[5] + ' ' + results[6]
				term_search_string = term_search_string.replace('{', ' ')
				term_search_string = term_search_string.replace('}', ' ')

				term_search_string = re.sub(r'[^\w]',' ',term_search_string)
			
				focal_species_set =  plant_inner_term_extractor(term_search_string)
				focal_species = []
				for x in focal_species_set:
					focal_species.append(x)

				genetic_tool =  tool_inner_term_extractor(term_search_string)
				countries =  get_plant_countries(focal_species)

				author_coo_group = results[4]

				authors_coo = get_author_countries(author_coo_group)

				year_text = results[2]
				journal_text = results[1]
				funding_text = results[7] + results[9]
				abstract_text = results[3]

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


				#nasty gross fixes
				for co in range(0, len(authors_coo)):
					if authors_coo[co] == 'USA':
						authors_coo[co] = 'UNITED STATES'
					#we can assume this, right?	
					if authors_coo[co] == 'KOREA':
						authors_coo[co] = 'SOUTH KOREA'
				for co in range(0, len(funding_coo)):
					if funding_coo[co] == 'USA':
						funding_coo[co] = 'UNITED STATES'
					if funding_coo[co] == 'KOREA':
						funding_coo[co] = 'SOUTH KOREA'

				year = year_text.encode('utf-8').strip()
				if len(year) == 0:
					year = -1
				else:
					year = int(year_text.encode('utf-8').strip())
				for tool in genetic_tool:
					tool.encode('utf-8').strip()

				print journal_text

				data.append({ 
					'focalspecies' : focal_species, #focal_species.encode('utf-8').strip(),
					'focalspeciesCOO' : countries,#countries.encode('utf-8').strip(), 
					'year' : year, 
					'journal' : journal_text.lower(),#.encode('utf-8').strip(),
					'genetictool' : genetic_tool,#.encode('utf-8').strip(), 
					'authorsCOO' : authors_coo,#.encode('utf-8').strip(), 
					'fundingorganization' : funding_text,#.encode('utf-8').strip(),
					'fundingCOO' : funding_coo,#.encode('utf-8').strip(),
					'abstracttext' : abstract_text
					})
				return 1
		start = time.clock()
		data = []
		for file in readfiles:
			readfile = open(file)
			
			text = bibtexparser.load(readfile)
			for article in text.entries_dict:
				extractor(text.entries_dict[article])
			readfile.close()
		json.dump(data, writefile, indent=4)
		writefile.close()
		elapsed = (time.clock() - start)
		print elapsed
	

