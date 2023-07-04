

AIRFLOW_VERSION=2.6.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.6.2/constraints-no-providers-3.7.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"


pip install "apache-airflow==2.6.2" apache-airflow-providers-google==10.1.0

celery,redis

pip install "apache-airflow[async,postgres,google,celery,redis]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

sudo apt update && sudo apt upgrade
sudo apt install postgresql postgresql-contrib
sudo systemctl status PostgreSQL
sudo systemctl stop PostgreSQL

pg_ctlcluster 13 main start

psql

CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
-- PostgreSQL 15 requires additional privileges:
USE airflow_db;
GRANT ALL ON SCHEMA public TO airflow_user;


ALTER USER airflow_user SET search_path = public;


postgresql+psycopg2://airflow_user:airflow_pass@localhost/airflow_db




airflow scheduler &
airflow webserver --port 8080 &



kill $(ps -o ppid= -p $(cat ~/airflow/airflow-webserver.pid))

kill $(cat ~/airflow/airflow-scheduler.pid)





pip install psycopg2-binary 



airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org


