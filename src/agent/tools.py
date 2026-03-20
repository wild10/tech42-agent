from langchain.tools import tool
# from src.rag.retriever import get_retriever
from src.agent.finance_tools import retrieve_realtime_stock_price, retrieve_historical_stock_price
from src.agent.rag_tool import retrieve_doc


def get_tools():
    """
    Returns a list of tools available for the agent.
    """
    return [
        retrieve_doc,
        retrieve_realtime_stock_price,
        retrieve_historical_stock_price
    ]
