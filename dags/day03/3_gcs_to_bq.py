
import datetime

from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

import os
import sys
from pathlib import Path

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(f'{CUR_DIR}')
sys.path.append(f'{CUR_DIR}/..')

from common import (default_args, GCS_BUCKET, CSV_FILE_PATH2)


with DAG(
    "23_proc_files",
    schedule = None, 
    start_date = datetime.datetime(2023,6,6),
    default_args = default_args,
    concurrency = 2,
) as dag:


    hook = GoogleCloudStorageHook()
    list_of_files = hook.list(GCS_BUCKET)

    # list_of_files = hook.list(bucket, prefix='FolderOne/SubFolder')
    DATASET = f'johneysadminproject.airflowstuff'

    with TaskGroup ('process_files') as process_files:
        for file_name in list_of_files:

            table_name = Path(file_name).stem

            gcs_to_bq = GCSToBigQueryOperator(
                task_id=f'gcs_to_bq_{table_name}',
                source_objects=[file_name],
                bucket=GCS_BUCKET,
                # google_cloud_storage_conn_id=GCP_CONN_ID,
                autodetect=True,
                # schema_object=table_schema_json,
                source_format='NEWLINE_DELIMITED_JSON',
                field_delimiter=',',
                quote_character='"',
                skip_leading_rows=1,
                max_bad_records=999999,
                allow_quoted_newlines=True,
                ignore_unknown_values=True,
                allow_jagged_rows=True,
                # BQ settings
                destination_project_dataset_table=f'{DATASET}.{table_name}',
                # gcp_conn_id=GCP_CONN_ID,
                create_disposition='CREATE_IF_NEEDED',
                write_disposition='WRITE_TRUNCATE',
            )
