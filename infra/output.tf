
output "agentcore_endpoint" {
  description = "Agentcore runtime endpoint URL"
  value       = aws_bedrockagentcore_agent_runtime.tech42_runtime.agent_runtime_arn
}

output "ecr_repository_url" {
  description = "ECR repository URL for docker push"
  value       = aws_ecr_repository.tech42_agent.repository_url
}
