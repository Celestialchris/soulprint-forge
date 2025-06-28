import argparse
from datetime import datetime
import os
import sys
# Allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from soulprint.app import create_app
from soulprint.app.models.memory import MemoryEntry
from soulprint.app.models.db import db

def ingest_md_files(root_folder):
    app = create_app()
    with app.app_context():
        for root, _, files in os.walk(root_folder):
            for file in files:
                if not file.endswith(".md"):
                    continue
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                entry = MemoryEntry(
                    role="user",
                    content=content,
                    tags="imported, markdown",
                    timestamp=datetime.utcnow()
                )
                db.session.add(entry)
                print(f"✅ Ingested: {file}")
        db.session.commit()
        print("🚀 All markdown files ingested.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, default='soulprint/app/uploads', help='Folder of markdown files')
    args = parser.parse_args()
    ingest_md_files(args.root)

if __name__ == '__main__':
    main()