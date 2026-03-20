import logging
logging.getLogger("opentelemetry").setLevel(logging.ERROR)
import asyncio
from langchain_core.messages import HumanMessage
from src.agent.workflow import agent_executor

# from langfuse.callback import CallbackHandler
from langfuse.langchain import CallbackHandler  # ✅

handler = CallbackHandler()

async def test_agent():
    query = "Compare Amazon's recent stock performance to what analysts predicted in their reports"
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # Test streaming
    print("Testing streaming output:")
    async for output in agent_executor.astream(inputs, config={"callbacks": [handler]}):
        # output is a dict with node names as keys
        for key, value in output.items():
            print(f"\n--- Node: {key} ---")
            if "messages" in value:
                # print last message
                last_msg = value["messages"][-1]
                print(f"Message: {last_msg.content}")
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    print(f"Tool Calls: {last_msg.tool_calls}")

                    

if __name__ == "__main__":
    asyncio.run(test_agent())
