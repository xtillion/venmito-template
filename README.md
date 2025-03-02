# Venmito Data Engineering Project

## Introduction

This project is designed to process and analyze data from various sources for Venmito, a payment company. The project involves setting up a database, importing data from multiple file formats, and providing insights into the data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or later installed on your machine.
- PostgreSQL installed and running.
- Access to the database with the necessary permissions to create tables.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Venmito-piter-24
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

To set up the database, you need to run the `init_db.py` script. This script will create the necessary tables in your PostgreSQL database.

### Running `init_db.py`

1. **Ensure PostgreSQL is Running**: Make sure your PostgreSQL server is running and you have access to it.

2. **Run the Script**:
   ```bash
   python init_db.py --user <db_user> --password <db_password> --host <db_host> --port <db_port> --db <db_name>
   ```

   Replace `<db_user>`, `<db_password>`, `<db_host>`, `<db_port>`, and `<db_name>` with your actual database credentials.

3. **Expected Output**: The script will print messages indicating whether each table was created successfully or already exists.

## Data Import

The `data_importer.py` script is used to import data from various file formats into the database. It processes files such as JSON, YAML, CSV, and XML, and inserts the data into the corresponding tables.

### What `data_importer.py` Does

- **Reads Data**: The script reads data from the following files:
  - `people.json` and `people.yml` for client information.
  - `transfers.csv` for fund transfer records.
  - `transactions.xml` for transaction details.
  - `promotions.csv` for promotional data.

- **Parses and Inserts Data**: It parses the data from these files and inserts it into the respective tables in the database:
  - `Person` table for client data.
  - `Transfer` table for transfer records.
  - `Transaction` and `Item` tables for transaction details and associated items.
  - `Promotion` table for promotional data.

- **Error Handling**: The script includes error handling to manage issues during data import, such as missing files or database connection errors.

- **File Management**: After processing, the script moves each file to a `data/processed` directory to prevent re-importing.

### Running `data_importer.py`

1. **Run the Script**:
   ```bash
   python data_importer.py <directory> --user <db_user> --password <db_password> --host <db_host> --port <db_port> --db <db_name>
   ```

   Replace `<directory>` with the path to the directory containing your data files.

