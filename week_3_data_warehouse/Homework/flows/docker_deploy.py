from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from etl_web_to_gcs_load_data import etl_parent_flow

docker_block = DockerContainer.load("zoom-week3-fhv")

docker_dep = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="docker-flow-week3",
    infrastructure=docker_block,
)

if __name__== "__main__":
    docker_dep.apply()