# Tech42-Agent: Agentic Finance Consultant

This project is an agentic chat assistant designed to help users with financial information leveraging external knowledge. It uses modern AI technologies including RAG (Retrieval-Augmented Generation), LangGraph for decision-making (ReAct methodology), and Pinecone as a vector database.

## 🚀 Features

- **RAG Pipeline**: Processes PDFs to provide context-aware answers.
- **Finance Tools**: Real-time and historical stock price retrieval via `yfinance`.
- **Agentic Logic**: Uses LangGraph to decide when to retrieve information, check stock prices, or continue reasoning.
- **Vector Search**: Integrated with Pinecone for efficient document retrieval.
- **MCP Ready**: Structured to easily transition to Model Context Protocol for tool scaling.
- **Monitoring**: Performance tracking with Langfuse.

## 🛠️ Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## ⚙️ Setup & Requirements

Create a `.env` file in the root directory with the following credentials:

```env
OPENAI_API_KEY=your_openai_api_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=your_langfuse_host

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=tech42-vdb
PINECONE_REGION=us-east-1
```

## 🏗️ Project Architecture

```text
tech42-agent/
├── data/
│   └── pdfs/           # Document source for RAG (PDFs)
├── notebooks/
│   └── demo_invocation.ipynb  # Notebook demo API usage
├── src/
|   |-- api/
|   |   |-- main.py
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
|   |---infra/
|   |   ├── main.tf          # Provider AWS + configuración general
|   |   |-- variable
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

## 🚀 Usage

### 1. Ingest Documents
Place your PDFs in `data/pdfs/` and run the ingestion script to populate the vector store:

```bash
python src/ingest_docs.py
```

### 2. Run every module

to test every module using poetry o uv you must follow them 

```bash
    # with poetry 
    poetry run python folder/file.py
    #example
    poetry run python -m src.main.py
```

### 3. Creating the docker
As we are using uv for fast manage and independency  you create a easy way
using docker image and run it using  below code

```bash
    #build 
    docker build -t tech42-agent .
    #run 
    docker run --env-file .env -p 8000:8000 tech42-agent
```

### 4 Access user for cognito

user1: teach42@gmail.com
password: Tech421!

user2: test12@gmail.com
password: test12AI!
