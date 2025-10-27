locals {
  raw_bucket     = "${var.project_id}-${var.imdb_prefix}-raw"
  curated_bucket = "${var.project_id}-${var.imdb_prefix}-curated"
  tmp_bucket     = "${var.project_id}-${var.imdb_prefix}-tmp"
}

resource "google_storage_bucket" "raw" {
  name                        = local.raw_bucket
  location                    = var.location
  uniform_bucket_level_access = true
  force_destroy               = true
  versioning { enabled = true }

  lifecycle_rule {
    condition { age = 90 }
    action { type = "Delete" }
  }

  labels = {
    environment = "dev"
    type        = "raw"
  }

  depends_on = [
    google_service_account.etl,
  ]
}

resource "google_storage_bucket" "curated" {
  name                        = local.curated_bucket
  location                    = var.location
  uniform_bucket_level_access = true
  versioning { enabled = true }

  labels = {
    environment = "dev"
    type        = "curated"
  }

  depends_on = [
    google_service_account.etl,
  ]

}

resource "google_storage_bucket" "tmp" {
  name                        = local.tmp_bucket
  location                    = var.location
  uniform_bucket_level_access = true
  force_destroy               = true

  labels = {
    environment = "dev"
    type        = "temp"
  }
  depends_on = [
    google_service_account.etl,
  ]

}


