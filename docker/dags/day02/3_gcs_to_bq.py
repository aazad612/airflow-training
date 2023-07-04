
import datetime

from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.operators.dummy_operator import DummyOperator

import os
import sys

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(f'{CUR_DIR}')
sys.path.append(f'{CUR_DIR}/..')

from common import default_args

CSV_FILE_PATH = f'{CUR_DIR}/csvs/tablist.csv'

GCS_BUCKET = 'mentor-airflow-training'

with DAG(
    "13_proc_files",
    schedule = None, 
    start_date = datetime.datetime(2023,6,6),
    default_args = default_args,
) as dag:


    hook = GoogleCloudStorageHook()
    list_of_files = hook.list(GCS_BUCKET)

    # list_of_files = hook.list(bucket, prefix='FolderOne/SubFolder')

    with TaskGroup ('process_files') as process_files:
        for file_name in list_of_files:
            # dummy_task = DummyOperator(
            #     task_id=f'dummy_task{file_name}',
            #     )


            gcs_to_bq = GCSToBigQueryOperator(
                task_id=f'gcs_to_bq_{file_name}',
                source_objects=[file_name],
                bucket=GCS_BUCKET,
                # google_cloud_storage_conn_id=GCP_CONN_ID,
                autodetect=True,
                # schema_object=table_schema_json,
                source_format='JSON',
                field_delimiter=',',
                quote_character='"',
                skip_leading_rows=1,
                max_bad_records=999999,
                allow_quoted_newlines=True,
                ignore_unknown_values=True,
                allow_jagged_rows=True,
                # BQ settings
                destination_project_dataset_table=destination_project_dataset_table,
                gcp_conn_id=GCP_CONN_ID,
                create_disposition='CREATE_IF_NEEDED',
                write_disposition='WRITE_TRUNCATE',
            )