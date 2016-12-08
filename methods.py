from HTML_extractor import *
import sys

def output_separator():
    print "\n------------------------------------------------------"


def collect_data(root):
    input_dict = {"classes": [], "values": []}
    tmp_line = []

    for table in root.iter('table'):
        # Extracting only the first table row which consists of class names, then removing that node from the tree
        for table_header in table.find('tr').findall('th'):
            tmp_line.append(table_header.text)
        for class_name in tmp_line[1:]:
            input_dict["classes"].append(class_name)
        tmp_line = []
        table.remove(table.find('tr'))

        # Extracting the data from the remainder of the tree
        for table_row in table.iter('tr'):
            for data in table_row.iter():
                tmp_line.append(data.text)
            input_dict["values"].append(tmp_line[2:])
            tmp_line = []
    return input_dict


def class_cardinality_check(header_one, header_two):
    if set(header_one["classes"]) == set(header_two["classes"]):
        header = []

        for line in header_one["classes"]:
            header.append(line.replace('@', '').replace('.', ''))
    else:
        print "Mismatch in class names between two headers, " \
              "please check if whole classes have been excluded/added to the feed "
        sys.exit(1)

    return header


def define_max_cell(excluded_data, added_data):
    max = 0

    for key in excluded_data:
        for cell in excluded_data[key]:
            if max < len(cell[0]):
                max = len(cell[0])

    for key in added_data:
        for cell in added_data[key]:
            if max < len(cell[0]):
                max = len(cell[0])

    return max

def define_num_of_tabs(excluded_data, added_data):
    num_of_tabs_ex = 0
    num_of_tabs_add = 0

    for key in excluded_data:
        if len(excluded_data[key]) != 0:
            num_of_tabs_ex += 1

    for key in added_data:
        if len(added_data[key]) != 0:
            num_of_tabs_add += 1

    return max(num_of_tabs_add, num_of_tabs_ex)

def write_data(data, max_cell, f):
    max_len = 0
    index = 0

    for key in data:
        for cell in data[key]:
            if max_cell < len(cell[0]):
                max_cell = len(cell[0])

    for key in data:
        f.write('{0:{fill}{align}{width}}'.format(key + '', fill='', align='^', width=max_cell))
        f.write('\t')

        if len(data[key]) > max_len:
            max_len = len(data[key])

    f.write('\n')

    try:
        while index < max_len:
            for key in data:
                try:
                    f.write('{0:{fill}{align}{width}}'.format(data[key][index][0], fill='', align='^', width=max_cell))
                    f.write('\t')
                except IndexError:
                    f.write('{0:{fill}{align}{width}}'.format('', fill='', align='^', width=max_cell))
                    f.write('\t')
                    continue
            f.write('\n')
            index += 1
    except IndexError as inderr:
        print "Romanian exception handler: " + inderr