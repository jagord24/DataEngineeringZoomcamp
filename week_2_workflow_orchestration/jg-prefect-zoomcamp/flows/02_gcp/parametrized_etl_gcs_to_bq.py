from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")

# @task()
# def transform(path: Path) -> pd.DataFrame:
#     """Data cleaning example"""
#     df = pd.read_parquet(path)
#     print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
#     df["passenger_count"].fillna(0, inplace=True)
#     print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
#     return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write dataframe to Big Query"""
    
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="dezoomcamp2023",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )

@flow(log_prints=True)
def el_gcs_to_bq(year: int, month: int, color: str) -> int:
    """Main ETL flow to load data into Big Query data warehouse"""
    path = extract_from_gcs(color, year, month)
    df = pd.read_parquet(path)
    write_bq(df)
    return(len(df))

@flow(log_prints=True)
def el_parent_flow(months: list[int] = [2,3], year: int = 2019, color: str = "yellow"):
    rows_processed = 0
    for month in months:
        rows_processed += el_gcs_to_bq(year, month, color)
    print(rows_processed)
        


if __name__=="__main__":
    color = "yellow"
    months = [2,3]
    year = 2019
    el_parent_flow(months, year, color)