"""
Venmito Data
===

About
---
begin.py: Runs the entire program.

Author
---
Code by Jared Hidalgo.
"""



#
# PREREQUISITES Part 1: Check Packages
#

# Set formatting.
WIDTH = 100
"""Width of printing borders and aligned text."""
BORDER = "-"*WIDTH
def mid_txt( input: str ):
    spaces = " "*(( WIDTH-len(input) )//2)
    return spaces + input + spaces
TITLE = "Venmito Evaluator"
HEADER = mid_txt(f"< < <   {TITLE}   > > >")
EXIT = f"> Quitting app...\n\n\n{HEADER}\n{BORDER}"
print(f"\nBooting {TITLE}...\n\n> Checking prerequisites [1/2]")

# Import internal packages.
import os, sys
from platform import system
from subprocess import call, Popen
from importlib.metadata import distributions
from json import load as json_load
from pickle import load as pickle_load, dump as pickle_dump
from datetime import datetime
from time import sleep

# Set URIs.
EXE_GLOBAL = f"{sys.executable}"
DIR_PROGRAM = os.getcwd()
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
DIR_PARENT = os.sep.join( DIR_PROGRAM.split(os.sep)[:-1] )
DIR_OUTPUT = os.path.join( DIR_PARENT, "Venmito Output" )
if not os.path.exists( DIR_OUTPUT ):
    os.mkdir( DIR_OUTPUT )
FILE_REQ = os.path.join( DIR_PROGRAM, "requirements.txt" )
FILE_LISTS = os.path.join( DIR_PROGRAM, "default_lists.p" )
with open( FILE_LISTS, 'rb' ) as f:
    tmp = pickle_load(f)
    DEVICES = list(tmp[0])
    # FEATURE: Scalable with permanent changes!

# Check dependent files.
for f in [FILE_REQ, FILE_LISTS]:
    if not os.path.exists(f):
        sys.exit( f"< ERROR | Missing file: {f}\n{EXIT}" )
FILES_DATA = [ # FEATURE: Scalable!
    "people.json",
    "people.yml",
    "transfers.csv",
    "promotions.csv",
    "transactions.xml"
]
FILE_EXIST = { f : os.path.exists(os.path.join(DIR_DATA, f)) for f in FILES_DATA }
b_can_add_data_files = any( FILE_EXIST.values() )

# Temporarily import program directory to PATH to import program files from any directory.
sys.path.append( DIR_PROGRAM )

# Set command(s) based on OS.
dict_od = {
    "Windows": "explorer", 
    "Darwin": "open"
}
OPEN_DIR = dict_od[system()] if system() in dict_od else "xdg-open"

# Package check: Offline check.
replace_pkg_name = { # Scalable!
    "psycopg[binary]": "psycopg"
}
with open(FILE_REQ, "r") as r:
    req_pkgs = { i.split("==" if "==" in i else "\n")[0] : i for i in r.readlines() }
for k in replace_pkg_name.keys():
    del req_pkgs[k]
req_pkgs = list(req_pkgs.keys())
for v in replace_pkg_name.values():
    req_pkgs.append( v )
curr_pkgs = [ "-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions() ]
miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]

if len(miss_pkgs) > 0:
    # Attempt online download.
    print("< WARNING | There are missing packages.\n>> Attempting online download...\n")
    call( f"{EXE_GLOBAL} -m pip install -U pip", shell=True )
    call( f"{EXE_GLOBAL} -m pip install -r \"{FILE_REQ}\"", shell=True )
    # Check again.
    curr_pkgs = [ "-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions() ]
    miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]
    if len(miss_pkgs) > 0:
        txt = "package" if len(miss_pkgs) == 1 else "packages"
        # TO DO: Maybe allow user option to continue?
        sys.exit( f"\n\n< ERROR | Missing {txt}: {",".join(miss_pkgs)}\n{EXIT}" )
    print("\n<< Packages installed successfully.")

# Import `rich` package features.
from rich.traceback import install
install( show_locals=True )
from rich.console import Console
console = Console(record=True)

# Import other external packages.
import chime, xmltodict, yaml
import pandas as pd
from sqlalchemy.engine import create_engine
chime.theme( "material" )


#
# PREREQUISITES Part 2: Set Up Class
#
print("> Checking prerequisites [2/2]")


class Venmito_Evaluator():
    """
    Master class for handling database and commands in the CLI.
    """

    b_can_add = b_can_add_data_files
    b_will_continue = True
    b_new_devices = False
    devices = DEVICES
    """Boolean to keep user in this program after finishing a task."""
    THE_PLAN = """This software isn't finished, but the plan is the following:

    - Create a MAIN MENU. The user can...
        - Manually import new data with `[0] Import New Data`.
        - Pick options to generate pre-made report scripts with `[1] Report Templates`.
        - Write their own SQL script and generate a graph from its results with `[2] DIY Report`.
        - Make an AI prompt with a customized DeepSeek LLM (online or local) with `[3] DeepSeek Prompt`.
        - Start over once they finish a task.
    - [1] Report Templates: For example, the user can select an option to...
        - Make a frequency graph of bought products from the TRANSACTION_UNIQUE and TRANSACTION_PRODUCTS tables.
        - 
    X"""

    def __init__( self ):
        try:
            self.engine = create_engine( "postgresql+psycopg://postgres:Space!3742@localhost:5432/postgres" )
            self.conn = self.engine.raw_connection()
            #self.conn = psycopg.connect( "dbname=postgres user=postgres password=Space!3742" )
        except:
            console.print_exception( show_locals=True )
            print(f"\n< Can't connect to database.\n{EXIT}")
            exit()
            # TO DO: Set up server from scratch here??

        # Check if tables exist.
        b_first_time = input( "= Would you like to start from scratch? (y/n): " )
        if b_first_time:
            self._func_first_time()
        
        print(f"< All prerequisites satisfied!\n\n\n{BORDER}\n{HEADER}\n\n")
        self.func_menu_loop()


    def _func_first_time( self ):
        self._func_reset_database()
        self._func_create_tables()
        if self.b_can_add:
            self._func_process_master( True )
            self._func_handle_views()
        else:
            sys.exit( "<< ERROR | No valid files detected in `data` folder.\n{EXIT}" )


    def _func_reset_database( self ):
        cur = self.conn.cursor()
        cur.execute( "DROP TABLE IF EXISTS people CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transfers CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS promotions CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transactions_unique CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transaction_products CASCADE" )
        cur.execute( "DROP VIEW IF EXISTS view_store_products CASCADE" )
        cur.execute( "DROP VIEW IF EXISTS view_transactions CASCADE" )
        self.conn.commit()
        cur.close()


    def _func_create_tables( self ):
        """
        Create tables with foreign key attributes and other features. 
        
        If tables exist and are broken, run `self._func_reset_database()` first.
        """
        cur = self.conn.cursor()
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
        self.conn.commit()
        cur.close()


    def _func_handle_views( self ):
        """
        Create or replace views. 
        
        If views exist and are broken, run `self._func_reset_database()` first.
        """
        cur = self.conn.cursor()
        cur.execute( """
                    CREATE OR REPLACE VIEW view_store_products AS 
                        SELECT t1.store, t2.item 
                        FROM transactions_unique as t1 
                        LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                    """ ) # DEV NOTE: Test and edit.
        cur.execute( """
                    CREATE OR REPLACE VIEW view_transactions AS 
                        SELECT t1.id, t1.customer_id, t1.store, t2.item, t2.price, t2.price_per_item, t2.quantity 
                        FROM transactions_unique as t1 
                        LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                    """ ) # DEV NOTE: Test and edit.
        self.conn.commit()
        cur.close()


    def _func_process_master( self, b_first_time: bool ):
        """
        Can only run when there are files to process.
        """
        c_p = 1
        n_p = len([v for v in FILE_EXIST.values() if v])
        DATA_PEOPLE = None
        lookup_email = None
        lookup_phone = None
        
        # PEOPLE: Process files.
        if FILE_EXIST["people.json"] or FILE_EXIST["people.yml"]:
            DATA_PEOPLE == None

            # TO DO: Rewrite code below to allow temporary tables on database.
            if FILE_EXIST["people.json"]:
                print(f">> Processing files [{c_p}/{n_p}]...")
                c_p += 1
                DJ = {}; dj = {}
                # Process data.
                with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                    DJ = json_load( f )
                for person in DJ:
                    dj[ int(person["id"]) ] = self._func_process_people_json( person )
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
                    dy[ int(person["id"]) ] = self._func_process_people_yml( person )
                # Handle database.
                DY = pd.DataFrame.from_dict( dy, orient='index' )
                if FILE_EXIST["people.json"]:
                    DATA_PEOPLE.update( DY )
                else:
                    DATA_PEOPLE = DY
                del DY, dy
            
            # Send to database + handle variables.
            # TO DO: Replace `if_exists` with `method` to ignore duplicates and [...].
            DATA_PEOPLE.to_sql( "people", self.engine, index=False, if_exists='append' ) 
        
        '''if DATA_PEOPLE == None and b_first_time:
            # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS NO usable data.
            # TO DO: Rewrite code below based on changes for temporary tables mentioned above.
            # - User must be prompted to find the right files to get rid of temporary tables.
            sys.exit(">> ERROR | Insufficient data for proper process.\nQuitting app...")
        elif DATA_PEOPLE == None and not b_first_time:
            # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS usable data.
            # TO DO: Create `self._func_get_lookups()` to extract ids, emails, and phones from complete database.
            # - `lookup_email`: `SELECT id, email FROM people`
            # - `lookup_phone`: `SELECT id, phone FROM people`
            pass'''
        lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
        lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}
        b_can_lookup = lookup_phone != {}
        
        # TRANSFERS: Process file.
        if FILE_EXIST["transfers.csv"]:
            print(f">> Processing files [{c_p}/{n_p}]...")
            c_p += 1
            TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )
            TRANSFERS.columns = [ h.lower() for h in TRANSFERS.columns ]
            TRANSFERS.to_sql( "transfers", self.engine, index=False, if_exists="append" )
        
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
                # TO DO: Apply `self._func_get_lookups()` from previous TO DOs.
                pass
            PROMOTIONS["responded"] = PROMOTIONS["responded"].map({ "Yes":True, "No":False })
            PROMOTIONS = PROMOTIONS[["id", "customer_id", *other_headers]]
        
        # TRANSACTIONS: Split into UNIQUE and PRODUCTS.
        if FILE_EXIST["transactions.xml"]:
            print(f">> Processing files [{c_p}/{n_p}]...")
            with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
                DT = xmltodict.parse(f)["transactions"]["transaction"]
            TRAN_PRODUCTS = []
            TRAN_UNIQUE = [ self._func_process_transactions_xml( transaction, TRAN_PRODUCTS, lookup_phone ) for transaction in DT ]
            db_name = "transactions_unique" if b_can_lookup else "tmp_transactions_unique"
            TRAN_UNIQUE = pd.DataFrame( TRAN_UNIQUE )
            TRAN_UNIQUE.to_sql( db_name, self.engine, index=False, if_exists="append" )
            TRAN_PRODUCTS = pd.DataFrame( TRAN_PRODUCTS )
            TRAN_PRODUCTS.to_sql( "transaction_products", self.engine, index=False, if_exists="append" )

        # Update views.
        self._func_handle_views()


    def _func_process_people_json( self, input: dict ) -> dict:
        """
        Function to process all parts of `people.json`. FEATURE: Scalable for new exceptions!
        """
        output = {}
        i2 = { k.lower():v for k, v in input.items() }
        for k, v in i2.items():
            match k:
                case "id":
                    output[k] = int(v)
                case "location":
                    # Get `{'City': ..., 'Country': ...}`.
                    output.update({ key.lower():value for key, value in v.items() })
                case "telephone":
                    # Change "telephone" to "phone".
                    output["phone"] = v
                case "devices":
                    # Get `"devices": [...]`.
                    output["has_android"] = "Android" in v
                    output["has_iphone"] = "Iphone" in v
                    output["has_desktop"] = "Desktop" in v
                    '''
                    # DEV NOTE: This is a draft for a loop to keep track of new devices.
                    for device in v:
                        device = device.lower()
                        # The device in the list exists.
                        output[f'has_{device}'] = True
                        # Add any new device.
                        if device not in self.devices:
                            self.b_new_devices = True
                            self.devices.append(device)
                    # Any devices from default list `self.devices` not in `v` don't exist.
                    for device in self.devices:
                        if device not in v:
                            output[f'has_{device}'] = False'''
                case _:
                    output[k] = v
        if self.b_new_devices:
            # TO DO: Open `FILE_LISTS` and update `self.devices` list.
            self.b_new_devices = False
        return output


    def _func_process_people_yml( self, input: dict ) -> dict:
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
                case tuple(self.devices):
                    # Individual boolean for each device. 
                    output[f"has_{k}"] = bool(v)
                case _:
                    output[k] = v
        return output


    def _func_process_transfers_csv( self, input: dict ) -> dict:
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

    
    def _func_process_item( self, item: dict, id ) -> dict:
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


    def _func_process_transactions_xml( self, input: dict, TRAN_PRODUCTS: list, lookup_phone: dict ) -> dict:
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
                        TRAN_PRODUCTS.append( self._func_process_item( v["item"], i2["id"] ) )
                    elif isinstance(v["item"], list):
                        TRAN_PRODUCTS.extend( [ self._func_process_item( item, i2["id"] ) for item in v["item"] ] )
                case "phone":
                    if b_can_lookup:
                        transaction_row["customer_id"] = lookup_phone[v]
                case _:
                    transaction_row[k] = v
        return transaction_row


    def _func_process_universal( self, input: dict ) -> dict:
        """
        Function to process all data when no exceptions are found.
        """
        return { k.lower():v for k, v in input.items() }

    
    def func_menu_loop( self ):
        """
        Loop to allow user to keep using this program after finishing a task.
        """
        print(mid_txt("THE PLAN"))
        print(self.THE_PLAN)



if __name__ == "__main__":
    Venmito_Evaluator()

file = f"traceback_{datetime.strftime( datetime.now(), "%Y %m %d, %H %M %S %f" )}.html"
fpath = os.path.join( DIR_OUTPUT, file )
with open( fpath, "w" ) as f:
    pass
console.save_html( os.path.join( DIR_OUTPUT, file ) )
x = Popen( [OPEN_DIR, DIR_OUTPUT] ) 
sleep(1)