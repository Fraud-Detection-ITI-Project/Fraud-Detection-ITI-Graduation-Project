# Cloud-Native, Real-Time Financial Fraud Detection System

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![XGBoost](https://img.shields.io/badge/XGBoost-006600?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMzIgMTZMMTYgMzJ2NjRsMTYtMTZWMzJsNDggNDh2MTZMNzIgODBMNDAgNDhsNDAgNDBINDY0VjE2SDMyem0zMiA0MGwtOCA4VjcyaDh2LTh6bTAtNDBMMzIgNDhoOFYyNGg0MHY0MGgtOFYyNGg4VjE2aC04djhoLTRWMzJoOFYxNkg2NHptMTYgNDBMMzIgNjRoOFY0MGg0MHY0MEg1NnYtOEg0OHYxNmwxNi0xNmg4di04eiIvPjwvc3ZnPg==)

This repository contains the full implementation of a cloud-native, real-time financial fraud detection system built entirely on Amazon Web Services (AWS). The project demonstrates an end-to-end pipeline that ingests, processes, analyzes, and visualizes financial transactions to detect and alert on fraudulent activity in near real-time.

This project was submitted as a capstone for the Information Technology Institute (ITI), Suez Canal Branch.

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [The Synthetic Data Simulator](#-the-synthetic-data-simulator)
- [Machine Learning Model](#-machine-learning-model)
- [Alerting and Automation](#-alerting-and-automation)
- [Results: The Fraud Analytics Dashboard](#-results-the-fraud-analytics-dashboard)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Deployment Steps](#deployment-steps)
- [Project Structure](#-project-structure)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [Team Members](#-team-members)

---

## 🌟 Project Overview

Traditional fraud detection systems often rely on batch processing and static rules, making them slow and ineffective against modern, sophisticated fraud schemes. This project addresses these limitations by building a scalable, serverless, and intelligent system capable of detecting fraud within minutes of a transaction occurring.

The pipeline simulates a real-world financial environment, starting with a custom data generator that produces realistic transaction streams. These streams are ingested via a resilient **Apache Kafka** cluster and fed into the AWS ecosystem through **Amazon Kinesis**. Data is then processed by **AWS Glue**, stored in an **Amazon Redshift** data warehouse, and scored by a high-performance **XGBoost** machine learning model.

When fraud is detected, an automated, event-driven workflow orchestrated by **AWS Step Functions** triggers an immediate email alert via **AWS Lambda** and **Amazon SNS**. Finally, a comprehensive **Amazon QuickSight** dashboard provides analysts with actionable insights and visualizations of fraud trends.

---

## ✨ Key Features

- **High-Fidelity Synthetic Data:** A custom Python-based data generator that produces realistic, labeled financial transactions, including various fraud personas like Account Takeover, Velocity Attacks, and Synthetic Identity Fraud.
- **Scalable Ingestion Pipeline:** A robust data ingestion layer using Apache Kafka and Amazon Kinesis to handle high-velocity streaming data.
- **Serverless ETL and Warehousing:** A centralized data warehouse in Amazon Redshift built with a modified star schema and populated by serverless AWS Glue ETL jobs.
- **High-Performance ML Model:** An XGBoost model trained to accurately classify transactions, achieving an F1-Score of **90.32%** and a Recall of **97.50%** on the test set.
- **Automated Orchestration:** An end-to-end, event-driven workflow managed by AWS Step Functions for a hands-off, reliable processing sequence.
- **Instantaneous Alerting:** A serverless alerting mechanism using AWS Lambda and SNS to notify stakeholders the moment a transaction is flagged as fraudulent.
- **Interactive Analytics Dashboard:** A dynamic Amazon QuickSight dashboard for monitoring KPIs, investigating fraud patterns, and evaluating model performance.
- **Secure and Compliant Infrastructure:** All components are deployed within a secure VPC, adhering to the principle of least privilege with meticulous IAM roles and security groups.

---

## 🏗️ System Architecture

The system is designed as a multi-layered, cloud-native architecture on AWS. Each layer performs a specific function, ensuring modularity, scalability, and maintainability.

![System Architecture Diagram](docs/images/architecture.png)

The data flows through five distinct layers:

1.  **Data Ingestion Layer:** A Python script on an EC2 instance produces synthetic transaction data and publishes it to a self-hosted Kafka cluster. A Kafka consumer forwards these messages to an Amazon Kinesis Data Stream, which reliably delivers them to an S3 data lake via Kinesis Firehose.
2.  **Data Processing Layer:** An AWS Glue ETL job is triggered, reading the raw data from S3, cleaning and transforming it, and loading it into a Redshift data warehouse. A second Glue job then reads the cleaned data, applies feature engineering, and uses a trained XGBoost model to predict fraud, writing the results to a prediction table in Redshift.
3.  **Fraud Alerting Layer:** An AWS Lambda function, orchestrated by Step Functions, regularly queries Redshift for new fraudulent transactions. Upon detection, it sends an alert message to an SNS topic.
4.  **Monitoring Layer:** Amazon CloudWatch automatically collects logs, metrics, and events from all AWS services, providing a centralized hub for operational oversight, debugging, and alarming.
5.  **Insights Layer:** Amazon QuickSight connects directly to the Redshift data warehouse to visualize key metrics, fraud trends, and model performance on an interactive dashboard.

---

## 🛠️ Tech Stack

- **Cloud Provider:** **Amazon Web Services (AWS)**
- **Data Streaming:** **Apache Kafka**, **Amazon Kinesis Data Streams**, **Amazon Kinesis Firehose**
- **Data Processing (ETL):** **AWS Glue** (using PySpark)
- **Data Warehouse:** **Amazon Redshift**
- **Data Lake:** **Amazon S3**
- **Machine Learning:** **XGBoost**, **Scikit-learn**, **Pandas**
- **Serverless Compute:** **AWS Lambda**
- **Orchestration & Automation:** **AWS Step Functions**
- **Alerting & Notification:** **Amazon SNS**, **Amazon SES**
- **BI & Visualization:** **Amazon QuickSight**
- **Infrastructure & Security:** **VPC**, **IAM**, **EC2**, **CloudWatch**, **Secrets Manager**
- **Containerization:** **Docker**, **Docker Compose** (for Kafka cluster)

---

## 🎭 The Synthetic Data Simulator

Since real financial data is sensitive and private, this project utilizes a custom-built data simulator in Python. It generates a large-scale dataset (500,000+ transactions) that mimics the patterns of the Egyptian market.

The simulator uses a **persona-based model** to create temporally consistent behavior for individual customers. It explicitly embeds and labels transactions from several pre-defined fraud personas, including:

- **`FraudPersona_AccountTakeover`**: A single, high-value transaction from a new device/IP.
- **`FraudPersona_CardTesting`**: A rapid burst of very small-value transactions.
- **`FraudPersona_VelocityAttack`**: A series of large-value transactions in a short time.
- **`FraudPersona_ImpossibleTravel`**: A legitimate transaction followed by a fraudulent one from a physically impossible distance away.
- **`FraudPersona_SyntheticIdentity`**: A new persona that makes a few small "warm-up" transactions before a massive cash-out.

---

## 🤖 Machine Learning Model

The core intelligence of the system is a supervised classification model.

- **Algorithm:** **XGBoost** (Extreme Gradient Boosting) was chosen for its high performance on tabular data, scalability, and built-in handling for imbalanced datasets.
- **Feature Engineering:** Features were engineered to capture complex behavioral patterns, such as `txn_per_hour`, `distance_to_merchant`, `is_far_txn`, and binary flags for high-risk events.
- **Performance:** The model was evaluated on a holdout test set with excellent results, proving its effectiveness.
  - **F1 Score:** **90.32%**
  - **Recall:** **97.50%** (Catches 97.5% of all true fraud)
  - **Precision:** **84.12%** (Over 84% of alerts are for true fraud)
  - **AUC:** **1.00**

---

## 🚨 Alerting and Automation

The alerting workflow is fully automated using a combination of serverless AWS services.

![State Machine Workflow](docs/images/step_function_workflow.png)

1.  **Orchestration:** An **AWS Step Functions** state machine orchestrates the entire process, running the Glue jobs in sequence.
2.  **Detection:** After the ML job, a polling loop is initiated. An **AWS Lambda** function queries the Redshift `predicted_fraud` table every 10 seconds for new entries that have not yet been alerted on.
3.  **Notification:** If new fraudulent transactions are found, the Lambda function formats an HTML email alert and publishes it to an **Amazon SNS** topic.
4.  **Delivery:** **Amazon SES** (Simple Email Service) is subscribed to the SNS topic and delivers the email to the fraud analysis team. The system then updates the database to prevent duplicate alerts.

---

## 📊 Results: The Fraud Analytics Dashboard

The Amazon QuickSight dashboard provides a powerful, at-a-glance interface for analysts to monitor and investigate fraud.

#### Key Performance Indicators (KPIs)
![KPI Dashboard](docs/images/quicksight_kpi.png)

#### Transaction Status & Fraud by Category
![Dashboard Charts](docs/images/quicksight_charts.png)

#### Model Performance & Trend Analysis
![Model Performance Dashboard](docs/images/quicksight_trends.png)

---

## 🚀 Getting Started

### Prerequisites

- An **AWS Account** with sufficient permissions to create the resources mentioned in the Tech Stack.
- **AWS CLI** configured with your credentials.
- **Python 3.8+**
- **Docker** and **Docker Compose**
- **Git**

### Deployment Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/financial-fraud-detection.git
    cd financial-fraud-detection
    ```

2.  **Setup Networking:**
    - Deploy the VPC, subnets (public/private), Internet Gateway, and security groups as detailed in the project documentation (or using the provided IaC scripts).

3.  **Launch EC2 & Deploy Kafka:**
    - Launch a `t3.medium` EC2 instance in the public subnet.
    - SSH into the instance, install Docker and Docker Compose.
    - Use the `docker-compose.yml` file in the `/kafka` directory to spin up the 3-broker Kafka cluster.

4.  **Configure AWS Services:**
    - Create the **Kinesis Data Stream** and **Kinesis Firehose** delivery stream, pointing Firehose to your S3 data lake bucket.
    - Create the **Amazon Redshift** cluster in the private subnets, ensuring its security group allows access from AWS Glue and QuickSight.
    - Create the necessary **IAM Roles** for EC2, Glue, Lambda, and Redshift, following the principle of least privilege.

5.  **Deploy Scripts and Models:**
    - Upload the **AWS Glue ETL and ML inference scripts** to your S3 bucket.
    - Upload the trained `xgb_fraud_model.pkl` file to S3.
    - Deploy the **AWS Lambda** function for alerting.

6.  **Orchestrate and Run:**
    - Define and deploy the **AWS Step Functions** state machine to automate the pipeline.
    - Run the `producer.py` script on the EC2 instance to start generating and streaming data.
    - Trigger the Step Functions workflow to process the initial batches of data.

7.  **Visualize:**
    - Connect **Amazon QuickSight** to your Redshift cluster and build the dashboard based on the `fact_transaction` and `predicted_fraud` tables.

---

## 📁 Project Structure

```
.
├── aws_glue_scripts/
│   ├── etl_cleaning_job.py       # Glue job for ETL and data cleaning
│   └── ml_inference_job.py       # Glue job for ML inference
├── data_simulator/
│   ├── synthetic_data_generator.py # Main script for generating data
│   └── profiles/                 # Configuration for fraud personas
├── kafka/
│   ├── docker-compose.yml        # Docker compose for Kafka cluster
│   ├── producer.py               # Produces data and sends to Kafka
│   └── consumer.py               # Consumes from Kafka and sends to Kinesis
├── lambda_function/
│   └── send_fraud_alert.py       # Lambda function for sending email alerts
├── docs/
│   ├── Project_Documentation.pdf # The full project report
│   └── images/                   # Diagrams and screenshots for README
└── README.md
```

---

## ⚠️ Limitations

- **Synthetic Data:** The model's performance is based on a synthetic dataset. While realistic, it cannot capture the full complexity and noise of real-world data. Performance in a live production environment may differ.
- **Near Real-Time vs. True Real-Time:** The architecture's latency is measured in minutes due to the batching nature of Kinesis Firehose and AWS Glue. It is designed for rapid investigation, not for instantaneous transaction blocking.
- **Static Model:** The model is static and does not automatically retrain. In a real-world scenario, this could lead to performance degradation over time as fraud patterns evolve (concept drift).

---

## 🔮 Future Enhancements

- **True Real-Time Inference:** Replace the Glue inference job with a streaming solution using **Kinesis Data Analytics** or **AWS Lambda** to score transactions in sub-seconds.
- **Automated MLOps Pipeline:** Implement a full MLOps pipeline using **Amazon SageMaker** to automate model retraining, evaluation, and deployment, combating concept drift.
- **Integrate Model Explainability (XAI):** Use libraries like **SHAP** to provide explanations for each fraud prediction, assisting analysts in their investigations.
- **Unsupervised Anomaly Detection:** Add an unsupervised model (e.g., Isolation Forest) to the pipeline to detect novel and previously unseen fraud patterns.

---

## 👥 Team Members

- Seif El-Deen Gaber
- Omar Adel
- Yasmine Samir
- Abdelrahman Wael
- Ahmed Srour

**Project Supervisor:** Ibrahim Mohamed
