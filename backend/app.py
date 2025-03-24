from backend import create_app, database
from backend.etl_scripts.data_loader import clean_database
from backend.etl_scripts.etl import tables_exist, run_etl


# Utility function to handle ETL scripts
def run_etl_scripts(db):
    required_tables = ["people", "promotions", "transactions", "transfers"]

    if not tables_exist(required_tables, db.engine):
        print("Tables are missing. Running ETL.")
    else:
        print("Tables already existed. Cleaning DB and Running ETL.")
        clean_database(db.session)

    # Run ETL process
    with app.app_context():
        run_etl(db.session)

# Main application entry point
if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        run_etl_scripts(database)  # Execute ETL scripts if necessary

    print(app.url_map)  # Print all available routes for debugging

    app.run(host='0.0.0.0', port=5000, debug=True)