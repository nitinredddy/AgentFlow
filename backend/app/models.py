from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Float, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

def now():
    return datetime.now(timezone.utc)

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    industry: Mapped[str] = mapped_column(String(80), default="financial_services")
    agent_name: Mapped[str] = mapped_column(String(120))
    system_prompt: Mapped[str] = mapped_column(Text)
    tone: Mapped[str] = mapped_column(String(40), default="professional")
    sms_fallback: Mapped[bool] = mapped_column(Boolean, default=True)
    max_transfer_attempts: Mapped[int] = mapped_column(Integer, default=2)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(80), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(40), default="")

class Policy(Base):
    __tablename__ = "policies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    policy_number: Mapped[str] = mapped_column(String(80), unique=True)
    customer_external_id: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(40))
    coverage_type: Mapped[str] = mapped_column(String(80))

class Claim(Base):
    __tablename__ = "claims"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    claim_number: Mapped[str] = mapped_column(String(80), unique=True)
    customer_external_id: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(80))
    amount: Mapped[float] = mapped_column(Float, default=0.0)

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer)
    customer_external_id: Mapped[str] = mapped_column(String(80))
    user_message: Mapped[str] = mapped_column(Text)
    intent: Mapped[str] = mapped_column(String(80))
    response: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="completed")
    guardrail_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class EvaluationScenario(Base):
    __tablename__ = "evaluation_scenarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    input_text: Mapped[str] = mapped_column(Text)
    expected_intent: Mapped[str] = mapped_column(String(80))
    expected_action: Mapped[str] = mapped_column(String(80))
    expected_guardrail: Mapped[bool] = mapped_column(Boolean, default=True)

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_id: Mapped[int] = mapped_column(Integer)
    predicted_intent: Mapped[str] = mapped_column(String(80))
    action: Mapped[str] = mapped_column(String(80))
    passed: Mapped[bool] = mapped_column(Boolean)
    reason: Mapped[str] = mapped_column(Text)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(80))
    entity_type: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[str] = mapped_column(String(80))
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
