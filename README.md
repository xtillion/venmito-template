# Venmito Data Engineering Project
## By: Emilio E De Jesus Hernandez
**Email:** emilio.dejesus@upr.edu

---

# **Project Overview**
The Venmito Data Engineering Project is a data consolidation and analysis solution developed for Xtillion's client, Venmito. The goal of the project was to integrate data from multiple file formats (JSON, YAML, CSV, XML), unify and store them into a scalable format (SQLite database), and provide insights using a CLI and GUI interface.

---

## **Solution Description**
This solution processes fragmented client data and stores it in an SQLite database. It offers two data consumption methods:
1. **Command Line Interface (CLI)** – for technical users to query, analyze, and extract insights.
2. **Graphical User Interface (GUI)** – for non-technical users to interact with data visually.

### **Key Features**
- **Data Ingestion** – Load and parse data from JSON, YAML, CSV, and XML files.
- **Data Matching and Unification** – Merge data across files to resolve inconsistencies.
- **Data Storage** – Store consolidated data in an SQLite database.
- **Data Analysis** – Generate insights such as most valuable clients, most effective promotions, etc.
- **Data Output** – Present data through a CLI and GUI.

---

## **Design Decisions**
1. **SQLite** – Chosen for its lightweight nature and ease of use for local data storage.
2. **Pandas** – Used for efficient data manipulation and analysis.
3. **tkinter** – Used for the GUI due to its simplicity and compatibility with Python.
4. **Command Line Interface (CLI)** – Enables direct querying and insight extraction for advanced users.
5. **Normalization** – Ensured consistent data formats and resolved conflicts across files.

---

# **Project Structure**
```bash
VENMITO-EMILIODEJESUS/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── ingestion.py
│   ├── transformation.py
│   ├── analysis.py
│   ├── output.py
│   ├── gui.py
├── README.md
├── requirements.txt
├── data/
│   ├── people.json
│   ├── people.yml
│   ├── transfers.csv
│   ├── transactions.xml
│   ├── promotions.csv

🛠️ How to Set Up and Run the Project

    1. Clone the Repository:
        git clone https://github.com/emiliodejesus/venmito-emiliodejesus.git
        cd venmito-emiliodejesus.git

    2. Create and Activate Virtual Environment:
        python3 -m venv .venv
        source .venv/bin/activate

    3. Install Dependencies:
        pip install -r requirements.txt

    4. Run the Application:
        python3 -m src.main

📕 Use Instructions
    -> Choose Between CLI or GUI
        After running the project, you’ll be prompted to choose between the Command Line Interface (CLI) or the Graphical User Interface (GUI):
            CLI – Use the CLI for detailed analysis and direct database queries.
            GUI – Use the GUI for a more visual and interactive experience.

    -> CLI Instructions:
        If you select CLI, you'll see a menu of options. Just type the corresponding number and press Enter to get the analysis or data you want. For example:
            1 – View Top Clients
            5 – View Top Senders
            15 – Run Custom SQL Query
            16 – Exit the CLI

    -> GUI Instructions
        If you select GUI, a window will open with buttons for each type of analysis. Just click the button to view the corresponding data.

    -> Exit
        To exit the CLI, type 16 or select the exit option in the GUI.
        You can always rerun the project to explore more data.

🔎 Key Insights Available

    -> Promotions Analysis:
        Client Promotions
        Promotion Effectiveness
        Promotion Suggestions
    -> Transactions Analysis:
        Top Clients
        Top Items
        Top Stores
        Most Popular Store for Each Item
        Store Customer Count
    -> Transfers Analysis:
        Top Senders
        Top Recipients
        Unusual Transfers
        Most Common Transfer Amount
        Transfer Pattern by Day of Week
    -> Client Insights:
        Most Valuable Clients (VIP)
        Location-Based Spending
