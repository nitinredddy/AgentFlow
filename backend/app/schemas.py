from pydantic import BaseModel, Field
from typing import Any

class ChatRequest(BaseModel):
    client_id: int
    customer_external_id: str
    message: str = Field(min_length=1, max_length=4000)

class ChatResponse(BaseModel):
    conversation_id: int
    intent: str
    response: str
    status: str
    guardrail_passed: bool
    latency_ms: float
    tool_events: list[dict[str, Any]] = []

class ClientCreate(BaseModel):
    name: str
    industry: str = "financial_services"
    agent_name: str
    system_prompt: str
    tone: str = "professional"
    sms_fallback: bool = True
    max_transfer_attempts: int = 2

class EvaluationRunResponse(BaseModel):
    total: int
    passed: int
    failed: int
    pass_rate: float
    results: list[dict[str, Any]]

class SMSRequest(BaseModel):
    client_id: int
    customer_external_id: str
    message: str
