# Prep Work 

### Sign up for a free account on Google 
### Enable the Compute API
### Create a Compute VM with default options
### Open port 8080 by creating a firewall rule


# OS Setup

## Install required packages (Ubuntu/Debian/Mint)
```bash
sudo apt update

# pyenv prerequisites 
sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# airflow prerequisites
sudo apt install -y --no-install-recommends apt-utils ca-certificates \
curl dumb-init freetds-bin krb5-user libgeos-dev \
ldap-utils libsasl2-2 libsasl2-modules libxmlsec1 locales \
libffi8 libldap-2.5-0 libssl3 netcat-openbsd \
lsb-release openssh-client  rsync sasl2-bin sqlite3 sudo unixodbc
```


## Create Airflow User

```bash
# Create airflow user and directories
sudo useradd --system --create-home --home-dir /opt/airflow --shell /bin/bash airflow
sudo mkdir -p /opt/airflow/airflow_home /opt/airflow/airflow_venv
sudo chown -R airflow:airflow /opt/airflow
sudo usermod -aG sudo airflow

```

## Install Python using pyenv

```bash
sudo su - airflow 

# Install Pyenv
curl -fsSL https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

### verify 
which pyenv
echo $PATH | grep --color=auto "$(pyenv root)/shims"

### Install Python 
pyenv install 3.11.9
pyenv global 3.11.9
```

## Install airflow 3.1.0

```bash
export AIRFLOW_HOME=/opt/airflow/airflow_home
export DAGBAG=/opt/airflow/airflow_home/dags
mkdir -p "$AIRFLOW_HOME" "$DAGBAG"

echo "source /opt/airflow/airflow_venv/bin/activate" >> .bash_profile
echo "export AIRFLOW_HOME=/opt/airflow/airflow_home" >> .bash_profile
echo "export DAGBAG=/opt/airflow/airflow_home" >> .bash_profile

# Python venv
python3 -m venv /opt/airflow/airflow_venv
source /opt/airflow/airflow_venv/bin/activate
python -m pip install --upgrade pip wheel setuptools

# Install Airflow 3 with official constraints
AIRFLOW_VERSION=3.1.0
PYTHON_MINOR="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_MINOR}.txt"


# Install core + common extras (adjust extras as needed)
pip install "apache-airflow[postgres,google,celery,fab]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

```

## Setup Postgres as Backend 

```bash
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh

sudo apt install postgresql-16

sudo -u postgres psql
```
### Execute as postgres user 

```sql
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'mypass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;

\c airflow_db

GRANT ALL ON SCHEMA public TO airflow_user;

ALTER USER airflow_user SET search_path = public;
```

### Enable DB Connectivity for Postgres

```bash
EDIT /etc/postgresql/16/main/pg_hba.conf

local   all             airflow_user            md5

sudo systemctl restart postgresql

```

## Update config to use FabAuthManger and postgress as backend
The following command execution will create airflow.cfg in the AIRFLOW_HOME
```
airflow config list
```

Update the auth_manager as below in the airflow.cfg

```
auth_manager = airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager
sql_alchemy_conn = postgresql+psycopg2://airflow_user:mypass@localhost/airflow_db
sql_alchemy_pool_size = 10

```

## Create the user
```bash

# Initiate Airflow DB
airflow db migrate

# Create Admin User 
airflow users create \
    --username admin1 \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin1@example.com \
    --password admin
```

## Automate Startup with systemctl

```bash
sudo su -

# Systemd units
cat >/etc/systemd/system/airflow-api.service <<'UNIT'
[Unit]
Description=Airflow API Server
After=network-online.target
Wants=network-online.target

[Service]
User=airflow
Group=airflow
Environment=AIRFLOW_HOME=/opt/airflow/airflow_home
Environment=PATH=/opt/airflow/airflow_venv/bin:/usr/bin:/bin
WorkingDirectory=/opt/airflow/airflow_home
ExecStart=/bin/bash -c 'source /opt/airflow/airflow_venv/bin/activate && airflow api-server'
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

cat >/etc/systemd/system/airflow-scheduler.service <<'UNIT'
[Unit]
Description=Airflow Scheduler
After=network-online.target
Wants=network-online.target

[Service]
User=airflow
Group=airflow
Environment=AIRFLOW_HOME=/opt/airflow/airflow_home
Environment=PATH=/opt/airflow/airflow_venv/bin:/usr/bin:/bin
WorkingDirectory=/opt/airflow/airflow_home
ExecStart=/bin/bash -c 'source /opt/airflow/airflow_venv/bin/activate && airflow scheduler'
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

cat >/etc/systemd/system/airflow-triggerer.service <<'UNIT'
[Unit]
Description=Airflow triggerer
After=network-online.target
Wants=network-online.target

[Service]
User=airflow
Group=airflow
Environment=AIRFLOW_HOME=/opt/airflow/airflow_home
Environment=PATH=/opt/airflow/airflow_venv/bin:/usr/bin:/bin
WorkingDirectory=/opt/airflow/airflow_home
ExecStart=/bin/bash -c 'source /opt/airflow/airflow_venv/bin/activate && airflow triggerer'
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

cat >/etc/systemd/system/airflow-dag-processor.service <<'UNIT'
[Unit]
Description=Airflow DAG Processor
After=network.target postgresql.service # Adjust dependencies if needed (e.g., your database service)

[Service]
Environment=AIRFLOW_HOME=/opt/airflow/airflow_home
Environment=PATH=/opt/airflow/airflow_venv/bin:/usr/bin:/bin
WorkingDirectory=/opt/airflow/airflow_home
Type=simple
ExecStart=/bin/bash -c 'source /opt/airflow/airflow_venv/bin/activate && airflow dag-processor'
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
UNIT



systemctl daemon-reload
systemctl enable --now airflow-api airflow-scheduler airflow-triggerer airflow-dag-processor

# for debugging
journalctl -xeu airflow-dag-processor.service


```



### reference
https://github.com/pyenv/pyenv/wiki/Why-pyenv%3F

https://github.com/apache/airflow/tree/main/scripts/systemd



