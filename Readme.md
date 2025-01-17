# Shopee AI Project

This repository contains a machine learning-based solution for Shopee, built using Python and Docker. The project involves setting up a PostgreSQL database with the `pgvector` extension, loading data, and running a Python-based AI model.

## Steps to Set Up and Run the Project

| **Step 1**: Clone the Repository | **Step 2**: Install Python Dependencies |
|----------------------------------|----------------------------------------|
| First, clone the repository to your local machine: | Next, install the required Python dependencies using `pip`: |
| git clone https://github.com/lkpilot/shopee-AI.git | pip install -r requirements.txt |
| cd shopee-AI | |

| **Step 3**: Install Docker and Set Up `pgvector` Database | **Step 4**: Load the Database |
|--------------------------------------------------------|-------------------------------|
| Ensure you have Docker installed on your machine. You can download Docker from [here](https://www.docker.com/get-started). Then, run the following command to set up the `pgvector` PostgreSQL database using Docker: | Once the Docker container is running, load the data into the PostgreSQL database by running the following Python script: |
| docker run --name pgvector -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 ankane/pgvector | python load_database.py |

| **Step 5**: Run the AI Model |
|-----------------------------|
| After the database has been set up and populated with data, run the AI model by executing the following Python script: |
| python main.py |

## Troubleshooting

- Ensure Docker is running before executing the `docker run` command.
- If there are any issues connecting to the database, you can check the Docker logs:

  docker logs pgvector
