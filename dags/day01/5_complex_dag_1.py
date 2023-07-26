from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Define the DAG
default_args = {
    'start_date': datetime(2023, 7, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    '05_complex_hierarchy_2',
    default_args=default_args,
    schedule_interval=None
)

# Define the tasks
with dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo "Executing Task 1"',
    )

    task_2 = BashOperator(
        task_id='task_2',
        bash_command='echo "Executing Task 2"',
    )

    task_3 = BashOperator(
        task_id='task_3',
        bash_command='echo "Executing Task 3"',
    )

    task_4 = BashOperator(
        task_id='task_4',
        bash_command='echo "Executing Task 4"',
    )

    task_5 = BashOperator(
        task_id='task_5',
        bash_command='echo "Executing Task 5"',
    )

    task_6 = BashOperator(
        task_id='task_6',
        bash_command='echo "Executing Task 6"',
    )

    task_7 = BashOperator(
        task_id='task_7',
        bash_command='echo "Executing Task 7"',
    )

    task_1 >> task_2 >> [ task_3, task_4 ]
    [ task_4, task_5 ] >> task_6 >> task_7
