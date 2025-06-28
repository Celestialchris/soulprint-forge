# soulprint/app/routes.py

import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename
import markdown2

from soulprint.app.models.memory import MemoryEntry
from soulprint.app.models.db import db

routes = Blueprint("routes", __name__)
ALLOWED_EXTENSIONS = {'md'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route("/", methods=["GET"])
def home():
    return "SoulPrint is live and ready."

@routes.route("/upload", methods=["POST"])
def upload_markdown():
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
            for line in lines:
                if line.strip():
                    entry = MemoryEntry(
                        timestamp=datetime.utcnow(),
                        role="user",
                        content=line.strip(),
                        tags="imported"
                    )
                    db.session.add(entry)

        db.session.commit()
        return jsonify({'status': 'Memory ingested successfully', 'file': filename}), 200

    return jsonify({'error': 'Invalid file type'}), 400

@routes.route("/memories", methods=["GET"])
def list_memories():
    entries = MemoryEntry.query.order_by(MemoryEntry.timestamp.desc()).limit(100).all()
    for entry in entries:
        if entry.content:
            entry.content = markdown2.markdown(entry.content)
    return render_template("memories.html", entries=entries)

@routes.route("/memory", methods=["GET"])
def get_all_entries():
    entries = MemoryEntry.query.order_by(MemoryEntry.timestamp.desc()).all()
    return jsonify([entry.to_dict() for entry in entries])

@routes.route("/memory/<int:entry_id>", methods=["GET"])
def get_entry(entry_id):
    entry = MemoryEntry.query.get_or_404(entry_id)
    return jsonify(entry.to_dict())

@routes.route("/memory/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    entry = MemoryEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "✅ Entry deleted."})

@routes.route("/memory", methods=["POST"])
def create_entry():
    data = request.json
    entry = MemoryEntry(
        role=data.get("role", "user"),
        content=data["content"],
        tags=data.get("tags"),
        timestamp=datetime.utcnow()
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201

@routes.route("/view", methods=["GET"])
def view_entries():
    tag = request.args.get("tag")
    if tag:
        entries = MemoryEntry.query.filter(MemoryEntry.tags.contains(tag)) \
            .order_by(MemoryEntry.timestamp.desc()).all()
    else:
        entries = MemoryEntry.query.order_by(MemoryEntry.timestamp.desc()).limit(100).all()
    return render_template("view.html", entries=entries)
