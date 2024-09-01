import json
import psycopg2
from kafka import KafkaConsumer

# Database connection parameters
db_params = {
    'database': 'ecommerce-kafka',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Kafka consumer configuration
kafka_params = {
    'bootstrap_servers': 'localhost:9092',
    'auto_offset_reset': 'earliest'
}

# Define the topic names
topics = ['users']

###########NOTE HERE that even though there is a dicitionary here, I had to run the code once for every topic individually.

# Establish a connection to the database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Function to consume and insert data
def consume_and_insert(topic):
    consumer = KafkaConsumer(topic, **kafka_params)
    for message in consumer:
        try:
            msg = json.loads(message.value.decode('utf-8'))
            values = []
            columns = ', '.join(msg.keys())
            placeholders = ', '.join(['%s'] * len(msg))
            sql = f"INSERT INTO {topic} ({columns}) VALUES ({placeholders})"
            # Handle the conversion and check if value is convertible
            for val in msg.values():
                if val == "":
                    values.append(None)
                else:
                    values.append(val)
            cur.execute(sql, values)
            conn.commit()
            print(f"Inserted message from topic {topic} into database.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()  # Rollback the current transaction if error occurs

# Process messages for each topic
for topic in topics:
    consume_and_insert(topic)

# Close the database connection
cur.close()
conn.close()
