# --- using AWS Secrets Manager ---

resource "aws_secretsmanager_secret" "tech42_secrets" {
  name        = "${var.project_name}_secrets"
  description = "Environment variables for tech42-agent"
}

resource "aws_secretsmanager_secret_version" "tech42_secrets" {
  secret_id = aws_secretsmanager_secret.tech42_secrets.id

  secret_string = jsonencode({

    OPENAI_API_KEY = var.openai_api_key

    LANGFUSE_SECRET_KEY = var.langfuse_secret_key
    LANGFUSE_PUBLIC_KEY = var.langfuse_public_key
    LANGFUSE_BASE_URL   = var.langfuse_base_url
    LANGFUSE_ENABLED    = var.langfuse_enabled

    PINECONE_API_KEY    = var.pinecone_api_key
    PINECONE_INDEX_NAME = var.pinecone_index_name
    PINECONE_REGION     = var.pinecone_region

    COGNITO_REGION        = var.cognito_region
    COGNITO_CLIENT_SECRET = var.cognito_client_secret
    COGNITO_USER_POOL_ID  = data.aws_cognito_user_pools.tech42_pool.ids[0]
    COGNITO_APP_CLIENT_ID = var.cognito_client_id
  })
}
