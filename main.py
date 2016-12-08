from data_import import *

excluded_data = data_export("header_old", "header_new", cur)

added_data = data_export("header_new", "header_old", cur)

output_separator()

try:
    conn.close()
    print "\nConnection with DB successfully closed"
except psycopg2.Error as psycoerr:
    print "\nFailure on closing connection with DB: {}".format(psycoerr)
    sys.exit(1)

max_cell = define_max_cell(excluded_data, added_data)
num_of_tabs = define_num_of_tabs(excluded_data,added_data)

f = open('/Users/backup/Desktop/treci', 'w')

f.write("{0:{fill}{align}{width}}\n".format('\tEXCLUDED DATA', fill='', align='^', width=len(header)*max_cell+4))
f.write("{0:{fill}{align}{width}}\n".format('-', fill='-', align='<', width=len(header)*max_cell+4))

write_data(excluded_data, max_cell, f)

f.write("\n\n{0:{fill}{align}{width}}\n".format('-', fill='-', align='<', width=len(header)*max_cell+4))
f.write("{0:{fill}{align}{width}}\n".format('-', fill='-', align='<', width=len(header)*max_cell+4))

f.write("\n\n{0:{fill}{align}{width}}\n".format('\tADDED DATA', fill='', align='^', width=len(header)*max_cell+4))
f.write("{0:{fill}{align}{width}}\n".format('-', fill='-', align='<', width=len(header)*max_cell+4))
write_data(added_data, max_cell, f)

print"\n\nExcluded data:"
for key in excluded_data:
    sys.stdout.write(key + ": ")
    print excluded_data[key]

print '\nAdded data:'

for key in added_data:
    sys.stdout.write(key + ": ")
    print added_data[key]
