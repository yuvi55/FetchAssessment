# Fetch Assessment Guidelines

This repository contains all necessary instructions and scripts to the completed Fetch assessment. Follow the steps outlined below to set up and run the assessment environment effectively.

## Prerequisites

Ensure Docker is installed on your machine. If not installed, follow the [official Docker installation guide](https://docs.docker.com/get-docker/).

## Setup and Execution

### Starting Docker Containers

1. Clone this repository to your local machine.
2. Navigate to the directory containing the `docker-compose.yml` file.
3. Execute the command below to build and start the Docker containers:
   ```bash
   docker-compose up --build

Running the Python Script
After the Docker containers are up and running, execute the Python script from the repository:
python path_to_script/main.py

Make sure to replace `path_to_script/main.py` with the actual path to your Python script within your repository. 

### Answers to the questions asked in the Assessment:


### 1. How would you deploy this application in production?

**Answer:** 
1. Containers can be deployed to cloud services like AWS ECS or EKS.
2. Implement a CI/CD pipeline using GitHub Actions, Jenkins, or CircleCI to automate testing and deployment.

### 2. What other components would you want to add to make this production ready?

**Answer:** 

1. Logging service such as Elasticsearch, Logstash, Kibana
2. Better Error handling and retry services to ensure smoother working of the application.
   
### 3. How can this application scale with a growing dataset?
**Answer:** 
We would need to deploy this application from LocalStack to the SQS cloud service. AWS SQS automatically scales, so ensure the application can handle larger volumes of messages.

### 4. How can PII be recovered later on?

**Answer:** Store a mapping of original PII to masked values in a secure, encrypted store. Access to this store should be strictly audited. The hashing algorithm used in the script is a one pass algorithm and does 
not allow us to go back to the original value. If required, we could also use a cryptographic cipher to encrypt and decrypt our PII values.

### 5. What are the assumptions you made?

**Answer:** 
1. Data coming in from the queue will always be in a consistent format (no validations have been written to test the data)
2. The app version coming in from the queue can be rounded to nearest integer value.



