
- [2.1.1 Data Lake](#211-data-lake)
  - [Features](#features)
  - [Data Lake vs. Data Warehouse](#data-lake-vs-data-warehouse)
  - [ETL vs ELT](#etl-vs-elt)
  - [Providers](#providers)
- [2.2.1 Introduction to Workflow Orchestration](#221-introduction-to-workflow-orchestration)
  - [What is orchestration?](#what-is-orchestration)
  - [Workflow orchestrators vs. other types of orchestrators](#workflow-orchestrators-vs-other-types-of-orchestrators)
  - [Core features of a workflow orchestration tool](#core-features-of-a-workflow-orchestration-tool)
  - [Different types of workflow orchestration tools that currently exist](#different-types-of-workflow-orchestration-tools-that-currently-exist)
- [2.2.2 Introduction to Prefect Concepts](#222-introduction-to-prefect-concepts)


# 2.1.1 Data Lake
A ata Lake is a central repository that holds big data from many sources.
The main goal behind a Data Lake is being able to ingest data as quickly as possible and making it available to the other team members.

- Secure
- Scalable
- Able to run on inexpensive hardware

## Features
- Ingest structured and unstructured data
- Stores, secures, and protects data at unlimited scale
- catalogs and indexes for analysis without data movement
- connects data with analytics and machine learning tools

## Data Lake vs. Data Warehouse

| | Data Lake | Data Warehouse |
| :--- | :--- | :--- |
| **Data Processing** | The data is raw and has undergone minimal processing. The data is generally unstructured.| the data is refined; it has been cleaned, pre-processed and structured for specific use cases.|
| **Size** |Data Lakes are large and contains vast amounts of data, in the order of petabytes. Data is transformed when in use only and can be stored indefinitely.|Data Warehouses are small in comparison with DLs. Data is always preprocessed before ingestion and may be purged periodically.|
| **Nature** | data is undefined and can be used for a wide variety of purposes.|data is historic and relational, such as transaction systems, etc.|
|**Users** |Data scientists, data analysts.|Business analysts.|
|**Use Cases**|Stream processing, machine learning, real-time analytics...|Batch processing, business intelligence, reporting.|

Data Lakes came into existence because as companies started to realize the importance of data, they soon found out that they couldn't ingest data right away into their DWs but they didn't want to waste uncollected data when their devs hadn't yet finished developing the necessary relationships for a DW, so the Data Lake was born to collect any potentially useful data that could later be used in later steps from the very start of any new projects.

## ETL vs ELT

| ETL | ELT |
| -- | -- |
|Export, Transform, and Load| Export, Load, and Transform| 
|small amount of data| big data|
| schema on write - data is transformed before getting to final destination| supports data lakes (schema on read) - store data directly w/o transformations and schemars are derived when reading data FROM the DL |

## Providers

- Google - GCP - cloud storage
- Amazon - AWS - S3
- Microsoft - AZURE - AZURE BLOB

# 2.2.1 Introduction to Workflow Orchestration

## What is orchestration?
- allow you to turn any data flow into something that can be scheduled, run, and observed
## Workflow orchestrators vs. other types of orchestrators
## Core features of a workflow orchestration tool
- Remote execution
- Scheduling
- Retries
- Caching
- Integration with external systems (APIs, databases)
- Ad-hoc runs
- Parametrization
- Alerts when they fail
## Different types of workflow orchestration tools that currently exist


# 2.2.2 Introduction to Prefect Concepts

Flow is the most basic python object
- container of logic, like functions
- use the @flow decorator on the main function
- flows can contain tasks
  - we are going to break the ingest_data script into 3 tasks
    1. extract
    2. transform load
- tasks not required for flows, but they are special since they can receive metadata about upstream dependencies including their state
  - can add
  ```python
  @task(log_prints=True, retries=3)
  ```

- in the file `ingest_data.py` we are going to break up the function `ingest_data` into multiple (ETL) functions
  - this is all done in the file `ingest_data_flow_diy.py`
  - these lines are just for the engine: 
  - `postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'`
  - `engine = create_engine(postgres_url)` 

- flows can contain other flows