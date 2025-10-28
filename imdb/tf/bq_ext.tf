locals {
  curated_uri = "gs://${google_storage_bucket.curated.name}"
}

resource "google_bigquery_table" "ext_title_basics" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "ext_title_basics"
  deletion_protection = false

  external_data_configuration {
    source_format = "PARQUET"
    autodetect    = true

    source_uris = [
      "${local.curated_uri}/title_basics/dt=*/part-*.parquet"
    ]

    hive_partitioning_options {
      mode              = "AUTO"
      source_uri_prefix = "${local.curated_uri}/title_basics/"
    }
  }

  labels = {
    source = "imdb"
    layer  = "external"
  }
}

# ----------------------------
# External: title_ratings
# ----------------------------
resource "google_bigquery_table" "ext_title_ratings" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "ext_title_ratings"
  deletion_protection = false

  external_data_configuration {
    source_format = "PARQUET"
    autodetect    = true

    source_uris = [
      "${local.curated_uri}/title_ratings/dt=*/part-*.parquet"
    ]

    hive_partitioning_options {
      mode              = "AUTO"
      source_uri_prefix = "${local.curated_uri}/title_ratings/"
    }
  }

  labels = {
    source = "imdb"
    layer  = "external"
  }
}

# ----------------------------
# External: title_principals
# ----------------------------
resource "google_bigquery_table" "ext_title_principals" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "ext_title_principals"
  deletion_protection = false

  external_data_configuration {
    source_format = "PARQUET"
    autodetect    = true

    source_uris = [
      "${local.curated_uri}/title_principals/dt=*/part-*.parquet"
    ]

    hive_partitioning_options {
      mode              = "AUTO"
      source_uri_prefix = "${local.curated_uri}/title_principals/"
    }
  }

  labels = {
    source = "imdb"
    layer  = "external"
  }
}

# ----------------------------
# External: name_basics
# ----------------------------
resource "google_bigquery_table" "ext_name_basics" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "ext_name_basics"
  deletion_protection = false

  external_data_configuration {
    source_format = "PARQUET"
    autodetect    = true

    source_uris = [
      "${local.curated_uri}/name_basics/dt=*/part-*.parquet"
    ]

    hive_partitioning_options {
      mode              = "AUTO"
      source_uri_prefix = "${local.curated_uri}/name_basics/"
    }
  }

  labels = {
    source = "imdb"
    layer  = "external"
  }
}

# ----------------------------
# External: title_akas
# ----------------------------
resource "google_bigquery_table" "ext_title_akas" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "ext_title_akas"
  deletion_protection = false

  external_data_configuration {
    source_format = "PARQUET"
    autodetect    = true

    source_uris = [
      "${local.curated_uri}/title_akas/dt=*/part-*.parquet"
    ]

    hive_partitioning_options {
      mode              = "AUTO"
      source_uri_prefix = "${local.curated_uri}/title_akas/"
    }
  }

  labels = {
    source = "imdb"
    layer  = "external"
  }
}

# ----------------------------
# External: title_episodes
# ----------------------------
resource "google_bigquery_table" "ext_title_episodes" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "ext_title_episodes"
  deletion_protection = false

  external_data_configuration {
    source_format = "PARQUET"
    autodetect    = true

    source_uris = [
      "${local.curated_uri}/title_episodes/dt=*/part-*.parquet"
    ]

    hive_partitioning_options {
      mode              = "AUTO"
      source_uri_prefix = "${local.curated_uri}/title_episodes/"
    }
  }

  labels = {
    source = "imdb"
    layer  = "external"
  }
}
