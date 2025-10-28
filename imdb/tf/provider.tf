terraform {
  required_version = ">= 1.5"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

provider "google" {
  credentials = file("/Users/johneyaazad/gcloud/learn-by-doing-data-engg-cfe.json")
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}