output "service_account_email" {
  value = google_service_account.etl.email
}

output "raw_bucket_name" {
  value = google_storage_bucket.raw.name
}

output "curated_bucket_name" {
  value = google_storage_bucket.curated.name
}

output "bq_dataset_id" {
  value = google_bigquery_dataset.imdb.dataset_id
}

