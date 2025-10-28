resource "google_service_account" "etl" {
  account_id   = "${var.imdb_prefix}-etl-sa"
  display_name = "IMDb Data Pipeline Service Account"
  description  = "Service account for Dataflow and Composer IMDb pipeline"
}

locals {
  etl_roles = [
    "roles/storage.objectAdmin",     # access GCS
    "roles/bigquery.dataEditor",     # write to BQ
    "roles/bigquery.jobUser",        # run BQ load jobs
    "roles/dataflow.admin",          # start Dataflow jobs
    "roles/dataflow.worker",         # Dataflow runtime
    "roles/logging.logWriter",       # log to Cloud Logging
    "roles/monitoring.metricWriter", # publish metrics
  ]
}

resource "google_project_iam_member" "etl_roles" {
  for_each = toset(local.etl_roles)
  project  = var.project_id
  role     = each.key
  member   = "serviceAccount:${google_service_account.etl.email}"
}

# Minimal roles (tighten as needed)
resource "google_project_iam_member" "sa_storage" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.etl.email}"
}
resource "google_project_iam_member" "sa_bq" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.etl.email}"
}
resource "google_project_iam_member" "sa_df_worker" {
  project = var.project_id
  role    = "roles/dataflow.worker"
  member  = "serviceAccount:${google_service_account.etl.email}"
}
resource "google_project_iam_member" "sa_df_admin" {
  project = var.project_id
  role    = "roles/dataflow.admin"
  member  = "serviceAccount:${google_service_account.etl.email}"
}
resource "google_project_iam_member" "sa_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.etl.email}"
}

