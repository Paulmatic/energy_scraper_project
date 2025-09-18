# Google Artifact Registry
resource "google_artifact_registry_repository" "gcr" {
  provider     = google
  location     = var.gcp_region
  repository_id = var.gcr_repo_name
  format       = "DOCKER"
}

# Cloud SQL (PostgreSQL)
resource "google_sql_database_instance" "sql" {
  name             = var.sql_instance_name
  database_version = "POSTGRES_15"
  region           = var.gcp_region

  settings {
    tier = "db-f1-micro"
  }

  root_password = var.sql_password
}

resource "google_sql_database" "db" {
  name     = var.sql_database_name
  instance = google_sql_database_instance.sql.name
}

resource "google_sql_user" "db_user" {
  name     = var.sql_user
  instance = google_sql_database_instance.sql.name
  password = var.sql_password
}

# Cloud Run (App Deployment)
resource "google_cloud_run_service" "app" {
  name     = "energy-scraper-app"
  location = var.gcp_region

  template {
    spec {
      containers {
        image = "${google_artifact_registry_repository.gcr.repository_id}-docker.pkg.dev/${var.gcp_project}/${var.gcr_repo_name}/energy-scraper:latest"
        env {
          name  = "DATABASE_URL"
          value = "postgresql://${var.sql_user}:${var.sql_password}@${google_sql_database_instance.sql.connection_name}/${var.sql_database_name}"
        }
        env {
          name  = "OPENAI_API_KEY"
          value = var.openai_api_key
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  service = google_cloud_run_service.app.name
  location = var.gcp_region
  role    = "roles/run.invoker"
  member  = "allUsers"
}
