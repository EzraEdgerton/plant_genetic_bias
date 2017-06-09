"""
Script to create lists of each country file created by format_species_w_authors.py

Creates a json file stored in plantgenmap/new_map/spec_country_lists.json

"""

import os
import json
import sys


first_auth = sorted(os.listdir('plantgenmap/species_first_auth'))

last_auth = sorted(os.listdir('plantgenmap/species_last_auth'))

all_auth = sorted(os.listdir('plantgenmap/species_all_auth'))

writefile = open('plantgenmap/new_map/spec_country_lists.json', 'w')

json.dump({'first_author' : first_auth, 'last_author' : last_auth, 'all_author' : all_auth}, writefile, indent = 4)
