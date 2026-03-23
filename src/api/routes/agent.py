import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from src.agent.workflow import agent_executor
from src.api.schemas import AgentInvokeRequest, AgentFinalResponse, AgentStepResponse, ToolCallInfo
from src.api.middleware.auth import get_current_user
from src.observability.langfuse_handler import get_callbacks

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/invoke", response_model=AgentFinalResponse)
async def invoke_agent(request: AgentInvokeRequest, user: dict = Depends(get_current_user)):
    """
    Invoque the agent synchronously and return the final response and steps.
    """
    inputs = {"messages": [HumanMessage(content=request.query)]}
    config = {"configurable": {"thread_id": request.thread_id}} if request.thread_id else {}
    
    try:
        callbacks = get_callbacks()
        result = await agent_executor.ainvoke(inputs, config={"configurable": {"thread_id": request.thread_id}, "callbacks": callbacks} if request.thread_id else {"callbacks": callbacks})
        
        messages = result["messages"]
        final_response = ""
        steps = []
        
        for msg in messages:
            if msg.type == "ai" and msg.content:
                final_response = msg.content
            
            step = AgentStepResponse(
                node="agent" if msg.type == "ai" else "tools",
                message=msg.content if msg.content else None,
                tool_calls=[ToolCallInfo(tool=tc["name"], args=tc["args"]) for tc in msg.tool_calls] if hasattr(msg, "tool_calls") and msg.tool_calls else None
            )
            steps.append(step)
            
        return AgentFinalResponse(
            query=request.query,
            response=final_response,
            steps=steps
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def stream_agent(request: AgentInvokeRequest, user: dict = Depends(get_current_user)):
    """
    Invoque the agent and stream the output nodes.
    """
    inputs = {"messages": [HumanMessage(content=request.query)]}
    config = {"configurable": {"thread_id": request.thread_id}} if request.thread_id else {}

    async def event_generator():
        try:
            callbacks = get_callbacks()
            full_config = config.copy()
            full_config["callbacks"] = callbacks
            async for output in agent_executor.astream(inputs, config=full_config):
                for key, value in output.items():
                    data = {
                        "node": key,
                        "messages": [
                            {
                                "content": msg.content,
                                "type": msg.type,
                                "tool_calls": getattr(msg, "tool_calls", None)
                            } for msg in value.get("messages", [])
                        ]
                    }
                    yield f"data: {json.dumps(data)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")