## provider AWS

terraform {
  required_version = ">= 1.14.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Name        = "tech42-agent"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

## --- Data Sources ---
# current AWS account ID and region- used in other files
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
