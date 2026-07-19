variable "project_name" {
  description = "Branch-scoped project name used as a resource prefix."
  type        = string
}

variable "ssh_public_key" {
  description = "RSA public key injected by the platform for SSH access."
  type        = string
}

variable "db_password" {
  description = "Master password for the RDS Postgres instance."
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Initial database name."
  type        = string
  default     = "shortener"
}

variable "db_username" {
  description = "Master username for the RDS Postgres instance."
  type        = string
  default     = "shortener"
}
