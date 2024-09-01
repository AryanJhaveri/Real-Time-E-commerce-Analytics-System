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
