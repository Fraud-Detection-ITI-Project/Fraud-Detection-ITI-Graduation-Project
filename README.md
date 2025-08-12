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

The architecture is designed with a multi-layered approach on AWS, ensuring a clear separation of concerns for data ingestion, processing, alerting, and analysis. The following is a step-by-step description of the data flow through each logical layer of the pipeline.

#### 1. Data Ingestion Layer
This layer is responsible for capturing raw transaction events and staging them in a central data lake.
-   **Data Generation:** The process originates on an **`EC2`** instance where a producer application, integrated with **`Apache Kafka`**, generates a stream of transaction data.
-   **Stream Consumption & Delivery:** A consumer process, powered by **`Amazon Kinesis`**, ingests this stream. It processes the events and delivers them to a final destination.
-   **Central Data Lake:** The processed stream is stored in an **`Amazon S3`** bucket, which serves as the durable, scalable, and centralized data lake for all raw transactional data.

#### 2. Data Processing Layer
This layer transforms the raw data into a structured format and applies the machine learning model to score for fraud.
-   **ETL and Data Cleaning:** An **`AWS Glue`** job is initiated, reading the raw data from the central S3 data lake. This serverless job cleans, validates, and transforms the data into a structured schema.
-   **Structured Data Storage:** The cleaned, structured data is loaded into a dedicated table (`Redshift Table 1`) within an **`Amazon Redshift`** data warehouse. This table acts as the primary source of truth for all transactions.
-   **Machine Learning Inference:** A second **`AWS Glue`** job reads the cleaned data from Redshift. It performs feature engineering and applies a pre-trained ML model to generate a fraud prediction for each transaction.

#### 3. Fraud Alerting Layer
This layer is an event-driven workflow that triggers immediate notifications upon the detection of fraud.
-   **Anomaly Storage:** The fraud predictions from the ML model are written to a separate "anomalies" table (`Redshift Table 2`) in Redshift.
-   **Serverless Detection:** An **`AWS Lambda`** function is triggered to query this table for newly identified fraudulent transactions.
-   **Notification Dispatch:** Upon finding a new fraud case, the Lambda function triggers an **`Amazon SNS`** (Simple Notification Service) topic. SNS then instantly distributes the alert as an **Email Fraud Notification** to subscribed stakeholders.

#### 4. Monitoring Layer
This layer provides centralized operational visibility across the entire pipeline.
-   **Log Aggregation:** **`Amazon CloudWatch`** automatically collects logs, metrics, and events from all services in the architecture (EC2, Kinesis, Glue, Redshift, Lambda).
-   **Log Archiving:** For long-term analysis or compliance, aggregated logs from CloudWatch can be loaded into a dedicated table (`Redshift Table 3`) for structured querying.

#### 5. Insights Layer
This is the business intelligence (BI) layer where analysts interact with the data.
-   **Data Visualization:** **`Amazon QuickSight`** connects directly to the Amazon Redshift data warehouse.
-   **Interactive Dashboards:** Analysts use QuickSight to build and view dashboards, visualizing key metrics from the cleaned transaction data (`Redshift Table 1`) and the fraud predictions (`Redshift Table 2`). This enables trend analysis, investigation of alerts, and monitoring of the model's performance.

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

-   Seif El-Deen Gaber
-   Omar Adel
-   Yasmine Samir
-   Abdelrahman Wael
-   Ahmed Srour

**Project Supervisor:** Ibrahim Mohamed
