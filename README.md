# Venmito Data Engineering Project

## Author
**Sebastian Soto Vazquez**  
**GitHub:** [soto2571](https://github.com/soto2571)  
**Email:** sebastian.soto1649@gmail.com  

## Introduction

Welcome to the Venmito Data Engineering project! This project is designed to process, clean, and analyze transaction and client data for Venmito, a payment company that enables users to transfer funds and make purchases in partner stores. The goal of this project is to extract meaningful insights from disparate data sources and present them in an accessible way for both technical and non-technical users.

## Project Overview

The project involves working with five different data files in various formats:
- `people.json` - Contains client information
- `people.yml` - Another source of client data
- `transfers.csv` - Transfer records between users
- `transactions.xml` - Transaction records with item-level details
- `promotions.csv` - Promotion offers and responses

### **Objectives:**
1. **Data Ingestion**: Load and standardize data from multiple formats (JSON, YAML, CSV, XML).
2. **Data Matching and Conforming**: Merge and clean data into a unified dataset stored in an SQLite database.
3. **Data Analysis**: Generate insights into promotions, store profitability, customer spending, and more.
4. **Data Output**: Provide an API and a dashboard for data visualization.
5. **Code Quality**: Ensure well-structured, documented, and maintainable code.

---

## **Setup Instructions**

### **1. Clone the Repository**
```sh
 git clone https://github.com/soto2571/Venmito-soto2571
 cd Venmito-soto2571/
```

### **2. Create a Virtual Environment and Install Dependencies**
```sh
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

### **3. Run the Project**
```sh
python app.py
```
The application will be accessible at `http://127.0.0.1:5000`.

---

## **API Endpoints**
The application provides a RESTful API to access analyzed data.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/clients/promotions` | GET | Get clients and their promotions |
| `/stores/top` | GET | Get the top-performing stores |
| `/stores/sales` | GET | Get monthly sales data |
| `/clients/top-transfers` | GET | Get top clients by transfer amount |
| `/earnings/avg-transaction` | GET | Get average transaction value |
| `/earnings/data` | GET | Get financial data per store |

---

## **Data Analysis Features**
The project extracts valuable insights from the provided data:
- **Client Promotions Analysis:** Determines which clients participated in promotions and suggests improvements.
- **Store Performance:** Identifies the most profitable stores and their revenue trends.
- **Transaction Trends:** Displays financial metrics such as average transaction value, highest transactions, and top customers.

---

## **Graphical Dashboard**
A front-end dashboard provides a **visual representation** of financial and transactional insights. Features include:
- **Sales Trends (Last 12 Months)**
- **Top Store Revenues**
- **Promotion Effectiveness**
- **Customer Insights**

### **How to Access the Dashboard?**
Simply visit `http://127.0.0.1:5000` in your browser after running `app.py`.

---

## **Technologies Used**
- **Backend:** Flask, Pandas, SQLite
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Data Processing:** Pandas for cleaning, merging, and analyzing data
- **Database:** SQLite for data storage and querying

---

## **Data Persistence**
The project stores the cleaned data in an SQLite database, allowing structured queries and efficient data retrieval. The database schema includes:
- **Clients Table**: Stores client information.


---

## **Final Notes**
This project successfully integrates multi-format data sources, cleans and processes data efficiently, and provides insightful analytics via an API and dashboard. It meets both technical and non-technical requirements, allowing seamless data exploration.

For any questions or further improvements, feel free to reach out!

---

## **License**
This project and its contents are the exclusive property of Xtillion, LLC and are intended solely for evaluation purposes. Unauthorized distribution, reproduction, or usage is strictly prohibited.
