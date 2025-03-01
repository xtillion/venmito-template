Name: Antonio Ahmed Tapia Maldonado
Email: antonio.tapia@upr.edu    

My solution for this project included the development an web application that presents the latest report and analytics created by business. Authorized users can upload their own data into the database. These uploaded files are then uploaded to the database via python scripts that know how to parse the data.

your design decisions:
1. Use python to upload the data into the database. Because it was very quick and easy to script in Python
2. Use Spring boot to host the web page. Because of my familiarity with java I can get something up quickly.
3. Use pure html, css, and javascript for developing the webpage.
4. Use power bi, to create charts of the data. Power BI is a easy tool to use that requires minimum training.


clear instructions on how to run your code:
#### To run the Spring Webpage:
1. Create the environment variable velow with the appropriate data:
    * DATABASE_PASSWORD: password login into the database
    * DATABASE_URL: url of the the given database
    * DATABASE_USER: username of the database user
    * JWT_SECRET: secret used to generate JWT tokens
2. run the gradle command bootRun
3. Enter and navigate to the url localhost:8090/app/v1/login on your browser 
4. Enter the username and password to login

#### To run the python scripts create a venv environment and install the following dependencies:
- pip install mysql-connector-python
- pip install pyyaml


## Running the Scripts
To run the scripts just execute the two following commands 
- source ./myenv/Scripts/activate
- install dependencies  
    - you only need to run this step once  
- python "scriptname" 

Future Work:
- Implementing the process that stores the new data file and then uploads the data to the database.