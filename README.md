<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF2400,100:800000&height=350&section=header&text=Cloud-Native%20Real-Time%20Financial%20Fraud%20Detection%20System&fontSize=30&fontColor=ffffff&animation=fadeIn&fontAlign=center&fontAlignY=40&desc=AWS%20•%20Kafka%20•%20Kinesis%20•%20S3%20•%20Glue%20•%20Redshift%20•%20XGBoost%20•%20Lambda%20•%20SNS%20•%20QuickSight%20•%20CloudWatch&descSize=18&descAlign=middle&descAlignY=75" alt="Header">
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-AWS-%23DC143C?logo=amazon-aws&logoColor=white" alt="AWS">
  <img src="https://img.shields.io/badge/Streaming-Apache%20Kafka-231F20?logo=apachekafka&logoColor=white&color=DC143C&labelColor=231F20" alt="Kafka">
  <img src="https://img.shields.io/badge/Streaming-Amazon%20Kinesis-DC143C?logo=amazon-aws&logoColor=white" alt="Kinesis">
  <img src="https://img.shields.io/badge/Data%20Storage-Amazon%20S3-DC143C?logo=amazons3&logoColor=white" alt="S3">
  <img src="https://img.shields.io/badge/Data%20Processing-AWS%20Glue-DC143C?logo=amazon-aws&logoColor=white" alt="AWS Glue">
  <img src="https://img.shields.io/badge/Data%20Warehouse-Amazon%20Redshift-DC143C?logo=amazon-redshift&logoColor=white" alt="Redshift">
  <img src="https://img.shields.io/badge/Monitoring-CloudWatch-DC143C?logo=amazon-aws&logoColor=white" alt="CloudWatch">
  <img src="https://img.shields.io/badge/Alerting-Amazon%20SNS-DC143C?logo=amazon-aws&logoColor=white" alt="SES">
  <img src="https://img.shields.io/badge/Serverless-AWS%20Lambda-DC143C?logo=awslambda&logoColor=white" alt="Lambda">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/ML%20Algorithm-XGBoost-DC143C" alt="XGBoost">
  <img src="https://img.shields.io/badge/Visualization-QuickSight-F2C811?logo=amazon-quicksight&logoColor=DC143C" alt="QuickSight">
</p>

---

## 🚀 Project Overview

This repository contains a comprehensive, cloud-native financial fraud detection system built on Amazon Web Services (AWS). The system ingests, processes, and analyzes high-velocity transaction data to identify and alert on fraudulent activity in near real-time, reducing detection latency from hours to minutes.

> **🎓Capstone Project** - Developed for the Information Technology Institute (ITI) graduation program

### ✨ Key Highlights

- **Real-time Processing**: Sub-minute fraud detection and alerting
- **Event-driven Architecture**: Scalable, serverless, and cost-effective
- **Advanced ML**: 97.91% accuracy with XGBoost algorithm
- **Rich Analytics**: Interactive dashboards and comprehensive monitoring
- **Enterprise Security**: VPC isolation and IAM best practices

## 📋 Table of Contents

- [🏗️ System Architecture](#-system-architecture)
- [💡 Key Features](#-key-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [🤖 Machine Learning Model](#-machine-learning-model)
- [📊 Data Pipeline](#-data-pipeline)
- [🔔 Alerting System](#-alerting-system)
- [📈 Analytics Dashboard](#-analytics-dashboard)
- [📁 Project Structure](#-project-structure)
- [🔒 Security](#-security)
- [📚 Documentation](#-documentation)
- [👥 Contributors](#-contributors)
- [📄 License](#-license)

## 🏗️ System Architecture

<div align="center">
  <img src="Architecture/fraud_arch.png" alt="System Architecture" width="90%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
</div>

### 🏛️ Architectural Layers

| Layer | Purpose | Key Components |
|-------|---------|----------------|
| **Ingestion** | High-throughput data capture | Apache Kafka, Amazon Kinesis, S3 |
| **Processing** | Serverless ETL and ML inference | AWS Glue, Step Functions |
| **Alerting** | Real-time fraud notifications | Lambda, SNS, SES |
| **Analytics** | Business intelligence & monitoring | QuickSight, CloudWatch, Redshift |
| **Security** | Infrastructure protection | VPC, IAM, Secrets Manager |

## 💡 Key Features

### 🚀 High-Performance Ingestion
- **Apache Kafka** cluster for durable message buffering
- **Amazon Kinesis** for scalable stream processing
- **S3 Data Lake** for centralized storage with lifecycle policies

### 🤖 Intelligent Fraud Detection
- **XGBoost Model** with 97.91% accuracy
- **Real-time Inference** on streaming data
- **Multiple Fraud Patterns** detection (account takeover, velocity attacks, etc.)

### 📈 Enterprise Analytics
- **QuickSight Dashboards** for executive reporting
- **CloudWatch Monitoring** with custom metrics
- **Redshift Data Warehouse** optimized for analytical queries

### 🔄 Full Automation
- **Step Functions** orchestration
- **Serverless Architecture** with auto-scaling
- **Error Handling** and retry mechanisms

## 🛠️ Technology Stack

<details>
<summary><b>🔧 Core Technologies</b></summary>

| Category | Technologies |
|----------|--------------|
| **Cloud Platform** | Amazon Web Services (AWS) |
| **Data Streaming** | Apache Kafka, Amazon Kinesis |
| **Data Storage** | Amazon S3, Amazon Redshift |
| **Data Processing** | AWS Glue (PySpark) |
| **Machine Learning** | Python, XGBoost, Scikit-learn, Pandas |
| **Orchestration** | AWS Step Functions |
| **Serverless** | AWS Lambda |
| **Messaging** | Amazon SNS, Amazon SES |
| **Analytics** | Amazon QuickSight |
| **Security** | VPC, IAM, Secrets Manager |
| **Monitoring** | Amazon CloudWatch |

</details>

## 🤖 Machine Learning Model

### 📊 Model Performance

<div align="center">

| Metric | Score | Description |
|--------|--------|-------------|
| **Accuracy** | `97.91%` | Overall classification accuracy |
| **Precision** | `84.12%` | True fraud / (True fraud + False positive) |
| **Recall** | `97.50%` | True fraud / (True fraud + False negative) |
| **F1-Score** | `90.32%` | Harmonic mean of precision and recall |
| **Cross-Val F1** | `94.17%` | Cross-validated F1 score |
| **AUC-ROC** | `1.00` | Area under the ROC curve |

</div>

### 🕵️ Fraud Scenarios Detected

- **Account Takeover**: Unauthorized access patterns
- **Card Testing**: Small transaction probing
- **Velocity Attacks**: Rapid transaction sequences  
- **Impossible Travel**: Geographically impossible transactions
- **Synthetic Identity**: Artificially created identities

## 📊 Data Pipeline

### 🔄 Processing Workflow

```mermaid
graph LR
    A[Transaction Data] --> B[Kafka Producer]
    B --> C[Kinesis Stream]
    C --> D[S3 Data Lake]
    D --> E[Glue ETL Job]
    E --> F[ML Inference]
    F --> G[Redshift DW]
    G --> H{Fraud Detected?}
    H -->|Yes| I[Send Alert]
    H -->|No| J[Store Results]
    G --> K[QuickSight Dashboard]
```

### 📈 Data Flow Stages

1. **Ingestion**: Kafka → Kinesis → S3
2. **Processing**: Glue ETL → Feature Engineering
3. **Inference**: XGBoost Model → Fraud Scoring
4. **Storage**: Results → Redshift Data Warehouse
5. **Alerting**: Lambda → SNS → Email Notifications
6. **Analytics**: QuickSight → Interactive Dashboards

## 🔔 Alerting System

### 📧 Alert Configuration

The system sends immediate email alerts when fraud is detected:

- **High Priority**: Fraud score > 0.9
- **Medium Priority**: Fraud score 0.7 - 0.9
- **Low Priority**: Fraud score 0.5 - 0.7

### 🚨 Alert Content

- Transaction details
- Fraud probability score
- Detected patterns
- Recommended actions

## 📈 Analytics Dashboard

### 📊 Key Performance Indicators

- **Transaction Volume**: Real-time processing metrics
- **Fraud Detection Rate**: Percentage of transactions flagged
- **False Positive Rate**: Model accuracy indicators
- **Response Time**: Alert latency measurements

### 📋 Dashboard Sections

1. **Executive Summary**: High-level KPIs and trends
2. **Fraud Analysis**: Detailed fraud pattern breakdowns
3. **Model Performance**: ML model accuracy and drift monitoring
4. **Operational Metrics**: System health and performance

### 📊 Key Insights & Analytics

Our QuickSight dashboard provides comprehensive fraud detection insights including:

- **Total Transaction Value**: Real-time transaction volume monitoring
- **Total Transaction Count**: Transaction frequency analysis
- **Fraud Rate Percentage**: System-wide fraud detection rates
- **Fraud Loss Value**: Financial impact assessment
- **Transaction Status Breakdown**: Status distribution analytics
- **Customer Count by Address Change Risk**: Risk profiling by address changes
- **Fraud Count by Dimension**: Pivotable bar chart for multi-dimensional analysis
- **Model Precision**: ML model accuracy metrics
- **False Positive Rate**: Model performance indicators
- **False Positive Rate Over Time**: Temporal FPR trend analysis
- **Fraud Count by Merchant Risk Score**: Merchant-based risk assessment

### 📸 Dashboard Screenshots

<div align="center">
  <img src="Insights/1.png" alt="Dashboard Analytics 1" width="15%" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); margin: 10px;">
  <img src="Insights/2.png" alt="Dashboard Analytics 2" width="60%" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); margin: 10px;">
</div>

<div align="center">
  <img src="Insights/3.png" alt="Dashboard Analytics 3" width="60%" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); margin: 10px;">
  <img src="Insights/4.png" alt="Dashboard Analytics 4" width="60%" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); margin: 10px;">
</div>

<div align="center">
  <img src="Insights/5.png" alt="Dashboard Analytics 5" width="60%" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); margin: 10px;">
</div>

## 📁 Project Structure

```
Fraud-Detection-ITI-Graduation-Project/
├── AWS GLUE/
│   ├── ETL JOB
│   └── ML Prediction Job
├── Architecture/
│   └── fraud_arch.png
├── Data Warehouse/
│   └── Data Warehouse.png
├── Docs/
│   └── Real-Time Financial Fraud De...
├── Email-Alert/
│   ├── Alert-Lambda.py
│   └── README.md
├── Ingestion-Layer/
│   ├── Consumer
│   ├── kafka-configs
│   ├── Producer
│   └── fraud_data_generator
├── .env
├── docker-compose.yml
├── Insights/
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   └── 5.png
├── Machine Learning/
│   ├── Fraud-Detection-Model.ipynb
│   ├── xgb_fraud_model.pkl
│   ├── xgb_fraud_model_pkl_4
│   └── README.md
```

## 🔒 Security

### 🛡️ Security Measures

- **VPC Isolation**: All resources within private subnets
- **IAM Least Privilege**: Role-based access control
- **Data Encryption**: At rest (S3, Redshift) and in transit (TLS)
- **Secrets Management**: AWS Secrets Manager for credentials
- **Network Security**: Security groups and NACLs
- **Audit Logging**: CloudTrail for API calls

### 🔐 Security Best Practices

- Regular security assessments
- Automated vulnerability scanning
- Multi-factor authentication
- Regular credential rotation

## 📚 Documentation

**[📖 Real-Time Financial Fraud Detection System](Docs/Real-Time%20Financial%20Fraud%20Detection%20System.pdf)**

Comprehensive project documentation including detailed system architecture, implementation details, and technical specifications.

## 🚧 Limitations & Future Work

### ⚠️ Current Limitations

- Synthetic data may not match real-world complexity
- Near real-time processing (not true real-time)
- Static model without automated retraining
- Limited to financial transaction fraud

### 🔮 Future Enhancements

- **MLOps Integration**: Automated model retraining with SageMaker
- **Explainable AI**: SHAP integration for model interpretability
- **True Real-time**: Streaming ML inference with Kinesis Analytics
- **Multi-cloud**: Support for Azure and GCP
- **Advanced Fraud Types**: Credit card, insurance, and identity fraud

## 👥 Contributors

- Seif El-Deen Gaber
- Omar Adel
- Yasmine Samir
- Abdelrahman Wael
- Ahmed Srour

**Project Supervisor:** Ibrahim Mohamed

### 🎓 Institution

**Information Technology Institute (ITI)**  
*Big Data and Data Science Track*

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
<p align="left">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</p>
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF2400,100:800000&height=120&section=footer" alt="Footer">
</div>
<div align="center">
**If this project helped you, please give it a star!**
</div>
