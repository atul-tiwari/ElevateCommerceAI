# Amazon Data Scraper Project

## Overview
This project is a data scraper for Amazon product details. It uses various APIs and requires specific API keys and database credentials to run successfully.

## Requirements
Before running the project, ensure you have the following:

1. DataASIN API Key for Amazon data scraping.
2. AWS account with an EC2 instance to host the API and an RDS EC2 instance for the database. Alternatively, you can deploy the API instance locally.
3. Database credentials (username, password, database name) for MySQL stored in a `.env` file in the Amazon API directory.

## Installation and Setup

### Step 1: Obtain API Keys
- Obtain the DataASIN API key for Amazon data scraping.
- Set up an AWS account with an EC2 instance and an RDS EC2 instance. Alternatively, set up the project to run locally.

### Step 2: Configure `.env` File
- In the Amazon API directory, create a `.env` file.
- Add your database credentials in the `.env` file using the following format:
- Save the `.env` file.

ClientID = 
ClientSecret = 
master_pass=
HOST_URL=
HOST_PORT=3306
DB_USER=admin
PASSWORD=
DB_NAME=ElevateCommerceAI
API_KEY=
ENV=DEVELOPMENT


### Step 3: Database Setup
- Navigate to the `database` folder in the project.
- Execute all the required data tables' definitions in MySQL to set up the database schema.

### Step 4: Run the API
- Set the API environment to "Developer mode" in the `.env` file to run the code locally.
- Start the API to begin scraping Amazon product details.

## Usage
Once the setup is complete, you can use the API to scrape Amazon product details. Make sure to handle the scraped data securely and in compliance with Amazon's terms of service.

## Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## Github link
https://github.com/atul-tiwari/ElevateCommerceAI
