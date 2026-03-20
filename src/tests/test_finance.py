from src.agent.finance_tools import retrieve_realtime_stock_price, retrieve_historical_stock_price
from src.agent.workflow import get_agent_executor
from langchain_core.messages import HumanMessage

def test_tools():
    print("Testing retrieve_realtime_stock_price...")
    print(retrieve_realtime_stock_price.invoke("NVDA"))
    
    print("\nTesting retrieve_historical_stock_price...")
    print(retrieve_historical_stock_price.invoke({"ticker": "TSLA", "period": "1mo"}))

def test_agent():
    print("\nTesting Agent with Finance Query...")
    executor = get_agent_executor()
    
    query = "What is the current price of NVIDIA (NVDA) and how has it performed in the last month?"
    inputs = {"messages": [HumanMessage(content=query)]}
    
    for chunk in executor.stream(inputs):
        for node, output in chunk.items():
            print(f"\n--- Node: {node} ---")
            for msg in output["messages"]:
                if msg.content:
                    print(msg.content)
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    print(f"Tool Calls: {msg.tool_calls}")

if __name__ == "__main__":
    test_tools()
    # test_agent()
