from psql_queries import *

import psycopg2

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='dejogenije111'")
    print "DB connection established"
except psycopg2.Error as psycoerr:
    print "DB connection failure: {}".format(psycoerr)
    sys.exit(1)

try:
    cur = conn.cursor()
    print "\nCursor creation successful"
except psycopg2.Error as psycoerr:
    print "\nCursor creation failure: {}".format(psycoerr)
    sys.exit(1)

# Dropping relations committed in the previous run
try:
    cur.execute("DROP TABLe IF EXISTS header_old, header_new")
    conn.commit()
    print "\nTables dropped successfully"
except psycopg2.Error as psycoerr:
    print "\nDrop tables failure: {}".format(psycoerr)
    sys.exit(1)

print "\n----------------------------------------------------"

# Creating a relation in DB for the old header
try:
    cur.execute(create_table_command)
    print "\nTable header_old created successfully using: " + create_table_command
except psycopg2.Error as psycoerr:
    print "\nTable creation failure. Tried with: " + create_table_command
    print psycoerr
    sys.exit(1)

iterator_index = 0

# Inserting data into header_old relation, row by row, from the header_old dict
print "\nAttempting to insert data into header_old using: " + insert_into_command
for list in header_old["values"]:
    try:
        iterator_index += 1
        cur.execute(insert_into_command,list)
    except psycopg2.Error as psycoerr:
        print "\nData insertion failure at row: " + iterator_index.__str__()
        print psycoerr
        sys.exit(1)
print "\nINSERTION INTO header_old SUCCESSFUL"

# Some serious hard coding. Converting the create_table_command to be used for creation of header_new relation
create_table_command = create_table_command.replace('header_old','header_new')

print "\n----------------------------------------------------"

# Creating a relation in DB for the new header
try:
    cur.execute(create_table_command)
    print "\nTable header_new created successfully using: " + create_table_command
except psycopg2.Error as psycoerr:
    print "\nTable creation failure. Tried with: " + create_table_command
    print psycoerr
    sys.exit(1)

del iterator_index
iterator_index = 0

# More serious hard coding. Converting the insert_into_command to be used for insertion of data into header_new relation
insert_into_command = insert_into_command.replace("header_old","header_new")

# Inserting data into header_new relation, row by row, from the header_new dict
print "\nAttempting to insert data into header_new using: " + insert_into_command
for list in header_new["values"]:
    try:
        iterator_index = iterator_index + 1
        cur.execute(insert_into_command,list)
    except psycopg2.Error as psycoerr:
        print "\nData insertion failure at row: " + iterator_index.__str__()
        print psycoerr
        sys.exit(1)
print "\nINSERTION INTO header_new SUCCESSFUL"

print "\n----------------------------------------------------"

# Commit both relations to DB
try:
    conn.commit()
    print "\nSuccessful commit"
except psycopg2.Error as psycoerr:
    print "\nCommit failed: {}".format(psycoerr)

print "\n----------------------------------------------------"



