# Automated Fraud Alert System

A serverless AWS project to automatically detect fraudulent transactions in Amazon Redshift and notify customers via email using Amazon SES.

## How It Works

This system operates on a simple, automated workflow:

1.  **Trigger:** An **Amazon EventBridge** rule runs on a schedule (e.g., every 5 minutes).
2.  **Execute:** The trigger invokes an **AWS Lambda function** containing the Python logic.
3.  **Query:** The function queries an **Amazon Redshift** table for new transactions marked as fraudulent.
4.  **Notify:** Using **Amazon SES**, it sends a formatted HTML email to the affected customer.
5.  **Update:** The function marks the transaction record as processed in Redshift to prevent duplicate emails.

*Credentials are stored securely in **AWS Secrets Manager** and accessed via an **IAM Role**.*

## Key Features

-   ✅ **Serverless:** No servers to manage. Pay only for what you use.
-   ✅ **Secure:** Uses IAM Roles and AWS Secrets Manager instead of hardcoded keys.
-   ✅ **Automated:** Runs on a schedule without manual intervention.
-   ✅ **Reliable:** State management in Redshift prevents sending duplicate alerts.

---

## Quick Start Guide

To deploy this system, you need an AWS account and the following resources configured.

### 1. Set up AWS Resources

-   **Amazon Redshift Table:** Create a table named `predicted_fraud` with columns like `transaction_id`, `email`, `is_fraud_pred`, and `email_sent`.
-   **IAM Role:** Create a role for the Lambda function with permissions for SES, Redshift Data API, and Secrets Manager.
-   **AWS Secrets Manager:** Store your Redshift database credentials in a new secret.

### 2. Deploy the Lambda Function

-   Create a new **AWS Lambda function** using a Python 3.9+ runtime.
-   Use the IAM Role created in the previous step.
-   Copy the code from `lambda_function.py` into the function's code editor.
-   Set the function **Timeout** to **1 minute**.

### 3. Configure Environment Variables

In your Lambda function's configuration, set the following environment variables:

| Key                 | Description                                                  |
| :------------------ | :----------------------------------------------------------- |
| `SENDER_EMAIL`      | Your verified "From" email address in Amazon SES.             |
| `REDSHIFT_CLUSTER_ID` | The identifier of your target Redshift cluster.              |
| `REDSHIFT_DATABASE` | The name of the database to connect to.                      |
| `SECRET_ARN`        | The full ARN of the secret holding the DB credentials. |

### 4. Create the Trigger

-   In the Lambda console, add an **EventBridge (CloudWatch Events)** trigger.
-   Set the schedule expression, for example: `rate(5 minutes)`.

Your system is now live. It will automatically check for fraud and send alerts based on your schedule.
