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

import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('transactions.xml')
root = tree.getroot()

# Iterate over each item in the XML list
for transaction in root.findall('transaction'):
    #############################################
    cursor.execute("""
            SELECT
            COUNT(*)
            FROM user_data_consolidated_origin_ids
            """)
    record_count = cursor.fetchone()[0]
    transac_id = str(uuid.uuid4())
    transac_phone = transaction.find("phone").text
    transac_store = transaction.find("store").text
    transac_id = transaction.get('id')

    transaction_ID = str(uuid.uuid4())
    insert_query = """
           INSERT INTO transaction (id,originid,store_name,user_telephone)
           VALUES (%s, %s, %s, %s)
           """

    # Define the data to be inserted
    arr = (transaction_ID,transac_id,transac_store, transac_phone)

    print(insert_query % arr)
    # Execute the SQL query with the data
    cursor.execute(insert_query, arr)
    #############################################

    for items in transaction.findall('items'):
        for item in items:
            name = item.find("item").text
            price = item.find('price').text
            price_per_item = item.find('price_per_item').text
            quantity = item.find('quantity').text

            #############################################

            insert_query = """
             INSERT INTO sale_item (id,name,value)
             VALUES (%s, %s, %s)
             """
            item_id = str(uuid.uuid4())
            # Define the data to be inserted
            arr = (item_id,name,price_per_item)


            print(insert_query %arr)
            # Execute the SQL query with the data
            cursor.execute(insert_query, arr)

            #############################################
            list_entry_id = str(uuid.uuid4())
            insert_query = """
                         INSERT INTO item_list_entry (id,item,quantity, value_at_purchase, total_value)
                         VALUES (%s, %s, %s, %s, %s)
                         """

            # Define the data to be inserted
            arr = (list_entry_id,item_id, quantity, price_per_item, price)

            print(insert_query % arr)
            # Execute the SQL query with the data
            cursor.execute(insert_query, arr)
            #############################################
            insert_query = """
                           INSERT INTO transaction_entries (transaction_id,entries_id,entries_order)
                           VALUES (%s, %s, %s)
                           """
            record_count += 1
            # Define the data to be inserted
            arr = (transaction_ID, list_entry_id,record_count)

            print(insert_query % arr)
            # Execute the SQL query with the data
            cursor.execute(insert_query, arr)
            #############################################


        conn.commit()


# Open the JSON file
# with open('promotions.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#
#     # Read the header (first row)
#     header = next(csv_reader)
#     print(f'Header: {header}')
#
#     # Iterate over the remaining rows
#     for row in csv_reader:
#         # Define the SQL query to insert data
#         insert_query = """
# INSERT INTO promotions (id,create_date,delete_date,email,is_deleted,promotion_name,responded,telephone_given_at_the_time_of_registration,origin_id)
# VALUES (%s, %s, null,%s, %s, %s,%s, %s, %s)"""
#
#         # Define the data to be inserted
#         arr = (str(uuid.uuid4()),str(datetime.now()),row[1],0,row[3],row[4].lower()=="yes", row[2], row[0])
#
#
#         print(insert_query %arr)
#         # Execute the SQL query with the data
#         cursor.execute(insert_query, arr)
#
#         # Commit the transaction
#         conn.commit()



# Close the cursor and connection
cursor.close()
conn.close()
