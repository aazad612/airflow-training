locals {
  dataset_id = var.imdb_prefix
}

resource "google_bigquery_dataset" "imdb" {
  dataset_id  = local.dataset_id
  location    = var.location
  description = "IMDb daily pipeline dataset (auto-ingested via Composer & Dataflow)"
  labels = {
    environment = "dev"
  }

  depends_on = [
    google_service_account.etl,
  ]
}

resource "google_bigquery_table" "title_basics" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "title_basics"
  deletion_protection = false

  schema = jsonencode([
    { name = "tconst", type = "STRING", mode = "REQUIRED" },
    { name = "titleType", type = "STRING", mode = "NULLABLE" },
    { name = "primaryTitle", type = "STRING", mode = "NULLABLE" },
    { name = "originalTitle", type = "STRING", mode = "NULLABLE" },
    { name = "isAdult", type = "BOOL", mode = "NULLABLE" },
    { name = "startYear", type = "INT64", mode = "NULLABLE" },
    { name = "endYear", type = "INT64", mode = "NULLABLE" },
    { name = "runtimeMinutes", type = "INT64", mode = "NULLABLE" },
    { name = "genres", type = "STRING", mode = "REPEATED" }
  ])

  time_partitioning {
    type  = "DAY"
    field = null # ingestion-time partitioning
  }

  clustering = ["titleType", "startYear"]

  labels = {
    source = "imdb"
    type   = "core"
  }
}

# ----------------------------
# title.ratings.tsv.gz
# ----------------------------
resource "google_bigquery_table" "title_ratings" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "title_ratings"
  deletion_protection = false

  schema = jsonencode([
    { name = "tconst", type = "STRING", mode = "REQUIRED" },
    { name = "averageRating", type = "FLOAT64", mode = "NULLABLE" },
    { name = "numVotes", type = "INT64", mode = "NULLABLE" }
  ])

  # clustering = ["averageRating"]

  labels = {
    source = "imdb"
    type   = "ratings"
  }
}

# ----------------------------
# title.principals.tsv.gz
# ----------------------------
resource "google_bigquery_table" "title_principals" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "title_principals"
  deletion_protection = false

  schema = jsonencode([
    { name = "tconst", type = "STRING", mode = "REQUIRED" },
    { name = "ordering", type = "INT64", mode = "NULLABLE" },
    { name = "nconst", type = "STRING", mode = "NULLABLE" },
    { name = "category", type = "STRING", mode = "NULLABLE" },
    { name = "job", type = "STRING", mode = "NULLABLE" },
    { name = "characters", type = "STRING", mode = "NULLABLE" }
  ])

  clustering = ["category"]

  labels = {
    source = "imdb"
    type   = "credits"
  }
}

# ----------------------------
# name.basics.tsv.gz
# ----------------------------
resource "google_bigquery_table" "name_basics" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "name_basics"
  deletion_protection = false

  schema = jsonencode([
    { name = "nconst", type = "STRING", mode = "REQUIRED" },
    { name = "primaryName", type = "STRING", mode = "NULLABLE" },
    { name = "birthYear", type = "INT64", mode = "NULLABLE" },
    { name = "deathYear", type = "INT64", mode = "NULLABLE" },
    { name = "primaryProfession", type = "STRING", mode = "REPEATED" },
    { name = "knownForTitles", type = "STRING", mode = "REPEATED" }
  ])

  clustering = ["birthYear"]

  labels = {
    source = "imdb"
    type   = "people"
  }
}

# ----------------------------
# title.akas.tsv.gz
# ----------------------------
resource "google_bigquery_table" "title_akas" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "title_akas"
  deletion_protection = false

  schema = jsonencode([
    { name = "titleId", type = "STRING", mode = "REQUIRED" },
    { name = "ordering", type = "INT64", mode = "NULLABLE" },
    { name = "title", type = "STRING", mode = "NULLABLE" },
    { name = "region", type = "STRING", mode = "NULLABLE" },
    { name = "language", type = "STRING", mode = "NULLABLE" },
    { name = "types", type = "STRING", mode = "REPEATED" },
    { name = "attributes", type = "STRING", mode = "REPEATED" },
    { name = "isOriginalTitle", type = "BOOL", mode = "NULLABLE" }
  ])

  clustering = ["region", "language"]

  labels = {
    source = "imdb"
    type   = "localized"
  }
}

# ----------------------------
# title.episode.tsv.gz
# ----------------------------
resource "google_bigquery_table" "title_episodes" {
  dataset_id          = google_bigquery_dataset.imdb.dataset_id
  table_id            = "title_episodes"
  deletion_protection = false

  schema = jsonencode([
    { name = "tconst", type = "STRING", mode = "REQUIRED" },
    { name = "parentTconst", type = "STRING", mode = "NULLABLE" },
    { name = "seasonNumber", type = "INT64", mode = "NULLABLE" },
    { name = "episodeNumber", type = "INT64", mode = "NULLABLE" }
  ])

  clustering = ["parentTconst", "seasonNumber"]

  labels = {
    source = "imdb"
    type   = "episodes"
  }
}
