variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "secret_key" {
  description = "Secret Key for encrypting the session"
  sensitive   = true
}

variable "oauth_client_id" {
  description = "OAuth client id"
}

variable "oauth_client_secret" {
  description = "OAuth client secret"
  sensitive   = true
}

variable "writer_user_ids" {
  description = "User Ids of users with the role WRITER"
  default     = ""
  sensitive   = true
}
