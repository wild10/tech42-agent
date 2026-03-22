## --- IAM Role for AgentCore ---

resource "aws_iam_role" "agentcore_role" {
  name = "${var.project_name}-agentcore-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "bedrock-agentcore.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-agentcore-role"
  }
}


# --- IAM Policy for AgentCore ---

resource "aws_iam_policy" "agentcore_policy" {
  name        = "${var.project_name}-agentcore-policy"
  description = "Permissions for AgentCore runtime "

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # ECR - pull docker image
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      },
      # CloudWatch -logs
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      # Cognito -validate tokens
      {
        Effect = "Allow"
        Action = [
          "cognito-idp:DescribeUserPool",
          "cognito-idp:DescribeUserPoolClient"
        ]
        Resource = tolist(data.aws_cognito_user_pools.tech42_pool.arns)[0] # arn REAL
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = aws_secretsmanager_secret.tech42_secrets.arn
      }
    ]

  })

}

# ---- Attach policies to role ----
resource "aws_iam_role_policy_attachment" "agentcore_attachment" {
  role       = aws_iam_role.agentcore_role.name
  policy_arn = aws_iam_policy.agentcore_policy.arn
}
