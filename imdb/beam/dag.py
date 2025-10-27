from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from google.cloud import storage
import requests

PROJECT_ID = Variable.get("PROJECT_ID")
REGION     = Variable.get("REGION", default_var="us-central1")
RAW_BUCKET = f"{PROJECT_ID}-imdb-raw"
CUR_BUCKET = f"{PROJECT_ID}-imdb-curated"
DF_TMP     = f"{PROJECT_ID}-dataflow-tmp"

IMDB_URLS = {
    "title_basics":  "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title_ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz",
}

def download_to_gcs(**context):
    ds = context['ds']  # YYYY-MM-DD
    client = storage.Client()
    for name, url in IMDB_URLS.items():
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        blob = client.bucket(RAW_BUCKET).blob(f"{name}/dt={ds}/{name}.tsv.gz")
        blob.upload_from_string(resp.content)

default_args = {
    "owner": "data-eng",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="imdb_daily",
    default_args=default_args,
    schedule_interval="0 6 * * *",  # daily 06:00
    catchup=False,
    max_active_runs=1,
    tags=["imdb", "gcp", "dataflow", "bigquery"]
) as dag:

    fetch = PythonOperator(
        task_id="fetch_imdb_raw",
        python_callable=download_to_gcs,
        provide_context=True
    )

    df_title_basics = DataflowCreatePythonJobOperator(
        task_id="df_title_basics",
        py_file=f"gs://{PROJECT_ID}-code/beam/beam_imdb_title_basics.py",
        options={
            "input_gcs":  f"gs://{RAW_BUCKET}/title_basics/dt={{ ds }}/title.basics.tsv.gz",
            "output_prefix": f"gs://{CUR_BUCKET}/title_basics/dt={{ ds }}/part",
            "temp_location": f"gs://{DF_TMP}/tmp",
            "region": REGION,
            "runner": "DataflowRunner",
            "project": PROJECT_ID,
            "experiments": ["use_runner_v2"]
        },
        location=REGION
    )

    load_title_basics = GCSToBigQueryOperator(
        task_id="bq_load_title_basics",
        bucket=CUR_BUCKET,
        source_objects=["title_basics/dt={{ ds }}/*.parquet"],
        destination_project_dataset_table=f"{PROJECT_ID}.imdb.title_basics",
        source_format="PARQUET",
        write_disposition="WRITE_TRUNCATE",
        time_partitioning={"type": "DAY"},
        autodetect=True
    )

    # (Optional) Add a second Dataflow job + load for title_ratings (mirror the above)

    fetch >> df_title_basics >> load_title_basics