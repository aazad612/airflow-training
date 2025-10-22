from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from itertools import chain

import os
import sys

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(f'{CUR_DIR}')

from common import default_args

with DAG(
    '20_exec_all',
    schedule_interval=None, 
    default_args=default_args
) as dag:

    dag_names={}
    
    dags=[
        '21_get_table_list',
        '22_pg_to_gcs',
        '23_proc_files'
    ]
    
    for dag_name in dags :
        dag_names[dag_name] = TriggerDagRunOperator(
            task_id= f'trigger_{dag_name}',
            trigger_dag_id=dag_name,
            wait_for_completion = True,
            allowed_states=['success','faied','skipped'],
            trigger_rule='all_done'
            )
    
    chain(
        dag_names['21_get_table_list'],
        dag_names['22_pg_to_gcs'],
        dag_names['23_proc_files']
        )
