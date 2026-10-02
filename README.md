# Client-Deployed AI Agent Platform

A production-oriented reference implementation of a forward-deployed AI agent platform for financial-services-style customer workflows.

## What it demonstrates

- Client-specific agent configuration
- Prompt and workflow versioning
- Tool/API integrations
- Deterministic guardrails
- Conversation and event logging
- AI output evaluation
- Regression scenarios
- Human escalation
- SMS fallback
- Deployment health checks
- Metrics suitable for a client success / forward-deployed workflow
- Optional OpenAI-compatible LLM provider
- Zero-key local demo mode

## Architecture

```text
Client Configuration
        |
        v
Conversation API
        |
        v
Intent Router
        |
        +--------------------+
        |                    |
        v                    v
Policy/Claim Tools      Escalation Rules
        |                    |
        +---------+----------+
                  |
                  v
             Guardrails
                  |
                  v
            Agent Response
                  |
        +---------+---------+
        |                   |
        v                   v
 Evaluation            Event Store
        |                   |
        +---------+---------+
                  |
                  v
             Dashboard
```

## Quick start

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

### Seed demo data

In another terminal:

```bash
cd backend
python seed_demo.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite.

### Run tests

```bash
cd backend
pytest -q
```

## Optional real LLM

The platform runs fully without an API key using a deterministic local provider. To use an OpenAI-compatible endpoint:

```bash
export LLM_PROVIDER=openai_compatible
export LLM_API_KEY=...
export LLM_BASE_URL=https://api.openai.com/v1
export LLM_MODEL=gpt-4o-mini
```

The integration is deliberately provider-agnostic.

## Demo scenarios

The seed script creates:

- Acme Insurance client
- policy and claim records
- 10 evaluation scenarios
- sample conversations
- sample failures

The API exposes `/health`, `/api/v1/clients`, `/api/v1/conversations`, `/api/v1/evaluations/run`, `/api/v1/metrics/overview`, and more.
