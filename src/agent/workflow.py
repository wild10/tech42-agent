from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from src.llm import get_llm
from src.agent.tools import get_tools
# from langfuse.decorators import observe

# Define the State
class AgentState(TypedDict):
    """
    Standard state for a ReAct agent.
    """
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]

# Define the nodes
# @observe(name="agent_llm_step")
def call_model(state: AgentState):
    """
    Calls the LLM to decide the next action.
    """
    messages = state["messages"]
    llm = get_llm()
    # Bind tools to the LLM
    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)
    
    response = llm_with_tools.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

def should_continue(state: AgentState):
    """
    Determines if the agent should continue or stop.
    """
    messages = state["messages"]
    last_message = messages[-1]
    # If there are tool calls, we continue to the tools node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # Otherwise, we stop
    return END

# Initialize the StateGraph
workflow = StateGraph(AgentState)

# Add our nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(get_tools()))

# Define the edges
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)
workflow.add_edge("tools", "agent")

# Compile the graph
agent_executor = workflow.compile()

# Show the graph with mermaid
# print(agent_executor.get_graph().draw_mermaid())

# Access to the graph object for streaming and execution
def get_agent_executor():
    return agent_executor


if __name__ == "__main__":
    print(f"Hello LangGraph!!")

    input_query = {
        "messages": [
            HumanMessage(content="how much the AWS sales increase in percentage in the 2024?")
        ]
    }

    agent_answer = agent_executor.invoke(input_query)
    
    for i, answer in enumerate(agent_answer["messages"]):
        print(f"\n--- Node: {i+1} [{answer.type.upper()}] ---")
        print(answer.content)
