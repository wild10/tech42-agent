# Tech42-Agent: Agentic Finance Consultant

This project is an agentic chat assistant designed to help users with financial information leveraging external knowledge. It uses modern AI technologies including RAG (Retrieval-Augmented Generation), LangGraph for decision-making (ReAct methodology), and Pinecone as a vector database.

## 🚀 Features

- **RAG Pipeline**: Processes PDFs to provide context-aware answers.
- **Agentic Logic**: Uses LangGraph to decide when to retrieve information or use tools.
- **Vector Search**: Integrated with Pinecone for efficient document retrieval.
- **Modern Stack**: Built with LangChain, OpenAI, and Poetry.

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
│   └── pdfs/           # Document source for RAG
├── src/
│   ├── agent/          # LangGraph logic and tools
│   │   ├── tools.py
│   │   └── workflow.py
│   ├── rag/            # RAG Pipeline components
│   │   ├── embeddings.py
│   │   ├── ingest.py
│   │   ├── loader.py
│   │   ├── pipeline.py
│   │   ├── retriever.py
│   │   ├── splitter.py
│   │   └── vectorstore.py
│   ├── config.py       # Configuration loader
│   ├── ingest_docs.py  # Main ingestion script
│   ├── llm.py          # LLM Factory
│   ├── main.py         # Entry point for the agent
│   └── test_rag.py     # RAG testing script
├── .env                # Environment variables (ignored by git)
├── .gitignore          # Git ignore rules
├── pyproject.toml      # Project dependencies and configuration
└── README.md           # This file
```

## 🚀 Usage

### 1. Ingest Documents
Place your PDFs in `data/pdfs/` and run the ingestion script to populate the vector store:

```bash
python src/ingest_docs.py
```

### 2. Run the Agent
Start the interactive chat agent:

```bash
python src/main.py
```

### 3. Testing
Run the RAG test script to verify retrieval and generation:

```bash
python src/test_rag.py
```
