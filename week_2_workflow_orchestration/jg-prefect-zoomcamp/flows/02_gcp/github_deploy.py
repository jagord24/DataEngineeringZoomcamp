from prefect.deployments import Deployment
from etl_web_to_gcs_homeoworkQ4 import etl_web_to_gcs
from prefect.filesystems import GitHub 

storage = GitHub.load("storage-block-hoemwork2")

deployment = Deployment.build_from_flow(
     flow=etl_web_to_gcs,
     name="github-homework",
     storage=storage,
     entrypoint="week_2_workflow_orchestration/jg-prefect-zoomcamp/flows/02_gcp/etl_web_to_gcs_homeoworkQ4.py:etl_web_to_gcs")

if __name__ == "__main__":
    deployment.apply()