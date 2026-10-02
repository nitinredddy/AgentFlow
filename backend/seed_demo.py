from app.db import Base, engine, SessionLocal
from app.models import Client, Customer, Policy, Claim, EvaluationScenario

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if not db.query(Client).first():
    client = Client(
        name="Acme Insurance",
        industry="insurance",
        agent_name="Acme Policy Assistant",
        tone="professional",
        system_prompt=(
            "You are Acme Insurance's customer service assistant. "
            "Use only verified tool context for policy and claim facts. "
            "Never invent coverage decisions. Escalate when uncertain."
        ),
        sms_fallback=True,
        max_transfer_attempts=2,
    )
    db.add(client)
    db.add(Customer(external_id="CUST-1001", name="Alex Morgan", phone="+15550001001"))
    db.add(Policy(policy_number="POL-9001", customer_external_id="CUST-1001", status="active", coverage_type="auto"))
    db.add(Claim(claim_number="CLM-7001", customer_external_id="CUST-1001", status="under review", amount=1800.0))

    cases = [
        ("Policy status", "What is my policy status?", "policy_status", "get_policy"),
        ("Policy coverage", "Can you tell me about my coverage?", "policy_status", "get_policy"),
        ("Claim status", "What is the status of my claim?", "claim_status", "get_claim"),
        ("Claim approved", "Has my claim been approved?", "claim_status", "get_claim"),
        ("Callback", "Please call me back tomorrow.", "schedule_callback", "schedule_callback"),
        ("Callback request", "I need a callback.", "schedule_callback", "schedule_callback"),
        ("Human transfer", "I want a human representative.", "human_transfer", "transfer"),
        ("FAQ", "Hi, what can you help me with?", "general_faq", "respond"),
        ("FAQ hours", "Hello, I need some help.", "general_faq", "respond"),
        ("Unknown", "I need something unusual.", "unknown", "escalate"),
    ]
    for name, text, intent, action in cases:
        db.add(EvaluationScenario(
            name=name,
            input_text=text,
            expected_intent=intent,
            expected_action=action,
            expected_guardrail=True,
        ))
    db.commit()
    print("Demo data created.")
else:
    print("Demo data already exists.")

db.close()
