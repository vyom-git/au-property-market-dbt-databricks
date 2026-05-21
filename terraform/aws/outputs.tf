output "bucket_name" {
  description = "Name of the S3 landing bucket."
  value       = aws_s3_bucket.property_landing.bucket
}

output "bucket_arn" {
  description = "ARN of the S3 landing bucket."
  value       = aws_s3_bucket.property_landing.arn
}

output "aws_region" {
  description = "AWS region used by this Terraform configuration."
  value       = var.aws_region
}