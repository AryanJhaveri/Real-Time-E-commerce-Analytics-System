# Real-Time-E-commerce-Analytics-System

## Overview
This project simulates a real-time e-commerce data processing pipeline using Apache Kafka and PostgreSQL. The project is designed to mimic the ingestion of live data streams into a Kafka cluster, followed by data storage in PostgreSQL, normalization, and subsequent analysis using SQL and Power BI. The pipeline handles multiple data sources including distribution centers, events, inventory items, order items, orders, products, and users.

## Table of Contents
- [Overview](#overview)
- [Start Kafka](#start-kafka)
  - [Download Kafka](#1-download-kafka)
  - [Extract Kafka](#2-extract-kafka)
  - [Verify Java Installation](#3-verify-java-installation)
- [Configuration](#configuration)
  - [Open the Kafka `config` Folder](#1-open-the-kafka-config-folder)
  - [Configure `zookeeper.properties`](#2-configure-zookeeperproperties)
  - [Create the ZooKeeper Data Directory](#3-create-the-zookeeper-data-directory)
  - [Configure `server.properties`](#4-configure-serverproperties)
  - [Create the Kafka Log Directory](#5-create-the-kafka-log-directory)
- [Start Services](#start-services)
  - [Start Zookeeper Service](#1-start-zookeeper-service)
  - [Start Kafka Service](#2-start-kafka-service)
- [Creating Staging Tables in PostgreSQL](#creating-staging-tables-in-postgresql)
  - [Run the SQL Script](#1-run-the-sql-script)
- [Creating Topics](#creating-topics)
  - [Create New Topics](#1-create-new-topics)
- [Ingesting Data from CSV](#ingesting-data-from-csv)
  - [Overview of Producer Script](#1-overview-of-producer-script)
  - [Template for the Script](#2-template-for-the-script)
- [Connection to PostgreSQL](#connection-to-postgresql)
- [Normalization](#normalization)
  - [Staging Tables](#staging-tables)
  - [Normalized Design](#normalized-design)
  - [Normalization Process](#normalization-process)
  - [Populating the Normalized Design](#populating-the-normalized-design)
- [Data Analysis](#data-analysis)
- [Final Notes](#final-notes)
- [Contributing](#contributing)


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

## Normalization 

### Staging Tables

Here's an overview of the staging tables:
![image](https://github.com/user-attachments/assets/714d1693-218b-4dff-837c-c2f3aef7b6c9)


Each staging table represents raw, unprocessed data as ingested from Kafka topics. The data from these tables is then normalized.

### Normalized Design

The normalized design restructures the staging tables into a set of related tables that eliminate redundancy and improve data integrity. The process involves creating multiple related tables, each storing data with minimal redundancy.

![image](https://github.com/user-attachments/assets/152e9c48-91ff-4b91-aa7b-49bb018ea0f7)

The ERD diagram above represents the normalized database structure.

### Normalization Process
The normalization process was aimed at optimizing the database for efficient data storage, eliminating redundancy, and ensuring data integrity. Below is a summary of the key changes made during normalization:

1.  **Location Table**:
    -   **Consolidation**: Location details were originally spread across the `events`, `users`, and `distribution_centers` tables. A new `location` table was created to centralize this information.
    -   **Hierarchy**: To avoid redundancy and potential discrepancies, a hierarchical structure was implemented where each location links to a city, each city links to a state, and each state links to a country. This ensures that each city is correctly associated with a single state and country.
    -   **Bridge Table**: A bridge table was introduced to manage the many-to-many relationship between `users` and `locations`, as each user can have multiple locations and vice versa.
2.  **Users Table**:
    -   **Location Removal**: Location details were moved to the new `location` table, while the remaining fields in the `users` table are dependent solely on `user_id`.
    -   **Unique Email**: It was assumed that each `user_id` is associated with a unique email address.
3.  **Events Tables**:
    -   **Vertical Partitioning**: The `events` table was split into core information in the main `events` table, location details moved to the `location` table, and rarely queried data was placed in an `events_extra` table.
4.  **Distribution Centers**:
    -   **Minimal Changes**: The primary change involved connecting the `distribution_centers` table to the `location` table for centralized location management.
5.  **Orders and Order Items**:
    -   **Separation of Concerns**: The `orders` table now contains details related to who placed the order and when, while `order_items` contains details on what was ordered.
    -   **Many-to-Many Relationships**: The relationship between `orders` and `products` is managed via a bridge table, as one order can include multiple products and each product can be part of multiple orders.
6.  **Products and Inventory Items**:
    -   **Functional Separation**: `inventory_items` now only stores information related to the storage of products, while `products` contains details about the actual products.
    -   **String Fields Management**: Separate tables were created for `brand`, `category`, and `department` to minimize discrepancies. Both `SKU` and `product_id` are retained, assuming they serve distinct purposes.

### Populating the Normalized Design

The normalized schema is populated using SQL scripts, which can be found in the `normalisation_population.sql` file located in the `/data_pipeline` directory. This script handles:

-   **Data Migration**: Transferring data from staging tables to the normalized tables.
-   **Data Transformation**: Ensuring that data fits the normalized structure.
-   **Referential Integrity**: Enforcing constraints to maintain relationships between tables.

The process ensures that the data in the normalized tables is consistent, free of redundancy, and optimized for querying.

## Data Analysis

After normalization, the data is ready for analysis. The `data_analysis.sql` script contains SQL queries designed to generate insights from the e-commerce data, including:

-   **Sales Performance**: Analyzing sales trends over time.
-   **Inventory Turnover**: Understanding how quickly products are moving in and out of inventory.
-   **Customer Segmentation**: Identifying key customer segments based on purchasing behavior.

## Final Notes

This project is an excellent foundation for building a scalable, real-time analytics platform using Apache Kafka and PostgreSQL. While the current implementation covers the basics, there are many opportunities for further enhancements, including more advanced analytics, better data visualization, and scaling to handle larger datasets.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request.


