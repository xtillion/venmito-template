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


# Open the JSON file
with open('people.yml', 'r') as file:
    data = yaml.safe_load(file)
    for user in data:
        # Define the SQL query to insert data
        insert_query = """
INSERT INTO user_data (id, origin_id, first_name, last_name, telephone, email, enabled, user_devices,  location_city, location_country, create_date, delete_date, is_deleted, origin)
VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, null, %s, %s)"""

        first_name = user['name'].split(' ')[0].strip()
        last_name = user['name'].split(' ')[1].strip()

        city = user['city'].split(',')[0].strip()
        country = user['city'].split(',')[1].strip()

        devices = ''
        if user["Android"] :
            devices = 'Android,'
        if user["Desktop"]:
            devices += 'Desktop,'
        if user["Iphone"] :
            devices += 'Iphone'
        if devices[-1] == ',':
            devices = devices[0:-1]
        # Define the data to be inserted
        arr = (str(uuid.uuid4()),user["id"],first_name,last_name,user["phone"],user["email"],1,devices,city,country,str(datetime.now()),0,"YML")


        print("YAML"+(insert_query %arr))
        # Execute the SQL query with the data
        cursor.execute(insert_query, arr)

        # Commit the transaction
        conn.commit()



# Close the cursor and connection
cursor.close()
conn.close()
