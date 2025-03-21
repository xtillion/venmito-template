# Venmito API

A RESTful API for the Venmito financial data pipeline, providing access to user data, transfers, transactions, and analytics.

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL

### Installation

1. Clone the repository

```
git clone https://github.com/yourusername/venmito.git
cd venmito
```

2. Create a virtual environment and install dependencies

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables

Create a `.env` file in the project root with the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
DB_NAME=venmito
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. Run the application

```
flask run
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### People/Users

- `GET /api/people` - Get all users
- `GET /api/people/{user_id}` - Get user by ID
- `POST /api/people` - Create a new user
- `PUT /api/people/{user_id}` - Update a user
- `DELETE /api/people/{user_id}` - Delete a user

### Transfers

- `GET /api/transfers` - Get all transfers
- `GET /api/transfers/{transfer_id}` - Get transfer by ID
- `POST /api/transfers` - Create a new transfer
- `GET /api/transfers/user/{user_id}/summary` - Get transfer summary for a user
- `GET /api/transfers/user/{user_id}/contacts` - Get frequent contacts for a user

### Transactions

- `GET /api/transactions` - Get all transactions
- `GET /api/transactions/{transaction_id}` - Get transaction by ID
- `GET /api/transactions/user/{user_id}/summary` - Get transaction summary for a user
- `GET /api/transactions/items/summary` - Get items summary
- `GET /api/transactions/stores/summary` - Get stores summary

### Analytics

- `GET /api/analytics/transactions/daily` - Get daily transactions summary
- `GET /api/analytics/transfers/daily` - Get daily transfers summary
- `GET /api/analytics/users/top-spending` - Get top users by spending
- `GET /api/analytics/users/top-transfers` - Get top users by transfers
- `GET /api/analytics/items/monthly-popular` - Get popular items by month
- `GET /api/analytics/users/spending-distribution` - Get user spending distribution
- `GET /api/analytics/geographic/spending` - Get geographic spending summary
- `GET /api/analytics/transfers/amount-distribution` - Get transfer amount distribution
- `GET /api/analytics/dashboard` - Get comprehensive analytics dashboard

## Examples

### Get all users

```
GET /api/people?page=1&per_page=20&search=john
```

Response:

```json
{
  "data": [
    {
      "user_id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "city": "New York",
      "country": "USA",
      "devices": "iPhone",
      "phone": "+1234567890"
    }
  ],
  "pagination": {
    "total": 1,
    "per_page": 20,
    "current_page": 1,
    "total_pages": 1
  }
}
```

### Create a new transfer

```
POST /api/transfers
```

Request:

```json
{
  "sender_id": 1,
  "recipient_id": 2,
  "amount": 100.00
}
```

Response:

```json
{
  "transfer_id": 123,
  "sender_id": 1,
  "recipient_id": 2,
  "amount": 100.00,
  "timestamp": "2023-09-10T14:30:00"
}
```

## Development

### Project Structure

```
venmito/
│
├── app.py                     # Flask application entry point
├── config.py                  # Application configuration
├── requirements.txt           # Project dependencies
│
├── src/                       # Source code
│   ├── db/                    # Database configuration
│   │   └── config.py          # Database connection and utilities
│   │
│   ├── api/                   # API modules
│   │   ├── routes.py          # API route definitions
│   │   │
│   │   ├── controllers/       # Request handling logic
│   │   │   ├── people_controller.py
│   │   │   ├── transfers_controller.py
│   │   │   ├── transactions_controller.py
│   │   │   └── analytics_controller.py
│   │   │
│   │   └── queries/           # Database queries
│   │       ├── people_queries.py
│   │       ├── transfers_queries.py
│   │       ├── transactions_queries.py
│   │       └── analytics_queries.py
│   │
│   └── ...                    # Other modules from the data pipeline
│
├── tests/                     # Test suite
│   ├── test_api/              # API tests
│   │   ├── test_people.py
│   │   ├── test_transfers.py
│   │   ├── test_transactions.py
│   │   └── test_analytics.py
│   │
│   └── ...                    # Other test modules
│
└── README.md                  # Project documentation
```

### Running Tests

```
pytest
```

For test coverage:

```
pytest --cov=src
```

## Data Pipeline

The API is built on top of the Venmito data pipeline, which includes:

- Data loading from various sources (JSON, YAML, CSV)
- Data validation for structure and content
- Data processing and transformation
- Data merging from different sources

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License.