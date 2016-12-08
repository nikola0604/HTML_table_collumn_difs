from methods import *
import xml.etree.ElementTree as ET
import sys

# Parsing old header
try:
    tree = ET.parse('/Users/backup/Desktop/prvi')
    root = tree.getroot()
except ET.ParseError as perr:
    print "Unable to parse the old header file: {}".format(perr)
    sys.exit(1)

header_old = collect_data(root)

del tree
del root

# Parsing the new header
try:
    tree = ET.parse('/Users/backup/Desktop/drugi')
    root = tree.getroot()
except ET.ParseError as perr:
    print "Unable to parse the new header file: {}".format(perr)
    sys.exit(1)

# Iterating through the nodes of the parse tree,
# creating a list of table cells and appending that list to the list of rows in dict header_old for key: values
header_new = collect_data(root)

# Checking if both headers still consist of the same classes. If not, execution stops.
header = class_cardinality_check(header_old, header_new)