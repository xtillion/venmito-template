# Venmito Data Analysis Platform

**Production URL:** [https://production.d3eyfli6a43az4.amplifyapp.com/](https://production.d3eyfli6a43az4.amplifyapp.com/)

A sophisticated data analysis platform built for Venmito, designed to handle and analyze customer and transaction data. This project is divided into two main components: a Flask-based API backend and a React frontend (located in the `ui` folder).

---

## Author

- **Name:** Felix Dasta  
- **Email:** [felix.dasta@hotmail.com](mailto:felix.dasta@hotmail.com)

---

## Description

This platform is designed to efficiently manage and analyze data related to customers' transactions, promotions, and transfers. The backend, powered by Python, Flask, and Pandas, offers a suite of API endpoints for data retrieval, manipulation, and analysis. 

Processed data can be **stored persistently by clicking the "Save JSON" button in the frontend**, ensuring it is readily available for future reference and further analysis.

### Key Capabilities

- **Data Analysis:**  
  Uses Pandas for high-performance data manipulation and analysis.

- **API-Driven Architecture:**  
  Exposes dedicated endpoints for flexible integration with various front-end applications and external systems.

- **ETL Processes:**  
  Incorporates ETL (Extract, Transform, Load) routines to systematically process raw data—cleaning, transforming, and storing it in a consistent format.

- **Persistent Data Storage:**  
  Uses **JSON storage** via the "Save JSON" button in the frontend, allowing users to export processed data.

---

## Design Decisions

### API-Driven Architecture

The backend is organized around clear, purpose-built API endpoints that handle data requests and responses. This approach streamlines data processing and facilitates seamless integration with various customers and systems.

### Data Handling, ETL, and Persistence

- **ETL Processes:**  
  Raw data is extracted, transformed (using Pandas for data cleansing and manipulation), and loaded into JSON format, which can be saved via the frontend.

- **Use of Pandas:**  
  Employed for robust data manipulation, Pandas enables efficient processing of large datasets and detailed analytical operations.

- **Persistent Storage:**  
  Processed data can be **saved as JSON** by clicking the "Save JSON" button in the UI, ensuring its availability for future use, reporting, and further analysis.

---

## Technologies Used

- **Python 3.9:** Core programming language.
- **Flask:** Lightweight framework for creating API endpoints.
- **Pandas:** Library for data manipulation and analysis.
- **React:** Frontend framework located in the `ui` folder.
- **JSON Storage:** Used for persistent data storage via the UI's "Save JSON" button.
- **ETL Routines:** Integrated within the backend to handle data extraction, transformation, and loading.

---

## Setup Instructions

### Backend Setup

1. **Clone the Repository:**

   ```bash
   git clone git@github.com:xtillion/venmito-felixdasta.git
   cd [project directory]
   ```

2. **Ensure Python 3.9 is Installed**

3. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

   or

   ```bash
   python3 -m venv venv
   ```

4. **Activate the Virtual Environment:**

   - macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

   - Windows:

     ```bash
     .\venv\Scripts\activate
     ```

5. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Application:**

   ```bash
   python -m api.app
   ```

   or

   ```bash
   python3 -m api.app
   ```

7. **Deactivate the Virtual Environment (when finished):**

   ```bash
   deactivate
   ```

### Frontend Setup

1. **Clone the Repository (if not already done):**

   ```bash
   git clone git@github.com:xtillion/venmito-felixdasta.git
   cd [project directory]
   ```

2. **Navigate to the UI Folder:**

   ```bash
   cd ui
   ```

3. **Install Dependencies:**

   - Using npm:

     ```bash
     npm install
     ```

   - Using yarn:

     ```bash
     yarn install
     ```

4. **Start the Development Server:**

   - Using npm:

     ```bash
     npm start
     ```

   - Using yarn:

     ```bash
     yarn start
     ```

The application will launch and open in your default browser at `http://localhost:3000`.

---



---

## API Endpoints & Feature Access

### Customer Promotions

- **List of Customers with Their Promotions**  
  - **Endpoint:** `/people/promotions`  
  - **Method:** GET  
  - **Description:** Retrieves a list of all customers along with their associated promotions.

- **Customers for a Specific Promotion**  
  - **Endpoint:** `/people/promotions/<promotion>`  
  - **Method:** GET  
  - **Description:** Returns customers linked to a specific promotion. Replace `<promotion>` with the desired promotion type.

- **Accepted Promotions**  
  - **Endpoint:** `/people/promotions/accepted-promotions`  
  - **Method:** GET  
  - **Description:** Retrieves promotions that customers have accepted.

- **Denied Promotions**  
  - **Endpoint:** `/people/promotions/denied-promotions`  
  - **Method:** GET  
  - **Description:** Retrieves promotions that customers have rejected.

- **Promotion Improvement Suggestions**  
  - **Endpoint:** `/people/promotions/improvement-suggestions`  
  - **Method:** GET  
  - **Description:** Provides suggestions to improve customer responses for promotions.

- **Improvement Suggestions for a Specific Promotion**  
  - **Endpoint:** `/people/promotions/<promotion>/improvement-suggestions`  
  - **Method:** GET  
  - **Description:** Retrieves improvement suggestions for a specific promotion.

### Transaction Insights

- **All Transactions**  
  - **Endpoint:** `/transactions`  
  - **Method:** GET  
  - **Description:** Returns all recorded transactions.

- **Best Selling Item**  
  - **Endpoint:** `/transactions/best-selling-item`  
  - **Method:** GET  
  - **Description:** Returns the best-selling item across all stores.

- **Best Selling Store**  
  - **Endpoint:** `/transactions/best-selling-store`  
  - **Method:** GET  
  - **Description:** Identifies the store with the highest number of sales.

- **Most Profitable Store**  
  - **Endpoint:** `/transactions/most-profitable-store`  
  - **Method:** GET  
  - **Description:** Identifies the store generating the highest profit.

- **Profitability of Items**  
  - **Endpoint:** `/transactions/profitability-of-items`  
  - **Method:** GET  
  - **Description:** Analyzes and ranks items based on profitability.

- **Items Sold by Store**  
  - **Endpoint:** `/transactions/items-sold-by-store`  
  - **Method:** GET  
  - **Description:** Retrieves a breakdown of items sold per store.

### Store Data

- **People Associated with a Store**  
  - **Endpoint:** `/stores/<name>/people`  
  - **Method:** GET  
  - **Description:** Lists people associated with a specific store.

### Item Insights

- **Transactions for a Specific Item**  
  - **Endpoint:** `/items/<name>/transactions`  
  - **Method:** GET  
  - **Description:** Retrieves transactions associated with a specific item.

- **People Who Purchased a Specific Item**  
  - **Endpoint:** `/items/<name>/people/transactions`  
  - **Method:** GET  
  - **Description:** Lists people who have purchased a specific item.

### Customer Transactions & Transfers

- **Transactions by Customers**  
  - **Endpoint:** `/people/transactions`  
  - **Method:** GET  
  - **Description:** Retrieves transaction history for customers.

- **Transfers by Customers**  
  - **Endpoint:** `/people/transfers`  
  - **Method:** GET  
  - **Description:** Lists all transfers made by customers.





---

## Data Consumption Methods

### Non-Technical Team (Frontend)
Non-technical users can interact with the **Venmito Data Analysis Platform** through the **web-based UI** at:
[**Venmito Data Analysis Platform**](https://production.d3eyfli6a43az4.amplifyapp.com/)

- The frontend provides an **intuitive interface** to analyze customer transactions, promotions, and transfers.  
- Users can **visualize data** using charts, tables, and reports without needing technical expertise.  
- The **"Save JSON" button** allows users to export processed data for further use.  

### Technical Team (Backend & Local Development)
Technical users can **consume data programmatically** in the following ways:

1. **Using the Public API**  
   - Developers and data engineers can interact directly with the backend's API endpoints.  
   - The API is publicly available at:  
     [**Venmito API (Public URL)**](https://venmito.ddns.net/venmito-felixdasta)  
   - Refer to the **API Endpoints** section to determine which endpoints to use.  

2. **Running the Platform Locally**  
   - The platform can also be **installed and run locally** for testing and development.  
   - Follow the **Setup Instructions** to install the backend and frontend.  
   - This allows for a **sandbox environment** where developers can modify and test the system without affecting live data.  

By providing both a **web interface for non-technical users** and a **public API for technical teams**, the platform ensures **flexible and scalable data access** for different stakeholders.


## How to Use the UI

### Accessing the Platform
- Open the platform: [Venmito Data Analysis Platform](https://production.d3eyfli6a43az4.amplifyapp.com/).

### Interacting with the UI
- Use the navbar or input fields to filter the data you want to analyze.
- Clicking on **pie charts, bar charts, or table rows** often reveals additional insights.

### Important Features You Might Miss

#### Clicking on Charts Unlocks Extra Data
- Click **on a section of a pie chart or a bar in a bar chart** to see additional relevant data.
- This can reveal breakdowns, trends, and hidden insights.

#### Clicking on Table Rows Shows More Details
- Clicking a row may display deeper insights about that item, customer, or store.
- Try interacting with different parts of the UI to uncover more data.

### Saving Data
- Click **“Save JSON”** to store processed data for later use.

If something isn’t working, try clicking different elements—you might uncover hidden insights.

---

## Troubleshooting

### Not Seeing Extra Data?
- Try clicking on different parts of the graph or table.
- If nothing happens, it may not be interactive for that specific dataset.

### Need Fresh Data?
- Click **“Save JSON”** before leaving the page to extract the recently seen insights.

---

## Important Notice
**Warning:** The production URL [https://production.d3eyfli6a43az4.amplifyapp.com/](https://production.d3eyfli6a43az4.amplifyapp.com/) will be **decommissioned** once the project evaluation is complete.

