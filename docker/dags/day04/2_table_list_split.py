from airflow.models import DAG
from datetime import datetime

# operators 
# from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
# from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.operators.bash import BashOperator

import os
import sys
import shutil
import pathlib
 
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(f'{CUR_DIR}/..')
sys.path.append(f'{CUR_DIR}')
 
from common import (default_args, GCS_BUCKET, CSV_FILE_PATH)
 
with DAG(
    dag_id=f'22_split_table_list',
    start_date=datetime(2022, 4, 1),
    default_args=default_args,
    description='Split config json into multiple files',
    schedule_interval=None,
    catchup=False,
    tags=[TENANT_NAME, 'initial_load'],
    concurrency=1
) as dag:
    table_list_file = CSV_FILE_PATH
    FILE_SIZE = 10
 
    # LOCAL_CONFIG_PATH = os.path.join(GKE_STAGE_DIR, TENANT_NAME, 'config')
    # shutil.rmtree(LOCAL_CONFIG_PATH, ignore_errors=True)
    # pathlib.Path(LOCAL_CONFIG_PATH).mkdir(parents=True)
 
    # download_config_json = GCSToLocalFilesystemOperator(
    #     task_id="download_config_json",
    #     object_name=f'{GCS_CONFIG_FOLDER}/{CONFIG_FILE}',
    #     bucket=GCS_BUCKET,
    #     filename=f'{LOCAL_CONFIG_PATH}/{CONFIG_FILE}',
    #     gcp_conn_id=GCP_CONN_ID
    #     )
 
    split_file = BashOperator(
        task_id="split_file",
        bash_command=f"split -l {FILE_SIZE} {CSV_FILE_PATH}"
    )
 
    # config_files = [os.path.join(LOCAL_CONFIG_PATH, f)
    #                 for f in os.listdir(LOCAL_CONFIG_PATH)]
   
 
    # upload_config_files_to_gcs = LocalFilesystemToGCSOperator(
    #     task_id='upload_config_files_to_gcs',
    #     src=config_files,
    #     bucket=GCS_BUCKET,
    #     dst=GCS_CONFIG_FOLDER,
    #     gcp_conn_id=GCP_CONN_ID,
    #     # impersonation_chain=DEFAULT_IMPERSONATION_ACCOUNT,
    # )
 
    # download_config_json >> split_file >> upload_config_files_to_gcs