from flask_sqlalchemy import SQLAlchemy
from src.soulprint.app.models.db import db
db = SQLAlchemy()

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    conversation = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ChatLog {self.id} {self.timestamp}>"
