# from langfuse.langchain import CallbackHandler
# from src.core.config import settings

# def get_callbacks() -> list:
#     if not settings.LANGFUSE_ENABLED:
#         return []
#     return [CallbackHandler(
#         public_key=settings.LANGFUSE_PUBLIC_KEY,
#         secret_key=settings.LANGFUSE_SECRET_KEY,
#     )]
# src/observability/langfuse_handler.py
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from src.core.config import settings

_langfuse_client: Langfuse | None = None

def get_callbacks() -> list:
    if not settings.LANGFUSE_ENABLED:
        return []
    
    global _langfuse_client
    _langfuse_client = Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
    )
    return [CallbackHandler()]

def flush():
    """Llamar al salir del chat loop o al shutdown de FastAPI."""
    if _langfuse_client:
        _langfuse_client.flush()