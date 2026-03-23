import logging
import os

from dotenv import load_dotenv

#adding 
import json 

def load_secrets():
    secret_arn = os.getenv("SECRET_ARN")
    if secret_arn:
        import boto3
        try:
            client = boto3.client('secretsmanager', region_name="us-east-1")
            response = client.get_secret_value(SecretId=secret_arn)
            secrets = json.loads(response['SecretString'])
            for key, value in secrets.items():
                os.environ[key] = str(value)
            logging.info("✅ Secrets loaded from AWS Secrets Manager")
        except Exception as e:
            logging.error(f"❌ Failed to load secrets: {e}")
    else:
        load_dotenv()
        logging.info("✅ Secrets loaded from .env")

load_secrets()


# load var in env.
# load_dotenv()


## load the credentials from the local env.
OPEN_API_KEY = os.getenv("OPENAI_API_KEY_TOKEN")
if not OPEN_API_KEY:
    logging.error("The OpenAI api key not found!")

# Load the Vector DB credentials PINECONE
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_REGION =  os.getenv("PINECONE_REGION")

class LangfuseSettings:
    LANGFUSE_ENABLED = os.getenv("LANGFUSE_ENABLED", "false").lower() == "true"
    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# Cognito Settings
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_REGION = os.getenv("COGNITO_REGION", "us-east-1")

settings = LangfuseSettings()

if __name__ =='__main__':
    print(OPEN_API_KEY)
    print(PINECONE_API_KEY)

