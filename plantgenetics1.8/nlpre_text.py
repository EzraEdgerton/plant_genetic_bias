"""
Script for cleaning pulled abstracts text file using nlpre library.
Replaces acronyms, gets rid of dashed words, and replaces words in the MeSh library
to be more intelligable


"""
from nlpre import titlecaps, dedash, identify_parenthetical_phrases
from nlpre import replace_acronyms, replace_from_dictionary
import os
import sys
import json
import string

readfilepath = sys.argv[1]

writefilepath = sys.argv[2]

readfile = open(readfilepath, 'r')

json_data = json.load(readfile)

absstring = ''
for d in json_data:
	s = d['abstracttext']
	absstring = absstring + ' ' + s
text = absstring
print type(text)
text = text.encode('utf-8').strip()
print type(text)
"""text = ("LYMPHOMA SURVIVORS IN KOREA. Describe the correlates of unmet needs "
        "among non-Hodgkin lymphoma (NHL) surv- ivors in Korea and identify "
        "NHL patients with an abnormal white blood cell count.")"""
print type(text)


ABBR = identify_parenthetical_phrases()(text)
print ABBR
parsers = [dedash(), replace_from_dictionary(prefix="MeSH_")]

for f in parsers:
	print (f)
	text = f(text)
mypunc = ''
for p in string.punctuation:
	if p != '_':
		mypunc = mypunc + p


#text = text.encode('utf-8').strip()
#text = text.encode('ascii')
text = text.lower().translate(None, mypunc)
#print(text)
#text = text.lower().translate(string.maketrans('', '',mypunc)
#)



writefile = open(writefilepath, 'w')

writefile.write(text)