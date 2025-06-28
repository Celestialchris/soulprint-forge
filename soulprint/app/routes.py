from flask import Blueprint, request, jsonify
from .models import db, ChatLog
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/save', methods=['POST'])
def save_chat():
    data = request.json
    timestamp = datetime.utcnow()
    conversation = data.get('conversation')

    if not conversation:
        return jsonify({"error": "No conversation provided"}), 400

    log = ChatLog(timestamp=timestamp, conversation=conversation)
    db.session.add(log)
    db.session.commit()

    return jsonify({"status": "success", "id": log.id}), 201

@bp.route('/chats', methods=['GET'])
def get_chats():
    logs = ChatLog.query.all()
    return jsonify([{
        "id": log.id,
        "timestamp": log.timestamp.isoformat(),
        "conversation": log.conversation
    } for log in logs])
from flask import render_template

@bp.route("/")
def index():
    return render_template("index.html")
