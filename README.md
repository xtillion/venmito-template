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
  - **Non-Technical Team:** An interactive dashboard built with Streamlit provides a user-friendly, real-time interface to explore key insights.
  - **Technical Team:** Jupyter Notebooks offer in-depth analysis, SQL query capabilities, and interactive visualizations using Pandas and Plotly.
---

## Design Decisions

- **Data Ingestion & Processing:**  
  The solution uses Python and Pandas for robust data manipulation. A modular script (processing/process_data.py) reads various file formats, transforms the data (e.g., converting device lists into boolean columns, flattening nested location data), and loads the consolidated data into a PostgreSQL database.
  
- **Database Choice:**  
  PostgreSQL was selected for its reliability and robust support for diverse data types. The schema was designed to normalize clients, transactions, transaction items, transfers, and promotions—ensuring referential integrity and simplifying queries.
  
- **Visualization & Analysis:**  
  Data insights are presented using Plotly within Jupyter Notebooks and through an interactive dashboard built with Streamlit. This dual approach allows non-technical users to explore the data in a user-friendly interface while technical users can dive deeper using notebooks.

- **Deployment:**  
  Docker and Docker Compose are used to containerize the solution, ensuring consistent environments for development, testing, and production. This setup simplifies dependency management and deployment.

- **Consumption Methods:**  
  - **For Non-Technical Users:** The interactive Streamlit dashboard (accessible via a web browser) provides real-time filtering, drill-down capabilities, and a polished look.
  - **For Technical Users:** Jupyter Notebooks provide the flexibility to modify queries, perform ad-hoc analysis, and interact with the data using SQL queries, Pandas, and Plotly.

---

## Installation & Running the Project

### Prerequisites

- **Python 3.9+**
- **Docker & Docker Compose** (for containerized deployment)
- **Git**

## 1. Clone the Repository

	git clone https://github.com/JoseMegret/Venmito-JoseMegret.git
	cd Venmito-JoseMegret

## 2. Setting up the Environment

### Using Docker

1. **Build and Run the Containers:**

 Run:
 		
   	docker-compose up --build
   
This command will start:

	•	A PostgreSQL container (venmito_db) with the initialized schema.
	•	A processing container (venmito_processing) that ingests and loads the data.
	•	A UI container (venmito_ui) that runs a Jupyter Notebook server for analysis and (if configured) a Streamlit dashboard.

2. **Access the Jupyter Notebook:**
   
Once the containers are running, check the logs of the UI container.

Run:
		
  	docker logs venmito_ui

You'll see output similar to:


		venmito_ui    | [I 2025-02-24 22:14:54.989 ServerApp] Jupyter Server 2.8.0 is running at:
		venmito_ui    | [I 2025-02-24 22:14:54.989 ServerApp] http://a464cc977bc0:8888/lab?token=4940e7bf...  👈
		venmito_ui    | [I 2025-02-24 22:14:54.989 ServerApp]  or http://127.0.0.1:8888/lab?token=4940e7bf... 👈
		venmito_ui    | [I 2025-02-24 22:14:54.990 ServerApp] Use Control-C to stop this server and shut down all kernels...

The important part is the URL (or token). You can open the notebook in your browser by navigating to one of the provided URLs (👈). 
For example:

	http://127.0.0.1:8888/lab?token=4940e7bf...
     
Steps to Access the Notebook:

	1.	Wait for the UI container logs to show the Jupyter Server URLs.
	2.	Copy the URL (which includes the token) from the logs.
	3.	Open your web browser and paste the URL.
	4.	You’ll be taken to the Jupyter Lab interface where you can explore the notebooks (e.g., analysis.ipynb).

If you ever lose the link, just check the Docker logs again or copy the token from the terminal output. Pressing Ctrl+C will stop the containers.

This approach ensures you have a running Jupyter environment with all the dependencies installed and configured automatically via Docker.

3. **Access the Interactive Dashboard:**

Once the containers are running, check the logs of the dashboard container.

Open your browser and navigate to:

	http://localhost:8501

### Or

Run:
		
  	docker logs venmito_dashboard

Where you'll see output similar to:

	You can now view your Streamlit app in your browser.

	  Local URL: http://localhost:8501         👈
	  Network URL: http://172.20.0.3:8501
	  External URL: http://70.45.176.121:8501

And Copy and Paste the "Local URL" in your web browser 

4. **Stopping the Containers:**

When you are finished, stop all containers by pressing Ctrl+C in your terminal or by running:

	docker-compose down

## 3. Data Consumption Methods
   
•	For Non-Technical Users:
		
  	The interactive dashboard built with Streamlit provides a user-friendly interface with real-time, drill-down visualizations. Simply navigate 	to http://localhost:8501 in your browser to interact with the dashboard.
	
 •	For Technical Users:
	
 	Jupyter Notebooks offer comprehensive analysis, detailed visualizations, and SQL query capabilities. Access the notebooks using the URL provided by the UI container logs.

## 4. Final Remarks & Future Improvements

•	Insights:
This project extracts actionable insights such as:

	•	Which clients received which types of promotions and how they responded.
	•	Best-selling items and store profitability.
	•	Transfer trends between clients, including net transfers and monthly patterns.

## Acknowledgements

This project showcases two complementary approaches for data consumption and analysis:

- **Jupyter Notebooks:**  
  In-depth analyses, SQL query capabilities, and interactive visualizations were developed in Jupyter Notebooks. This approach allows technical users to explore and modify the analysis in detail.

- **Streamlit Dashboard:**  
  An interactive dashboard built with Streamlit was also implemented to provide non-technical users with a user-friendly, real-time interface to explore key insights. This dashboard features dynamic filtering, drill-down capabilities, and visually appealing charts.

Both solutions were integrated into the project to ensure that stakeholders with different technical backgrounds can access and benefit from the insights derived from the data.

Thank you for Reviewing This Project!
 
