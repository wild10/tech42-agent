import logging
logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)

import asyncio
from langchain_core.messages import HumanMessage
from src.agent.workflow import agent_executor
from langfuse.langchain import CallbackHandler
from langfuse import Langfuse

async def test_agent1():
    Langfuse_client = Langfuse()
    handler = CallbackHandler()  # instancia dentro del async context, no fuera
    
    query = "how much the AWS sales increase in percentage in the 2024?"
    inputs = {"messages": [HumanMessage(content=query)]}
    
    print("Testing streaming output:")
    try:
        async for output in agent_executor.astream(inputs, config={"callbacks": [handler]}):
            for key, value in output.items():
                print(f"\n--- Node: {key} ---")
                if "messages" in value:
                    last_msg = value["messages"][-1]
                    print(f"Message: {last_msg.content}")
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        print(f"Tool Calls: {last_msg.tool_calls}")
    finally:
        Langfuse_client.flush()  # garantiza flush incluso si hay excepción

async def test_agent():
    langfuse_client = Langfuse()
    handler = CallbackHandler()

    my_query2 = "What were the stock prices for Amazon in Q4 last year?"
    my_query4 = "I’m researching AMZN give me the current price and any relevant information about their AI business"
    my_query5 = "What is the total amount of office space Amazon owned in North America in 2024?"
    query = my_query5
    inputs = {"messages": [HumanMessage(content=query)]}

    print("Testing streaming output:")
    final_response = None

    try:
        async for output in agent_executor.astream(inputs, config={"callbacks": [handler]}):
            for key, value in output.items():
                print(f"\n--- Node: {key} ---")
                if "messages" in value:
                    last_msg = value["messages"][-1]
                    print(f"Message: {last_msg.content}")
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        print(f"Tool Calls: {last_msg.tool_calls}")

                    # respuesta final = nodo agent + tiene contenido + sin tool_calls
                    if (
                        key == "agent"
                        and last_msg.content
                        and not getattr(last_msg, "tool_calls", None)
                    ):
                        final_response = last_msg.content

    finally:
        langfuse_client.flush()

    print("\n" + "="*40)
    print("FINAL RESPONSE:")
    print(final_response)

async def test_agent_invocation(query:str):

    langfuse_client = Langfuse()
    handler = CallbackHandler()

    inputs = {"messages": [HumanMessage(content=query)]}

    print("Testing streaming output:")
    final_response = None

    try:
        async for output in agent_executor.astream(inputs, config={"callbacks": [handler]}):
            for key, value in output.items():
                print(f"\n--- Node: {key} ---")
                if "messages" in value:
                    last_msg = value["messages"][-1]
                    print(f"Message: {last_msg.content}")
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        print(f"Tool Calls: {last_msg.tool_calls}")

                    # respuesta final = nodo agent + tiene contenido + sin tool_calls
                    if (
                        key == "agent"
                        and last_msg.content
                        and not getattr(last_msg, "tool_calls", None)
                    ):
                        final_response = last_msg.content

    finally:
        langfuse_client.flush()

    return final_response

if __name__ == "__main__":
    asyncio.run(test_agent())