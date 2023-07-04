# Airflow Install

```
AIRFLOW_VERSION=2.6.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.6.2/constraints-no-providers-3.7.txt
pip install "apache-airflow[async,postgres,google,celery,redis]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```


# Postgres Backend

Execute the following steps to install postgres. This will install postgres under use postges.

```bash
sudo apt update && sudo apt upgrade
sudo apt install postgresql postgresql-contrib

# Install drivers to access postgres, remember to do it in your virtual environment
pip install psycopg2-binary 

# change user to postgres 
sudo su postgres
# Start PSQL you will be connected as superuser postgres 
psql
```
### Create airflow DB and Users.
```sql
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
-- PostgreSQL 15 requires additional privileges:
USE airflow_db;
GRANT ALL ON SCHEMA public TO airflow_user;

ALTER USER airflow_user SET search_path = public;
```

Helpful commands 
```bash
sudo systemctl status PostgreSQL
sudo systemctl stop PostgreSQL
pg_ctlcluster 13 main start
```

### Airflow update 
Once the Postgres DB is up, we need to update the airflow configuration file.

```
~/airflow/airflow.cfg

sql_alchemy_conn=postgresql+psycopg2://airflow_user:airflow_pass@localhost/airflow_db
celery_results_backend='db+postgresql://user:password@localhost/db_name
```

Once the above steps are complete we will need to create the schema required for airflow. Which is done by below command. 
```
airflow db init
```
After which we will create our first user, this user info is stored in the backend database. 
```bash
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```

## Airflow start stop

The following steps work but airflow should be started and stopped using systemctl commands. 

Start airflow 
```bash
airflow scheduler &
airflow webserver --port 8080 &
```

Stop airflow
```
kill $(ps -o ppid= -p $(cat ~/airflow/airflow-webserver.pid))
```

Systemctl approach

https://airflow.apache.org/docs/apache-airflow/stable/howto/run-with-systemd.html












