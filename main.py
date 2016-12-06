from data_import import *
from collections import OrderedDict

# try:
#     tmp_cur = conn.cursor()
#     print "Cursor creation successful"
# except:
#     print "Cursor creation failure"
#
# create_table_command = create_table_command.replace("header_new", "excluded_data")
# try:
#     cur.execute(create_table_command)
#     print "Table excluded_data created successfully using: " + create_table_command
# except:
#     print "Table creation failure. Tried with: " + create_table_command
#
# try:
#     for class_name in header:
#         # print "SELECT {} FROM header_old EXCEPT SELECT {} FROM header_new".format(class_name,class_name)
#         cur.execute("SELECT {} FROM header_old EXCEPT SELECT {} FROM header_new".format(class_name,class_name))
#         for data in cur:
#             # print "INSERT INTO excluded_data ({}) VALUES (%s)".format(class_name), data
#             tmp_cur.execute("INSERT INTO excluded_data ({}) VALUES (%s)".format(class_name), data)
#     print "Table excluded_data populated successfully"
# except:
#     print "Failure on finding excluded data"
#
# print "----------------------------------------------------"
# print "----------------------------------------------------"
# print "EXCLUDED_DATA"
# cur.execute("SELECT * FROM excluded_data")
# for data in cur:
#     print data
#
# print "----------------------------------------------------"
# print "----------------------------------------------------"
#
# create_table_command = create_table_command.replace("excluded_data", "added_data")
# try:
#     cur.execute(create_table_command)
#     print "Table added_data created successfully using: " + create_table_command
# except:
#     print "Table creation failure. Tried with: " + create_table_command
#
# try:
#     for class_name in header:
#         # print "SELECT {} FROM header_old EXCEPT SELECT {} FROM header_new".format(class_name,class_name)
#         cur.execute("SELECT {} FROM header_new EXCEPT SELECT {} FROM header_old".format(class_name, class_name))
#         for data in cur:
#             # print "INSERT INTO added_data ({}) VALUES (%s)".format(class_name), data
#             tmp_cur.execute("INSERT INTO added_data ({}) VALUES (%s)".format(class_name), data)
#     print "Table added_data populated successfully"
# except:
#     print "Failure on finding added data"
#
# print "----------------------------------------------------"
# print "----------------------------------------------------"
# print "ADDED_DATA"
# cur.execute("SELECT * FROM added_data")
# for data in cur:
#     print data
#
# print "----------------------------------------------------"
# print "----------------------------------------------------"
#
# try:
#     conn.commit()
#     print "Successful commit"
# except:
#     print "Commit failure"
#
# print "----------------------------------------------------"

excluded_data = OrderedDict([])
added_data = OrderedDict([])

# Finding fields excluded from each class separately by fetching its column from both relations, then performing set subtraction (OLD / NEW)
# Writing the results into excluded_data dictionary (key: class_name, value: list_of_elements_in_set{OLD/NEW})
try:
    for class_name in header:
        cur.execute("SELECT {} FROM header_old EXCEPT SELECT {} FROM header_new".format(class_name,class_name))
        excluded_data.update({class_name : []})
        for data in cur:
            excluded_data[class_name].append(data)
    print "\nExcluded data successfully extracted"
except psycopg2.Error as psycoerr:
    print "\nFailure on extracting excluded data: {}".format(psycoerr)
    sys.exit(1)

# Finding fields added in each class separately by fetching its column from both relations, then performing set subtraction (NEW / OLD)
# Writing the results into added_data dictionary (key: class_name, value: list_of_elements_in_set{NEW/OLD})
try:
    for class_name in header:
        cur.execute("SELECT {} FROM header_new EXCEPT SELECT {} FROM header_old".format(class_name,class_name))
        added_data.update({class_name : []})
        for data in cur:
            added_data[class_name].append(data)
    print "\nAdded data successfully extracted"
except psycopg2.Error as psycoerr:
    print "\nFailure on extracting added data: {}".format(psycoerr)
    sys.exit(1)

print "\n----------------------------------------------------"

try:
    conn.close()
    print "\nConnection with DB successfully closed"
except psycopg2.Error as psycoerr:
    print "\nFailure on closing connection with DB: {}".format(psycoerr)
    sys.exit(1)

print "\n----------------------------------------------------"
print "----------------------------------------------------"

print "\nEXCLUDED DATA:"
for key in excluded_data:
    print key + ': {}'.format(excluded_data[key])

print "\n----------------------------------------------------"

print "\nADDED DATA:"
for key in added_data:
    print key + ': {}'.format(added_data[key])