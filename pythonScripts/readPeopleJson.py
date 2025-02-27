import mysql.connector
import uuid
from datetime import datetime
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


import json

# Open the JSON file
with open('people.json', 'r') as file:
    data = json.load(file)
    for user in data:
        # Define the SQL query to insert data
        insert_query = """
INSERT INTO user_data (id, origin_id, first_name, last_name, telephone, email, enabled, user_devices,  location_city, location_country, create_date, delete_date, is_deleted, origin)
VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, null, %s, %s)"""

        # Define the data to be inserted
        arr = (str(uuid.uuid4()),user["id"],user["first_name"],user["last_name"],user["telephone"],user["email"],1,','.join(user["devices"]),user["location"]["City"],user["location"]["Country"],str(datetime.now()),0,"JSON")


        print(insert_query %arr)
        # Execute the SQL query with the data
        cursor.execute(insert_query, arr)

        # Commit the transaction
        conn.commit()



# Close the cursor and connection
cursor.close()
conn.close()
