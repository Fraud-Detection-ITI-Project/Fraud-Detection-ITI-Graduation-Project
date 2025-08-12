# Cloud-Native Real-Time Financial Fraud Detection System

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This repository contains the source code and documentation for an end-to-end, cloud-native financial fraud detection system. The architecture is built entirely on Amazon Web Services (AWS) and is designed to ingest, process, and analyze high-velocity transaction data to identify and alert on fraudulent activity in near real-time.

This project was developed as a capstone for the Information Technology Institute (ITI).

## Table of Contents

- [Project Abstract](#project-abstract)
- [Key Architectural Features](#key-architectural-features)
- [System Architecture and Data Flow](#system-architecture-and-data-flow)
- [Technology Stack](#technology-stack)
- [Synthetic Data Generation](#synthetic-data-generation)
- [Machine Learning Model](#machine-learning-model)
- [Automated Alerting Workflow](#automated-alerting-workflow)
- [Analytics and Visualization](#analytics-and-visualization)
- [Deployment Guide](#deployment-guide)
- [Project Structure](#project-structure)
- [Limitations and Future Work](#limitations-and-future-work)
- [Contributors](#contributors)

## Project Abstract

Traditional fraud detection mechanisms, often characterized by batch processing and static rule engines, are ill-equipped to handle the speed and sophistication of modern financial fraud. This project implements a modern alternative: a scalable, event-driven pipeline that leverages serverless computing and machine learning. The system is capable of processing transaction streams, applying a predictive model to score for fraud, and triggering automated alerts, reducing the detection-to-response latency from hours to minutes.

## Key Architectural Features

-   **High-Throughput, Resilient Ingestion:** Utilizes a self-managed Apache Kafka cluster as a durable buffer, decoupling the data source from the cloud pipeline and ensuring data integrity, with Amazon Kinesis for scalable stream ingestion into AWS.
-   **Serverless Data Processing:** Employs AWS Glue for serverless ETL and ML inference, automatically scaling resources to match the workload, eliminating the need for server management.
-   **Optimized Data Warehousing:** A centralized data warehouse in Amazon Redshift is designed with a modified star schema and strategic distribution keys to ensure high-performance analytical queries.
-   **Intelligent Fraud Detection:** A high-performance XGBoost model serves as the core detection engine, trained to identify complex, non-linear patterns indicative of fraudulent behavior.
-   **End-to-End Automation:** The entire workflow, from data processing to alerting, is orchestrated by AWS Step Functions, providing robust error handling, state management, and a auditable execution history.
-   **Secure by Design:** The entire infrastructure is provisioned within a logically isolated Amazon VPC, with strict network controls and IAM roles that adhere to the principle of least privilege.

## System Architecture and Data Flow

The architecture is layered to separate concerns, ensuring modularity and scalability. The data progresses through the system in the following sequence:

1.  **Ingestion:**
    -   An `EC2` instance hosts a Python script that simulates financial transactions and publishes them to a self-hosted `Apache Kafka` cluster.
    -   A Kafka consumer script reads from the topic and forwards messages to an `Amazon Kinesis Data Stream`.

2.  **Staging and Persistence:**
    -   `Amazon Kinesis Firehose` consumes from the Kinesis stream, batches records into optimally sized files, and delivers them to an `Amazon S3` bucket, creating a partitioned data lake (`YYYY/MM/DD/HH/`).

3.  **ETL and Warehousing:**
    -   An `AWS Glue` ETL job is triggered by the arrival of new data in S3. It cleans, transforms, and structures the raw JSON data, loading it into dimension and fact tables within the `Amazon Redshift` data warehouse.

4.  **Machine Learning Inference:**
    -   A second `AWS Glue` job runs sequentially. It reads the newly cleaned transaction data from Redshift, applies the same feature engineering used in training, and invokes a pre-trained `XGBoost` model to generate fraud predictions. These predictions are written back to a dedicated table in Redshift.

5.  **Alerting and Notification:**
    -   Orchestrated by `AWS Step Functions`, an `AWS Lambda` function queries Redshift for new, high-confidence fraud predictions.
    -   If detected, the function constructs a detailed alert and publishes it to an `Amazon SNS` topic, which then dispatches an email notification via `Amazon SES`.

6.  **Monitoring and Visualization:**
    -   `Amazon CloudWatch` provides unified monitoring, collecting logs and performance metrics from all services.
    -   `Amazon QuickSight` connects directly to Redshift, serving as the business intelligence layer for analysts to monitor trends and investigate alerts.

## Technology Stack

-   **Data Ingestion:** Apache Kafka, Amazon Kinesis Data Streams, Amazon Kinesis Firehose
-   **Data Storage:** Amazon S3 (Data Lake), Amazon Redshift (Data Warehouse)
-   **Data Processing:** AWS Glue (PySpark)
-   **Machine Learning:** Python, Pandas, Scikit-learn, XGBoost
-   **Orchestration:** AWS Step Functions
-   **Serverless Compute:** AWS Lambda
-   **Alerting:** Amazon SNS, Amazon SES
-   **Analytics:** Amazon QuickSight
-   **Infrastructure & Security:** Amazon VPC, EC2, IAM, CloudWatch, Secrets Manager

## Synthetic Data Generation

To train and test the system without using sensitive real-world data, a custom Python simulator was developed. It generates a large-scale, temporally consistent dataset with labeled transactions. The simulator creates user "personas," including several distinct fraud archetypes:
-   **Account Takeover:** A single, large transaction from a new device/IP.
-   **Card Testing:** A rapid series of very small transactions to validate stolen card details.
-   **Velocity Attack:** Multiple high-value transactions across different merchants in a short period.
-   **Impossible Travel:** Two transactions spaced by a time interval insufficient to travel the geographical distance between them.
-   **Synthetic Identity:** A new account with "warm-up" transactions followed by a large cash-out.

## Machine Learning Model

A supervised classification model forms the intelligent core of the system.

-   **Algorithm:** **XGBoost** (Extreme Gradient Boosting) was selected for its performance, scalability, and native ability to handle class imbalance.
-   **Evaluation:** The model's performance was rigorously evaluated, prioritizing high recall to minimize missed fraud (false negatives) while maintaining strong precision to reduce false alarms.
    -   **F1 Score:** `90.32%`
    -   **Recall:** `97.50%`
    -   **Precision:** `84.12%`
    -   **AUC (ROC):** `1.00`

## Automated Alerting Workflow

The system's response mechanism is fully automated and orchestrated by an AWS Step Functions state machine.

The state machine executes the following sequence:
1.  **`Start`**: The workflow is triggered on a schedule or by an event.
2.  **`RunDataCleaningJob`**: Invokes the first AWS Glue job to perform ETL.
3.  **`RunMLInferenceJob`**: On success, invokes the second Glue job for ML scoring.
4.  **`CheckForNewFraud`**: Invokes a Lambda function to query Redshift for newly identified fraudulent transactions that have not yet been alerted.
5.  **`DispatchAlerts` (Choice State)**: If the previous step finds new fraud cases, the workflow proceeds to send notifications.
6.  **`End`**: The workflow completes successfully or enters a failed state with logged errors.

## Analytics and Visualization

An Amazon QuickSight dashboard serves as the primary interface for human analysts. It provides a comprehensive, at-a-glance view of transaction health and fraud patterns through several key visualizations:

-   **Headline KPIs:** A top-level banner displaying critical, time-filtered metrics: Total Transaction Value (TTV), Total Transaction Count, Fraud Rate (%), and Fraud Loss Value.
-   **Operational Dashboards:** Donut charts showing transaction approval/decline rates and pivotable bar charts breaking down fraud counts by dimensions such as Merchant Category, Card Type, Device OS, or Issuing Bank.
-   **Model Performance Monitoring:** Line charts tracking the model's Precision and False Positive Rate (FPR) over time to detect performance degradation.
-   **Trend Analysis:** Visualizations tracking the volume of fraud within specific high-risk segments (e.g., transactions originating from a VPN or first-time customer-merchant interactions).

## Deployment Guide

Deploying this system involves provisioning and configuring multiple interconnected AWS services. The high-level steps are as follows:

1.  **Clone the Repository:** Secure a local copy of the project source code.
2.  **Provision Core Infrastructure:** Set up the networking layer (VPC, Subnets, Security Groups) and the S3 data lake bucket.
3.  **Deploy Ingestion Layer:** Launch the EC2 instance, install Docker, and start the Kafka cluster using the provided `docker-compose.yml`.
4.  **Configure Data Services:** Create and configure the Kinesis Data Stream, Kinesis Firehose, and the Redshift Cluster. Ensure network paths and permissions are correctly set.
5.  **Deploy Serverless Logic:** Create the Glue jobs, Lambda function, and Step Functions state machine, uploading the relevant Python scripts and assigning the appropriate IAM roles.
6.  **Initiate Data Flow:** Run the `producer.py` script on the EC2 instance to begin generating and streaming data into the pipeline.
7.  **Connect Visualization Layer:** Establish a connection from Amazon QuickSight to the Redshift cluster and build the analytics dashboard.

## Project Structure

```
.
├── aws_glue_scripts/
│   ├── etl_cleaning_job.py       # Glue job for ETL and data warehouse loading
│   └── ml_inference_job.py       # Glue job for feature engineering and ML scoring
├── data_simulator/
│   └── synthetic_data_generator.py # Script for generating the synthetic dataset
├── kafka/
│   ├── docker-compose.yml        # Configuration for the Apache Kafka cluster
│   ├── producer.py               # Produces data and sends to a Kafka topic
│   └── consumer.py               # Consumes from Kafka and forwards to Kinesis
├── lambda_function/
│   └── send_fraud_alert.py       # Serverless function for dispatching alerts
└── documentation/
    └── Full_Project_Documentation.pdf # The complete academic report
```

## Limitations and Future Work

### Limitations

-   **Synthetic Data Reliance:** The system's performance metrics are based on a synthetic dataset, which may not fully capture the nuances of real-world transaction data.
-   **Near Real-Time Latency:** The architecture is designed for "near real-time" analysis (minutes), not "true real-time" (sub-second) transaction blocking, due to the batching nature of Glue and Kinesis Firehose.
-   **Static Model Deployment:** The current implementation uses a statically trained model. Without a retraining mechanism, its performance may degrade over time as fraud patterns evolve (concept drift).

### Future Enhancements

-   **Streaming Inference:** Augment the architecture with a true streaming component (e.g., Kinesis Data Analytics or a Lambda-based scorer) to enable sub-second inference for real-time transaction blocking.
-   **MLOps Integration:** Implement an automated MLOps pipeline using services like Amazon SageMaker to monitor for data and model drift, and to trigger automated model retraining and deployment.
-   **Model Explainability (XAI):** Integrate libraries like SHAP (SHapley Additive exPlanations) to generate human-interpretable reasons for each fraud prediction, aiding analyst investigations and improving model transparency.

## Contributors

-   Omar Adel
-   Seif El-Deen Gaber
-   Yasmine Samir
-   Abdelrahman Wael
-   Ahmed Srour

**Project Supervisor:** Ibrahim Mohamed
