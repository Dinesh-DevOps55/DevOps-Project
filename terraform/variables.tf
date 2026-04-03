# Input variables to keep Terraform reusable across environments.
variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster."
  type        = string
  default     = "devops-demo-eks"
}

variable "vpc_name" {
  description = "Name for the VPC."
  type        = string
  default     = "devops-demo-vpc"
}

variable "user_service_repo_name" {
  description = "ECR repo name for user-service."
  type        = string
  default     = "user-service"
}

variable "product_service_repo_name" {
  description = "ECR repo name for product-service."
  type        = string
  default     = "product-service"
}
