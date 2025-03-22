# Venmito-ControlYourPotatoes

A comprehensive financial data platform featuring a complete data pipeline, robust API, and elegant dark-themed UI dashboard for financial transaction visualization and analysis.

![Venmito Dashboard](https://via.placeholder.com/800x400?text=Venmito+Dashboard)

## ✨ Features

- **Complete Data Pipeline**: Process and transform data from multiple sources (JSON, YAML, CSV, XML)
- **RESTful API**: Access all data through a well-structured API with comprehensive endpoints
- **Elegant Web Dashboard**: Modern dark-themed UI for powerful data visualization
- **Advanced Analytics**: In-depth analysis of user behaviors, spending patterns, and financial trends
- **Responsive Design**: Full mobile and desktop compatibility

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Node.js 14+ (for frontend development)

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/Venmito-ControlYourPotatoes.git
cd Venmito-ControlYourPotatoes
```

2. Set up the Python environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables

Create a `.env` file in the project root:

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

4. Initialize the database

```bash
flask init-db
```

5. Start the application

```bash
flask run
```

The web interface will be available at `http://localhost:5000` and the API at `http://localhost:5000/api`.

## 🔄 Data Pipeline

The data pipeline handles the complete ETL (Extract, Transform, Load) process:

### Data Loading
- Support for multiple file formats (JSON, YAML, CSV, XML)
- Extensible loader framework for custom data sources
- Robust error handling and reporting

### Data Validation
- Schema validation for all data sources
- Format verification for critical fields (emails, phone numbers, etc.)
- Consistency checks across related data

### Data Processing
- Standardization of data formats (names, locations, dates)
- Entity resolution and deduplication
- Field transformation and normalization

### Data Merging
- Entity relationship management
- Cross-source data integration
- Analytical aggregation for reporting

## 🌐 API Endpoints

The API provides complete access to all data and analytics functionality:

### User Data
- `GET /api/people` - List all users
- `GET /api/people/{user_id}` - Get user details
- `POST /api/people` - Create new user
- `PUT /api/people/{user_id}` - Update user
- `DELETE /api/people/{user_id}` - Delete user

### Financial Transactions
- `GET /api/transfers` - List transfers
- `GET /api/transfers/{transfer_id}` - Get transfer details
- `POST /api/transfers` - Create transfer
- `GET /api/transfers/user/{user_id}/summary` - Get user transfer summary
- `GET /api/transfers/user/{user_id}/contacts` - Get user contacts

### Purchase Transactions
- `GET /api/transactions` - List transactions
- `GET /api/transactions/{transaction_id}` - Get transaction details
- `GET /api/transactions/user/{user_id}/summary` - Get user transaction summary
- `GET /api/transactions/items/summary` - Get items summary
- `GET /api/transactions/stores/summary` - Get stores summary

### Analytics
- `GET /api/analytics/transactions/daily` - Get daily transaction trends
- `GET /api/analytics/transfers/daily` - Get daily transfer trends
- `GET /api/analytics/users/top-spending` - Get top spenders
- `GET /api/analytics/users/spending-distribution` - Get spending distribution
- `GET /api/analytics/dashboard` - Get complete analytics summary

## 🎨 Web Dashboard

The dashboard provides intuitive visualization of all data:

### Dashboard Pages
- **Home**: Overview with key metrics and recent activity
- **People**: User management and profiles
- **Transfers**: Money transfer tracking and analysis
- **Transactions**: Purchase transaction monitoring
- **Analytics**: In-depth data visualization and reporting

### Visualization Features
- Interactive charts and graphs
- Geographic data mapping
- Temporal trend analysis
- User behavior patterns
- Financial flow visualization

### Theme Features
- Modern dark theme with accent colors
- Responsive layout for all devices
- Consistent chart styling
- Data-dense information display
- Accessibility-compliant design

## 🧪 Testing

Run the test suite to ensure all components are working correctly:

```bash
# Run all tests
pytest

# Test with coverage
pytest --cov=src

# Test specific components
pytest tests/test_data/
pytest tests/test_api/
```

## 🛠️ Development

### Project Structure

```
venmito-controlwourpotatoes/
│
├── data/                      # Raw and processed data
│   ├── raw/                   # Original source files
│   └── processed/             # Processed data files
│
├── src/                       # Source code
│   ├── data/                  # Data pipeline
│   │   ├── loader.py          # Data loading components
│   │   ├── validator.py       # Data validation logic
│   │   ├── processor.py       # Data processing transformations
│   │   └── merger.py          # Data merging operations
│   │
│   ├── models/                # Data models
│   │   ├── people.py          # User models
│   │   ├── promotions.py      # Promotion models
│   │   └── transfers.py       # Transfer models
│   │
│   ├── analytics/             # Analytics logic
│   │   ├── user_analytics.py  # User-focused analytics
│   │   └── business_analytics.py  # Business metrics
│   │
│   └── api/                   # API implementation
│       ├── routes.py          # API route definitions
│       └── controllers/       # API controllers
│
├── static/                    # Web assets
│   ├── css/                   # CSS stylesheets
│   │   └── dark-theme.css     # Dark theme styles
│   ├── js/                    # JavaScript files
│   └── images/                # Image assets
│
├── templates/                 # HTML templates
│   ├── layout.html            # Base template
│   ├── index.html             # Dashboard homepage
│   └── analytics.html         # Analytics page
│
├── tests/                     # Test suite
│   ├── test_data/             # Data pipeline tests
│   ├── test_api/              # API tests
│   └── test_web/              # Web interface tests
│
├── app.py                     # Application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Extending the Platform

The modular architecture allows for easy extension:

1. **Adding data sources**: Extend the `BaseLoader` class in `loader.py`
2. **Custom analytics**: Add new functions to the analytics modules
3. **New API endpoints**: Define routes in `routes.py` and implement controllers
4. **UI components**: Add to the templates and static assets

## 📊 Example Usage

### API Example: Get User Summary

```bash
curl -X GET http://localhost:5000/api/people/1
```

Response:
```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "city": "new york",
  "country": "usa",
  "devices": "iPhone",
  "phone": "+1234567890"
}
```

### Data Pipeline Usage

```python
from src.data.loader import load_file
from src.data.validator import validate_dataframe
from src.data.processor import process_dataframe
from src.data.merger import PeopleMerger

# Load people data from different sources
people_json = load_file('data/raw/people.json')
people_yml = load_file('data/raw/people.yml')

# Validate the loaded data
validation_errors = validate_dataframe(people_json, 'people')
if validation_errors:
    print(f"Validation errors: {validation_errors}")

# Process the data
processed_json = process_dataframe(people_json, 'people')
processed_yml = process_dataframe(people_yml, 'people')

# Merge the processed data
people_merger = PeopleMerger(processed_json, processed_yml)
merged_data = people_merger.merge()

# Access the merged data
people_data = merged_data['people']
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Pandas](https://pandas.pydata.org/) - Data processing
- [Chart.js](https://www.chartjs.org/) - Data visualization
- [Bootstrap](https://getbootstrap.com/) - UI framework

Alexander Puga -  pugadev@gmail.com