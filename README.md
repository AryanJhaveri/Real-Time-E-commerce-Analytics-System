# Real-Time-E-commerce-Analytics-System

## Overview
This project simulates a real-time e-commerce data processing pipeline using Apache Kafka and PostgreSQL. The project is designed to mimic the ingestion of live data streams into a Kafka cluster, followed by data storage in PostgreSQL, normalization, and subsequent analysis using SQL and Power BI. The pipeline handles multiple data sources including distribution centers, events, inventory items, order items, orders, products, and users.

## Repository Structure

```plaintext
/Kafka-Ecommerce-Analytics
│
├── /data_ingestion
│   ├── kafka_producer_distribution_centers.py
│   ├── kafka_producer_events.py
│   ├── kafka_producer_inventory_items.py
│   ├── kafka_producer_order_items.py
│   ├── kafka_producer_orders.py
│   ├── kafka_producer_products.py
│   └── kafka_producer_users.py
│
├── /data_pipeline
│   ├── kafka_to_postgres.py
│   ├── tablecreation_postgre.sql
│   ├── normalisation_population.sql
└── analysis.sql
```


## Start Kafka
### 1\. Download Kafka

-   Visit the [Apache Kafka website](https://kafka.apache.org/downloads).
-   Download the latest Kafka release. It comes as a `.tgz` file for Unix-like systems or a `.zip` file for Windows.

### 2\. Extract Kafka

-   Once downloaded, extract the Kafka binaries from the `.tgz` or `.zip` file to a directory of your choice on your local machine.

### 3\. Verify Java Installation

-   Kafka is written in Java, so you need to have Java installed on your machine.
-   To check if Java is installed and determine its version, open a terminal (Command Prompt or PowerShell on Windows, Terminal app on macOS, or shell on Linux/Unix) and run:
`java -version`


## Configuration

### 1\. Open the Kafka `config` folder

-   Navigate to `C:\kafka_2.13-3.7.0\config`.

### 2\. Configure `zookeeper.properties`

-   Open `zookeeper.properties` with a text editor like Notepad.
-   Locate the line `dataDir=/tmp/zookeeper` and change the path `/tmp/zookeeper` to a path where you want ZooKeeper to store its data, for example `C:\kafka-data\zookeeper`.
-   Save and close the file.

### 3\. Create the ZooKeeper data directory

-   Create the directory you specified for `dataDir` in the `zookeeper.properties` file (e.g., `C:\kafka-data\zookeeper`).

### 4\. Configure `server.properties`

-   Open `server.properties` with a text editor.
-   Locate the line that starts with `log.dirs=` and change the path `/tmp/kafka-logs` to a path where you want Kafka to store its logs, for example `C:\kafka-data\kafka-logs`.
-   Optionally, set a `broker.id` that is unique to each Kafka server in your cluster. For a single development server, you can leave it as `broker.id=0`.
-   Save and close the file.

### 5\. Create the Kafka log directory

-   Create the directory you specified for `log.dirs` in the `server.properties` file (e.g., `C:\kafka-data\kafka-logs`).

With these configurations, you have set up the basic directory structure that Kafka and ZooKeeper will use for storing data.


## Start Services

### 1\. Start Zookeeper Service

Zookeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. Kafka uses it to manage the cluster state and configurations.

#### 1.1 Start Zookeeper:

-   Open a new terminal or command prompt window.
-   Navigate to the Kafka directory where you extracted the Kafka binaries.
-   Run the Zookeeper server using the following command:

For Windows:
`.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties`

### 2\. Start Kafka Service

#### 2.1 Start Kafka Server:

-   Open another new terminal or command prompt window.
-   Navigate to the Kafka directory if you're not already there.
-   Start the Kafka server using the following command:

For Windows:
`.\bin\windows\kafka-server-start.bat .\config\server.properties`


## Creating Staging Tables in PostgreSQL

Before ingesting data, staging tables need to be created in PostgreSQL to store the raw data from Kafka topics. The staging tables reflect the schema of the incoming data and act as an intermediary storage layer before the data is normalized.

### 1\. Run the SQL Script

-   The SQL script `tablecreation_postgre.sql` in the `/data_pipeline` directory contains the necessary commands to create staging tables for all the Kafka topics.
-   Connect to your PostgreSQL database using a tool like pgAdmin or psql and run the script to create the tables.


## Creating Topics

### 1\. Create New Topics

Use the `kafka-topics.sh` script to create new topics. Run these commands in a new command prompt window. For example, to create a topic named `distribution_centers`, you would use:

`kafka-topics.sh --create --topic distribution_centers --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1`

Repeat this step to create all the necessary topics corresponding to the data sources.


## Ingesting Data from CSV

Each Kafka producer script in the `/data_ingestion` directory is responsible for reading data from a specific CSV file and sending it to the corresponding Kafka topic.

### 1\. Overview of Producer Script

Here's a basic outline of what the producer script will do:

1.  Read the CSV file line by line.
2.  Convert each line into a dictionary (to simulate a JSON object).
3.  Send each JSON object to the Kafka topic named 'distribution_centers'.

### 2\. Template for the Script

You'll need to replace `YOUR_BOOTSTRAP_SERVER` with the actual address of your Kafka server (since you're running Kafka locally, it should be `localhost:9092`) and the path to your CSV file with the actual path where the file is located on your system.

Refer to the Python scripts in the `/data_ingestion` folder for the actual implementation.


## Connection to PostgreSQL

The script `kafka_to_postgres.py` in the `/data_pipeline` directory will:

-   Connect to Kafka.
-   Subscribe to the relevant topics.
-   Read messages from each topic.
-   Insert the messages into the corresponding PostgreSQL table.

You can run this script after starting Kafka and Zookeeper to start ingesting data into the staging tables.
