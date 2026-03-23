from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import agent
#adding new ------------------
from fastapi import Request, Depends
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from src.api.middleware.auth import get_current_user
import json

app = FastAPI(
    title="Tech42 Financial Agent API",
    description="API for interacting with the specialized Amazon financial agent.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Tech42 Financial Agent API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


# --- AgentCore required for endponts -----
@app.get("/ping")
async def ping():
    """AgentCore health check"""
    return {"status": "ok"}

@app.post("/invocations")
async def invocations(request: Request):
    """AgentCore main invocation endpoint"""
    from src.agent.workflow import agent_executor
    
    body = await request.json()
    query = body.get("prompt") or body.get("query") or body.get("input", "")
    thread_id = body.get("thread_id", None)
    
    inputs = {"messages": [HumanMessage(content=query)]}
    config = {"configurable": {"thread_id": thread_id}} if thread_id else {}

    async def event_generator():
        try:
            async for output in agent_executor.astream(inputs, config=config):
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8080, reload=True)
