terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.92"
    }
  }

  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "krldevopstodoapptfstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }

}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "Softwire21_KirstenLand_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-terraformed-todoapp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id

  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|kirstyland/todo-app:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "FLASK_APP"                  = "todo_app/app"
    "MONGO_CONNECTION_STRING"    = azurerm_cosmosdb_account.main.connection_strings[0]
    "MONGO_DATABASE_NAME"        = azurerm_cosmosdb_mongo_database.main.name,
    "SECRET_KEY"                 = var.secret_key
    "OAUTH_CLIENT_ID"            = var.oauth_client_id
    "OAUTH_CLIENT_SECRET"        = var.oauth_client_secret
    "WRITER_USER_IDS"            = var.writer_user_ids
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                 = "${var.prefix}-terraformed-cosmos-db-account"
  location             = data.azurerm_resource_group.main.location
  resource_group_name  = data.azurerm_resource_group.main.name
  offer_type           = "Standard"
  kind                 = "MongoDB"
  mongo_server_version = 4.2

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "todoapp-database"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  lifecycle {
    prevent_destroy = true
  }
}
