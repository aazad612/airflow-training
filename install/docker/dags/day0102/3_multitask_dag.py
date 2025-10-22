import datetime

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

with DAG(
    "03_multi_task_dag",
    schedule=None, 
    start_date=datetime.datetime(2023,6,6)
) as dag:

    bash_task = BashOperator(
        task_id = "bash_taks",
        bash_command = "echo This DAG is using BASH Operator"
    )

    def calculate (a,b):
        c = a + b
        print(c)
        return c
        
    python_task = PythonOperator(
        task_id = "python_task",
        python_callable = calculate,
        op_kwargs = {
            'a': '1',
            'b': '2'
        }
    )

    python_task >> bash_task
