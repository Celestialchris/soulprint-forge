
import json
import os
import sys
from datetime import datetime
from flask import Flask
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db
from app.models.memory import MemoryEntry

def parse_conversations(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = []
    for convo in data.get("mapping", {}).values():
        message = convo.get("message")
        if not message or "content" not in message:
            continue

        role = message.get("author", {}).get("role", "unknown")
        parts = message["content"].get("parts", [])
        content = "\n".join(parts)
        timestamp = message.get("create_time", datetime.utcnow().timestamp())

        messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcfromtimestamp(timestamp),
            "tags": "chatgpt,imported"
        })
    return messages

def ingest(filepath):
    app = create_app()
    with app.app_context():
        from app.models import db
        messages = parse_conversations(filepath)
        for msg in messages:
            entry = MemoryEntry(
                role=msg["role"],
                content=msg["content"],
                timestamp=msg["timestamp"],
                tags=msg["tags"]
            )
            db.session.add(entry)
        db.session.commit()
        print(f"✅ Ingested {len(messages)} messages.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest_openai_json.py <path_to_conversations.json>")
        sys.exit(1)
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    ingest(filepath)
