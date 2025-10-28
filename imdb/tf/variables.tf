variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "learn-by-doing-data-engg"
}

variable "region" {
  description = "Region for GCP resources"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Zone for GCP resources"
  type        = string
  default     = "us-central1-a"
}

variable "location" {
  description = "BigQuery and GCS location"
  type        = string
  default     = "US"
}

variable "imdb_prefix" {
  description = "Prefix for IMDb resources"
  type        = string
  default     = "imdb"
}

variable "gcp_service_list" {
  type        = list(string)
  description = "The list of apis necessary for the project"
  default     = ["storage.googleapis.com"]
}
