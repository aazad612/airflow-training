from __future__ import annotations
from airflow import DAG
from airflow.models import Variable
from airflow.providers.standard.operators.python import PythonOperator

from datetime import datetime, timedelta
import os
import requests

from google.cloud import storage

# =========================
# To be moved out later
# =========================
PROJECT_ID   = "learn-by-doing-data-engg"
RAW_BUCKET   = "learn-by-doing-data-engg-imdb-raw"
CURATED_BUCKET   = "learn-by-doing-data-engg-imdb-raw"
BQ_DATASET = "imdb"


TIMEOUT_SEC  = 300
IMDB_BASE = "https://datasets.imdbws.com/"
ALL_FILES = [
    "title.basics.tsv.gz",
    "title.ratings.tsv.gz",
    "title.principals.tsv.gz",
    "name.basics.tsv.gz",
    "title.akas.tsv.gz",
    "title.episode.tsv.gz",
]


def _safe_table_name(filename: str) -> str:
    """
    Map filename to folder name under RAW bucket.
    e.g. title.basics.tsv.gz -> title_basics
    """
    base = filename.replace(".tsv.gz", "")
    return base.replace(".", "_")

def download_to_gcs(ds: str, **_):
    """
    Downloads each IMDb *.tsv.gz file to:
      gs://<RAW_BUCKET>/<table>/dt=<YYYY-MM-DD>/<filename>.tsv.gz

    Idempotent: if destination blob exists with same size, skip upload.
    """
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(RAW_BUCKET)

    with requests.Session() as sess:
        sess.headers.update({"User-Agent": "composer-imdb-fetch/1.0"})

        for fname in ALL_FILES:
            url = IMDB_BASE + fname

            # HEAD to get size for idempotency check (not all servers support HEAD; fallback to GET)
            content_length = None
            try:
                h = sess.head(url, timeout=TIMEOUT_SEC, allow_redirects=True)
                if h.ok and "Content-Length" in h.headers:
                    content_length = int(h.headers["Content-Length"])
            except Exception:
                # non-fatal; we’ll still try GET
                pass

            table = _safe_table_name(fname)
            object_path = f"{table}/dt={ds}/{fname}"
            blob = bucket.blob(object_path)

            # Idempotent skip if same size exists
            if blob.exists():
                blob.reload()
                if content_length is not None and blob.size == content_length:
                    # already present with same size -> skip
                    continue

            # Stream download to memory and upload
            resp = sess.get(url, timeout=TIMEOUT_SEC, stream=True)
            resp.raise_for_status()
            data = resp.content  # files are .gz; keep compressed

            # Upload (set cache-control & content-encoding if you like; content-type is binary)
            blob.cache_control = "no-cache"
            blob.upload_from_string(data)


default_args = {
    "owner": "data-eng",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="imdb_fetch_raw_to_gcs",
    default_args=default_args,
    schedule="0 6 * * *",  # daily at 06:00 UTC
    catchup=False,
    max_active_runs=1,
    tags=["imdb", "gcs", "raw", "fetch"],
) as dag:

    fetch_raw = PythonOperator(
        task_id="fetch_imdb_tsvs_to_gcs",
        python_callable=download_to_gcs,
        op_kwargs={"ds": "{{ ds }}"},
    )

