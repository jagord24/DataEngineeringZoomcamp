# Homework A

## Question 1. Knowing Docker Tags

Which tag has the following text? - *Write the image ID to the file*
Answer: **--iidfile string**

`docker --help`
`docker build --help`

## Question 2. Understanding Docker First Run

**Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules that are installed ( use pip list). **

**How many python packages/modules are installed?**

Need to start a python container as bash and then do `pip list`

`docker run -it --entrypoint=bash python:3.9`

Result: 
```bash
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```
**Answer: 3**

## Preparing Postgres

Modified ingest_data.py by adding the following code block to get around error from tpep:
```python        
try:
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
except AttributeError:
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
```

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --url=${URL}
```


## Question 3. Count Records

**How many taxi trips were totally made on January 15?**

*Tip: started and finished on 2019-01-15.
*
Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

```SQL
SELECT count(1)
FROM green_taxi_trips
WHERE
	lpep_pickup_datetime >= '2019-01-15 00:00:00' AND
	lpep_pickup_datetime < '2019-01-16 00:00:00' AND
	lpep_dropoff_datetime < '2019-01-16 00:00:00' AND
	lpep_dropoff_datetime >= '2019-01-15 00:00:00'
```

RESULT: **20530**

## Question 4. Largest trip for each day

```SQL
SELECT 
	CAST(lpep_pickup_datetime as DATE),
	max(trip_distance)
FROM green_taxi_trips
GROUP BY CAST(lpep_pickup_datetime as DATE)
ORDER BY max(trip_distance) desc
```

Result (head of table):
| Pickup Date | Trip Distance (max) |
| ----------- | ----------- |
| **"2019-01-15"** | **117.99**     |
| "2019-01-18" | 80.96       |
|"2019-01-28" | 64.27 |
|"2019-01-10" | 64.2 |
|"2019-01-06" | 60.91 |


## Question 5. The number of passengers

```SQL
SELECT
	passenger_count,
	count(*)
FROM green_taxi_trips
WHERE
	(passenger_count = 2 or passenger_count = 3)
	AND
	(lpep_pickup_datetime >= '2019-01-01 00:00:00' AND
	lpep_pickup_datetime < '2019-01-02 00:00:00')
GROUP BY
	passenger_count
```
Result:
|"passenger_count"	|"count"|
|-----|----|
|2|	1282|
|3	|254|


## Question 6. Largest Tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

```SQL
SELECT
	zdo."Zone" as DropoffZone,
	max(t.tip_amount) as MaxTip
FROM
	green_taxi_trips t,
	zones zdo,
	zones zpu
WHERE
	t."DOLocationID" = zdo."LocationID"
	AND
	t."PULocationID" = zpu."LocationID"
	AND
	zpu."Zone" = 'Astoria'
GROUP BY DropoffZone
ORDER BY MaxTip desc;
```
Answer: Long Island City/Queens Plaza with a max of $88


# Part B - Terraform

## Question 1. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

```bash
(base) jagord24_gmail_com@de-zoomcamp:~/jg-de-zoomcamp/week_1_basics_n_setup/1_terraform_gcp$ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "northamerica-northeast1"
      + project                    = "dezoomcamp2023"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + dataset {
              + target_types = (known after apply)

              + dataset {
                  + dataset_id = (known after apply)
                  + project_id = (known after apply)
                }
            }

          + routine {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + routine_id = (known after apply)
            }

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "NORTHAMERICA-NORTHEAST1"
      + name                        = "dtc_data_lake_dezoomcamp2023"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 1s [id=dtc_data_lake_dezoomcamp2023]
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/dezoomcamp2023/datasets/trips_data_all]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.```