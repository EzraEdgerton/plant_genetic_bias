import os
import sys
import csv
import json
import re


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

		plant_terms = open('important_data/all_plantspecies_cc_dict.json', 'r')

		plant_reader = json.load(plant_terms)
		genetic_tool_reader = csv.reader(genetic_terms)
		country_reader = csv.reader(countries)

		tool_terms = []
		country_terms = []
		for row in genetic_tool_reader:
			tool_terms.append(row)
		for row in country_reader:
			country_terms.append(row)


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
			search_result = []
			for item in plant_reader:
				subsearch_result = text_to_search.find(' ' + item.lower() + ' ')
				if subsearch_result != -1:
					if item != 'species':
						if item != '':
							search_result.append(item)
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
			text_to_search = author_text
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
			print return_val
			return return_val


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
			countries =  get_plant_countries(focal_species)

			author_coo_group = results[4]

			authors_coo = get_author_countries(author_coo_group)

			year_text = results[2]
			journal_text = results[1]
			funding_text = results[7]
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

			
			data.append({ 
				'focalspecies' : focal_species, #focal_species.encode('utf-8').strip(),
				'focalspeciesCOO' : countries,#countries.encode('utf-8').strip(), 
				'year' : int(year_text.encode('utf-8').strip()), 
				'journal' : journal_text.encode('utf-8').strip(),
				'genetictool' : genetic_tool, #.encode('utf-8').strip(), 
				'authorsCOO' : authors_coo,#.encode('utf-8').strip(), 
				'fundingorganization' : funding_text.encode('utf-8').strip(),
				'fundingCOO' : funding_coo,#.encode('utf-8').strip(),
				'abstracttext' : abstract_text
				})
			return 1

		data = []
		for file in readfiles:
			readfile = open(file)
			text =  readfile.read()
			text = text.lower()

			index_start = text.find('@article')
			index_end = text.find('@article', index_start + 7)

			while 1:
				print index_start
				extractor(text[index_start: index_end])
				index_start = index_end + 8
				index_end = text.find('@article', index_start)
				if index_start == 7:
					break
			readfile.close()
		json.dump(data, writefile, indent=4)
		writefile.close()
	

