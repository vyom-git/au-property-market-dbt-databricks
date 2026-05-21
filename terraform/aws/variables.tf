variable "aws_region" {
  description = "AWS region where the S3 landing bucket is located."
  type        = string
  default     = "ap-southeast-2"
}

variable "bucket_name" {
  description = "Name of the S3 landing bucket for raw property sales data."
  type        = string
  default     = "au-property-market-landing-313589910075-ap-southeast-2-an"
}

variable "environment" {
  description = "Environment name for tagging resources."
  type        = string
  default     = "dev"
}