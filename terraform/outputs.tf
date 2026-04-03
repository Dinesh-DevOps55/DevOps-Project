# Useful values for CI/CD and kubectl setup.
output "cluster_name" {
  description = "EKS cluster name."
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "EKS API server endpoint."
  value       = module.eks.cluster_endpoint
}

output "user_service_ecr_repository_url" {
  description = "URI of user-service ECR repository."
  value       = aws_ecr_repository.user_service.repository_url
}

output "product_service_ecr_repository_url" {
  description = "URI of product-service ECR repository."
  value       = aws_ecr_repository.product_service.repository_url
}
