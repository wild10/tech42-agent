import logging
import os

from dotenv import load_dotenv

# load var in env.
load_dotenv()


## load the credentials from the local env.
OPEN_API_KEY = os.getenv("OPENAI_API_KEY_TOKEN")
if not OPEN_API_KEY:
    logging.error("The OpenAI api key not found!")

# Load the Vector DB credentials PINECONE
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_REGION =  os.getenv("PINECONE_REGION")


if __name__ =='__main__':
    print(OPEN_API_KEY)
    print(PINECONE_API_KEY)

