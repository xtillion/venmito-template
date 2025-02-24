# Venmito Data Engineering Project

## Author Information

- **Name:** José A. Megret Bonilla
- **Email:** megretjose@gmail.com
- **GitHub:** [JoseMegret](https://github.com/JoseMegret)

---

## Project Overview

The Venmito Data Engineering Project aims to consolidate and analyze disparate data files from Venmito—a payment company—to extract actionable insights about clients, transactions, transfers, and promotions. The solution involves:

- **Data Ingestion:** Reading data from multiple file formats (JSON, YAML, CSV, XML) and loading it into PostgreSQL.
- **Data Matching & Conforming:** Merging data from various sources to form a unified dataset.
- **Data Analysis & Visualization:** Aggregating and analyzing the data to understand:
  - Which clients received what type of promotion and how they responded.
  - Transaction trends, best-selling items, and store profitability.
  - Transfer patterns among clients (money sent vs. received).
- **Data Consumption Methods:**
  - **Non-Technical Team:** An static dashboard built with screenshots that uses Jupyter Notebook for graphs.
  - **Technical Team:** Jupyter Notebook with SQL queries and detailed data visualizations using Pandas and Plotly.

---

## Design Decisions

- **Data Ingestion & Processing:**  
  The solution uses Python with Pandas for its powerful data manipulation capabilities. We developed a modular script (`process_data.py`) that reads various file formats, transforms the data (e.g., converting device lists into boolean columns, flattening nested location data), and loads the consolidated data into a PostgreSQL database.
  
- **Database Choice:**  
  PostgreSQL was chosen for its reliability and support for diverse data types. The schema was designed to normalize clients, transactions, transaction items, transfers, and promotions, ensuring referential integrity and easy querying.

- **Visualization & Analysis:**  
  Data insights are presented using Plotly within Jupyter Notebooks. This approach allows for interactive, high-quality visualizations that can be easily shared and modified by both technical and non-technical teams.

- **Deployment:**  
  Docker and Docker Compose are used to containerize the solution, ensuring consistent environments for development, testing, and production. This setup simplifies dependency management and deployment.

- **Consumption Methods:**  
  - **For Non-Technical Users:** An  offers a user-friendly interface.
  - **For Technical Users:** Jupyter Notebooks provide in-depth analysis and SQL query capabilities for further exploration.

---

## Installation & Running the Project

### Prerequisites

- **Python 3.9+**
- **Docker & Docker Compose** (if using containerized deployment)
- **Git**

### 1. Clone the Repository

git clone https://github.com/JoseMegret/Venmito-JoseMegret.git
cd Venmito-JoseMegret

## 2. Setting up the Environment

### Option A: Using Docker

1. **Build and Run the Containers:**

   docker-compose up --build
This command will start:
	•	A PostgreSQL container (venmito_db) with the initialized schema.
	•	A processing container (venmito_processing) that ingests and loads the data.
	•	A UI container (venmito_ui) that runs a Jupyter Notebook server for analysis and (if configured) a Streamlit dashboard.

2.	**Access the Jupyter Notebook:
    Open your browser and navigate to:
    http://127.0.0.1:8888/lab

### Option B: Running Locally

1.	Set up a Virtual Environment:
    python3 -m venv env
    source env/bin/activate   # For Windows: env\Scripts\activate

2.	Install Dependencies:
    pip install -r requirements.txt

3.	Configure PostgreSQL:
    Ensure that PostgreSQL is running on your machine. Update the DATABASE_URL in the code if necessary.    

4.	Run the Data Processing Script:
    python processing/process_data.py

5.	Start the Jupyter Notebook:
    jupyter notebook
    Then, open your notebook for data analysis.


4. Data Consumption Methods
	•	For Technical Users: Jupyter Notebooks
Jupyter Notebooks provide in-depth analysis, SQL query capabilities, and detailed visualizations using Pandas and Plotly. Technical users can modify and run custom queries as needed.
How to Access the Notebook:
	•	Using Docker:
Run:
    docker-compose up --build
Then open your browser at:
    http://127.0.0.1:8888/lab

•	Locally:
After setting up your environment and installing dependencies, run:
    jupyter notebook

## 5. Final Remarks & Future Improvements

•	Insights:
This project extracts actionable insights such as:
	•	Which clients received which types of promotions and how they responded.
	•	Best-selling items and store profitability.
	•	Transfer trends between clients, including net transfers and monthly patterns.
•	Future Work:
	•	Real-time Data Processing: Integrate with tools like Apache Kafka or Spark Streaming for real-time analytics.
	•	Enhanced Dashboards: Expand the interactive dashboard with additional filters and drill-down capabilities.
	•	Further Analysis: Explore additional insights such as fraud detection and personalized recommendations.  

### Acknowledgements on Interactive Dashboard

While the initial project plan included building an interactive dashboard using Streamlit to provide a user-friendly interface for non-technical users, time constraints prevented me from developing a fully polished dashboard. Instead, I have focused on creating comprehensive data analyses and visualizations within Jupyter Notebooks. This approach ensures that all key insights are accessible and well-documented.

In future iterations, I plan to integrate a dedicated Streamlit dashboard that will:
- Offer an intuitive and interactive user interface.
- Provide real-time filtering and drill-down capabilities.
- Enhance data presentation for non-technical stakeholders.

For now, non-technical users can view the detailed analyses and interactive visualizations by accessing the Jupyter Notebook export (HTML or PDF), which has been carefully styled for clarity.

Thank you for your understanding!
 
