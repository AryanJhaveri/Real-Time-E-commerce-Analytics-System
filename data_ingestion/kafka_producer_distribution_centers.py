from kafka import KafkaProducer
import csv
import json

# Replace 'localhost:9092' with your Kafka server if it's different
bootstrap_servers = 'localhost:9092'
topic_name = 'distribution_centers'

# Initialize a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Path to your CSV file
csv_file_path = 'D:/1_BU/Advanced DBMS/Term Project/data/distribution_centers.csv'

# Function to read CSV and publish to Kafka topic
def publish_csv_to_kafka(csv_file_path, topic_name):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            producer.send(topic_name, value=row)
            producer.flush()

# Call the function to start sending messages
publish_csv_to_kafka(csv_file_path, topic_name)

# Close the producer when we're done
producer.close()
