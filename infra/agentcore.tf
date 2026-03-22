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

  # Only cognito will call my API
  authorizer_configuration {
    custom_jwt_authorizer {
      discovery_url    = "https://cognito-idp.${var.aws_region}.amazonaws.com/${data.aws_cognito_user_pools.tech42_pool.ids[0]}/.well-known/openid-configuration"
      allowed_audience = [var.cognito_client_id]
    }
  }

  environment_variables = {
    ENVIRONMENT = var.environment
  }

  tags = {
    Name = "${var.project_name}_runtime"
  }
}
