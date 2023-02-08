
# Question 1. Load January 2020 data

Ran this in bash
`prefect deployment run etl-parent-flow/docker-flow -p "months=[1]" -p "color=green" -p "year=2020"`

Got `KeyError: 'tpep_pickup_datetime'`
- Needed to add an 'if' to parametrized flow transform to account for different naming

```python
    if color == 'yellow':
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    elif color == 'green':
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
```

This resulted in having to rebuild and push the docker image before running the code.

`rows: 447770`


# Question 2 Cron Schedule

Requirement: Run on the first of every month @ 5am UTC

Answer: "0 5 1 * *"
```bash
prefect deployment build flows/03_deployments/parameterized_flow.py:etl_parent_flow -n etl3 --cron "0 5 1 * *"  --timezone 'UTC' -a
```

# Question 3 Loading data to BigQuery

Download data to GCS with 
`prefect deployment run etl-parent-flow/docker-flow -p "months=[2,3]" -p "color=yellow" -p "year=2019"`

`prefect deployment build flows/02_gcp/parametrized_etl_gcs_to_bq.py:el_parent_flow -n "Homework 2 Question 3"`

`prefect deployment apply el_parent_flow-deployment.yaml`

`prefect deployment run el-parent-flow/"Homework 2 Question 3" -p "months=[2,3]" -p "color=yellow" -p "year=2019"`

RESULT: 14,851,920