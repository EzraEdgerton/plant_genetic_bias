import os
import sys
import csv
import json
import re
import xml
from xml.dom import minidom

def checkfornewline(list_item):
	try:
		thing = list_item.data
		return False
	except AttributeError:
		return True


def filterlistfornewline(nodelist):
	filtered = []
	for item in nodelist:
		if checkfornewline(item):
			filtered.append(item)
	return filtered

def getArticleInfo(item):
	item = filterlistfornewline(item)
	for element in item:
		print item
def getJournalInfo(item):
	print item
	#item = filterlistfornewline(item)
	#for element in item:
#		print item
def getHeadingInfo(item):
	item = item.getElementsByTagName('')

def getText(element):
	return element.childNodes[0].data

def getTextData(element):
	if len(element) > 0:
		getText(element[0])
	else: return False

def getGrants(grantlist):
	funding = ''
	if len(grantlist) > 0:
		grants =  grantlist[0].getElementsByTagName('Grant')
		for grant in grants:
			grant_country = grant.getElementsByTagName('Country')
			grant_agency =  grant.getElementsByTagName('Agency')
			if len(grant_agency) > 0 and len(grant_country) > 0:
				funding = funding + grant_agency[0].childNodes[0].data+' '+grant_country[0].childNodes[0].data +', '
	return funding

def getAffiliation(affiliationlist):
	affiliations = ''
	if len(affiliationlist) > 0:
		for affiliation in affiliationlist:
			affiliations = affiliations + getText(affiliation) + '++ '

	return affiliations

def getChemicalTerms(chemlist):
	#print chemlist
	chemicals = ''
	if len(chemlist) > 0:
		for chemical in chemlist:
			chemicals = chemicals + getText(chemical) + ' '
	return chemicals

class Citation:
	author_coo_str = ''
	journal_str = ''
	year_str = ''
	focal_terms = ''
	funding_organization_str = ''
	def __init__(self, author_coo, journal, year, focal_terms, funding_organization):
		self.author_coo_str = author_coo.encode("ascii", "ignore")
		self.journal_str = journal.encode("ascii", "ignore")
		self.year_str = year.encode("ascii", "ignore")
		self.focal_terms_str = focal_terms.encode("ascii", "ignore")
		self.funding_organization_str = funding_organization.encode("ascii", "ignore")


def getHeadingTerms(heading_list):
	headings = ''
	for heading in heading_list:
		descriptors = heading.getElementsByTagName('DescriptorName')
		qualifiers = heading.getElementsByTagName('QualifierName')

		if len(descriptors) > 0:
			headings = headings + getText(descriptors[0]) + ' '
		if len(qualifiers) > 0:
			for qualifier in qualifiers:
				headings = headings + getText(qualifier) + ' '
		headings = headings + ' '

	return headings

def getCitationFields(citation):


	abstracttext = citation.getElementsByTagName('AbstractText')
	articletitle = citation.getElementsByTagName('ArticleTitle')
	journaltitle = citation.getElementsByTagName('Title')
	journalyear = citation.getElementsByTagName('Year')
	authoraffiliationlist = citation.getElementsByTagName('Affiliation')

	meshheadinglist = citation.getElementsByTagName('MeshHeading')
	chemicallist = citation.getElementsByTagName('NameOfSubstance')
	grantlist = citation.getElementsByTagName('GrantList')
	

	if len(articletitle) > 0:
		articletitle = articletitle[0].childNodes[0].data
	else:
		articletitle = ''
	if len(abstracttext) > 0:
		abstracttext = abstracttext[0].childNodes[0].data
	else:
		abstracttext = ''
	if len(journaltitle) > 0:
		journaltitle = journaltitle[0].childNodes[0].data
	else:
		journaltitle = ''
	if len(journalyear) > 0:
		journalyear = journalyear[0].childNodes[0].data
	else:
		journalyear = ''
	funding = getGrants(grantlist)
	affiliations = getAffiliation(authoraffiliationlist)
	chem_terms = getChemicalTerms(chemicallist)
	heading_terms = getHeadingTerms(meshheadinglist)


	author_coo = affiliations
	journal = journaltitle
	year = journalyear
	focal_terms = abstracttext + ' ' + articletitle + ' ' + chem_terms + ' ' + heading_terms
	funding_organization = funding







	

	thing = Citation(author_coo, journal, year, focal_terms, funding_organization)

	return thing
	





filename = sys.argv[1]
writefilename = sys.argv[2]
#readfile = open(filename)
writefile = open(writefilename, 'w')

data = []

xmldoc = minidom.parse(filename)


citations = xmldoc.childNodes[1]
citations = citations.childNodes

citations = filterlistfornewline(citations)

citationdata = []
for cit in citations:
	citationdata.append(getCitationFields(cit))





with open('plant_genera_new.csv', 'rb') as plant_terms:
	with open('genetic_tools.csv', 'rb') as genetic_terms:
		with open('countries.csv', 'rb') as countries:

 


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


			def extractor(cit):


				
				term_search_string = cit.focal_terms_str
				term_search_string = re.sub(r'[^\w\s]',' ',term_search_string) 
				#print term_search_string
				focal_species =  plant_inner_term_extractor(term_search_string)
				genetic_tool =  tool_inner_term_extractor(term_search_string)
				countries =  country_inner_term_extractor(term_search_string)

				author_coo_group = c.author_coo_str.split('++') #affiliation_text.split('.\n')
				authors_coo = ''
				for author in author_coo_group:
					text_to_search = author.lower()
					if text_to_search.find('reprint author') != -1:
						authors_coo = authors_coo + ' Reprint Author '
					for row in country_terms:
						if text_to_search.find(row[0].lower()) != -1:
							authors_coo = authors_coo + row[0] + ', '







				data.append({ 'focal-species' : focal_species, 'focal-species-COO' : countries, 'year' : c.year_str, 'journal' : c.journal_str, 'genetic-tool' : genetic_tool, 'authors-COO' : authors_coo, 'funding-organization' : c.funding_organization_str})# \n {} \n {} \n {} \n {} \n {} \n {} \n \n'.format(focal_species, countries, year_text, journal_text, genetic_tool, authors_coo, funding_text))

			
			for c in citationdata:
				extractor(c)
				#print c.author_coo_str
				#print c.journal_str
				#print c.year_str
				#print c.focal_terms_str
				#print c.funding_organization_str
				print c.year_str[3]


			json.dump(data, writefile, indent=4)


			writefile.close()
