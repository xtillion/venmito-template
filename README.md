# Venmito Data Engineering Project

## Created by: Luis E. Telemaco Márquez

## Technologies Used: 
- Python3
- Javascript
- Flask API
- Vite React
- PostgreSQL
- Docker
- NodeJS 

## Description
My Venmito solution provides the ETL process through the use of Python scripts with to extract, transform and load the data. For the sake of providing two solutions for the technical team I developed a RESTful backend which connects to a PostgreSQL database. This backend can be consumed independently of the frontend through the use of tools such as Postman, and for the non-technical team I created some visualizations in a frontend done with Vite React.

## Design Decisions
I decided to implement the project this way because I wanted to make use of tools that I was familiar, but also learn new ones that are used in the industry. The decision to implement the backend in Flask was because of its lightweight nature and its ability to help me prototype really fast. As for Vite instead of other React applications is due to its Hot Module Replacement which automatically updates the application with little to no delay. Finally the decision to make use of a PostgreSQL database is because that is the one I'm most familiar with and so far it's been really performant for my use cases.

## Environment Prerequisites:
- Python3.13
- Docker Desktop
- NodeJS

## Step-by-Step Guide for Running the Program:
1. Setup Backend Dependencies by running: `pip install -r requirements.txt`
2. If Docker Desktop is installed this will create the Database: `docker.compose up`
3. To start the Backend go to the backend directory: `cd backend`
4. Once in the Backend run: `flask run` This will run the ETL scripts and populate the Database tables
5. After the Backend is up go to the Frontend directory: `cd ../frontend'`
6. Install the required dependencies specified in the package.json: `npm install`
7. Finally run: `npm run dev` this will start the Frontend and it will populate the pages with visuals