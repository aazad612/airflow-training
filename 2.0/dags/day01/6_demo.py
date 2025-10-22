from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

# Define the DAG
default_args = {
    'start_date': datetime(2023, 7, 24),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    '6_demo_tasks',
    default_args=default_args,
    schedule_interval=None
)

# Define the tasks
with dag:
    task_1 = DummyOperator(
		task_id='extract_oracle_to_gcs'
	)

    task_2 = DummyOperator(
        task_id='gcs_to_local'
    )

    task_3 = DummyOperator(
        task_id='transform'
    )

    task_4 = DummyOperator(
        task_id='load_to_gcs'
    )

    task_5 = DummyOperator(
        task_id='load_gcs_to_bq'
    )


    task_1 >> task_2 >> task_3 >> task_4 >> task_5
