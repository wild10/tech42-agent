from pydantic import BaseModel, Field
from typing import List, Optional, Any

class AgentInvokeRequest(BaseModel):
    query: str = Field(..., description="The user's question for the agent.")
    thread_id: Optional[str] = Field(None, description="Optional thread ID for conversational memory.")

class ToolCallInfo(BaseModel):
    tool: str
    args: Any

class AgentStepResponse(BaseModel):
    node: str
    message: Optional[str] = None
    tool_calls: Optional[List[ToolCallInfo]] = None

class AgentFinalResponse(BaseModel):
    query: str
    response: str
    steps: List[AgentStepResponse]