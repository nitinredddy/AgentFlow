from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models import Client, Conversation, EvaluationScenario
from app.schemas import ChatRequest, ChatResponse, ClientCreate, EvaluationRunResponse, SMSRequest
from app.services.agent import run_agent
from app.services.evaluation import run_evaluation
from app.services.tools import send_sms

router = APIRouter(prefix="/api/v1")

@router.get("/clients")
def clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.post("/clients")
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.post("/conversations", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(404, "Client not found")
    conv, tool_events = run_agent(db, client, payload.customer_external_id, payload.message)
    return ChatResponse(
        conversation_id=conv.id,
        intent=conv.intent,
        response=conv.response,
        status=conv.status,
        guardrail_passed=conv.guardrail_passed,
        latency_ms=conv.latency_ms,
        tool_events=tool_events,
    )

@router.post("/sms")
def sms(payload: SMSRequest):
    return send_sms(payload.customer_external_id, payload.message)

@router.post("/evaluations/run", response_model=EvaluationRunResponse)
def evaluate(client_id: int, db: Session = Depends(get_db)):
    if not db.get(Client, client_id):
        raise HTTPException(404, "Client not found")
    return run_evaluation(db, client_id)

@router.get("/evaluations/scenarios")
def scenarios(db: Session = Depends(get_db)):
    return db.query(EvaluationScenario).all()

@router.get("/conversations")
def conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).order_by(Conversation.id.desc()).limit(100).all()

@router.get("/metrics/overview")
def metrics(db: Session = Depends(get_db)):
    total = db.query(func.count(Conversation.id)).scalar() or 0
    escalated = db.query(func.count(Conversation.id)).filter(Conversation.status == "escalated").scalar() or 0
    guarded = db.query(func.count(Conversation.id)).filter(Conversation.guardrail_passed == False).scalar() or 0
    avg_latency = db.query(func.avg(Conversation.latency_ms)).scalar() or 0
    return {
        "conversations": total,
        "escalation_rate": round(escalated / total * 100, 2) if total else 0,
        "guardrail_failure_rate": round(guarded / total * 100, 2) if total else 0,
        "avg_latency_ms": round(float(avg_latency), 2),
    }

@router.get("/health")
def api_health():
    return {"status": "ok", "service": "agent-platform"}
