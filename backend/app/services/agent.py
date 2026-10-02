import time
import json
from sqlalchemy.orm import Session
from app.models import Client, Conversation, Event
from app.services.intent import classify
from app.services.tools import get_policy, get_claim, schedule_callback, send_sms
from app.services.guardrails import validate_output
from app.services.llm import get_provider

def log_event(db, event_type, entity_type, entity_id, payload):
    db.add(Event(event_type=event_type, entity_type=entity_type, entity_id=str(entity_id), payload=json.dumps(payload)))
    db.commit()

def run_agent(db: Session, client: Client, customer_external_id: str, message: str):
    started = time.perf_counter()
    intent = classify(message)
    context = {"intent": intent}
    tool_events = []

    if intent == "policy_status":
        result = get_policy(db, customer_external_id)
        context["policy"] = result
        tool_events.append({"tool": "get_policy", "result": result})
    elif intent == "claim_status":
        result = get_claim(db, customer_external_id)
        context["claim"] = result
        tool_events.append({"tool": "get_claim", "result": result})
    elif intent == "schedule_callback":
        result = schedule_callback(customer_external_id)
        context["callback"] = result
        tool_events.append({"tool": "schedule_callback", "result": result})

    response = get_provider().generate(client.system_prompt, message, context)
    passed, violations = validate_output(response)

    status = "completed"
    if not passed:
        response = "I can't safely complete that request. I'll connect you with a representative."
        status = "escalated"

    if intent == "human_transfer":
        status = "escalated"

    latency = round((time.perf_counter() - started) * 1000, 2)
    conv = Conversation(
        client_id=client.id,
        customer_external_id=customer_external_id,
        user_message=message,
        intent=intent,
        response=response,
        status=status,
        guardrail_passed=passed,
        latency_ms=latency,
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)

    log_event(db, "agent_run", "conversation", conv.id, {
        "intent": intent,
        "status": status,
        "guardrail_passed": passed,
        "violations": violations,
        "tools": tool_events,
        "latency_ms": latency,
    })
    return conv, tool_events
