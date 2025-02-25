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
  - **Non-Technical Team:** The initial plan included an interactive dashboard built with Streamlit to provide a user-friendly interface. Due to time constraints, the final deliverable presents comprehensive analysis and visualizations via Jupyter Notebooks (accompanied by high-quality screenshots) as an alternative.
  - **Technical Team:** Jupyter Notebooks offer in-depth analysis, SQL query capabilities, and interactive visualizations using Pandas and Plotly.
---

## Design Decisions

- **Data Ingestion & Processing:**  
  The solution uses Python and Pandas for robust data manipulation. A modular script (processing/process_data.py) reads various file formats, transforms the data (e.g., converting device lists into boolean columns, flattening nested location data), and loads the consolidated data into a PostgreSQL database.
  
- **Database Choice:**  
  PostgreSQL was selected for its reliability and robust support for diverse data types. The schema was designed to normalize clients, transactions, transaction items, transfers, and promotions—ensuring referential integrity and simplifying queries.
  
- **Visualization & Analysis:**  
  Interactive visualizations are generated using Plotly within Jupyter Notebooks. This allows for high-quality, dynamic charts that can be tailored by technical users while still being accessible to non-technical stakeholders through static exports or screenshots.

- **Deployment:**  
  Docker and Docker Compose are used to containerize the solution, ensuring consistent environments for development, testing, and production. This setup simplifies dependency management and deployment.

- **Consumption Methods:**  
  - **For Non-Technical Users:** Although a Streamlit dashboard was initially planned for an interactive user interface, time constraints led to delivering detailed analysis via Jupyter Notebooks along with visual exports. Future iterations may include a dedicated Streamlit dashboard.
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


		venmito_ui    | [I 2025-02-24 22:14:54.989 ServerApp] Serving notebooks from local directory: /home/jovyan
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

3. **Stopping the Containers:**

When you are finished, stop all containers by pressing Ctrl+C in your terminal or by running:

	docker-compose down

## 3. Data Consumption Methods
   
	•	For Technical Users: Jupyter Notebooks

		Jupyter Notebooks provide in-depth analysis, SQL query capabilities, and detailed visualizations using Pandas and Plotly. Technical users can modify and run custom queries as needed.

	•	For Non-Technical Users: Static Dashboard Exports

	Although a fully interactive Streamlit dashboard was planned, due to time constraints, key insights are presented via Jupyter Notebook visualizations and exported screenshots. These static exports are available in the Charts folder and offer a user-friendly overview of the analysis.

## 4. Final Remarks & Future Improvements

•	Insights:
This project extracts actionable insights such as:

	•	Which clients received which types of promotions and how they responded.
	•	Best-selling items and store profitability.
	•	Transfer trends between clients, including net transfers and monthly patterns.
•	Future Work:

	•	Enhanced Dashboards: Expand the interactive dashboard with additional filters and drill-down capabilities.
	•	Further Analysis: Explore additional insights such as fraud detection and personalized recommendations.  

## Acknowledgements on Interactive Dashboard

While the initial project plan included building an interactive dashboard using Streamlit to provide a user-friendly interface for non-technical users, time constraints prevented me from developing a fully polished dashboard. Instead, I have focused on creating comprehensive data analyses and visualizations within Jupyter Notebooks. This approach ensures that all key insights are accessible and well-documented.

In future iterations, I plan to integrate a dedicated Streamlit dashboard that will:
- Offer an intuitive and interactive user interface.
- Provide real-time filtering and drill-down capabilities.
- Enhance data presentation for non-technical stakeholders.

For now, non-technical users can view the detailed analyses and interactive visualizations by accessing the Charts folder where there are renditions of the Jupyter notebook's charts. 

Thank you for Reviewing This Project!
 
