SENSITIVE_PATTERNS = [
    "guaranteed coverage",
    "guarantee that",
    "give me your password",
    "tell me another customer's",
]

def validate_output(text: str) -> tuple[bool, list[str]]:
    lowered = text.lower()
    violations = [p for p in SENSITIVE_PATTERNS if p in lowered]
    return len(violations) == 0, violations
