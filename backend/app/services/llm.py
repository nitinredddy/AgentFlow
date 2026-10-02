import json
import urllib.request
from app.core.config import settings

class LLMProvider:
    def generate(self, system_prompt: str, user_message: str, context: dict) -> str:
        raise NotImplementedError

class MockProvider(LLMProvider):
    def generate(self, system_prompt: str, user_message: str, context: dict) -> str:
        intent = context.get("intent", "unknown")
        if intent == "policy_status":
            if context.get("policy", {}).get("found"):
                p = context["policy"]
                return f"Your policy {p['policy_number']} is currently {p['status']} with {p['coverage_type']} coverage."
            return "I couldn't locate a policy for this customer. I can transfer you to a representative."
        if intent == "claim_status":
            if context.get("claim", {}).get("found"):
                c = context["claim"]
                return f"Your claim {c['claim_number']} is currently {c['status']}."
            return "I couldn't locate a claim for this customer. I can transfer you to a representative."
        if intent == "schedule_callback":
            return "I've scheduled a callback for the next business day."
        if intent == "human_transfer":
            return "I'll transfer you to a representative."
        if intent == "general_faq":
            return "I can help with policy status, claim status, callbacks, or connect you with a representative."
        return "I couldn't confidently determine what you need. I can connect you with a representative."

class OpenAICompatibleProvider(LLMProvider):
    def generate(self, system_prompt: str, user_message: str, context: dict) -> str:
        payload = {
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_message}\n\nVerified tool context:\n{json.dumps(context)}"},
            ],
            "temperature": 0.1,
        }
        req = urllib.request.Request(
            f"{settings.llm_base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.llm_api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read())
        return data["choices"][0]["message"]["content"]

def get_provider():
    if settings.llm_provider == "openai_compatible" and settings.llm_api_key:
        return OpenAICompatibleProvider()
    return MockProvider()
