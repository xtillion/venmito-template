These scripts were created in order to import the different type text data into the given database tables. This was in my opinion the most straight forward way to consolidate the data in a database. While also preping for future scenarios if I get more data. 

#### To run the scripts create a venv environment and install the following dependencies:
- pip install mysql-connector-python
- pip install pyyaml


# Running the Scripts
To run the scripts just execute the two following commands 
- source ./myenv/Scripts/activate
- install dependencies  
    - you only need to run this step once  
- python "scriptname"

Notes:
- single items table with all purchased items id, price, name, 
- single itemlist table with id, itemid, amountbought, total price bought at, price per item
- single Purchases table with ID for each transaction, itemlistid, 
- single transfers table with ID for each transfer, sender_id,recipient_id,amount,date
- Single users table with ID firstname, lastname, telephone(NON Nullable), email(non nullable), User Devices, locationCity,locationcountry, originid (id in the original file)
- promotions table with id, email, telephone, promotionname, responded


Future work:
These scripts can be reworked into a tool that automatically loads data from the data base and reconciles the differences in the data.


