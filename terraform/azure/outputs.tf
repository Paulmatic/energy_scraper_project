output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "app_service_url" {
  value = azurerm_linux_web_app.app.default_hostname
}

output "sql_connection_string" {
  value     = azurerm_linux_web_app.app.app_settings["DATABASE_URL"]
  sensitive = true
}
output "openai_endpoint" {
  value = var.openai_endpoint
}

output "openai_deployment" {
  value = var.openai_deployment
}
