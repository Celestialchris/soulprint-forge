from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'arkos'
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ChatLog {self.timestamp} {self.sender}>'
