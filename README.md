# Tech42-Agent: Agentic Finance Consultant

This project is an agentic chat assistant designed to help users with financial information about AMAZON, leveraging external knowledge. It uses modern AI technologies including **RAG (Retrieval-Augmented Generation)** as knowledge base,external** @tools(api calls)** and an **agentic workflow using LangGraph for decision-making (ReAct methodology)**.  Pinecone as a vector database and was deployed using **AWS Bedrock AgentCore** host runtime using **IaC Terraform** for fast and reliable deployment and a Notebook(jupyter) as a demo for testing.

## 🚀 Features

- **RAG Pipeline**: Processes PDFs to provide context-aware answers.
- **Finance Tools**: Real-time and historical stock price retrieval via `yfinance`.
- **Agentic Logic**: Uses LangGraph to decide when to retrieve information, check stock prices, or continue reasoning.
- **Vector Search**: Integrated with Pinecone for efficient document retrieval.
- **tools**: Structured to easily external access through Yfinance for stock prices.
- **Monitoring**: Performance tracking with Langfuse.

## 🛠️ Initial Project Setup (dev)

This project uses [Poetry](https://python-poetry.org/) or [uv](https://docs.astral.sh/uv/) for dependency management.

open your terminal and run the following commands:
```bash
mkdir tech42-agent
cd tech42-agent

## Install dependencies
uv sync .
# Add new dependencies
uv add <package_name>
```

## ⚙️ Setup & Requirements
as you want to run the full project, you need many credentials from different platforms,you can check out this in the .env.example file. create the .env file and replace the values they are like below.
```env
OPENAI_API_KEY=your_openai_api_key
LANGFUSE_PUBLIC_KEY= ...others
```

## 🏗️ Project Architecture

```text
tech42-agent/
├── data/
│   └── pdfs/           # Document source for RAG (PDFs)
├── infra/
│   ├── main.tf         # Provider AWS + backend config.
│   |-- variables.tf    # Variables for the infra.
│   |-- ecr.tf          # ECR repository config.
|   |-- iam.tf          # IAM roles and policies config.
|   |-- cognito.tf      # Cognito User Pool + Client 
│   |-- agentcore.tf    # AgentCore Runtime
│   |-- outputs.tf      # Outputs (endpoint, URL,ECR URL etc)
|   |-- terraform.tfvars # Real values (not in git)
├── notebooks/
│   └── demo_invocation_aws.ipynb  # Notebook demo API usage AWS
│   └── demo_invocation_local.ipynb  # Notebook demo local usage
├── src/
|   |-- api/
|   |   |-- middleware/
|   |   |   |-- auth.py 
|   |   |-- routes/ 
|   |   |   |-- agent.py 
|   |   |-- app.py
|   |   |-- schemas.py
|   |   
│   ├── agent/          # LangGraph logic and tools
|   |   ├── prompts.py       # System prompt for the agent
|   |   ├── state.py         # State definition for the agent
|   |   ├── finance_tools.py # toos & yfinance integration
│   │   ├── tools.py         # Main tool registry & calls 
│   │   └── workflow.py      # ReAct + LangGraph StateGraph (agent graph)
|   |---core
│   |   ├── config.py        # Configuration loader
│   |   ├── llm.py           # LLM Factory
│   |---observability
│   |   ├── langfuse.py      # Langfuse integration
│   |---rag/                 # RAG Pipeline components
│   │   ├── embeddings.py
│   │   ├── ingest.py
│   │   ├── loader.py
│   │   ├── pipeline.py
│   │   ├── retriever.py
│   │   ├── splitter.py
│   │   └── vectorstore.py
|   |-- tests
│   |   ├── test_agent.py      # Test Agent + Langfuse
│   |   ├── test_rag.py        # Test RAG + Pinecone
│   |   └── test_finance.py    # Test yfinance api as function.
│   ├── ingest_docs.py         # Main ingestion PDFS, Docs to Pinecone
│   ├── main.py                # Entry point for the agent
├── .env                       # Environment variables (ignored by git)
├── .dockerignore              # Docker ignore rules
├── Dockerfile                 # Dockerfile
├── .gitignore                 # Git ignore rules
├── pyproject.toml               # Project dependencies and configuration
└── README.md                    # This file
```
### demo here 

demo video link [video](https://drive.google.com/file/d/1n7i_04cDHQgOdEw-0sJ0alwYrIvYlVxI/view?usp=sharing)

<video src="notebooks/test-video-demo-tech42.mp4" controls title="Video demo" width="400" height="200">
  Your browser does not support the video tag.
</video>

### 1. Ingest Documents(pdfs)
Place your PDFs in `data/pdfs/` and run the ingestion script to populate the vector store.
Note: I am using Pinecone as vector store and openai as embedding model, you need to create your account in [Pinecone](https://www.pinecone.io/) and [OpenAI](https://openai.com/) and setup .env file with your credentials.
```bash
python src/ingest_docs.py
```
### 2. Run every module
If you want to test every module you can use poetry or [uv](https://docs.astral.sh/uv/).

```bash
    # with poetry 
    uv run python -m folder.file
    #example
    poetry run python -m src.main
```

### 3. Run the Agent and Api (dev locally)
for dev and local testing first you can create and use the docker image.
```bash
    #build 
    docker build -t tech42_agent-prod:latest .
    #run 
    docker run --env-file .env -p 8080:8080 tech42_agent-prod:latest
```

### 4 Test Registered and Access user for cognito

these below emails were setup for test purposes of login and access to the API.
these users are created in the AWS Cognito User Pool for testing purpose.

Allowed user for testing:

user1: teach42@gmail.com
password: Tech421!
<!-- 
user2: test12@gmail.com
password: test12AI! -->

user1: user@gmail.com
password: [PASSWORD]

user2: test2@gmail.com
password: [PASSWORD]

# Deployment procedure aws agentcore runtime

For this deployment you need to have [terraform](https://developer.hashicorp.com/terraform) installed and configured in your machine as we are going to use IaC (Infrastructure as Code) for this deployment.

the procedure is as follows:
- Login to AWS ECR(Elastic Container Registry) as repository for the docker image.
- Build the docker image (for arm64 architecture only accepted by AWS AgentCore)
- Tag and push the image to ECR, this will make it callable by AWS AgentCore.
- Deploy the rest of the resources using terraform, this will create the AgentCore runtime and other resources.

## 1. Create the  ECR resource using terraform

This command will create the ECR resource using terraform. to do that you must be in the `infra` folder.

```bash
terraform apply -target=aws_ecr_repository.tech42_agent
```

Output sample:

```bash
ecr_repository_url = "129987787606.dkr.ecr.us-east-1.amazonaws.com/tech42_agent-prod"
```

## 2. From the root of the project — build and push your image

From the root of the project you need to build the [docker](https://www.docker.com/) image and push it  to ECR. 

quoete: if you are in the amd64 or any other then you can test it locally using the command below, but for aws agentcore you must use arm64 architecture.

building with amd64 for local testing purpose.
```bash
cd ..
docker build -t tech42_agent-prod .
```
This command will build the docker image in amd64 architecture ready for agentcore deployment.

the image must be in arm64 architecture i used buildx which has arm64 kernel installed in ubuntu(linux) to generate this and push it to ecr.

###  Build para arm64( (udpate, build an push to ecr)

```bash
docker buildx build --platform linux/arm64 \
  -t 129987787606.dkr.ecr.us-east-1.amazonaws.com/tech42_agent-prod:latest \
  --push \
  .
```

## 3. Login to ECR (Only once)

After we have our image we are ready to push it to ECR. first we need to login to aws ecr and then push our image to this space.

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  129987787606.dkr.ecr.us-east-1.amazonaws.com
```

## 4. Tag and push

This is very important to tag the image, as in dev we use to have many versions of the same image, so we need to tag it.

```bash
docker tag tech42_agent-prod:latest \
  129987787606.dkr.ecr.us-east-1.amazonaws.com/tech42_agent-prod:latest

docker push \
  129987787606.dkr.ecr.us-east-1.amazonaws.com/tech42_agent-prod:latest

```

## 5. Deploy the rest

Atfter pushing the image to ECR you can deploy the rest of the resources using terraform IaC definded in this project in the folder `infra`.

```bash

  cd infra/
  terraform apply

```
you can check the runtime(i defined as'tech42_agent_runtime') out in the aws bedrock agentcore console and use the sandboxt test with the endpoint, interactive chatbot.

## 6. Test the Agent

for this demo i prepare 2 notebooks that test localally and cloud deployment.
**Note: you need newest boto3>=1.42 version** if you want to run from other folder.
`demo_notebook_local.ipynb` - for local testing (use cognito login), local host agent is running on port 8080.
`demo_notebook_cloud.ipynb` - for cloud deployment (use cognito login), cloud agent is running on aws agentcore runtime.