import boto3
import json
import os
import time

# Initialize clients
ses_client = boto3.client('ses')
redshift_data_client = boto3.client('redshift-data')

# Get configuration from environment variables
SENDER_EMAIL = os.environ['SENDER_EMAIL']
REDSHIFT_CLUSTER_ID = os.environ['REDSHIFT_CLUSTER_ID']
REDSHIFT_DATABASE = os.environ['REDSHIFT_DATABASE'] 
SECRET_ARN = os.environ['SECRET_ARN']
# --- THIS IS THE CORRECTED LINE ---
REDSHIFT_TABLE = 'predicted_fraud' 

def lambda_handler(event, context):
    print("Function triggered. Checking Redshift for new fraud...")

    # SQL query to find fraudulent transactions that have not been processed
    select_sql = f"""
        SELECT 
            transaction_id, 
            email
        FROM {REDSHIFT_TABLE}
        WHERE is_fraud_pred = 1 AND email_sent = false
        LIMIT 10;
    """

    try:
        response = redshift_data_client.execute_statement(
            ClusterIdentifier=REDSHIFT_CLUSTER_ID,
            Database=REDSHIFT_DATABASE,
            SecretArn=SECRET_ARN,
            Sql=select_sql
        )
        query_id = response['Id']
        print(f"Executed SELECT query. Query ID: {query_id}")

        # Wait for the query to finish
        status = ''
        while status not in ['FINISHED', 'FAILED', 'ABORTED']:
            time.sleep(1)
            description = redshift_data_client.describe_statement(Id=query_id)
            status = description['Status']
        
        if status != 'FINISHED':
            error_message = description.get('Error', 'Query failed without a specific error message.')
            raise Exception(f"Query did not finish successfully. Status: {status}, Error: {error_message}")

        statement_result = redshift_data_client.get_statement_result(Id=query_id)
        records = statement_result['Records']
        
        if not records:
            print("No new fraudulent transactions found.")
            return

        print(f"Found {len(records)} fraudulent transactions to process.")
        
        processed_ids = []
        for record in records:
            transaction_id = record[0]['stringValue']
            recipient_email = record[1]['stringValue']
            
            # Send the email (using static data for simplicity)
            try:
                # =================== ONLY THIS PART IS MODIFIED ===================
                html_body = f"""
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333; line-height: 1.6;">
                    <p>Dear Valued Customer,</p>
                    <p>We've detected a potentially fraudulent transaction on your account.</p>
                    
                    <h3 style="font-family: Arial, sans-serif; margin-top: 24px; margin-bottom: 12px; font-size: 16px;">Transaction Details:</h3>
                    <p style="margin: 5px 0;"><strong>Amount:</strong> $457.82</p>
                    <p style="margin: 5px 0;"><strong>Merchant:</strong> GlobalTechMart.com</p>
                    <p style="margin: 5px 0;"><strong>Date:</strong> 2023-10-27</p>
                    <p style="margin: 5px 0;"><strong>Transaction ID:</strong> {transaction_id}</p>

                    <h3 style="font-family: Arial, sans-serif; margin-top: 24px; margin-bottom: 12px; font-size: 16px;">What You Need To Do Now</h3>
                    <ol style="padding-left: 20px; margin: 0;">
                        <li style="margin-bottom: 10px;"><strong>Do not click any links in this email to log in.</strong></li>
                        <li style="margin-bottom: 10px;">Log in to your account and review your recent transaction history.</li>
                        <li style="margin-bottom: 10px;">You will be prompted to confirm if you authorized this transaction.</li>
                    </ol>

                    <p style="margin-top: 24px;">For more information, please see our <a href="https://yourcompany.com/security-info" style="color: #007bff;">fraud protection guide</a>.</p>

                    <p style="margin-top: 24px;">Thank you,<br>The SecureBank Corp Security Team</p>

                    <hr style="border: none; border-top: 1px solid #e0e0e0; margin-top: 24px;">
                    <p style="font-size: 12px; color: #888;">© 2023 SecureBank Corp. All rights reserved.</p>
                </div>
                """
                # ==================================================================
                
                ses_client.send_email(
                    Source=SENDER_EMAIL,
                    Destination={'ToAddresses': [recipient_email]},
                    Message={ 'Subject': {'Data': 'Security Alert'}, 'Body': {'Html': {'Data': html_body}} }
                )
                print(f"Email sent for transaction {transaction_id}")
                processed_ids.append(transaction_id)
            except Exception as e:
                print(f"Error sending email for transaction {transaction_id}: {e}")

        # Update the database for the records we processed
        if processed_ids:
            quoted_ids = [f"'{_id}'" for _id in processed_ids]
            id_list_for_sql = ','.join(quoted_ids)
            update_sql = f"UPDATE {REDSHIFT_TABLE} SET email_sent = true WHERE transaction_id IN ({id_list_for_sql});"
            print(f"Updating records: {id_list_for_sql}")
            redshift_data_client.execute_statement(
                ClusterIdentifier=REDSHIFT_CLUSTER_ID,
                Database=REDSHIFT_DATABASE,
                SecretArn=SECRET_ARN,
                Sql=update_sql
            )
            print("Update complete.")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e