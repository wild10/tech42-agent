from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from src.core.config import settings

_langfuse_client: Langfuse | None = None

if settings.LANGFUSE_ENABLED:
    _langfuse_client = Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_HOST
    )

def get_callbacks() -> list:
    """
    Returns a list containing the Langfuse CallbackHandler if enabled.
    """
    if not settings.LANGFUSE_ENABLED:
        return []
    
    return [CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY
    )]

def flush():
    """
    Ensure all traces are sent to Langfuse.
    Call this on application shutdown.
    """
    global _langfuse_client
    if _langfuse_client:
        _langfuse_client.flush()
    # Alternatively, the CallbackHandler handles its own flushing, 
    # but having a manual flush can be useful.