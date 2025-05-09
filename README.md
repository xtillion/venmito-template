--Project submission:
-name: Kevin J. Bonet Guadalupe
-email: kevinjbonet@gmail.com
-a description of your solution: Took provided files and turned them into database objects (tables). These tables i made sure to standardize the column titles for easier use (reading, merging, relating). Once it was all made easier to work with, a master table was created. A gui with preloaded questions/queries was made covering the overall utility of the project.
-your design decisions: Tried at first to just get everything onto a table, but this lended itself to errors. Decided to just turn everything into tables first and then start connecting them in a modular approach. Once it was all connected, it was time to put it to work, used the suggested questions as a guid for what calculations to make and what information to display.
-clear instructions on how to run your code: 
Guide to Running the Venmito Data Explorer

Prerequisites

Before running the script, ensure that the following requirements are met:

Python is installed on your system (preferably Python 3.x).

The necessary Python libraries are installed:

tkinter (built into Python)

sqlite3 (built into Python)

matplotlib

Installation of Required Libraries

If you haven't installed matplotlib, activate your virtual environment (if applicable) and install it using:

pip install matplotlib

Running the GUI

To launch the Venmito Data Explorer, follow these steps:

Navigate to the Project Directory:
Open a terminal or command prompt and change the directory to where the script is located.

cd path/to/your/project

Activate Virtual Environment (if applicable):
If you're using a virtual environment, activate it:

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

Run the script:

python venmito_data_gui.py

Using the GUI

A window will open with a dropdown menu containing different queries.

Select a question from the dropdown menu.

Click the Run Query button to execute the query.

The results will be displayed in a message box or as a visualization.

Understanding the Available Queries

The GUI provides insights into the data stored in venmito_master.db. The available queries include:

Which clients have what type of promotion?

Give suggestions on how to turn 'No' responses from clients in the promotions file.

What item is the best seller? (Excludes blank entries)

What store has had the most profit?

How can we use the data we got from the transfer file? (Generates a visualization of top senders)

Troubleshooting

ImportError: No module named 'matplotlib'

Run pip install matplotlib to install the missing module.

Database Errors (e.g., Table Not Found)

Ensure venmito_master.db exists in the same directory as the script.

GUI Not Launching

Check that you're running Python with the required libraries installed.

-A method to consume the reorganized and analyzed data: python venmito_data_gui.py will allow you to launch the gui and see the data in action.

# Venmito Data Engineering Project

## Introduction

*Welcome to Xtillion's Data Engineering Project. For this exercise, we will simulate a client interaction where you are an engineering consultant for Venmito, your client. We're excited to see how you tackle this challenge and provide us with a solution that can bring together disparate data sources into an insightful and valuable resource.* 

We are Venmito, a modest payments startup focused on making it easy for our customers to transfer funds, shop at participating local stores, and enjoy personalized promotions tailored just for them. As our popularity has steadily grown, so has the volume and complexity of our data. Unfortunately, this sustained growth has overwhelmed our original data systems, and we now find ourselves with a setup that's no longer sustainable.

**That's where you come in**. Your mission is to unravel and consolidate our fragmented data into a scalable, insightful, and consumable solution. We're counting on your technical skills, creativity, and resourcefulness to guide us from data chaos to clarity, enabling smarter decisions and continued growth.

We have five data files available:

- people.json
- people.yml
- transfers.csv
- transactions.xml
- promotions.csv

These files contain information about our customers, transactions, transfers, or promotions.

Your task is to develop a solution that reads, unifies, and structures our data into a consumable format. Additionally, we would like you to analyze this data and provide clear, actionable insights based solely on your findings. These insights should help us better understand our customers, improve our processes, and make informed, data-driven decisions going forward.

## Requirements

1. **Data Ingestion**: Your solution should be able to read and load data from all the provided files. Take into account that these files are in different formats (JSON, YAML, CSV, XML).

2. **Data Matching and Conforming**: Once the data is loaded, your solution should be capable of matching and conforming the data across these files. This includes identifying common entities, resolving inconsistencies, and organizing the data into a unified format. Furthermore, the consolidated data should not only be transient but also persistent. This persistence should be achieved using appropriate methods such as storing in a file, database, or other suitable data storage solutions, and not restricted to just a variable in memory. This way, the integrity and availability of the consolidated data are ensured for future use and analysis.

3. **Data Analysis**: Your solution should be able to process the conformed data to derive insights about our clients and transactions. This would involve implementing data aggregations, calculating relevant metrics, and identifying patterns. These insights will be invaluable in helping us understand our clientele and transaction trends better. **Here are just a few ideas to get you started—don't limit yourself to just these examples, think outside the box and come up with your own metrics as you work through the project**! For example, you might look into:
    - Which clients have what type of promotion?
    - Give suggestions on how to turn "No" responses from clients in the promotions file.
    - Insights on stores, like:
        - What item is the best seller?
        - What store has had the most profit?
        - Etc.
    - How can we use the data we got from the transfer file?

4. **Data Output**: The final output of your solution should enable us to consume the reorganized and analyzed data in a meaningful way. This could be, but is not restricted to, a command line interface (CLI), a GUI featuring interactive visualizations, a Jupyter Notebook, or a RESTful API. We invite you to leverage other innovative methods that you believe would be beneficial for a company like Venmito. Please provide at least 2 data consumption methods, 1 for the non-technical team and 1 for the technical team.


5. **Code**: The code for your solution should be well-structured and comprehensible, with comments included where necessary. Remember, the quality and readability of the code will be a significant factor in the evaluation of the final deliverable.

Note: The examples provided in these requirements (such as GUI, RESTful API etc.) are purely illustrative. You are free to employ any solution or technology you deem fit for fulfilling these requirements

## Deliverables

1. Source code.
2. A README file with your name, email, a description of your solution, your design decisions, and clear instructions on how to run your code.
3. A method to consume the reorganized and analyzed data.

## Instructions for Submission

1. Complete your project as described above in a branch within your fork.
2. Write a detailed README file with your name, email, a description explaining your approach, the technologies you used, and provides clear instructions on how to run your code.
3. Submit your project by uploading a zip file to the provided URL.

We look forward to seeing your solution!

Thank you,

Venmito

## DISCLAIMER:

This project and its contents are the exclusive property of Xtillion, LLC and are intended solely for the evaluation of the individual to whom it was provided. Any distribution, reproduction, or unauthorized use is strictly prohibited. By accessing and using this project, you agree to abide by these conditions. Failure to comply with these terms may result in legal action.

Please note that this project is provided "as is", without warranty of any kind, express or implied. Xtillion is not liable for any damages or claims that might arise from using or misusing this project.
