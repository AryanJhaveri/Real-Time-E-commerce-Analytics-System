from kafka import KafkaProducer
import csv
import json

# Replace 'localhost:9092' with your Kafka server if it's different
bootstrap_servers = 'localhost:9092'
topic_name = 'inventory_items'

# Initialize a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Path to your CSV file
csv_file_path = 'D:/1_BU/Advanced DBMS/Term Project/data/inventory_items.csv'


def publish_csv_to_kafka(csv_file_path, topic_name):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:  # Specifying encoding here
        reader = csv.DictReader(csvfile)
        for row in reader:
            producer.send(topic_name, row)
            producer.flush()  # Ensure all messages are sent


# Call the function to start sending messages
publish_csv_to_kafka(csv_file_path, topic_name)

# Close the producer when we're done
producer.close()
