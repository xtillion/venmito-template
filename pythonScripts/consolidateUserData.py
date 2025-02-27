import mysql.connector
import uuid
from datetime import datetime
import yaml

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

cursor.execute(f"SELECT id, origin_id, first_name, last_name, telephone, email, enabled, user_devices,  location_city, location_country, create_date, delete_date, is_deleted, origin"
               f" FROM user_data"
               f" WHERE origin=\'JSON\'")
data = cursor.fetchall()


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


def UpdateRecord(row):
    pass


def InsertOrUpdateRecord(row):
    cursor.execute("""
SELECT udc.* 
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
        UpdateRecord(row)


# Process the data
for row in data:
    InsertOrUpdateRecord(row)
# Close the cursor and connection
cursor.close()
conn.close()
