import xml.etree.ElementTree as ET
import sys

# Parsing old header
try:
    tree = ET.parse('/home/pseudo-dev/Desktop/header_old.html')
    root = tree.getroot()
except ET.ParseError as perr:
    print "Unable to parse the old header file: {}".format(perr)
    sys.exit(1)

header_old = {"classes": [], "values": []}
tmp_line = []

# Iterating through the nodes of the parse tree, creating a list of table cells and appending that list to the list of rows in dict header_old for key: values
for table in root.iter('table'):
    # Extracting only the first table row which consists of class names, then removing that node from the tree
    for table_header in table.find('tr').findall('th'):
        tmp_line.append(table_header.text)
    for class_name in tmp_line[1:]:
        header_old["classes"].append(class_name)
    tmp_line = []
    table.remove(table.find('tr'))

    # Extracting the data from the remainder of the tree
    for table_row in table.iter('tr'):
        for data in table_row.iter():
            tmp_line.append(data.text)
        header_old["values"].append(tmp_line[2:])
        tmp_line = []

del tree
del root
del tmp_line

# Parsing the new header
try:
    tree = ET.parse('/home/pseudo-dev/Desktop/header_new.html')
    root = tree.getroot()
except ET.ParseError as perr:
    print "Unable to parse the new header file: {}".format(perr)
    sys.exit(1)


header_new = {"classes": [], "values": []}
tmp_line = []

# Iterating through the nodes of the parse tree, creating a list of table cells and appending that list to the list of rows in dict header_old for key: values
for table in root.iter('table'):
    # Extracting only the first table row which consists of class names, then removing that node from the tree
    for table_header in table.find('tr').findall('th'):
        tmp_line.append(table_header.text)
    for class_name in tmp_line[1:]:
        header_new["classes"].append(class_name)
    tmp_line = []
    table.remove(table.find('tr'))

    # Extracting the data from the remainder of the tree
    for table_row in table.iter('tr'):
        for data in table_row.iter():
            tmp_line.append(data.text)
        header_new["values"].append(tmp_line[2:])
        tmp_line = []

# Checking if both headers still consist of the same classes. If not, execution stops.
if set(header_old["classes"]) == set(header_new["classes"]):
    header = []
    for line in header_old["classes"]:
        header.append(line.replace('@',''))
else:
    print "Mismatch in class names between two headers, please check if whole classes have been excluded/added to the feed"
    sys.exit(1)