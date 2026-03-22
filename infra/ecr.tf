##--- ECR Repository for Docker Images ----

resource "aws_ecr_repository" "tech42_agent" {
  name                 = "${var.project_name}-${var.environment}"
  image_tag_mutability = "MUTABLE" # allow overwrite images

  image_scanning_configuration {
    scan_on_push = true #scan push images
  }

  tags = {
    Name = "${var.project_name}-ecr"
  }
}

## --- ECR Lyfecycle Policy ----
## save only 3 images
resource "aws_ecr_lifecycle_policy" "tech42_agent" {
  repository = aws_ecr_repository.tech42_agent.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 3 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 3
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
