# Venmito Data Engineering Project

## Introduction

This project is designed to process and analyze data from various sources for Venmito, a payment company. The project involves setting up a database, importing data from multiple file formats, and providing insights into the data through a RESTful API.

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

### Running `data_importer.py`

1. **Run the Script**:
   ```bash
   python data_importer.py <directory> --user <db_user> --password <db_password> --host <db_host> --port <db_port> --db <db_name>
   ```

   Replace `<directory>` with the path to the directory containing your data files.

## API Endpoints

The API provides several endpoints to interact with the data. Below is a list of available endpoints, what they return, and the arguments they can take.

### Clients Endpoints

#### 1. Get Clients Promotions
- **Path**: `/clients/promotions`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches a list of clients along with their associated promotions.
- **Output**: 
  - `200 OK`: Returns a JSON array of objects, each containing:
    - `email`: The client's email.
    - `promotion`: The promotion associated with the client.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 2. Search Clients
- **Path**: `/clients/search`
- **Method**: `GET`
- **Parameters**: Query parameters to filter clients. At least one parameter is required.
  - `id`: Client ID
  - `first_name`: Client's first name
  - `last_name`: Client's last name
  - `telephone`: Client's telephone number
  - `email`: Client's email
  - `android`: Boolean indicating if the client uses an Android device
  - `desktop`: Boolean indicating if the client uses a desktop
  - `iphone`: Boolean indicating if the client uses an iPhone
  - `city`: Client's city
  - `country`: Client's country
- **Description**: Searches for clients based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON array of client objects matching the search criteria.
  - `400 Bad Request`: Returns an error message if no search parameters are provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 3. Count Clients
- **Path**: `/clients/count`
- **Method**: `GET`
- **Parameters**: Query parameters to filter clients. Optional.
  - `id`: Client ID
  - `first_name`: Client's first name
  - `last_name`: Client's last name
  - `telephone`: Client's telephone number
  - `email`: Client's email
  - `android`: Boolean indicating if the client uses an Android device
  - `desktop`: Boolean indicating if the client uses a desktop
  - `iphone`: Boolean indicating if the client uses an iPhone
  - `city`: Client's city
  - `country`: Client's country
- **Description**: Counts the number of clients based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON object with the count of clients.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

### Items Endpoints

#### 1. Search Items
- **Path**: `/items/search`
- **Method**: `GET`
- **Parameters**: Query parameters to filter items. At least one parameter is required.
  - `id`: Item ID
  - `transaction_id`: ID of the transaction the item is part of
  - `item_name`: Name of the item
  - `price`: Total price of the item
  - `price_per_item`: Price per individual item
  - `quantity`: Quantity of the item
- **Description**: Searches for items based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON array of item objects matching the search criteria.
  - `400 Bad Request`: Returns an error message if no search parameters are provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 2. Count Items
- **Path**: `/items/count`
- **Method**: `GET`
- **Parameters**: Query parameters to filter items. Optional.
  - `id`: Item ID
  - `transaction_id`: ID of the transaction the item is part of
  - `item_name`: Name of the item
  - `price`: Total price of the item
  - `price_per_item`: Price per individual item
  - `quantity`: Quantity of the item
- **Description**: Counts the number of items based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON object with the count of items.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 3. Aggregate Items
- **Path**: `/items/aggregation`
- **Method**: `GET`
- **Parameters**: 
  - `type`: The type of aggregation to perform (`min`, `max`, `sum`, `avg`)
- **Description**: Performs an aggregation operation on the item prices.
- **Output**: 
  - `200 OK`: Returns a JSON object with the result of the aggregation.
  - `400 Bad Request`: Returns an error message if an invalid aggregation type is provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 4. Best and Worst Seller
- **Path**: `/items/best_worst_seller`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches the best and worst selling items based on quantity.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the best and worst selling items.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 5. Item Summary
- **Path**: `/items/summary`
- **Method**: `GET`
- **Parameters**: 
  - `item_name`: (Optional) Name of the item to get a summary for
- **Description**: Provides a summary of items, including total quantity and total price.
- **Output**: 
  - `200 OK`: Returns a JSON object with the summary of the specified item or all items if no name is provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

### Promotions Endpoints

#### 1. Search Promotions
- **Path**: `/promotions/search`
- **Method**: `GET`
- **Parameters**: Query parameters to filter promotions. At least one parameter is required.
  - `id`: Promotion ID
  - `client_email`: Email of the client associated with the promotion
  - `telephone`: Telephone number of the client
  - `promotion`: Promotion details
  - `responded`: Boolean indicating if the client responded to the promotion
- **Description**: Searches for promotions based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON array of promotion objects matching the search criteria.
  - `400 Bad Request`: Returns an error message if no search parameters are provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 2. Search Promotions by Person
- **Path**: `/promotions/search/person`
- **Method**: `GET`
- **Parameters**: Query parameters to filter promotions by person attributes. At least one parameter is required.
  - `id`: Person ID
  - `first_name`: Person's first name
  - `last_name`: Person's last name
  - `telephone`: Person's telephone number
  - `email`: Person's email
  - `android`: Boolean indicating if the person uses an Android device
  - `desktop`: Boolean indicating if the person uses a desktop
  - `iphone`: Boolean indicating if the person uses an iPhone
  - `city`: Person's city
  - `country`: Person's country
- **Description**: Searches for promotions by person attributes.
- **Output**: 
  - `200 OK`: Returns a JSON array of promotions with person details.
  - `400 Bad Request`: Returns an error message if no person attributes are provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 3. Count Promotions
- **Path**: `/promotions/count`
- **Method**: `GET`
- **Parameters**: Query parameters to filter promotions. Optional.
  - `id`: Promotion ID
  - `client_email`: Email of the client associated with the promotion
  - `telephone`: Telephone number of the client
  - `promotion`: Promotion details
  - `responded`: Boolean indicating if the client responded to the promotion
- **Description**: Counts the number of promotions based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON object with the count of promotions.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 4. Responded Promotions Max/Min
- **Path**: `/promotions/responded/max_min`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches the promotion with the maximum and minimum number of responses.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the promotions with the most and least responses.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 5. Responded Promotions by City Max/Min
- **Path**: `/promotions/responded/city/max_min`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches the city with the maximum and minimum number of responses to promotions.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the cities with the most and least responses.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 6. Responded Promotions by Device Max/Min
- **Path**: `/promotions/responded/device/max_min`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches the device type with the highest and lowest number of responses to promotions.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the devices with the most and least responses.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

### Stores Endpoints

#### 1. Store Profit
- **Path**: `/stores/profit`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches the store with the most and least profit.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the store with the highest and lowest total profit.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 2. Store Profit List
- **Path**: `/stores/profit/list`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches a list of all stores and their total profits.
- **Output**: 
  - `200 OK`: Returns a JSON array of stores with their total profits.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 3. Store Quantity
- **Path**: `/stores/quantity`
- **Method**: `GET`
- **Parameters**: 
  - `store`: (Optional) Name of the store to get quantity details for
- **Description**: Fetches a list of all stores and their total quantities sold, or details for a specific store if provided.
- **Output**: 
  - `200 OK`: Returns a JSON array of stores with their total quantities, or a JSON object for a specific store.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 4. Store Quantity Max/Min
- **Path**: `/stores/quantity/max_min`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches the store with the maximum and minimum quantity sold.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the store with the highest and lowest total quantity sold.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 5. Search Stores
- **Path**: `/stores/search`
- **Method**: `GET`
- **Parameters**: 
  - `store`: (Optional) Name of the store to search for
- **Description**: Searches for stores and provides their total profit and quantity details.
- **Output**: 
  - `200 OK`: Returns a JSON array of stores with their total profit and quantity, or a JSON object for a specific store.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

### Transactions Endpoints

#### 1. Search Transactions
- **Path**: `/transactions/search`
- **Method**: `GET`
- **Parameters**: Query parameters to filter transactions. At least one parameter is required.
  - `id`: Transaction ID
  - `phone`: Phone number associated with the transaction
  - `store`: Store where the transaction took place
- **Description**: Searches for transactions based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON array of transaction objects matching the search criteria.
  - `400 Bad Request`: Returns an error message if no search parameters are provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 2. Count Transactions
- **Path**: `/transactions/count`
- **Method**: `GET`
- **Parameters**: Query parameters to filter transactions. Optional.
  - `id`: Transaction ID
  - `phone`: Phone number associated with the transaction
  - `store`: Store where the transaction took place
- **Description**: Counts the number of transactions based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON object with the count of transactions.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 3. Transaction Aggregation
- **Path**: `/transactions/aggregation`
- **Method**: `GET`
- **Parameters**: 
  - `type`: The type of aggregation to perform (`min`, `max`, `sum`, `avg`)
- **Description**: Performs an aggregation operation on the transaction amounts.
- **Output**: 
  - `200 OK`: Returns a JSON object with the result of the aggregation.
  - `400 Bad Request`: Returns an error message if an invalid aggregation type is provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 4. Transaction Summary
- **Path**: `/transactions/summary`
- **Method**: `GET`
- **Parameters**: 
  - `store`: (Optional) Name of the store to get a summary for
- **Description**: Provides a summary of transactions, including total amount and count.
- **Output**: 
  - `200 OK`: Returns a JSON object with the summary of the specified store or all stores if no name is provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

### Transfers Endpoints

#### 1. Search Transfers
- **Path**: `/transfers/search`
- **Method**: `GET`
- **Parameters**: Query parameters to filter transfers. At least one parameter is required.
  - `id`: Transfer ID
  - `sender_id`: ID of the sender
  - `recipient_id`: ID of the recipient
  - `amount`: Amount transferred
  - `date`: Date of the transfer
- **Description**: Searches for transfers based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON array of transfer objects matching the search criteria.
  - `400 Bad Request`: Returns an error message if no search parameters are provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 2. Count Transfers
- **Path**: `/transfers/count`
- **Method**: `GET`
- **Parameters**: Query parameters to filter transfers. Optional.
  - `id`: Transfer ID
  - `sender_id`: ID of the sender
  - `recipient_id`: ID of the recipient
  - `amount`: Amount transferred
  - `date`: Date of the transfer
- **Description**: Counts the number of transfers based on the provided query parameters.
- **Output**: 
  - `200 OK`: Returns a JSON object with the count of transfers.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 3. Max/Min Transferred by Person
- **Path**: `/transfers/max_min`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Fetches the person with the maximum and minimum amount of money transferred.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the person with the most and least money transferred.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 4. List Person Transferred
- **Path**: `/transfers/list`
- **Method**: `GET`
- **Parameters**: None
- **Description**: Lists all persons with their total transferred amounts.
- **Output**: 
  - `200 OK`: Returns a JSON array of persons with their total transferred amounts.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 5. Search Person Transfers
- **Path**: `/transfers/amount/search`
- **Method**: `GET`
- **Parameters**: Query parameters to filter transfers by person attributes. At least one parameter is required.
  - `id`: Person ID
  - `first_name`: Person's first name
  - `last_name`: Person's last name
  - `telephone`: Person's telephone number
  - `email`: Person's email
  - `city`: Person's city
  - `country`: Person's country
- **Description**: Searches for transfers by person attributes.
- **Output**: 
  - `200 OK`: Returns a JSON array of transfers with person details.
  - `400 Bad Request`: Returns an error message if no person attributes are provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 6. Total Transferred by Device
- **Path**: `/transfers/device/total`
- **Method**: `GET`
- **Parameters**: 
  - `device`: The type of device (`android`, `desktop`, `iphone`)
- **Description**: Calculates the total amount transferred by users of a specific device type.
- **Output**: 
  - `200 OK`: Returns a JSON object with the total amount transferred by the specified device type.
  - `400 Bad Request`: Returns an error message if an invalid device type is provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

#### 7. Max/Min Transferred by Device
- **Path**: `/transfers/device/max_min`
- **Method**: `GET`
- **Parameters**: 
  - `device`: The type of device (`android`, `desktop`, `iphone`)
- **Description**: Fetches the person with the maximum and minimum amount of money transferred for a specific device type.
- **Output**: 
  - `200 OK`: Returns a JSON object with details of the person with the most and least money transferred for the specified device type.
  - `400 Bad Request`: Returns an error message if an invalid device type is provided.
  - `500 Internal Server Error`: Returns an error message if the operation fails.

## Running the API

To run the API, execute the following command:

```bash
python venmito_api.py --user <db_user> --password <db_password> --host <db_host> --port <db_port> --db <db_name>
```

Replace `<db_user>`, `<db_password>`, `<db_host>`, `<db_port>`, and `<db_name>` with your actual database credentials.

## Conclusion

This project provides a comprehensive setup for processing, analyzing, and interacting with data for Venmito. The API endpoints offer a flexible way to query and visualize data insights.

