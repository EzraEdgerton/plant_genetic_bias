import os
from unidecode import unidecode

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

file = open('scopusabstractscleaned.txt', 'r')

tex = file.read()





write = open('scopusabstractcleanedascii.txt', 'w')

write.write(remove_non_ascii(tex))
