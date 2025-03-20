x = """
    TEST 
    TEST"""
print(x)
exit()


'''
#
# PREREQUISITES Part 2: Set Up Functions
# > These functions are here to auto-setup the database for the first time.
#


def func_process_people_json( input: dict ) -> dict:
    """
    Function to process all parts of `people.json`. FEATURE: Scalable for new exceptions!
    """
    output = {}
    i2 = { k.lower():v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            case "location":
                # Get `{'City': ..., 'Country': ...}`.
                output.update({ key.lower():value for key, value in v.items() })
            case "telephone":
                # Change "telephone" to "phone".
                output["phone"] = v
            case "devices":
                # Get `"devices": [...]`.
                for device in v:
                    device = device.lower()
                    # The device in the list exists.
                    output[f'has_{device}'] = True
                    # Add any new device.
                    if device not in DEVICES:
                        ANY_NEW_DEVICES = True
                        DEVICES.append(device)
                # Any devices from default list `DEVICES` not in `v` don't exist.
                for device in DEVICES:
                    if device not in v:
                        output[f'has_{device}'] = False
            case _:
                output[k] = v
    if ANY_NEW_DEVICES:
        # TO DO: Open `FILE_LISTS` and update `DEVICES` list.
        ANY_NEW_DEVICES = False
    return output


def func_process_people_yml( input: dict ) -> dict:
    """
    Function to process all parts of `people.yml`. FEATURE: Scalable for new exceptions!
    """
    output = {}
    i2 = { k.lower():v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            case "name":
                # Split "name" into first and last names.
                spl = v.split(" ")
                output["first_name"] = spl[0]
                if len(spl) == 2:
                    output["last_name"] = spl[1]
            case tuple(DEVICES):
                # Individual boolean for each device. 
                output[f"has_{k}"] = bool(v)
            case _:
                output[k] = v
    return output


def func_process_transfers_csv( input: dict ) -> dict:
    """
    Function to process all parts of `transfers.csv`. FEATURE: Scalable for new exceptions!
    """
    output = {}
    i2 = { k.lower():v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            # FEATURE: Add exceptions here.
            case _:
                output[k] = v
    return output


def func_process_transactions_xml( input: dict, TRAN_PRODUCTS: list, lookup_phone: dict ) -> dict:
    """
    Function to process each transaction of `transactions.xml`. FEATURE: Scalable for new exceptions!
    """
    transaction_row = {}
    i2 = {}
    b_can_lookup = lookup_phone != {}
    # Make keys lowercase and capture transaction ID.
    for k, v in input.items():
        match k:
            case "@id":
                i2["id"] = v
            case _:
                i2[k.lower()] = v
    # Process data.
    for k, v in i2.items():
        match k:
            case "items":
                # Create one row for each item in table `transaction_products`.
                if isinstance(v["item"], dict):
                    TRAN_PRODUCTS.append( func_process_item( v["item"], i2["id"] ) )
                elif isinstance(v["item"], list):
                    TRAN_PRODUCTS.extend( [ func_process_item( item, i2["id"] ) for item in v["item"] ] )
            case "phone":
                if b_can_lookup:
                    transaction_row["customer_id"] = lookup_phone[v]
            case _:
                transaction_row[k] = v
    return transaction_row

def func_process_item( item: dict, id ) -> dict:
    """
    Function to process each nested item of a transaction in `transactions.xml`.
    """
    item_row = {"id":id}
    for k, v in item.items():
        match k:
            # FEATURE: Add cases here.
            case _:
                item_row[k] = v
    return item_row


def func_process_universal( input: dict ) -> dict:
    """
    Function to process all data when no exceptions are found.
    """
    return { k.lower():v for k, v in input.items() }


def func_sql_method( table_name, CONN: psycopg.Connection, keys, data_iter ):
    """
    DEV NOTE: DOESN'T WORK. IS IT USEFUL?
    Function to insert data into PostgreSQL using psycopg3,
    while ignoring duplicate primary keys or unique constraints.
    """
    data = [dict(zip(keys, row)) for row in data_iter]  # Convert iterator to list of dictionaries
    columns = ', '.join(keys)  # Column names as CSV
    placeholders = ', '.join([f'%({key})s' for key in keys])  # Named placeholders

    query = f"""
        INSERT INTO {table_name} ({columns}) 
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
    """

    with CONN.cursor() as cur:
        cur.executemany(query, data)
        CONN.commit()


def func_process_files( b_first_time: bool ):
    """
    Only runs when there are files to process.
    """
    c_p = 1
    n_p = len([v for v in FILE_EXIST.values() if v])
    DATA_PEOPLE = {}
    lookup_email = {}
    lookup_phone = {}
    
    # PEOPLE: Process files.
    if FILE_EXIST["people.json"] or FILE_EXIST["people.yml"]:
        DATA_PEOPLE == {}

        # TO DO: Rewrite code below to allow temporary tables on database.
        if FILE_EXIST["people.json"]:
            print(f">> Processing files [{c_p}/{n_p}]...")
            c_p += 1
            DJ = {}; dj = {}
            # Process data.
            with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                DJ = json.load( f )
            for person in DJ:
                dj[ int(person["id"]) ] = func_process_people_json( person )
            # Handle database.
            DJ = pd.DataFrame.from_dict( dj, orient='index' )
            DATA_PEOPLE = DJ
            del DJ, dj
        
        if FILE_EXIST["people.yml"]:
            print(f">> Processing files [{c_p}/{n_p}]...")
            c_p += 1
            DY = {}; dy = {}
            # Process data.
            with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
                DY = yaml.safe_load( f )
            for person in DY:
                dy[ int(person["id"]) ] = func_process_people_yml( person )
            # Handle database.
            DY = pd.DataFrame.from_dict( dy, orient='index' )
            if FILE_EXIST["people.json"]:
                DATA_PEOPLE.update( DY )
            else:
                DATA_PEOPLE = DY
            del DY, dy
        
        # Send to database + handle variables.
        # TO DO: Replace `if_exists` with `method` to ignore duplicates and [...].
        DATA_PEOPLE.to_sql( "people", CONN, index=False, if_exists='append' ) 
    
    if DATA_PEOPLE == {} and b_first_time:
        # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS NO usable data.
        # TO DO: Rewrite code below based on changes for temporary tables mentioned above.
        # - User must be prompted to find the right files to get rid of temporary tables.
        sys.exit(">> ERROR | Insufficient data for proper process.\nQuitting app...")
    elif DATA_PEOPLE == {} and not b_first_time:
        # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS usable data.
        # TO DO: Create `func_get_lookups()` to extract ids, emails, and phones from complete database.
        # - `lookup_email`: `SELECT id, email FROM people`
        # - `lookup_phone`: `SELECT id, phone FROM people`
        pass
    lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
    lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}
    b_can_lookup = lookup_phone != {}
    
    # TRANSFERS: Process file.
    if FILE_EXIST["transfers.csv"]:
        print(f">> Processing files [{c_p}/{n_p}]...")
        c_p += 1
        TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )
        TRANSFERS.columns = [ h.lower() for h in TRANSFERS.columns ]
        TRANSFERS.to_sql( "transfers", CONN, index=False, if_exists="append" )
    
    # PROMOTIONS: Process file.
    if FILE_EXIST["promotions.csv"]:
        print(f">> Processing files [{c_p}/{n_p}]...")
        c_p += 1
        PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
        PROMOTIONS.columns = [ h.lower() for h in PROMOTIONS.columns ]
        other_headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
        if b_can_lookup:
            s1 = PROMOTIONS["client_email"].map( lookup_email )
            s2 = PROMOTIONS["telephone"].map( lookup_phone )
            PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
            del s1, s2
        else:
            # TO DO: Apply `func_get_lookups()` from previous TO DOs.
            pass
        PROMOTIONS["responded"] = PROMOTIONS["responded"].map({ "Yes":True, "No":False })
        PROMOTIONS = PROMOTIONS[["id", "customer_id", *other_headers]]
    
    # TRANSACTIONS: Split into UNIQUE and PRODUCTS.
    if FILE_EXIST["transactions.xml"]:
        print(f">> Processing files [{c_p}/{n_p}]...")
        with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
            DT = xmltodict.parse(f)["transactions"]["transaction"]
        TRAN_PRODUCTS = []
        TRAN_UNIQUE = [ func_process_transactions_xml( transaction, TRAN_PRODUCTS, lookup_phone ) for transaction in DT ]
        db_name = "transactions_unique" if b_can_lookup else "tmp_transactions_unique"
        TRAN_UNIQUE = pd.DataFrame( TRAN_UNIQUE )
        TRAN_UNIQUE.to_sql( db_name, CONN, index=False, if_exists="append" )
        TRAN_PRODUCTS = pd.DataFrame( TRAN_PRODUCTS )
        TRAN_PRODUCTS.to_sql( "transaction_products", CONN, index=False, if_exists="append" )


def func_create_tables():
    """
    Create tables with foreign key attributes and other features. If tables already exist first, run `func_reset_databases()`.
    """
    with CONN.cursor() as cur:
        CONN.set_autocommit(True)
        cur.execute( """
                    CREATE TABLE people ( 
                        id INTEGER PRIMARY KEY, 
                        first_name TEXT, 
                        last_name TEXT, 
                        phone TEXT UNIQUE, 
                        email TEXT UNIQUE, 
                        city TEXT, 
                        country TEXT, 
                        has_android BOOLEAN, 
                        has_iphone BOOLEAN, 
                        has_desktop BOOLEAN 
                    )""" )
        cur.execute( """
                    CREATE TABLE transfers ( 
                        sender_id INTEGER, 
                        recipient_id INTEGER, 
                        amount MONEY, 
                        date DATE, 
                        FOREIGN KEY(sender_id) REFERENCES people(id), 
                        FOREIGN KEY(recipient_id) REFERENCES people(id) 
                    )""" )
        cur.execute( """
                    CREATE TABLE promotions ( 
                        id INTEGER PRIMARY KEY, 
                        customer_id INTEGER, 
                        promotion TEXT, 
                        responded BOOLEAN, 
                        FOREIGN KEY (customer_id) REFERENCES people(id) 
                    )""" )
        cur.execute( """
                    CREATE TABLE transactions_unique ( 
                        id INTEGER PRIMARY KEY, 
                        customer_id INTEGER, 
                        store TEXT, 
                        FOREIGN KEY (customer_id) REFERENCES people(id)
                    )""" )
        cur.execute( """
                    CREATE TABLE transaction_products ( 
                        transaction_id INTEGER, 
                        item TEXT, 
                        price MONEY, 
                        price_per_item MONEY, 
                        quantity INTEGER, 
                        FOREIGN KEY (transaction_id) REFERENCES transactions_unique(id) 
                    )""" )
        cur.execute( """
                    CREATE VIEW view_store_products AS 
                        SELECT t1.store, t2.item 
                        FROM transactions_unique as t1 
                        LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                    """ ) # DEV NOTE: Test and edit.
        cur.execute( """
                    CREATE VIEW view_transactions AS 
                        SELECT t1.id, t1.customer_id, t1.store, t2.item, t2.price, t2.price_per_item, t2.quantity 
                        FROM transactions_unique as t1 
                        LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                    """ ) # DEV NOTE: Test and edit.
        CONN.set_autocommit(False)


def func_first_time():
    func_create_tables()
    if CAN_ADD:
        func_process_files( True )
    else:
        print("< ERROR | No files to add.")
        exit()


def func_reset_databases():
    with CONN.cursor() as cur:
        CONN.set_autocommit(True)
        cur.execute( "DROP TABLE IF EXISTS people CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transfers CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS promotions CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transactions CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transaction_products CASCADE" )
        cur.execute( "DROP VIEW IF EXISTS view_store_products CASCADE" )
        CONN.set_autocommit(False)


#
# PREREQUISITES Part 3: Check Database
#
print("> Checking prerequisites [3/3]")

# Check if database exists.
try:
    CONN = psycopg.connect( "dbname=postgres user=postgres password=Space!3742" )
except:
    console.print_exception( show_locals=True )
    print("\n< Can't connect to database.\n> Quitting app...\n")
    exit()
    # TO DO: Set up server from scratch here??

# Check if database is complete.
try:
    with CONN.cursor() as cur:
        # DEV NOTE: Test!
        cur.execute( """SELECT EXISTS ( SELECT 1 FROM people ) AS table_existence""" )
        x = cur.fetchone()
        print(x)
        exit()
except:
    CONN.rollback()
    console.print(">> First time setup...")
    func_reset_databases()
    func_first_time()



#
# PART 2: Introduction
#
print(f"\n< All prerequisites satisfied!\n\n\n{BORDER}\n{mid_txt(TITLE)}\n\n")
print("MAIN MENU\n[0] Import data\n[1]")
'''






import os, xmltodict

DIR_PROGRAM = os.getcwd()
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
FILES_DATA = [ # Scalable!
    "people.json",
    "people.yml",
    "transfers.csv",
    "promotions.csv",
    "transactions.xml"
]
FILE_EXIST = { f : os.path.exists(os.path.join(DIR_DATA, f)) for f in FILES_DATA }


def func_process_transactions_xml( TRAN_PRODUCTS: list, input: dict ) -> dict:
    """
    Function to process each transaction of `transactions.xml` with scalability for new exceptions.
    """
    transaction_row = {}
    i2 = {}
    # Make keys lowercase and capture transaction ID.
    for k, v in input.items():
        match k:
            case "@id":
                i2["id"] = v
            case _:
                i2[k.lower()] = v
    # Process data.
    for k, v in i2.items():
        match k:
            case "items":
                # Create one row for each item in table `transaction_products`.
                if isinstance(v["item"], dict):
                    TRAN_PRODUCTS.append( func_process_item( v["item"], i2["id"] ) )
                    #TRAN_PRODUCTS[ i2["id"] ] = func_process_item( v, i2["id"] )
                elif isinstance(v["item"], list):
                    TRAN_PRODUCTS.extend( [ func_process_item( item, i2["id"] ) for item in v["item"] ] )
                    #for item in v: TRAN_PRODUCTS[ i2["id"] ] = func_process_item( item, i2["id"] )
            case _:
                transaction_row[k] = v
    return transaction_row

def func_process_item( item: dict, id ) -> dict:
    """
    Function to process each nested item of a transaction in `transactions.xml`.
    """
    item_row = {"id":id}
    for k, v in item.items():
        match k:
            # FEATURE: Add cases here.
            case _:
                item_row[k] = v
    return item_row


if FILE_EXIST["transactions.xml"]:
    #TRAN_UNIQUE = []
    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
        DT = xmltodict.parse(f)["transactions"]["transaction"]
    TRAN_PRODUCTS = []
    TRAN_UNIQUE = [ func_process_transactions_xml( TRAN_PRODUCTS, transaction ) for transaction in DT ]
    #for transaction in DT:
    #    func_process_transactions_xml( TRAN_UNIQUE, TRAN_PRODUCTS, transaction )
    print(TRAN_UNIQUE)
    print(TRAN_PRODUCTS)

exit()







'''
### BOOKMARK
def func_one_sql( command: str, *args ):
    """DEV NOTE: Necessary???"""
    with CONN.cursor() as cur:
        if len(args) == 0:
            cur.execute( sql.SQL( command ) )
        else:
            cur.execute( sql.SQL( command ).format( *args ) )
        CONN.commit()
'''



"""### BOOKMARK First time importing to `default_lists.p`
import pickle
DEVICES = ["android", "iphone", "desktop"]
with open("default_lists.p", 'wb') as f:
    pickle.dump(DEVICES, f)
exit()"""


'''"""

Venmito Data
===

About
---
begin.py: Generates GUI and binds commands.

Author
---
Code by Jared Hidalgo.

"""



#
# PREREQUISITES Part 1: Check Packages
#
TITLE = "Venmito Data Processer"
print("\n> Checking prerequisites...")

# Import internal packages.
import os, sys, json, csv
from platform import system
from subprocess import call, Popen
from importlib.metadata import distributions
#import xml.etree.ElementTree as ET

# Set variables.
EXE_GLOBAL = f"{sys.executable}"
DIR_PROGRAM = os.getcwd() #"_".join( os.getcwd().split(" ") )
TXT_REQ = os.path.join( DIR_PROGRAM, "requirements.txt" )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
ANY_DATA = False

# Set formatting.
N = 50
BORDER = "-"*N
def mid_txt( input: str ):
    spaces = " "*(( N-len(input) )//2)
    return spaces + input + spaces

# Check dependent files. 
req_files = [ # Scalable!
    "people.json",
    "people.yml",
    "transfers.csv",
    "promotions.csv",
    "transactions.xml"
]
FILE_EXIST = { f : os.path.exists(os.path.join(DIR_DATA, f)) for f in req_files }
WILL_ADD = any( FILE_EXIST.values() )

# Temporarily import program directory to PATH to import program files from any directory.
sys.path.append( DIR_PROGRAM )

# Set command(s) based on OS.
dict_od = {
    "Windows": "explorer", 
    "Darwin": "open"
}
OPEN_DIR = dict_od[system()] if system() in dict_od else "xdg-open"

# Package check: Offline check.
dict_pk = {
    "psycopg[binary]": "psycopg"
}
with open(TXT_REQ, "r") as r:
    req_pkgs = { i.split("==" if "==" in i else "\n")[0] : i for i in r.readlines() }
for k in dict_pk.keys():
    del req_pkgs[k]
req_pkgs = req_pkgs.keys()
for v in dict_pk.values():
    req_pkgs.append( v )
curr_pkgs = [ "-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions() ]
miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]

if len(miss_pkgs) > 0:
    # Attempt online download.
    print()
    call( f"{EXE_GLOBAL} -m pip install -U pip", shell=True )
    call( f"{EXE_GLOBAL} -m pip install -r \"{TXT_REQ}\"", shell=True )
    # Check again.
    curr_pkgs = [ "-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions() ]
    miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]
    if len(miss_pkgs) > 0:
        txt = "package" if len(miss_pkgs) == 1 else "packages"
        sys.exit( f"\n\n< ERROR | Missing {txt}: {",".join(miss_pkgs)}\n--> Can't run program." )
    print()

# Import external packages.
import psycopg, xmltodict, yaml
from psycopg import sql
import pandas as pd
import chime
chime.theme( "material" )
from rich.traceback import install
install( show_locals=True )
from rich.console import Console
console = Console()


#
# PREREQUISITES Part 2: Set Up Functions
# > These functions are here to auto-setup the database for the first time.
#
def func_universal( input: dict ) -> dict:
    """
    Parent function to process all known exceptions. Designed to scale for more exceptions.

    Args:
        input (dict): Original dictionary from the file.

    Returns:
        dict: Processed dictionary.
    """
    tmp = {}
    i2 = { k.lower() : v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            case "location":
                tmp.update(v)
            case "telephone":
                tmp["phone"] = v
            case "name":
                spl = v.split(" ")
                tmp["first_name"] = spl[0]
                if len(spl) == 2:
                    tmp["last_name"] = spl[1]
            case "devices":
                tmp["has_android"] = "Android" in v
                tmp["has_iphone"] = "Iphone" in v
                tmp["has_desktop"] = "Desktop" in v
            case "android" | "desktop" | "iphone":
                tmp[f"has_{k}"] = bool(v)
            case _:
                tmp[k] = v
    return tmp


def func_sql_method(table_name, conn: psycopg.Connection, keys, data_iter):
    """
    Function to insert data into PostgreSQL using psycopg3,
    while ignoring duplicate primary keys or unique constraints.
    """
    data = [dict(zip(keys, row)) for row in data_iter]  # Convert iterator to list of dictionaries
    columns = ', '.join(keys)  # Column names as CSV
    placeholders = ', '.join([f'%({key})s' for key in keys])  # Named placeholders

    query = f"""
        INSERT INTO {table_name} ({columns}) 
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
    """

    with conn.cursor() as cur:
        cur.executemany(query, data)
        conn.commit()


def func_process_files( cur: psycopg.Cursor, from_scratch: bool ):

    print("> Processing files...")

    # Process people.
    if FILE_EXIST["people.json"] or FILE_EXIST["people.yml"]:
        DATA_PEOPLE = {}
        DJ = {}
        DY = {}

        # Process files.
        if FILE_EXIST["people.json"]:
            with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                for person in json.load( f ):
                    DJ[ int(person["id"]) ] = func_universal( person )
            DJ = pd.DataFrame.from_dict( DJ, orient='index' )
            DJ.to_sql( "people", conn, index=False, method=func_sql_method )
        
        if FILE_EXIST["people.yml"]:
            with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
                for person in yaml.safe_load( f ):
                    DY[ int(person["id"]) ] = func_universal( person )
            DY = pd.DataFrame.from_dict( DY, orient='index' )
            DY.to_sql( "people", conn, index=False, method=func_sql_method )
        
        #
        #
        
        # Cleanup dictionaries.
        if FILE_EXIST["people.json"] and FILE_EXIST["people.yml"]:
            common = list( set(DJ.keys()) & set(DY.keys()) )
            # DEV NOTE: Handle data overlap here.
        else:
            DATA_PEOPLE = DJ if FILE_EXIST["people.json"] else DY
        DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )

        # Send to database.
        DATA_PEOPLE.to_sql( "people", conn, if_exists="append", index=False )

        # DEV NOTE: If not first_time, then extract full database first.
        if from_scratch:
            lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
            lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}
    
    if FILE_EXIST["transfers.csv"]:
        TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )
        # DEV NOTE: Cast correct data types here.
        TRANSFERS.to_sql( "tmp_transfers", conn, if_exists="append", index=False )
        cur.execute( """
                     INSERT INTO transfers 
                        (SELECT * FROM tmp_transfers)
                        ON CONFLICT DO NOTHING
                     """ )

    PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
    headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
    s1 = PROMOTIONS["client_email"].map( lookup_email )
    s2 = PROMOTIONS["telephone"].map( lookup_phone )
    PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
    PROMOTIONS["responded"] = PROMOTIONS["responded"].map( {"Yes":True, "No":False} )
    PROMOTIONS = PROMOTIONS[["id", "customer_id", *headers]]

    ### BOOKMARK
    TRANSACTIONS = []
    PRODUCTS = [] # DEV NOTE: Change this to a view within a schema?
    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'r' ) as f:
        tree = ET.parse(f)
    root = tree.getroot()
    for transaction in root.findall("transaction"):
        t_id = transaction.get("id")
        customer_id = lookup_phone[transaction.find("phone").text]
        store = transaction.find("store").text
        # DEV NOTE: Set loop for other variables except for known exceptions. Also split into two databases.
        for item in transaction.find("items").findall("item"):
            TRANSACTIONS.append({
                "transaction_id": int(t_id),
                "customer_id": customer_id,
                "store": store,
                "item": item.find("item").text,
                "price": float(item.find("price").text),
                "price_per_item": float(item.find("price_per_item").text),
                "quantity": int(item.find("quantity").text)
            })
            PRODUCTS.append( {store, item.find("item").text} )

    TRANSACTIONS = pd.DataFrame( TRANSACTIONS )
    TRANSACTIONS["customer_id"] = TRANSACTIONS["customer_id"].astype(int)
    PRODUCTS = pd.DataFrame( PRODUCTS, columns=["Store", "Item"] )


    ### BOOKMARK
    # DATA 4/4: Add to database.
    DATA_PEOPLE.to_sql( "people", conn, if_exists="append", index=False )
    """for person in DATA_PEOPLE:
        cur.execute( 
            "INSERT OR IGNORE INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple( person.values() )
        )"""
    TRANSFERS.to_sql( "transfers", conn, if_exists="append", index=False )
    PROMOTIONS.to_sql( "promotions", conn, if_exists="append", index=False )
    TRANSACTIONS.to_sql( "transactions", conn, if_exists="append", index=False )
    PRODUCTS.to_sql( "products", conn, if_exists="append", index=False )


def func_create_databases( cur: psycopg.Cursor ):
    
    cur.execute( sql.SQL( "CREATE SCHEMA {}" ).format( sql.Identifier("venmito_evaluator") ) )
    cur.execute( """
                CREATE TABLE venmito_evaluator.people ( 
                    id INTEGER PRIMARY KEY, 
                    first_name TEXT, 
                    last_name TEXT, 
                    phone TEXT, 
                    email TEXT, 
                    city TEXT, 
                    country TEXT, 
                    has_android BOOLEAN, 
                    has_iphone BOOLEAN, 
                    has_desktop BOOLEAN 
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.transfers ( 
                    sender_id INTEGER, 
                    recipient_id INTEGER, 
                    amount MONEY, 
                    date DATE, 
                    FOREIGN KEY(sender_id) REFERENCES venmito_evaluator.people(id), 
                    FOREIGN KEY(recipient_id) REFERENCES venmito_evaluator.people(id) 
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.promotions ( 
                    id INTEGER PRIMARY KEY, 
                    customer_id INTEGER, 
                    phone TEXT, 
                    promotion TEXT, 
                    responded BOOLEAN, 
                    FOREIGN KEY (customer_id) REFERENCES venmito_evaluator.people(id) 
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.transactions ( 
                    id INTEGER PRIMARY KEY, 
                    customer_id TEXT, 
                    store TEXT, 
                    FOREIGN KEY (customer_id) REFERENCES venmito_evaluator.people(id)
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.transaction_products ( 
                    transaction_id INTEGER, 
                    item TEXT, 
                    price REAL, 
                    price_per_item REAL, 
                    quantity INTEGER, 
                    FOREIGN KEY (transaction_id) REFERENCES venmito_evaluator.transactions(id) 
                )""" )
    cur.execute( """
                CREATE VIEW venmito_evaluator.products AS 
                    SELECT t1.store, t2.item 
                    FROM venmito_evaluator.transactions as t1 
                    LEFT JOIN venmito_evaluator.transaction_products as t2 ON t1.id = t2.transaction_id
                """ )


def func_first_time( cur: psycopg.Cursor ):
    func_create_databases( cur )
    if WILL_ADD:
        func_process_files( cur, True )
    else:
        print("< ERROR | No files to add.")
        exit()


def func_reset_databases( cur: psycopg.Cursor ):
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.people CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.transfers CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.products CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.promotions CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.transactions CASCADE")
    cur.execute("DROP SCHEMA IF EXISTS venmito_evaluator CASCADE")


#
# PREREQUISITES Part 3: Check Database
#

# Connect.
try:
    conn = psycopg.connect( "dbname=postgres user=postgres password=Space!3742" )
    cur = conn.cursor()
    func_reset_databases(cur)
except:
    console.print_exception( show_locals=True )
    print("\n< Can't continue.\n> Quitting app...\n")
    exit()
    # DEV NOTE: Set up server from scratch here?

# Check if database exists.
try:
    cur.execute( "SELECT * FROM people" )
    text = input( "Before we begin, would you like to reset existing databases? (y/n)" )
    from_scratch = text.lower() == "y"
    if from_scratch:
        func_reset_databases( cur )
        func_first_time( cur )
except:
    # DEV NOTE: Ignore intentional error.
    print("< First time setup!")
    func_first_time( cur )



#
# PART 2: Introduction
#
print(f"< Prerequisites satisfied!\n\n\n{BORDER}\n{mid_txt(TITLE)}\n\n")
print("CLI Menu\n[0] Import data\n[1]")
exit()
'''


'''
#
# ChatGPT suggestions
#

# 1: Best-selling Items
conn = sqlite3.connect("business_data.db")
best_selling = pd.read_sql_query("""
    SELECT item, SUM(quantity) as total_sold 
    FROM transactions 
    GROUP BY item 
    ORDER BY total_sold DESC 
    LIMIT 5
""", conn)
print(best_selling)

# 2: Store with Most Profit
most_profitable_store = pd.read_sql_query("""
    SELECT store, SUM(price) as total_profit 
    FROM transactions 
    GROUP BY store 
    ORDER BY total_profit DESC 
    LIMIT 1
""", conn)
print(most_profitable_store)

# 3: Identify Clients with Promotions
clients_promotions = pd.read_sql_query("""
    SELECT p.client_email, p.promotion, ppl.first_name, ppl.last_name
    FROM promotions p
    JOIN people ppl ON p.client_email = ppl.email
""", conn)
print(clients_promotions)
'''



#req_pkgs = [i.split("==" if "==" in i else "\n")[0] for i in r.readlines()]


"""TITLE = "Venmito Data Processer"
print("\n> Checking requirements...\n")

# Import internal packages.
import os, sys
from platform import system
from subprocess import call, Popen
from importlib.metadata import distributions
import xml.etree.ElementTree as ET

# Set variables.
EXE_GLOBAL = f"{sys.executable}"
DIR_PROGRAM = os.getcwd() #"_".join( os.getcwd().split(" ") )
TXT_REQ = os.path.join( DIR_PROGRAM, "requirements.txt" )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
DB_INFO = {"name": "postgres", "user": "postgres", "password": "Space!3742"}
DATA_ORG = {}
IS_READY = True

# Check dependent files.
req_files = [ "people.json", "people.yml", "transfers.csv", "promotions.csv", "transactions.xml" ]
curr_files = [ os.path.join(DIR_DATA, f) for f in req_files ]
miss_files = [ x for x in req_files if x not in curr_files ]
WILL_ADD = len(miss_files) != len(req_files)

# Temporarily import program directory to PATH to import program files from any directory.
sys.path.append( DIR_PROGRAM )

# Set commands based on OS.
dict_od = {
    "Windows": "explorer", 
    "Darwin": "open"
}
OPEN_DIR = dict_od[system()] if system() in dict_od else "xdg-open"

# Package check: Offline check.
with open(TXT_REQ, "r") as r:
    req_pkgs = [i.split("==" if "==" in i else "\n")[0] for i in r.readlines()]
curr_pkgs    = ["-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions()]
miss_pkgs = [x for x in req_pkgs if x not in curr_pkgs]

if len(miss_pkgs) > 0:
    # Attempt online download.
    call( f"{EXE_GLOBAL} -m pip install -U pip", shell=True )
    call( f"{EXE_GLOBAL} -m pip install -r \"{TXT_REQ}\"", shell=True )
    # Check again.
    curr_pkgs    = [dist.metadata["Name"] for dist in distributions()]
    miss_pkgs = [x for x in req_pkgs if x not in curr_pkgs]
    if len(miss_pkgs) > 0:
        txt = "package" if len(miss_pkgs) == 1 else "packages"
        sys.exit( f"\n\nERROR: Missing {txt}: {",".join(miss_pkgs)}\n--> Can't run program." )
print(">> Importing external packages...")

# Import external packages.
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import chime
chime.theme("material")
from rich.traceback import install
install(show_locals=True)
from rich.console import Console
console = Console()
import yaml, json, csv
import pandas as pd


#
# PART 2: Setup pgAdmin 4.
#

print(">> Checking database...")
try:
    conn = psycopg2.connect( database = DB_INFO["name"],
                            host = "",
                            user = DB_INFO["user"],
                            password = DB_INFO["password"],
                            port = 5432 )
    del conn
except:
    pass"""







'''import os, csv, json, yaml, psycopg
import pandas as pd
import xml.etree.ElementTree as ET

import xmltodict
from rich.traceback import install
install(show_locals=True)

DATA_ORG = {}
DIR_PROGRAM = "_".join( os.getcwd().split(" ") )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )

conn = psycopg.connect( "dbname=postgres user=postgres password=Space!3742" )
cur = conn.cursor()

# DATA 1: Process people.
DATA_PEOPLE = {}
with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
    dataPJ = json.load(f)
for person in dataPJ:
    DATA_PEOPLE[ person["id"] ] = { k:v for k,v in person.items() if not( isinstance(v, (list, dict)) ) }
    if "devices" in person.keys():
        DATA_PEOPLE[ person["id"] ]["has_android"] = "Android" in person["devices"]
        DATA_PEOPLE[ person["id"] ]["has_iphone"] = "Iphone" in person["devices"]
        DATA_PEOPLE[ person["id"] ]["has_desktop"] = "Desktop" in person["devices"]
    if "location" in person.keys():
        DATA_PEOPLE[ person["id"] ]["city"] = person["location"]["City"]
        DATA_PEOPLE[ person["id"] ]["country"] = person["location"]["Country"]
    # Other version
    """for k, v in person.items():
        if isinstance(v, dict):
            DATA_PEOPLE[ person["id"] ]["city"] = v["City"]
            DATA_PEOPLE[ person["id"] ]["country"] = v["Country"]
        elif k == "devices":
            DATA_PEOPLE[ person["id"] ]["has_android"] = "Android" in v
            DATA_PEOPLE[ person["id"] ]["has_iphone"] = "Iphone" in v
            DATA_PEOPLE[ person["id"] ]["has_desktop"] = "Desktop" in v
        else:
            DATA_PEOPLE[ person["id"] ][k] = v"""

with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
    dataPY = yaml.safe_load( f )
for person in dataPY:
    id = person["id"]
    tmp = {
            #"id": person["id"],
            "first_name": person["name"].split()[0],
            "last_name": person["name"].split()[1] if len(person["name"].split()) > 1 else "",
            "phone": person["phone"],
            "email": person["email"],
            "city": person["city"].split(",")[0],
            "country": person["city"].split(",")[-1].strip(),
            "has_android": person["Android"],
            "has_iphone": person["Iphone"],
            "has_desktop": person["Desktop"],
        }
    if id in DATA_PEOPLE:
        # [Insert code to decide which info to prioritize.]
        pass
    else:
        DATA_PEOPLE[id] = tmp
DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )
del dataPJ, dataPY
lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}

# DATA 2: Get other files.
PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
s1 = PROMOTIONS["client_email"].map( lookup_email )
s2 = PROMOTIONS["telephone"].map( lookup_phone )
PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
PROMOTIONS["responded"] = PROMOTIONS["responded"].map( {"Yes":True, "No":False} )
PROMOTIONS = PROMOTIONS[["id", "customer_id", *headers]]


TRAN_UNIQUE = []
PRODUCTS = []
with open( os.path.join( DIR_DATA, "transactions.xml" ), 'r' ) as f:
    x = xmltodict.parse(f)
    #tree = ET.parse(f)
print(x)
exit()
root = tree.getroot()
for transaction in root.findall("transaction"):
    #standard = 
    t_id = transaction.get("id")
    customer_id = lookup_phone[transaction.find("phone").text]
    store = transaction.find("store").text

    for item in transaction.find("items").findall("item"):
        TRAN_UNIQUE.append({
            "transaction_id": int(t_id),
            "customer_id": customer_id,
            "store": store,
            "item": item.find("item").text,
            "price": float(item.find("price").text),
            "price_per_item": float(item.find("price_per_item").text),
            "quantity": int(item.find("quantity").text)
        })
        PRODUCTS.append( {store, item.find("item").text} )

TRAN_UNIQUE = pd.DataFrame( TRAN_UNIQUE )
TRAN_UNIQUE["customer_id"] = TRAN_UNIQUE["customer_id"].astype(int)
PRODUCTS = pd.DataFrame( PRODUCTS, columns=["Store", "Item"] )
print(TRAN_UNIQUE)'''




"""
# File 2
    with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
        dataPY = yaml.safe_load( f )
    for person in dataPY:
        tmp = {}
        for k, v in person.items():
            if k.lower() == "name":
                spl = v.split(" ")
                tmp["first_name"] = spl[0]
                tmp["last_name"] = spl[1]
            else:
                tmp[k] = v
        
        print(person)
        id = person["id"]
        # DEV NOTE: Set loop for other variables except for known exceptions.
        tmp = {
                "id": person["id"],
                "first_name": person["name"].split()[0],
                "last_name": person["name"].split()[1] if len(person["name"].split()) > 1 else "",
                "phone": person["phone"],
                "email": person["email"],
                "city": person["city"].split(",")[0],
                "country": person["city"].split(",")[-1].strip(),
                "has_android": person["Android"],
                "has_iphone": person["Iphone"],
                "has_desktop": person["Desktop"],
            }
        if id in DATA_PEOPLE:
            # [Insert code to decide which info to prioritize.]
            pass
        else:
            DATA_PEOPLE[id] = tmp

    DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )
    del dataPY
"""



"""for FILE in os.listdir( DIR_DATA ):
    fpath = os.path.join( DIR_DATA, FILE )
    fDecode = os.fsdecode( FILE )
    #fspl = fDecode.split(".")
    #fname = ".".join( fspl[:-1] )
    ftype = fDecode.split(".")[-1]
    with open( fpath, 'r', encoding='utf-8-sig' ) as f:
        if ftype == "xml":
            tree = ET.parse(f)
            root = tree.getroot()
            for transaction in root.findall("transaction"):
                transaction_id = transaction.get("id")
                phone = transaction.find("phone").text
                store = transaction.find("store").text

                print(f"Transaction ID: {transaction_id}")
                print(f"Phone: {phone}")
                print(f"Store: {store}")
                print("Items:")

                # Iterate over items in each transaction
                for item in transaction.find("items").findall("item"):
                    item_name = item.find("item").text
                    price = item.find("price").text
                    price_per_item = item.find("price_per_item").text
                    quantity = item.find("quantity").text

                    print(f"  - Item: {item_name}, Price: {price}, Price per item: {price_per_item}, Quantity: {quantity}")

                print("-" * 50)  # Separator for readability"""



"""import os, yaml
from rich.traceback import install
install(show_locals=True)

DIR_PROGRAM = "_".join( os.getcwd().split(" ") )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )

for FILE in os.listdir( DIR_DATA ):
    fspl = os.fsdecode( FILE ).split(".")
    fname = ".".join( fspl[:-1] )
    ftype = fspl[-1]
    with open( os.path.join(DIR_DATA, FILE), 'r' ) as f:
        if ftype == "yml":
            print("hi")
            dict = yaml.full_load(f)
            print(dict)"""


"""import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

con = psycopg2.connect(dbname='postgres',
      user=user_name, host='',
      password=password)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()

# Use the psycopg2.sql module instead of string concatenation 
# in order to avoid sql injection attacks.
cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(db_name))
    )"""


"""import virtualenv, os
PROJECT_NAME = 'new_project'
virtualenvs_folder = os.path.expanduser("~/.virtualenvs")
venv_dir = os.path.join(virtualenvs_folder, PROJECT_NAME)
virtualenv.create_environment(venv_dir)
command = ". {}/{}/bin/activate && pip install -r requirements.txt".format(virtualenvs_folder, PROJECT_NAME)
os.system(command)"""






#
# ARCHIVED
#
exit()



print( f"> Check done!\n{BORDER}\n> Connecting to database..." )

print( f"\n> Connected!\n{BORDER}\n> Booting {TITLE}..." )
#
# [A GUI function]: Process external data.
#


#print( f"\n\nPART 1/3 Done!\n{BORDER}\nPART 2/3: Database Setup\n> Checking connection..." )

# Connect to database.
conn = psycopg_binary.connect( database = DB_INFO["name"],
                         host = "",
                         user = DB_INFO["user"],
                         password = DB_INFO["password"],
                         port = 5432)
conn.set_isolation_level( ISOLATION_LEVEL_AUTOCOMMIT )
cur = conn.cursor()

# CREATE TABLES IF NOT EXIST
print("> Setting up tables...")

# DEV NOTE: Maybe ask user if they want tables to be dropped before running?
cur.execute("DROP TABLE IF EXISTS people CASCADE")
cur.execute("DROP TABLE IF EXISTS transfers CASCADE")
cur.execute("DROP TABLE IF EXISTS products CASCADE")
cur.execute("DROP TABLE IF EXISTS promotions CASCADE")
cur.execute("DROP TABLE IF EXISTS transactions CASCADE")


def process_all( input: dict ) -> dict:
    """
    Parent function to process all known exceptions. Designed to scale for more exceptions.

    Args:
        input (dict): Original data from the file.

    Returns:
        dict: Processed data.
    """
    tmp = {}
    for k, v in input.items():
        k = k.lower()
        match k:
            case "location":
                tmp.update(v)
            case "telephone":
                tmp["phone"] = v
            case "name":
                spl = v.split(" ")
                tmp["first_name"] = spl[0]
                if len(spl) == 2:
                    tmp["last_name"] = spl[1]
            case "devices":
                tmp["has_android"] = "Android" in v
                tmp["has_iphone"] = "Iphone" in v
                tmp["has_desktop"] = "Desktop" in v
            case "android" | "desktop" | "iphone":
                tmp[f"has_{k}"] = bool(v)
            case _:
                tmp[k] = v

        """k = k.lower()
        if k == "location":
            tmp.update(v)
        elif k == "telephone":
            tmp["phone"] = v
        elif k == "name":
            spl = v.split(" ")
            tmp["first_name"] = spl[0]
            if len(spl) == 2:
                tmp["last_name"] = spl[1]
        elif k == "devices":
            tmp["has_android"] = "Android" in v
            tmp["has_iphone"] = "Iphone" in v
            tmp["has_desktop"] = "Desktop" in v
        elif k in ["android", "desktop", "iphone"]:
            tmp[f"has_{k}"] = bool(v)
        else:
            tmp[k] = v"""
    return tmp


if WILL_ADD:
    print("> Processing files from data directory...")
    
    # DATA 2/4: Process people.
    DATA_PEOPLE = {}
    D1 = {}
    with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
        for person in json.load( f ):
            D1[ int(person["id"]) ] = process_all( person )
    D2 = {}
    with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
        for person in yaml.safe_load( f ):
            D2[ int(person["id"]) ] = process_all( person )
    
    common = list( set(D1.keys()) & set(D2.keys()) )
    # DEV NOTE: Handle data overlap here.
    
    DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )
    lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
    lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}

    # DATA 3/4: Process other files.
    TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )

    PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
    headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
    s1 = PROMOTIONS["client_email"].map( lookup_email )
    s2 = PROMOTIONS["telephone"].map( lookup_phone )
    PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
    PROMOTIONS["responded"] = PROMOTIONS["responded"].map( {"Yes":True, "No":False} )
    PROMOTIONS = PROMOTIONS[["id", "customer_id", *headers]]

    TRAN_UNIQUE = []
    PRODUCTS = [] # DEV NOTE: Change this to a view within a schema?
    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'r' ) as f:
        tree = ET.parse(f)
    root = tree.getroot()
    for transaction in root.findall("transaction"):
        t_id = transaction.get("id")
        customer_id = lookup_phone[transaction.find("phone").text]
        store = transaction.find("store").text
        # DEV NOTE: Set loop for other variables except for known exceptions. Also split into two databases.
        for item in transaction.find("items").findall("item"):
            TRAN_UNIQUE.append({
                "transaction_id": int(t_id),
                "customer_id": customer_id,
                "store": store,
                "item": item.find("item").text,
                "price": float(item.find("price").text),
                "price_per_item": float(item.find("price_per_item").text),
                "quantity": int(item.find("quantity").text)
            })
            PRODUCTS.append( {store, item.find("item").text} )

    TRAN_UNIQUE = pd.DataFrame( TRAN_UNIQUE )
    TRAN_UNIQUE["customer_id"] = TRAN_UNIQUE["customer_id"].astype(int)
    PRODUCTS = pd.DataFrame( PRODUCTS, columns=["Store", "Item"] )


    # DATA 4/4: Add to database.
    DATA_PEOPLE.to_sql( "people", conn, if_exists="append", index=False )
    """for person in DATA_PEOPLE:
        cur.execute( 
            "INSERT OR IGNORE INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple( person.values() )
        )"""
    TRANSFERS.to_sql( "transfers", conn, if_exists="append", index=False )
    PROMOTIONS.to_sql( "promotions", conn, if_exists="append", index=False )
    TRAN_UNIQUE.to_sql( "transactions", conn, if_exists="append", index=False )
    PRODUCTS.to_sql( "products", conn, if_exists="append", index=False )

    # Add foreign keys.
    cur.execute("""
                ALTER TABLE transfers 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                    FOREIGN KEY (recipient_id) REFERENCES people(id)
                """)
    cur.execute("""
                ALTER TABLE promotions 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                """)
    cur.execute("""
                ALTER TABLE transactions 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                    FOREIGN KEY (recipient_id) REFERENCES people(id)
                """)
    cur.execute("""
                ALTER TABLE products 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                    FOREIGN KEY (recipient_id) REFERENCES people(id)
                """)

#