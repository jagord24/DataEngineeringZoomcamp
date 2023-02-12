

# Homework Week 3

## SETUP
Amended the code from week 2 and created local deployment and build using prefect. Had to modify code to do csv.gz files

```SQL
-- Setup
CREATE OR REPLACE EXTERNAL TABLE `fhv.fhv2019gz`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_dezoomcamp2023/data/fhv_gz/fhv_tripdata_2019-*.csv.gz']
);
```

## Question 1

```SQL
-- Question 1 - create an external table with 2019 FHV data

SELECT count(*) FROM `fhv.fhv2019gz`;
```
**RESULT: 43244696** (b)
*note: performance was terrible using csv.gz compared to parquet when I initially tried it*

## Question 2

Need to create a BQ table in addition to the external table

### Setup
```SQL
  CREATE OR REPLACE TABLE dezoomcamp2023.fhv.fhv2019gz_non_partitioned AS
  SELECT * FROM `dezoomcamp2023.fhv.fhv2019gz`
```

### Queries

```SQL
SELECT COUNT(DISTINCT Affiliated_base_number)
  FROM `dezoomcamp2023.fhv.fhv2019gz`; -- 0 B (result 3163)

SELECT COUNT(DISTINCT Affiliated_base_number)
  FROM `dezoomcamp2023.fhv.fhv2019gz_non_partitioned`; --319.94 MB (result 3163)
```

**Answer: 0 MB for the External Table and 317.94MB for the BQ Table**

## Question 3

```SQL
-- Question 3
  -- How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?

SELECT count(*)
  FROM `dezoomcamp2023.fhv.fhv2019gz_non_partitioned`
  WHERE
    PUlocationID IS NULL and
    DOlocationID IS NULL;
-- Result = 717748
-- 638.9 MB
```

**ANSWER: 717,748**

## Question 4
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

Partition by pickup_datetime for filtering since you will chunk it into intervals. That way if you filter on the date you will only have to look through chunks of the data. Then you cluster the data by the base number so it is in the order you are usually 

**ANSWER: (b) Partition by pickup_datetime Cluster on affiliated_base_number**

## Question 5
Implement the optimized solution you chose for question 4. 

```SQL
CREATE OR REPLACE TABLE `dezoomcamp2023.fhv.fhv2019gz_partitioned_and_clustered`
  PARTITION BY DATE(pickup_datetime)
  CLUSTER BY Affiliated_base_number
  AS
  SELECT * FROM `fhv.fhv2019gz`;
-- elapsed time = 1 min 38 sec
```

Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).

Use the BQ table you created earlier in your from clause and note the estimated bytes. 

Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. 

What are these values? Choose the answer which most closely matches.

```SQL
-- NON Partitioned Table
SELECT COUNT(DISTINCT Affiliated_base_number)
  FROM `dezoomcamp2023.fhv.fhv2019gz_non_partitioned`
  WHERE
    pickup_datetime <= TIMESTAMP('2019-03-31 23:59:59 UTC') and
    pickup_datetime >= TIMESTAMP('2019-03-01 00:00:00 UTC');
  -- 647.87 MB (count = 724)

-- Partitioned and Clustered Table
SELECT COUNT(DISTINCT Affiliated_base_number)
  FROM `dezoomcamp2023.fhv.fhv2019gz_partitioned_and_clustered`
  WHERE
    pickup_datetime <= TIMESTAMP('2019-03-31 23:59:59 UTC') and
    pickup_datetime >= TIMESTAMP('2019-03-01 00:00:00 UTC');
  -- 23.05 MB (count = 724)
```

**Answer: (b) 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table**

## Question 6
Where is the data stored in the External Table you created?

**Answer: GCP Bucket (GCS)**+

## Question 7
It is best practice in Big Query to always cluster your data:

**FALSE**
Datasets under 1 GB can even increase cost because of additional metadata and processing


## Question 8

SO MUCH FASTER USING PARQUET...wow. Used code from previous week and modified slightly to send to GCS by converting dtypes and normalizing column names. Then did the GCS queries and looked at the size of the processing. 