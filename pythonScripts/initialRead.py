import mysql.connector
import uuid

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
        INSERT INTO user_data (id, firstName, lastName, telephone, email, enabled, userDevices, originId, locationCity, locationCountry, createDate, deleteDate, isDeleted)
        VALUES (%s, %s, %s)
        """

        # Define the data to be inserted
        arr = (str(uuid.uuid4()),data[])

        # Execute the SQL query with the data
        cursor.execute(insert_query, arr)

        # Commit the transaction
        conn.commit()



# Close the cursor and connection
cursor.close()
conn.close()
