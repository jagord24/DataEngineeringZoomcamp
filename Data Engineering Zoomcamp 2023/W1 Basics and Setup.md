# Introduction

-   [Video](https://www.youtube.com/watch?v=-zpVha7bw5A)
-   [Slides](https://www.slideshare.net/AlexeyGrigorev/data-engineering-zoomcamp-introduction)
-   Overview of [Architecture](https://github.com/DataTalksClub/data-engineering-zoomcamp#overview), [Technologies](https://github.com/DataTalksClub/data-engineering-zoomcamp#technologies) & [Pre-Requisites](https://github.com/DataTalksClub/data-engineering-zoomcamp#prerequisites)

We suggest watching videos in the same order as in this document.

The last video (setting up the environment) is optional, but you can check it earlier if you have troubles setting up the environment and following along with the videos.

# Intro to GCP
- 

# Docker + Postgres

[Code](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/2_docker_sql)

### [Introduction to Docker](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
#### Why do we need Docker
- delivers software in containers which are isolated from each other
- a data pipleine takes data and modifies or moves it to produce more data. you can string together many pipelines
- the 2 postgres (one in docker and one on the host machine) will be completely isolated from each other
- docker provides reproducability
	- can take a docker image and run it in a different environment
##### Why do we care about docker?
- Reproducability
- local experiments to make sure that the behavior is as we expect
- integration tests (CI/CD)
- running pipelines on the cloud (AWS batch, Kubernetes jobs)
- Spark
- serverless (AWS Lambda, Google functions)
-  `ssh -i ~/.ssh/gcp jagor24_gmail_com@34.152.41.97
	- run that to connect to the VM

#### Creating a simple "data pipeline" in Docker
### [Ingesting NY Taxi Data to Postgres](https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
#### Running Postgres locally with Docker
#### Using `pgcli` for connecting to the database
#### Exploring the NY Taxi dataset
#### Ingesting the data into the database
#### *Note* if you have problems with `pgcli`, check [this video](https://www.youtube.com/watch?v=3IkfkTwqHx4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) for an alternative way to connect to your database
### [Connecting pgAdmin and Postgres](https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
#### The pgAdmin tool
#### Docker networks
### [Putting the ingestion script into Docker](https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
#### Converting the Jupyter notebook to a Python script
#### Parametrizing the script with argparse
#### Dockerizing the ingestion script
### [Running Postgres and pgAdmin with Docker-Compose](https://www.youtube.com/watch?v=hKI6PkPhpa0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
#### Why do we need Docker-compose
#### Docker-compose YAML file
#### Running multiple containers with `docker-compose up`
-   [SQL refresher](https://www.youtube.com/watch?v=QEcps_iskgg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
#### Adding the Zones table
#### Inner joins
#### Basic data quality checks
#### Left, Right and Outer joins
#### Group by
### Optional: If you have some problems with docker networking, check [Port Mapping and Networks in Docker](https://www.youtube.com/watch?v=tOr4hTsHOzU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
#### Docker networks
#### Port forwarding to the host environment
#### Communicating between containers in the network
#### `.dockerignore` file
### *Optional*: If you are willing to do the steps from "Ingesting NY Taxi Data to Postgres" till "Running Postgres and pgAdmin with Docker-Compose" with Windows Subsystem Linux please check [Docker Module Walk-Through on WSL](https://www.youtube.com/watch?v=Mv4zFm2AwzQ)

# [GCP + Terraform](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup#gcp--terraform)

[Code](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp)

-   Introduction to GCP (Google Cloud Platform)
    -   [Video](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
-   Introduction to Terraform Concepts & GCP Pre-Requisites
    -   [Video](https://www.youtube.com/watch?v=Hajwnmj0xfQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
    -   [Companion Notes](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp)
-   Workshop: Creating GCP Infrastructure with Terraform
    -   [Video](https://www.youtube.com/watch?v=dNkEgO-CExg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
    -   [Workshop](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/terraform)
-   Configuring terraform and GCP SDK on Windows
    -   [Instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/windows.md)

### [](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup#environment-setup)Environment setup

For the course you'll need:

-   Python 3 (e.g. installed with Anaconda)
-   Google Cloud SDK
-   Docker with docker-compose
-   Terraform

If you have problems setting up the env, you can check this video:

-   [Setting up the environment on cloud VM](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
    -   Generating SSH keys
    -   Creating a virtual machine on GCP
    -   Connecting to the VM with SSH
    -   Installing Anaconda
    -   Installing Docker
    -   Creating SSH `config` file
    -   Accessing the remote machine with VS Code and SSH remote
    -   Installing docker-compose
    -   Installing pgcli
    -   Port-forwarding with VS code: connecting to pgAdmin and Jupyter from the local computer
    -   Installing Terraform
    -   Using `sftp` for putting the credentials to the remote machine
    -   Shutting down and removing the instance

### [](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup#homework)Homework

-   [Homework](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2023/week_1_docker_sql/homework.md)
-   [Homework-PartB](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2023/week_1_terraform/homework.md)