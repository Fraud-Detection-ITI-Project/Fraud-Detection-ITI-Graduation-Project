Of course. Here is the complete documentation in Markdown format. You can copy and paste this content directly into a README.md file.

Egypt-Centric Financial Fraud Detection Dataset Generator
Overview

This project contains a sophisticated Python script for generating a large-scale, realistic, synthetic dataset of financial transactions. The dataset is specifically tailored to the Egyptian market, using real-world Egyptian bank names, merchant categories, and geographical locations.

The primary purpose of this script is to create high-quality, labeled data suitable for training and evaluating machine learning models for fraud detection. It simulates both normal customer behavior and a wide variety of common and complex fraudulent activities.

Key Features

Egypt-Centric: Utilizes Egyptian bank names, popular merchants, common email domains, and geographically accurate coordinates for cities and districts across Egypt.

Realistic Personas: Simulates individual "personas," each with their own spending habits, home location, tenure, and transaction history.

10 Diverse Fraud Scenarios: Goes beyond simple fraud flags to model ten distinct and realistic fraud patterns, including account takeovers, card testing, velocity attacks, impossible travel, and synthetic identity fraud.

Rich Feature Set: Generates a comprehensive set of over 35 features for each transaction, including transactional data, customer details, merchant information, geo-spatial calculations, and behavioral metrics.

Highly Configurable: Key parameters like the number of transactions, fraud rate, and date range can be easily modified at the top of the script.

Labeled Data: Each transaction is explicitly labeled with an is_fraud flag (True/False), making it ready for supervised machine learning tasks.

Dynamic Simulation: The script simulates transactions over a specified time period, maintaining state for each persona (e.g., last transaction time and location) to generate time-dependent features.

Getting Started
Prerequisites

You need to have Python 3 installed. Additionally, you'll need to install the following Python libraries:

code
Bash
download
content_copy
expand_less

pip install Faker numpy
Configuration

Before running the script, you can customize the data generation process by modifying the configuration variables in the Configuration section at the top of generate_transactions.py.

Variable	Default Value	Description
OUTPUT_CSV_FILE	transactions_...v3.csv	The name of the output CSV file where the data will be saved.
NUM_TRANSACTIONS	500000	The total number of transaction records to generate.
FRAUD_PERSONA_RATE	0.11	The approximate probability (11%) that a newly created customer persona will be a fraudulent one.
NUM_INITIAL_MERCHANTS	300	The number of legitimate merchants to create in the simulation.
NUM_FRAUD_MERCHANTS	5	The number of fraudulent merchants to create for use in specific fraud scenarios.
START_DATE	2023-01-01	The beginning of the time window for the transaction simulation.
END_DATE	2023-12-31	The end of the time window for the transaction simulation.
Running the Script

To generate the dataset, simply run the script from your terminal:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python generate_transactions.py

The script will print its progress to the console, indicating each transaction being written. Upon completion, the output CSV file will be available in the same directory.

Dataset Schema

The generated CSV file contains the following columns, providing a rich set of features for analysis and model training.

Column Name	Data Type	Description
Transaction Info		
transaction_id	String (UUID)	A unique identifier for each transaction.
transaction_timestamp	String (ISO)	The date and time of the transaction in UTC (ISO 8601 format, e.g., YYYY-MM-DDTHH:MM:SSZ).
transaction_amount	Float	The monetary value of the transaction in EGP.
currency	String	The currency of the transaction (fixed to EGP).
transaction_type	String	The channel of the transaction (POS, ONL, MOB, ATM, QR).
transaction_status	String	The outcome of the transaction (approved, declined, pending).
transaction_hour_of_day	Integer	The hour of the day (0-23) when the transaction occurred.
Customer Info		
customer_id	String (UUID)	A unique identifier for each customer persona.
customer_name	String	The full name of the customer (generated from common Arabic names).
customer_email	String	The customer's email address.
customer_email_domain	String	The domain part of the customer's email (e.g., gmail.com).
customer_tenure_days	Integer	The number of days the customer has been with the bank.
customer_address_change_days	Integer	The number of days since the customer's last address change.
customer_latitude	Float	The latitude of the customer at the time of the transaction.
customer_longitude	Float	The longitude of the customer at the time of the transaction.
Card Info		
card_number_hash	String (SHA256)	A SHA256 hash of the credit/debit card number.
card_type	String	The card scheme (Visa, MasterCard, Meeza).
issuing_bank_name	String	The name of the Egyptian bank that issued the card.
card_entry_method	String	How the card details were captured (e.g., chip, online, contactless_mobile).
cvv_match_result	String	The result of the CVV check (match, no_match).
Merchant Info		
merchant_id	String (UUID)	A unique identifier for each merchant.
merchant_name	String	The name of the merchant, often including its location.
merchant_category	String	The business category of the merchant (e.g., Grocery, Electronics, Restaurants).
merchant_latitude	Float	The latitude of the merchant's location.
merchant_longitude	Float	The longitude of the merchant's location.
merchant_risk_score	Float	A synthetic risk score associated with the merchant (0.0 to 1.0).
Contextual & Behavioral Info		
ip_address	String	The IP address used for the transaction.
ip_proxy_type	String	The type of proxy detected (none, vpn, tor, proxy).
device_id	String (UUID)	A unique identifier for the device used (e.g., phone, computer).
device_os	String	The operating system of the device (Android, iOS, Windows, MacOS).
user_agent	String	The user agent string from the customer's browser or device.
is_international	Boolean	True if the card-issuing country is different from the merchant country.
distance_from_home_km	Float	The Haversine distance (in km) between the customer's home location and the transaction location.
distance_from_last_txn_km	Float	The Haversine distance (in km) between this transaction and the customer's previous transaction.
time_since_last_txn_sec	Integer	The time elapsed in seconds since the customer's last transaction.
is_first_time_customer_merchant	Boolean	True if this is the first time this customer has transacted with this merchant.
Target Label		
is_fraud	Boolean	The target variable. True if the transaction is fraudulent, False otherwise.
Fraud Scenarios Explained

The script simulates the following 10 types of fraudulent behavior, each modeled by a specific FraudPersona class.

Account Takeover (FraudPersona_AccountTakeover): Simulates a classic ATO scenario where a fraudster gains control of a legitimate account. This is characterized by a single, unusually large transaction from a new device and IP address, often using a VPN.

Card Testing (FraudPersona_CardTesting): Models the behavior of testing stolen card details. It generates a rapid burst of very small-value transactions in quick succession from the same IP/device. Early attempts may be approved, while later ones are declined.

Velocity Attack (FraudPersona_VelocityAttack): A fraudster with a new or stolen card makes multiple high-value transactions at different merchants in a short period before the card is blocked.

Impossible Travel (FraudPersona_ImpossibleTravel): Generates two transactions for the same customer. The first is legitimate. The second occurs shortly after but at a geographically impossible distance (e.g., a transaction in Cairo followed minutes later by one in Hurghada), indicating two different individuals are using the card.

Merchant Bust-Out (FraudPersona_MerchantBustOut): A fraudulent persona colludes with a fraudulent merchant. The persona makes several large transactions at this specific complicit merchant to cash out.

Spending Anomaly (FraudPersona_SpendingAnomaly): A legitimate-looking persona suddenly makes a very large purchase in a product category they have never shopped in before (e.g., a customer who only buys groceries suddenly buys EGP 20,000 worth of electronics).

Synthetic Identity (FraudPersona_SyntheticIdentity): A fraudster creates a new account using a mix of real and fake information (synthetic identity). They "warm up" the account with a few small, normal-looking transactions before making a single, massive purchase to "cash out" and disappear. These personas often use high-risk email domains.

Anomalous Hour (FraudPersona_AnomalousHour): Simulates a transaction occurring at a very unusual time for the customer, typically in the middle of the night (e.g., 3 AM), for a significant amount.

Address Change (FraudPersona_AddressChange): Models fraud that occurs immediately after a customer's registered address is changed. A fraudster makes a large online purchase to be shipped to a new, fraudulent address.

Channel Pivot (FraudPersona_ChannelPivot): A customer who exclusively uses one transaction channel (e.g., physical Point-of-Sale POS) suddenly performs a large transaction on a different channel (e.g., Online) from a new device.