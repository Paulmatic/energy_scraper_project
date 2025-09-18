output "gcr_repo_url" {
  value = google_artifact_registry_repository.gcr.repository_id
}

output "cloud_run_url" {
  value = google_cloud_run_service.app.status[0].url
}

output "sql_connection_string" {
  value     = "postgresql://${var.sql_user}:${var.sql_password}@${google_sql_database_instance.sql.connection_name}/${var.sql_database_name}"
  sensitive = true
}
