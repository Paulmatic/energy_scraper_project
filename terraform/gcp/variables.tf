# GCP Project & Region
variable "gcp_project" {
  type        = string
  description = "GCP project ID"
}

variable "gcp_region" {
  type        = string
  description = "GCP region for resources"
}

variable "gcp_credentials_file" {
  type        = string
  description = "Path to GCP service account JSON file"
}

# Cloud SQL
variable "sql_instance_name" {
  type        = string
  description = "Cloud SQL instance name"
}

variable "sql_database_name" {
  type        = string
  description = "Database name"
}

variable "sql_user" {
  type        = string
  description = "Database username"
}

variable "sql_password" {
  type        = string
  description = "Database password"
  sensitive   = true
}

# Container Registry
variable "gcr_repo_name" {
  type        = string
  description = "GCP Container Registry repo name"
}

# OpenAI
variable "openai_api_key" {
  type        = string
  description = "OpenAI API Key"
  sensitive   = true
}
