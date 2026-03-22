## --- Reference existing Cognito user Pool --- 

data "aws_cognito_user_pools" "tech42_pool" {
  name = var.cognito_user_pool_name
}

data "aws_cognito_user_pool_client" "tech42_client" {
  user_pool_id = data.aws_cognito_user_pools.tech42_pool.ids[0]
  client_id    = var.cognito_client_id
}
