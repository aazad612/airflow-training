# Airflow Training
Cloud composer is the managed version of Apcahce Airflow and easiest way to get started.

## Airflow Installation on your local machine

1. Enable WSL on if using a windows machine
2. Install Python 3.8, PIP and GitBash
3. Execute the scripts below, change the version of airflow to your liking

```
# Setup a virual Environment
virtualenv -p airflow_venv26
source airflow_venv26/bin/activate

# Airflow version you want to install
AIRFLOW_VERSION=2.6.2

# Determine the version of Python installed on your machine 3.7 or 3.8  
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow[async,postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Additional providers can be installed as below.
pip install "apache-airflow-providers-google==8.0.0"
```

## Airflow Installation other options 
1. Most beneficial to gain knowledge would be a dockerized setup on your local machine.
```
https://hub.docker.com/r/bitnami/airflow/

curl -sSL https://raw.githubusercontent.com/bitnami/containers/main/bitnami/airflow/docker-compose.yml > docker-compose.yml

docker-compose up -d
```

2. An advanced but best of the breed install would be on GKE using Community helm chart, for learning do not use Bitnami.

https://airflow.apache.org/docs/helm-chart/stable/index.html
