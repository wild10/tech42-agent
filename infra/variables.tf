variable "aws_region" {
  description = "AWS region to deploy resource"
  type        = string
  default     = "us-east-1"

}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "tech42 financial ai agent"
  type        = string
  default     = "tech42-agent"
}

variable "cognito_user_pool_name" {
  description = "Existing Cognito User Pool name"
  type        = string
}

variable "cognito_client_id" {
  description = "Existing Cognito User Pool Client ID"
  type        = string
}

variable "openai_api_key" {
  description = "OpenAI API Key"
  type        = string
  sensitive   = true # <- not shots in logs terraform.
}

variable "langfuse_secret_key" {
  description = "Langfuse Secret Key"
  type        = string
  sensitive   = true
}

variable "langfuse_public_key" {
  description = "Langfuse Public Key"
  type        = string
}

variable "langfuse_base_url" {
  description = "Langfuse Base URL"
  type        = string
}

variable "langfuse_enabled" {
  description = "Langfuse Enabled"
  type        = string
}

variable "pinecone_api_key" {
  description = "Pinecone API Key"
  type        = string
}

variable "pinecone_index_name" {
  description = "Pinecone Index Name"
  type        = string
}

variable "pinecone_region" {
  description = "Pinecone Region"
  type        = string
}

variable "cognito_client_secret" {
  description = "Cognito Client Secret"
  type        = string
}

variable "cognito_region" {
  description = "Cognito Region"
  type        = string
}
