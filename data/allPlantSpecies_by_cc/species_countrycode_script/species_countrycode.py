#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:06:27 2017

@author: robert
"""

import os
import sys
import json
from collections import defaultdict

filename = sys.argv[1]
writefilename = sys.argv[2]

writefile = open(writefilename, 'w')

with open(filename, 'rb') as occurence:
    species_dict = defaultdict(list)
    for line in occurence:
        if line.split('\t')[120] not in species_dict[line.split('\t')[228]]:
            species_dict[line.split('\t')[228]].append(line.split('\t')[120])

    json.dump(species_dict, writefile, indent = 4)
    occurence.close()
    
writefile.close()
