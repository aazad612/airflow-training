# Airflow dockerized installation 

The docker-compose.yaml is the official Apache image on 01/01/2023, with slight modifications for disabling the default connections and example dags. 

Before you start, 

1. Please ensure at least 4GB of RAM is allocated in the docker configuration. 

2. Create the following directories in the same folder where you have the docker-compose.yaml, if you are cloning the repo they should already exist. 

mkdir -p ./dags ./logs ./plugins ./config

3. The database must be initiated and so use the following command to start the docker stack. 

docker compose up airflow-init


