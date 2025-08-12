import json
import sys
import time
import uuid
import logging
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import boto3
from botocore.exceptions import ClientError

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output
        # logging.FileHandler("kafka_kinesis_forwarder.log")  # Uncomment to log to file
    ]
)
logger = logging.getLogger(__name__)

# --- Configuration Section ---
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092', 'localhost:9093', 'localhost:9094']
KAFKA_TOPIC_NAME = 'transactions'
KAFKA_CONSUMER_GROUP = 'kinesis-forwarder-group'
AWS_REGION = 'eu-north-1'
KINESIS_STREAM_NAME = 'kinesis_data_stream'

# --- Batching & Throttling Configuration ---
BATCH_SIZE = 500
BATCH_TIMEOUT = 5
MAX_RETRIES = 5
RETRY_DELAY = 1
RATE_LIMIT_DELAY = 0.5

# --- Initialization ---
logger.info("--- Kafka to Kinesis Forwarder (Throttled) ---")
kinesis_client = boto3.client('kinesis', region_name=AWS_REGION)

try:
    consumer = KafkaConsumer(
        KAFKA_TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        auto_offset_reset='earliest',
    )
except NoBrokersAvailable as e:
    logger.error("Kafka brokers are not available. Check your server connections.")
    sys.exit(1)

logger.info(f"🚀 Starting to consume messages. Rate limit delay: {RATE_LIMIT_DELAY}s.")

# --- Function to send batch to Kinesis ---
def send_batch_to_kinesis(batch):
    if not batch:
        return True

    records_to_retry = batch
    for attempt in range(MAX_RETRIES + 1):
        if not records_to_retry:
            break

        logger.info(f"  -> [KINESIS] Attempt {attempt+1}: Sending a batch of {len(records_to_retry)} records...")
        try:
            response = kinesis_client.put_records(
                StreamName=KINESIS_STREAM_NAME,
                Records=records_to_retry
            )
            failed_count = response.get('FailedRecordCount', 0)
            if failed_count == 0:
                logger.info(f"  ✅ Batch sent successfully.")
                return True

            logger.warning(f"  ⚠️  Partial failure. {failed_count} records failed. Retrying...")
            failed_records = []
            for i, record in enumerate(response['Records']):
                if 'ErrorCode' in record:
                    failed_records.append(records_to_retry[i])
            records_to_retry = failed_records
            time.sleep(RETRY_DELAY)
        except ClientError as e:
            logger.error(f"  ❌ AWS ClientError on attempt {attempt+1}: {e}")
            time.sleep(RETRY_DELAY)
    return False

# --- Main loop to consume and forward messages ---
buffer = []
last_batch_time = time.time()

for message in consumer:
    try:
        msg_value = json.loads(message.value.decode('utf-8'))
    except Exception as e:
        logger.warning(f"⚠️  Skipping invalid JSON message: {e}")
        continue

    buffer.append({
        'Data': json.dumps(msg_value),
        'PartitionKey': str(uuid.uuid4())
    })

    now = time.time()
    time_passed = now - last_batch_time
    if len(buffer) >= BATCH_SIZE or time_passed >= BATCH_TIMEOUT:
        logger.info(f"\n📦 Sending batch of {len(buffer)} messages to Kinesis...")
        success = send_batch_to_kinesis(buffer)
        if success:
            buffer = []
            last_batch_time = time.time()
            time.sleep(RATE_LIMIT_DELAY)
        else:
            logger.error("❌ ERROR: Failed to send batch after retries. Keeping data in buffer."