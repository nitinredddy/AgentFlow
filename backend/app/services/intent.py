INTENT_RULES = {
    "policy_status": ["policy status", "policy active", "is my policy", "policy number", "coverage"],
    "claim_status": ["claim status", "claim", "approved", "settled", "claim number"],
    "schedule_callback": ["call me", "callback", "call back", "schedule a call"],
    "human_transfer": ["human", "agent", "representative", "person"],
    "general_faq": ["hello", "hi", "hours", "help", "how does this work"],
}

def classify(text: str) -> str:
    t = text.lower()
    scores = {intent: sum(1 for k in keys if k in t) for intent, keys in INTENT_RULES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unknown"
