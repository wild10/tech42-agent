#--- AgentCore Runtime --- 

resource "aws_bedrockagentcore_agent_runtime" "tech42_runtime" {
  agent_runtime_name = "${var.project_name}_runtime"
  description        = "Tech42 Financial AI Agent - FastAPI Runtime"
  role_arn           = aws_iam_role.agentcore_role.arn

  # setup container tags name
  agent_runtime_artifact {
    container_configuration {
      container_uri = "${aws_ecr_repository.tech42_agent.repository_url}:latest"
    }
  }

  # Public access over the internet.
  network_configuration {
    network_mode = "PUBLIC"
  }


  #setup environment variables
  environment_variables = {
    ENVIRONMENT = var.environment
    SECRET_ARN  = aws_secretsmanager_secret.tech42_secrets.arn
  }


  # Agentcore inject secrets as env vars
  #secret_arn = aws_secretsmanager_secret.tech42_secrets.arn

  # setup tags name
  tags = {
    Name = "${var.project_name}_runtime"
  }
}
