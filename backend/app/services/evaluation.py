import time
from sqlalchemy.orm import Session
from app.models import EvaluationScenario, EvaluationResult, Client
from app.services.intent import classify

def run_evaluation(db: Session, client_id: int):
    scenarios = db.query(EvaluationScenario).all()
    results = []
    for s in scenarios:
        start = time.perf_counter()
        predicted = classify(s.input_text)
        action = {
            "policy_status": "get_policy",
            "claim_status": "get_claim",
            "schedule_callback": "schedule_callback",
            "human_transfer": "transfer",
            "general_faq": "respond",
            "unknown": "escalate",
        }[predicted]
        passed = predicted == s.expected_intent and action == s.expected_action
        latency = round((time.perf_counter() - start) * 1000, 3)
        reason = "matched expected behavior" if passed else f"expected {s.expected_intent}/{s.expected_action}"
        row = EvaluationResult(
            scenario_id=s.id,
            predicted_intent=predicted,
            action=action,
            passed=passed,
            reason=reason,
            latency_ms=latency,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        results.append({
            "scenario": s.name,
            "predicted_intent": predicted,
            "action": action,
            "passed": passed,
            "reason": reason,
            "latency_ms": latency,
        })
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total * 100, 2) if total else 0,
        "results": results,
    }
