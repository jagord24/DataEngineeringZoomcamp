from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(log_prints=True, retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas dataframe"""
    ## example to show how retries work below
    # if randint(0, 1) > 0:
    #     raise Exception

    df = pd.read_csv(dataset_url)
    return df

# @task(log_prints=True)
# def clean(df: pd.DataFrame) -> pd.DataFrame:
#     """Fix dtype issues"""
#     print(df.head(2))
#     df.columns= df.columns.str.lower()
#     df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
#     df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])


#     print(df.head(2))
#     print(f"columns: {df.dtypes}")
#     print(f"rows: {len(df)}")
#     return df


@task(log_prints=True)
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write dataframe out locally as a parquet file"""
    print(dataset_file)
    path = Path(f"data/fhv_gz/{dataset_file}.csv.gz")
    print(path)
    df.to_csv(path, compression="gzip")
    return path

@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Upload parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def etl_web_to_gcs(year: int, month: int) -> None:
    """The main ETL function"""
    # Model URL:    https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz
    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    print(dataset_file)
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"
    # print(dataset_url)
    df = fetch(dataset_url)
    # df_clean = clean(df)
    path = write_local(df, dataset_file)
    write_gcs(path)

@flow()
def etl_parent_flow(
    months: list[int] = [1, 2], years: list[int] = [2019]
):
    for year in years:
        for month in months:
            etl_web_to_gcs(year, month)

if __name__ == "__main__":
    months = [1, 2, 3]
    years = [2019]
    etl_parent_flow(months, years)
