Automated Fraud Alert System
This project provides a serverless solution on AWS to automatically detect fraudulent transactions in Amazon Redshift and notify customers via email using Amazon SES.
Architecture Overview
The system is event-driven and uses a stack of managed AWS services for security, scalability, and cost-efficiency.
code
Code
┌────────────────────┐      ┌─────────────────┐
│  Amazon EventBridge  ├─────►│   AWS Lambda    │
│ (Scheduled Trigger)  │      │ (Python Script) │
└────────────────────┘      └───────┬─────────┘
                                    │
                           ┌────────┼────────┐
                           ▼        ▼        ▼
┌───────────────────┐    ┌─────────────┐    ┌─────────────┐
│ Amazon Redshift   │◄───┤ AWS Secrets ├───►│ Amazon SES  │
│ (Read/Write Data) │    │   Manager   │    │ (Send Email)│
└───────────────────┘    └─────────────┘    └─────────────┘
Key Features
Serverless: No servers to manage; only pay for what you use.
Secure: Uses IAM Roles and AWS Secrets Manager for credential handling. No hardcoded secrets.
Scalable: The architecture handles growing transaction volumes seamlessly.
Idempotent: A state-tracking flag (email_sent) in Redshift prevents sending duplicate alerts.
Technology Stack
Compute: AWS Lambda (Python 3.9+)
Database: Amazon Redshift
Email Service: Amazon SES
Scheduling: Amazon EventBridge
Security: AWS IAM & AWS Secrets Manager
Setup & Configuration
To deploy this system, you will need to set up the following AWS resources and configure the Lambda function with the correct environment variables.
Quick Setup Steps
Create Redshift Table: Set up the predicted_fraud table in your database.
Store Credentials: Store your Redshift database credentials in AWS Secrets Manager.
Create IAM Role: Create an IAM Role for the Lambda function with permissions for SES, Redshift Data API, and Secrets Manager.
Deploy Lambda Function: Deploy the lambda_function.py script and configure the environment variables below.
Create EventBridge Trigger: Set up a scheduled rule (e.g., rate(5 minutes)) to trigger the Lambda function.
Required Environment Variables
The Lambda function requires the following environment variables to be set:
Key	Description
SENDER_EMAIL	The verified "From" email address in Amazon SES.
REDSHIFT_CLUSTER_ID	The identifier of your target Redshift cluster.
REDSHIFT_DATABASE	The name of the database to connect to.
SECRET_ARN	The full ARN of the secret in Secrets Manager holding the DB credentials.
