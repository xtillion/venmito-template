import mysql.connector
import uuid
from datetime import datetime
import yaml

def InsertNewRecord(row):
    #############################################
    eorigin_id = str(uuid.uuid4())
    insert_query = """
        INSERT INTO eorigin_id (id,my_id_value)
        VALUES (%s, %s)"""
    # Define the data to be inserted
    arr = (eorigin_id, int(row[1]))
    cursor.execute(insert_query, arr)
    #############################################
    cursor.execute("""
        SELECT
        COUNT(*)
        FROM user_data_consolidated_origin_ids
        """)
    record_count = cursor.fetchone()
    #############################################
    origin_ids = str(uuid.uuid4())
    insert_query = """
        INSERT INTO user_data_consolidated (id, first_names, last_names, telephones, emails, enabled, user_devices,  location_city, location_country, create_date, delete_date, is_deleted)
        VALUES (%s, %s, %s, %s, %s,%s, %s, %s,%s,  %s, null, %s)"""
    # Define the data to be inserted
    arr = (origin_ids, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], 0)
    # Execute the SQL query with the data
    cursor.execute(insert_query, arr)
    # Commit the transaction
    #############################################################
    insert_query = """
                INSERT INTO user_data_consolidated_origin_ids (origin_ids_order,user_data_consolidated_id,origin_ids_id)
                VALUES (%s, %s, %s)"""
    # Define the data to be inserted
    arr = (record_count[0] + 1, origin_ids, eorigin_id)
    # Execute the SQL query with the data
    cursor.execute(insert_query, arr)
    #############################################
    conn.commit()

def UpdateExistingRecord(id,parameterToUpdate,valueToUpdate):
    print('UPDATE user_data_consolidated udc'
        f'\nSET udc.{parameterToUpdate} = %s'
        '\nWHERE udc.id = %s'%(valueToUpdate.encode('utf-8'),id))
    cursor.execute(
        'UPDATE user_data_consolidated udc'
        f'\nSET udc.{parameterToUpdate} = %s'
        '\nWHERE udc.id = %s'
    , (valueToUpdate.encode('utf-8'),id))
    conn.commit()


def UpdateRecord(row,consolidated_record):
    row_first_name = row[2]
    first_names = consolidated_record[5].decode('utf-8')
    if row_first_name not in first_names:
        print(row_first_name+" not found "+first_names)
        coma = "," if len(first_names) > 0  else ""
        UpdateExistingRecord(consolidated_record[0],"first_names",first_names+coma+row_first_name)

    row_last_name = row[3]
    last_names = consolidated_record[7].decode('utf-8')
    if row_last_name not in last_names:
        print(row_last_name +" not found "+last_names)
        coma = "," if len(last_names) > 0 else ""
        UpdateExistingRecord(consolidated_record[0], "last_names", last_names + coma + row_last_name)

    row_telephone = row[4]
    telephones = consolidated_record[10].decode('utf-8')
    if row_telephone not in telephones:
        print(row_telephone +" not found "+telephones)
        coma = "," if len(telephones) > 0 else ""
        UpdateExistingRecord(consolidated_record[0], "telephones", telephones + coma + row_telephone)

    row_email= row[5]
    emails = consolidated_record[3].decode('utf-8')
    if row_email not in emails:
        print(row_email+" not found "+emails)
        coma = "," if len(emails) > 0 else ""
        UpdateExistingRecord(consolidated_record[0], "emails", emails + coma + row_email)

    row_user_devices = row[7].decode('utf-8')
    user_devices = consolidated_record[11].decode('utf-8')
    for word in row_user_devices.split(","):
        if word not in user_devices:
            print(row_user_devices+" not found "+user_devices)
            coma = "," if len(user_devices) > 0 else ""
            UpdateExistingRecord(consolidated_record[0], "user_devices", user_devices + coma + row_user_devices)

    row_location_city = row[8]
    location_cities = consolidated_record[8].decode('utf-8')
    if row_location_city not in location_cities:
        print(row_location_city+" not found "+location_cities)
        coma = "," if len(location_cities) > 0 else ""
        UpdateExistingRecord(consolidated_record[0], "location_city", location_cities + coma + row_location_city)

    row_location_country= row[9]
    location_countries = consolidated_record[9].decode('utf-8')
    if row_location_country not in location_countries:
        print(row_location_country+" not found "+location_countries)
        coma = "," if len(location_countries) > 0 else ""
        UpdateExistingRecord(consolidated_record[0], "location_country", location_countries + coma + row_location_country )

def InsertOrUpdateRecord(row):
    cursor.execute("""
SELECT udc.id,udc.create_date,udc.delete_date,udc.emails,udc.enabled,
       udc.first_names,udc.is_deleted,udc.last_names,udc.location_city,
       udc.location_country,udc.telephones,udc.user_devices
FROM eorigin_id eo 
JOIN user_data_consolidated_origin_ids ids
ON eo.my_id_value = %s and ids.origin_ids_id = eo.id
JOIN user_data_consolidated udc
ON udc.id = ids.user_data_consolidated_id
    """, (int(row[1]),))
    consolidated_record = cursor.fetchone()
    if consolidated_record == None:
        InsertNewRecord(row)
    else:
        print("Found record" + str(int(row[1])))
        UpdateRecord(row, consolidated_record)

# Establish the connection
conn = mysql.connector.connect(
    host="localhost",  # e.g., "localhost"
    user="root",
    password="my-secret-pw",
    database="testdb",
    port=8083
)

# Create a cursor object
cursor = conn.cursor()

targetSources = ["YML","JSON"]

for target in targetSources:
    cursor.execute(f"SELECT id, origin_id, first_name, last_name, telephone, email, enabled, user_devices,  location_city, "
                   f"location_country, create_date, delete_date, is_deleted, origin"
                   f" FROM user_data"
                   f" WHERE origin=\'{target}\'")
    data = cursor.fetchall()

    # Process the data
    for row in data:
        InsertOrUpdateRecord(row)
# Close the cursor and connection
cursor.close()
conn.close()
