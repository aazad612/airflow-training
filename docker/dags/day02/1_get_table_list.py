import datetime

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models.connection import Connection

import os
import sys

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(f'{CUR_DIR}')
sys.path.append(f'{CUR_DIR}/..')

from common import default_args

CSV_FILE_PATH = f'{CUR_DIR}/csvs/tablist.csv'

with DAG(
    "11_get_table_list",
    schedule = None, 
    start_date = datetime.datetime(2023,6,6),
    default_args = default_args,
) as dag:

    SQL = f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname !='pg_catalog' AND schemaname <> 'information_schema'"

    def export_to_csv():
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
        connection = postgres_hook.get_conn()
        cursor = connection.cursor()
        with open(CSV_FILE_PATH, "w") as f:
            # with closing(db.get_conn()) as conn:
            #     with closing(conn.cursor()) as cur:
            cursor.copy_expert(
                f"COPY ({SQL}) TO STDOUT CSV HEADER;", f
            )
    
    python_task = PythonOperator(
        task_id = "python_task",
        python_callable = export_to_csv,
    )




