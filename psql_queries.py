from HTML_extractor import *

# Dynamically generating an SQL query which will create a relation in DB for the old header using the class names as column names
# Will be manually adapted, in data_import.py, to serve the same purpose for the new header. Assuming their class names match.
rows = ''
for row_name in header:
    rows = ''.join((rows, row_name," VARCHAR(255), "))

create_table_command = ''.join(("CREATE TABLE header_old (", ''.join((rows[:-2],rows[-2:].replace(',', ')')))))
create_table_command = create_table_command.replace('@','')

# Dynamically generating an SQL query which will be used to insert one row of data into header_old
# Will be manually adapted, in data_import.py, to serve the same purpose for the new header. Assuming their class names match.
insert_into_values_chunk = ""
for each in header:
    insert_into_values_chunk = ''.join((insert_into_values_chunk, "%s, "))
insert_into_command = ''.join(("INSERT INTO header_old VALUES (", ''.join((insert_into_values_chunk[:-2], insert_into_values_chunk[-2:].replace(',',')')))))
