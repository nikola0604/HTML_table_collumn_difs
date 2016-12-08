from psql_queries import *
from methods import *

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
drop_tables(conn, cur, "header_old", "header_new")

output_separator()

# Creating a relation in DB for the old header
create_table("header_old", cur)

# Inserting data into header_old relation, row by row, from the header_old dict
insert_into("header_old", header_old, cur)

output_separator()

# Creating a relation in DB for the new header
create_table("header_new", cur)

# Inserting data into header_new relation, row by row, from the header_new dict
insert_into("header_new", header_new, cur)

output_separator()

# Commit both relations to DB
try:
    conn.commit()
    print "\nSuccessful commit"
except psycopg2.Error as psycoerr:
    print "\nCommit failed: {}".format(psycoerr)

output_separator()


