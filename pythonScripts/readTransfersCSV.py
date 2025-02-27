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

import csv

# Open the JSON file
with open('transfers.csv', 'r') as file:
    csv_reader = csv.reader(file)

    # Read the header (first row)
    header = next(csv_reader)

    # Iterate over the remaining rows
    for row in csv_reader:
        # Define the SQL query to insert data
        insert_query = """
INSERT INTO money_transfers (id,amount,create_date,senderid,receiverid,transfer_date)
VALUES (%s, %s, %s, %s, %s, %s)"""

        # Define the data to be inserted
        arr = (str(uuid.uuid4()),row[2],str(datetime.now()),row[0],row[1],row[3])


        print(insert_query %arr)
        # Execute the SQL query with the data
        cursor.execute(insert_query, arr)

        # Commit the transaction
        conn.commit()



# Close the cursor and connection
cursor.close()
conn.close()
