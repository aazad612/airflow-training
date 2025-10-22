from datetime import datetime

import os
import sys

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

default_args = {
    'owner': 'Johney Aazad',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 0,
    'start_date': datetime(2023,6,6),
    'catchup': False,
    'concurrency': 4,
}


GCS_BUCKET = 'mentor-airflow-training'
CSV_FILE_PATH = f'{CUR_DIR}/csvs/tablist2.csv'
CSV_FILE_PATH2 = f'{CUR_DIR}/csvs/tablist2.csv'
GCP_CONN_ID = 'google_cloud_default'
PG_CONN_ID = 'postgres_default'

