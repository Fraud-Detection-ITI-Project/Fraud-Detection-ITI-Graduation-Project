<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF2400,100:800000&height=350&section=header&text=Cloud-Native%20Real-Time%20Financial%20Fraud%20Detection%20System&fontSize=30&fontColor=ffffff&animation=fadeIn&fontAlign=center&fontAlignY=40&desc=AWS%20•%20Kafka%20•%20Glue%20•%20Redshift%20•%20XGBoost%20•%20QuickSight%20•%20Kinesis%20•%20S3%20•%20CloudWatch%20•%20SNS%20•%20Lambda&descSize=18&descAlign=middle&descAlignY=75" alt="Header">
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-AWS-%23DC143C?logo=amazon-aws&logoColor=white" alt="AWS">
  <img src="https://img.shields.io/badge/Streaming-Apache%20Kafka-231F20?logo=apachekafka&logoColor=white&color=DC143C&labelColor=231F20" alt="Kafka">
  <img src="https://img.shields.io/badge/Streaming-Amazon%20Kinesis-DC143C?logo=amazon-aws&logoColor=white" alt="Kinesis">
  <img src="https://img.shields.io/badge/Data%20Storage-Amazon%20S3-DC143C?logo=amazons3&logoColor=white" alt="S3">
  <img src="https://img.shields.io/badge/Data%20Processing-AWS%20Glue-DC143C?logo=amazon-aws&logoColor=white" alt="AWS Glue">
  <img src="https://img.shields.io/badge/Data%20Warehouse-Amazon%20Redshift-DC143C?logo=amazon-redshift&logoColor=white" alt="Redshift">
  <img src="https://img.shields.io/badge/Monitoring-CloudWatch-DC143C?logo=amazon-aws&logoColor=white" alt="CloudWatch">
  <img src="https://img.shields.io/badge/Alerting-Amazon%20SNS-DC143C?logo=amazon-aws&logoColor=white" alt="SNS">
  <img src="https://img.shields.io/badge/Serverless-AWS%20Lambda-DC143C?logo=awslambda&logoColor=white" alt="Lambda">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/ML%20Algorithm-XGBoost-DC143C" alt="XGBoost">
  <img src="https://img.shields.io/badge/Visualization-QuickSight-F2C811?logo=amazon-quicksight&logoColor=DC143C" alt="QuickSight">
</p>

---

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

- **High-Throughput, Resilient Ingestion:** Utilizes a self-managed Apache Kafka cluster as a durable buffer, decoupling the data source from the cloud pipeline and ensuring data integrity, with Amazon Kinesis for scalable stream ingestion into AWS.
- **Serverless Data Processing:** Employs AWS Glue for serverless ETL and ML inference, automatically scaling resources to match the workload, eliminating the need for server management.
- **Optimized Data Warehousing:** A centralized data warehouse in Amazon Redshift is designed with a modified star schema and strategic distribution keys to ensure high-performance analytical queries.
- **Intelligent Fraud Detection:** A high-performance XGBoost model serves as the core detection engine, trained to identify complex, non-linear patterns indicative of fraudulent behavior.
- **End-to-End Automation:** The entire workflow, from data processing to alerting, is orchestrated by AWS Step Functions, providing robust error handling, state management, and an auditable execution history.
- **Secure by Design:** The entire infrastructure is provisioned within a logically isolated Amazon VPC, with strict network controls and IAM roles that adhere to the principle of least privilege.

## System Architecture and Data Flow

<p align="center">
  <img src="Architecture/fraud_arch.png" alt="System Architecture" width="85%">
</p>

**Architectural Layers Description:**

1. **Data Ingestion Layer:** Captures raw transaction data from an EC2 instance acting as a Kafka Producer. Data is temporarily staged in S3 before being consumed by Amazon Kinesis and stored in a Central Data Lake (S3).
2. **Data Processing Layer:** AWS Glue jobs clean and transform data, load it into Redshift, and run ML inference using the XGBoost model.
3. **Fraud Alerting Layer:** Predictions are stored in Redshift, then AWS Lambda checks for new anomalies and triggers Amazon SNS to send fraud alerts via email.
4. **Monitoring Layer:** CloudWatch collects logs and metrics from all services, archived into Redshift for analysis.
5. **Insights Layer:** Amazon QuickSight connects to Redshift to provide interactive fraud analytics dashboards.

## Technology Stack

- **Data Ingestion:** Apache Kafka, Amazon Kinesis Data Streams, Amazon Kinesis Firehose
- **Data Storage:** Amazon S3 (Data Lake), Amazon Redshift (Data Warehouse)
- **Data Processing:** AWS Glue (PySpark)
- **Machine Learning:** Python, Pandas, Scikit-learn, XGBoost
- **Orchestration:** AWS Step Functions
- **Serverless Compute:** AWS Lambda
- **Alerting:** Amazon SNS, Amazon SES
- **Analytics:** Amazon QuickSight
- **Infrastructure & Security:** Amazon VPC, EC2, IAM, CloudWatch, Secrets Manager

## Synthetic Data Generation

A custom Python simulator generates synthetic financial transactions with labeled fraud cases for model training/testing. Fraud scenarios include:
- **Account Takeover**
- **Card Testing**
- **Velocity Attack**
- **Impossible Travel**
- **Synthetic Identity**

## Machine Learning Model

- **Algorithm:** XGBoost (Extreme Gradient Boosting)  
- **Metrics:**  
  - Accuracy: `97.91%`  
  - Precision: `84.12%`  
  - Recall: `97.50%`  
  - F1-Score: `90.32%`  
  - Cross-Validation F1: `94.17%`  
  - AUC (ROC): `1.00`  

## Automated Alerting Workflow

Orchestrated by AWS Step Functions:
1. Run ETL in AWS Glue
2. Run ML Inference Job
3. Check Redshift for new fraud
4. Trigger SNS alerts via Lambda

## Analytics and Visualization

Amazon QuickSight dashboard includes:
- KPIs (TTV, Fraud Rate, Loss)
- Fraud distribution charts
- Model performance trends
- High-risk transaction tracking

## Deployment Guide

1. Clone repository  
2. Set up AWS infrastructure (VPC, S3, Redshift, Kinesis, Glue, Lambda)  
3. Launch Kafka cluster on EC2  
4. Configure Glue jobs & Step Functions  
5. Run producer to stream data  
6. Connect QuickSight to Redshift

## Project Structure

```text
.
├── aws_glue_scripts/
│   ├── etl_cleaning_job.py
│   └── ml_inference_job.py
├── data_simulator/
│   └── synthetic_data_generator.py
├── kafka/
│   ├── docker-compose.yml
│   ├── producer.py
│   └── consumer.py
├── lambda_function/
│   └── send_fraud_alert.py
├── Architecture/
│   └── fraud_arch.png
└── documentation/
    └── Full_Project_Documentation.pdf 
```

## Limitations and Future Work

**Limitations:**
- Synthetic data may not match real-world complexity
- Near real-time, not true real-time
- Static model without auto-retraining

**Future Work:**
- Add streaming inference
- Integrate MLOps with SageMaker
- Implement explainable AI (SHAP)

## Contributors

- Seif El-Deen Gaber  
- Omar Adel  
- Yasmine Samir  
- Abdelrahman Wael  
- Ahmed Srour  

**Project Supervisor:** Ibrahim Mohamed


