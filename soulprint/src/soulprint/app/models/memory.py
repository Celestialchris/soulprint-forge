from datetime import datetime
from .db import db

class MemoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=False, default='user')
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else "Unknown"
        return f"<MemoryEntry {self.id} role={self.role} on {ts}>"
    def to_dict(self):
         return {
        "id": self.id,
        "timestamp": self.timestamp.isoformat(),
        "role": self.role,
        "content": self.content,
        "tags": self.tags
        }
