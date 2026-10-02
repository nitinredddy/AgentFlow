from sqlalchemy.orm import Session
from app.models import Policy, Claim, Customer

def get_policy(db: Session, customer_id: str):
    row = db.query(Policy).filter(Policy.customer_external_id == customer_id).first()
    if not row:
        return {"found": False}
    return {
        "found": True,
        "policy_number": row.policy_number,
        "status": row.status,
        "coverage_type": row.coverage_type,
    }

def get_claim(db: Session, customer_id: str):
    row = db.query(Claim).filter(Claim.customer_external_id == customer_id).first()
    if not row:
        return {"found": False}
    return {
        "found": True,
        "claim_number": row.claim_number,
        "status": row.status,
        "amount": row.amount,
    }

def schedule_callback(customer_id: str):
    return {"scheduled": True, "customer_external_id": customer_id, "window": "next business day"}

def send_sms(customer_id: str, message: str):
    return {"sent": True, "customer_external_id": customer_id, "message_preview": message[:100]}
