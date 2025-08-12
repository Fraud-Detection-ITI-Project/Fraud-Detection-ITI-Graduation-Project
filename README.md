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
-   **End-to-End Automation:** The entire workflow, from data processing to alerting, is orchestrated by AWS Step Functions, providing robust error handling, state management, and an auditable execution history.
-   **Secure by Design:** The entire infrastructure is provisioned within a logically isolated Amazon VPC, with strict network controls and IAM roles that adhere to the principle of least privilege.

## System Architecture and Data Flow

The architecture is designed as a modular, five-layer pipeline, visualized below. Each layer handles a specific stage of the data lifecycle, from initial capture to actionable insight.

```mermaid
graph TD
    subgraph "1. Data Ingestion Layer"
        A1[EC2 (Kafka Producer)] --> A2[S3 Bucket<br/>Temp Storage]
        A2 --> A3[Amazon Kinesis<br/>Consumer]
        A3 --> A4[S3 Bucket<br/>Central Data Lake]
    end

    subgraph "2. Data Processing Layer"
        B1[AWS Glue<br/>Data Cleaning] --> B2[Amazon Redshift<br/>Table 1: Cleaned Data]
        B2 --> B3[AWS Glue<br/>ML Model]
    end

    subgraph "3. Fraud Alerting Layer"
        C1[Amazon Redshift<br/>Table 2: Anomalies] --> C2[AWS Lambda<br/>Detect New Fraud]
        C2 -- SNS Trigger --> C3[Amazon SNS<br/>Notification Topic]
        C3 --> C4[Email Fraud Notification]
    end

    subgraph "4. Monitoring Layer"
        D1[Amazon CloudWatch<br/>Logs From All Services] --> D2[Amazon Redshift<br/>Table 3: Storage for Logs]
    end

    subgraph "5. Insights Layer"
        E1[Amazon QuickSight<br/>Visualization Dashboard]
    end

    %% --- Inter-Layer Connections ---
    A4 --> B1
    B3 --> C1
    B2 --> E1
    C1 --> E1

    %% --- Styling ---
    classDef storage fill:#D1F2EB,stroke:#007A5E,stroke-width:2px;
    classDef compute fill:#FADBD8,stroke:#C0392B,stroke-width:2px;
    classDef serverless fill:#D6EAF8,stroke:#2E86C1,stroke-width:2px;
    classDef analytics fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px;
    classDef messaging fill:#E8DAEF,stroke:#8E44AD,stroke-width:2px;

    class A1,C2 compute;
    class A2,A4,B2,C1,D2 storage;
    class B1,B3 serverless;
    class A3,C3,C4 messaging;
    class D1,E1 analytics;
```

---

#### 1. Data Ingestion Layer
This layer is responsible for capturing raw transaction events and durably storing them in a central location.
-   **EC2 (Kafka Producer):** The process starts on an **`EC2`** instance where a producer application generates a high-velocity stream of transaction data and publishes it to a Kafka topic.
-   **Temp Storage (S3):** The initial stream is temporarily stored in an **`Amazon S3`** bucket.
-   **Stream Consumption (Kinesis):** **`Amazon Kinesis`** acts as a consumer, ingesting the data from the temporary S3 storage for processing within the AWS ecosystem.
-   **Central Data Lake (S3):** Kinesis delivers the raw data to a final **`Amazon S3`** bucket, which serves as the permanent, central data lake for the entire system.

#### 2. Data Processing Layer
This layer transforms the raw data into an analysis-ready format and applies the fraud detection model.
-   **Data Cleaning (AWS Glue):** An **`AWS Glue`** ETL job is triggered by the arrival of new data in the central data lake. This serverless job cleans, validates, and transforms the raw data into a structured schema.
-   **Structured Storage (Amazon Redshift):** The cleaned data is loaded into `Table 1` in an **`Amazon Redshift`** data warehouse, serving as the single source of truth for transactions.
-   **ML Inference (AWS Glue):** A second **`AWS Glue`** job reads the cleaned data from Redshift, performs feature engineering, and uses a pre-trained machine learning model to generate fraud predictions.

#### 3. Fraud Alerting Layer
This event-driven layer is responsible for triggering immediate notifications upon fraud detection.
-   **Anomaly Storage (Amazon Redshift):** The fraud predictions from the ML model are written to `Table 2` in Redshift, which stores all identified anomalies.
-   **Serverless Detection (AWS Lambda):** An **`AWS Lambda`** function is triggered to query the anomalies table for newly detected fraudulent transactions.
-   **Notification Dispatch (Amazon SNS):** Upon finding a new case, the Lambda function publishes a message to an **`Amazon SNS`** topic, which instantly distributes an **Email Fraud Notification** to subscribed stakeholders.

#### 4. Monitoring Layer
This layer provides centralized operational visibility and logging for the entire pipeline.
-   **Log Aggregation (Amazon CloudWatch):** **`Amazon CloudWatch`** serves as the central hub, collecting logs, metrics, and events from all other services in the pipeline (EC2, Kinesis, Glue, Redshift, Lambda).
-   **Log Archiving (Amazon Redshift):** For long-term analysis and structured querying, the aggregated logs can be loaded from CloudWatch into `Table 3` in Redshift.

#### 5. Insights Layer
This is the business intelligence (BI) layer where analysts interact with the processed data.
-   **Visualization (Amazon QuickSight):** **`Amazon QuickSight`** connects directly to the Amazon Redshift data warehouse.
-   **Interactive Dashboards:** Analysts use QuickSight to query both the cleaned transaction data (`Table 1`) and the fraud predictions (`Table 2`) to build dashboards. This enables real-time trend analysis, investigation of alerts, and monitoring of the ML model's performance.

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
