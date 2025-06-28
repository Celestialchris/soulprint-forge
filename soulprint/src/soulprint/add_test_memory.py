from app import create_app
from src.soulprint.app.models.db import db
from app.models.memory import MemoryEntry

app = create_app()

with app.app_context():
    entry = MemoryEntry(
        title="The Day SoulPrint Was Born",
        content="This is the first official memory logged into SoulPrint. I now control my own archive.",
        tags="initiation,log,start",
        source="manual"
    )
    db.session.add(entry)
    db.session.commit()
    print(f"[✓] Entry added: {entry}")
