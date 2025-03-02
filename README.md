# Venmito Data Engineering Project

## 📌 Project Overview
Venmito is a **payment processing company** that allows users to **transfer funds, make purchases at partner stores, and receive promotions**. This project is a **data engineering solution** that:

- **Ingests** multiple data sources (JSON, YAML, CSV, XML)
- **Cleans and standardizes** data into a structured **SQLite database**
- **Exposes an API** (FastAPI) for developers to query the data
- **Provides reporting & analysis** via Jupyter Notebooks
- **Runs everything automatically** when executing `main.py` (NOTE:If you ctrl + c to kill server and want to run again, delete database file and re-run main.py)

---

## 🛠️ Technologies Used
- **Python** (Primary programming language)
- **FastAPI** (API development)
- **SQLite** (Database storage)
- **Pandas** (Data processing & ingestion)
- **Jupyter Notebook** (Data analysis & visualization)
- **Uvicorn** (FastAPI server)

---

## 📥 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone <repo_url>
cd Venmito--ChrisGuzman94-
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Project**
Simply execute **`main.py`**, which will:
1. **Set up the database** (runs `setup_db.py`)
2. **Run ingestion scripts** (populates SQLite with data)
3. **Start the FastAPI server**
4. **Launch the Jupyter Notebook server**

```bash
python main.py
```

---

## 📁 Project Structure
```bash
📦 Venmito
├── 📂 data              # Raw data files
├── 📂 notebooks         # Jupyter Notebooks for analysis
├── 📂 src
│   ├── 📂 api          # API endpoints
│   ├── 📂 database     # Database setup & schema
│   ├── 📂 ingestions   # Data ingestion scripts
├── 📂 venv             # Virtual environment
├── main.py             # Main execution script
├── requirements.txt    # Python dependencies
├── server.py           # API server runner
├── README.md           # Documentation
```

---

## API Endpoints
### People API (`/people`)
- `GET /people` - Retrieve a list of people (filterable by email, phone, city, country, with a limit parameter).
- `GET /people/device_counts` - Get the total count of each device type used.
- `GET /people/{id}` - Fetch details of a specific person.
- `POST /people` - Create a new person entry (requires either email or phone).

### Promotions API (`/promotions`)
- `GET /promotions` - Retrieve promotions data (filterable by email, type, response status, with a limit parameter).
- `GET /promotions/most_popular` - Retrieve all promotions sorted by popularity, highlighting the top 5.
- `GET /promotions/{promotion_id}` - Fetch details of a specific promotion.
- `POST /promotions` - Create a new promotion entry.

### Transactions API (`/transactions`)
- `GET /transactions` - Retrieve transaction data, including items (filterable by phone, store, with a limit parameter).
- `GET /transactions/items_summary` - Show total quantity sold and revenue per item.
- `GET /transactions/{transaction_id}` - Fetch a specific transaction with its associated items.
- `POST /transactions` - Create a new transaction, optionally including items.

### Transfers API (`/transfers`)
- `GET /transfers` - Retrieve all transfers (optional limit parameter).
- `GET /transfers/{id}` - Fetch all transfers related to a specific user (as sender or recipient).
- `POST /transfers` - Create a new transfer record.

## How to Access the API
- The FastAPI Swagger UI can be accessed at:
  ```
  http://127.0.0.1:8000/docs
  ```
- You can test API requests using **cURL**, **Postman**, or directly through the Swagger UI.

---

## 📊 Data Analysis (Jupyter Notebooks)
To analyze data:
1. Run `main.py` (Jupyter starts automatically)
2. Open your browser and go to:
   ```bash
   http://localhost:8888
   ```
3. Open `Data_Analysis.ipynb` and explore:
   - **Device type distribution**
   - **Top-selling items**
   - **Transaction insights**
   - **Promotion effectiveness**

**There is a working example in the root folder, simply open Data_Analysis.html

---

## 👥 Contributors
- **Christopher J Guzman Laracuente**  
- **Email:** cj.guzman98@gmail.com  

---

## 📌 Notes
- Future improvements include **deploying the API**, **adding authentication**, and **automating data ingestion scheduling**.

