from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine, SessionLocal
from app.models import Client

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_intent_and_chat():
    db = SessionLocal()
    row = db.query(Client).first()
    if not row:
        row = Client(
            name="Test Client",
            agent_name="Test Agent",
            system_prompt="Use verified context only.",
        )
        db.add(row)
        db.commit()
        db.refresh(row)
    client_id = row.id
    db.close()

    response = client.post("/api/v1/conversations", json={
        "client_id": client_id,
        "customer_external_id": "UNKNOWN",
        "message": "I want to speak to a human representative.",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "human_transfer"
    assert body["status"] == "escalated"
