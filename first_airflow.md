# Sign up for a free account on Google 

# Enable the Compute API

# Create a Compute VM 


```bash
# Install required packages
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    python3-venv python3-pip python3-dev build-essential \
    libssl-dev libffi-dev libpq-dev sqlite3 \
    curl ca-certificates git

# Create airflow user and directories
sudo useradd --system --create-home --home-dir /opt/airflow --shell /bin/bash airflow
sudo mkdir -p /opt/airflow/app /opt/airflow/venv
sudo chown -R airflow:airflow /opt/airflow
```

# Install airflow as airflow user

```bash
sudo su - airflow 

# Python venv
python3 -m venv /opt/airflow/venv
source /opt/airflow/venv/bin/activate
python -m pip install --upgrade pip wheel setuptools

# Install Airflow 3 with official constraints
AIRFLOW_VERSION=3.1.0
PYTHON_MINOR="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_MINOR}.txt"

# Install core + common extras (adjust extras as needed)
pip install "apache-airflow[postgres,google,celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Initialize metadata DB (SQLite for demo)
export AIRFLOW_HOME=/opt/airflow/app
mkdir -p "$AIRFLOW_HOME"

airflow standalone
```