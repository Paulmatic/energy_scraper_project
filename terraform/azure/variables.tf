variable "subscription_id" {}
variable "tenant_id" {}
variable "client_id" {}
variable "client_secret" {}

variable "location" {
  default = "westus2"
}

variable "resource_group_name" {
  default = "rg-hybrid-scrapper"
}

variable "acr_name" {
  default = "hybridacr01"
}

variable "app_service_plan_name" {
  default = "hybrid-asp"
}

variable "app_service_name" {
  default = "hybrid-app-service"
}

variable "sql_server_name" {
  description = "Name of the Azure SQL Server"
}

variable "sql_admin_user" {
  description = "SQL Admin username"
}

variable "sql_admin_password" {
  description = "SQL Admin password"
  sensitive   = true
}

variable "sql_database_name" {
  description = "Name of the Azure SQL Database"
}
# OpenAI Settings
variable "openai_api_key" {
  description = "OpenAI API key"
  sensitive   = true
}

variable "openai_endpoint" {
  description = "OpenAI endpoint (for Azure or OpenAI API)"
  default     = "https://api.openai.com/v1"
}

variable "openai_deployment" {
  description = "OpenAI model deployment name"
  default     = "text-embedding-3-small"
}

