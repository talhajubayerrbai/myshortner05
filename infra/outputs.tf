output "instance_ip" {
  description = "Elastic IP of the app server."
  value       = aws_eip.app.public_ip
}

output "rds_endpoint" {
  description = "RDS Postgres hostname (without port)."
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "RDS Postgres port."
  value       = aws_db_instance.postgres.port
}
