import datetime

from airflow.models import DAG
from airflow.operators.bash import BashOperator

with DAG(
    "01_bash_dag",
    schedule=None, 
    start_date=datetime.datetime(2023,6,6)
) as dag:

    bash_task = BashOperator(
        task_id = "bash_taks",
        bash_command = "echo This DAG is using BASH Operator"
    )

    bash_task

