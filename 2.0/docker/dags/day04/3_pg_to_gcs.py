import datetime

from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator

import os
import sys

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(f'{CUR_DIR}')
sys.path.append(f'{CUR_DIR}/..')

from common import (default_args, GCS_BUCKET, CSV_FILE_PATH)

with DAG(
    "23_pg_to_gcs",
    schedule = None, 
    start_date = datetime.datetime(2023,6,6),
    default_args = default_args,
) as dag:

    import pandas as pd 
    table_list_df = pd.read_csv( filepath_or_buffer=CSV_FILE_PATH,
                                 sep=',', 
                                 quotechar='"'
                               )
    table_list = table_list_df['tablename'].to_list()
    
    with TaskGroup ('load') as load_tables:
        for table_name in table_list:
            SQL_QUERY = f'select * from {table_name}'
            pg_server_cursor_data = PostgresToGCSOperator(
                task_id=f"pg_server_cursor_data_{table_name}",
                sql=SQL_QUERY,
                bucket=GCS_BUCKET,
                filename=f'{table_name}.csv',
                gzip=False,
                use_server_side_cursor=True,
            )