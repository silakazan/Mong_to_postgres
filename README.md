# MongoDB to PostgreSQL ETL Project

This project demonstrates how to perform an ETL (Extract, Transform, Load) process to transfer data from MongoDB to PostgreSQL using Python. The goal is to extract shipment data from MongoDB, transform it into a suitable format, and load it into a PostgreSQL database.

## Project Overview

In this project, we simulate the process of extracting shipment data from MongoDB, transforming it (e.g., ensuring it adheres to the format required by PostgreSQL), and loading it into PostgreSQL. The project highlights how to work with two popular databases and how to use Python libraries such as `pymongo` and `psycopg2` to interact with them.

## Technologies Used
- **MongoDB**: Source database where shipment data is stored.
- **PostgreSQL**: Target database where the data will be transferred.
- **Python**: Used for scripting and data manipulation.
- **pymongo**: Python library for MongoDB integration.
- **psycopg2**: Python library for PostgreSQL integration.

## Setup and Installation

### Prerequisites

- **MongoDB**: Ensure MongoDB is installed and running.
- **PostgreSQL**: Ensure PostgreSQL is installed and running.
- **Python**: Python 3.x must be installed.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/silakazan/mongodb-to-postgresql-etl.git
   cd mongodb-to-postgresql-etl
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate     # For Windows
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
Running the Project
Generate sample data: The generate_data.py script generates sample shipment data and inserts it into MongoDB.

   ```bash
   python generate_data.py
Run the ETL Process: The etl_process.py script performs the ETL process: extracting data from MongoDB, transforming it, and loading it into PostgreSQL.

   ```bash
   python etl_process.py
Check PostgreSQL Data: After running the ETL process, the data will be transferred to PostgreSQL. You can verify the data using a PostgreSQL client or by running the following command in the script:
   ```bash
   python check_data.py

