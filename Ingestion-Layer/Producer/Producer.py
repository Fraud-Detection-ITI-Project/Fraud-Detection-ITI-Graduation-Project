from kafka import KafkaProducer
import json
import pandas as pd
import time

df = pd.read_csv('/home/ec2-user/kafka-cluster/transactions_egypt_centric_final_v7.csv')

print("🛠️ Configuring Kafka Producer with custom batching (500 records per batch)...")
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
    key_serializer=lambda x: json.dumps(x).encode('utf-8'),
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),

    batch_size=65536,
    linger_ms=20
)

records = df.to_dict(orient='records')
batch_size_records = 500

print(f" Preparing to send {len(records)} records in batches of {batch_size_records}...")

start = time.time()

for i in range(0, len(records), batch_size_records):
    batch = records[i:i + batch_size_records]
    for record in batch:
        producer.send('transactions', key='stream', value=record)

    producer.flush()
    print(f"📤 Sent records {i} to {i + len(batch) - 1}")

end = time.time()
print(f" All records sent in {end - start:.2f} seconds.")