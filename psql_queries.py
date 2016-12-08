from HTML_extractor import *
from collections import OrderedDict

import psycopg2


# Dynamically generating an SQL query which will create a relation in DB with a given table_name
def generate_ctc(table_name):
    rows = ''
    for row_name in header:
        rows = ''.join((rows, row_name, " VARCHAR(255), "))

    create_table_command = ''.join(
        ("CREATE TABLE {} (".format(table_name),
         ''.join((rows[:-2], rows[-2:].replace(',', ')'))))).replace('@', '').replace('.', '')
    return create_table_command


# Creates a relation in DB using the previously generated create_table_command
def create_table(table_name, cur):
    try:
        create_table_command = generate_ctc(table_name)
        cur.execute(create_table_command)
        print "\nTable " + table_name + " created successfully using: " + create_table_command
    except psycopg2.Error as psycoerr:
        print "\nTable creation failure. Tried with: " + create_table_command
        print psycoerr
        sys.exit(1)


# Dynamically generating an SQL query which will be used to insert one row of data into table_name
def generate_iic(table_name):
    insert_into_values_chunk = ""

    for each in header:
        insert_into_values_chunk = ''.join((insert_into_values_chunk, "%s, "))

    insert_into_command = ''.join(("INSERT INTO " + table_name + " VALUES (", ''.join(
        (insert_into_values_chunk[:-2], insert_into_values_chunk[-2:].replace(',', ')')))))

    return insert_into_command


# Imports data from the matrix header_***["values"] into the table_name relation
def insert_into(table_name, header, cur):
    insert_into_command = generate_iic(table_name)

    print "\nAttempting to insert data into " + table_name + " using: " + insert_into_command

    iterator_index = 0

    for list in header["values"]:
        try:
            iterator_index += 1
            cur.execute(insert_into_command, list)
        except psycopg2.Error as psycoerr:
            print "\nData insertion failure at row: " + iterator_index.__str__()
            print psycoerr
            sys.exit(1)

    print "\nINSERTION INTO header_old SUCCESSFUL"


def drop_tables(conn, cur, table_one, table_two):
    try:
        cur.execute("DROP TABLE IF EXISTS {}, {}".format(table_one, table_two))
        conn.commit()
        print "\nTables dropped successfully"
    except psycopg2.Error as psycoerr:
        print "\nDrop tables failure: {}".format(psycoerr)
        sys.exit(1)


# Finding fields excluded/added from each class separately by fetching its column from both relations,
# then performing set subtraction (ONE / TWO)
# Writing the results into output_data_dict dictionary (key: class_name, value: list_of_elements_in_set{ONE/TWO}
def data_export(table_one, table_two, cur):
    output_data_dict = OrderedDict([])

    try:
        for class_name in header:
            cur.execute("SELECT {} FROM ".format(class_name) + table_one + " EXCEPT SELECT {} FROM ".format(
                class_name) + table_two)
            output_data_dict.update({class_name: []})
            for data in cur:
                output_data_dict[class_name].append(data)
        print "\nExcluded data successfully extracted"

        return output_data_dict
    except psycopg2.Error as psycoerr:
        print "\nFailure on extracting excluded data: {}".format(psycoerr)
        sys.exit(1)
