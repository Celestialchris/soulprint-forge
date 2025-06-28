import os
import sys
from datetime import datetime
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from soulprint.app import create_app
from soulprint.app.models import db
from soulprint.app.models.memory import MemoryEntry

def ingest_md_files(root_folder="uploads"):
    app = create_app()
    with app.app_context():
        entries = []
        count = 0

        for root, _, files in os.walk(root_folder):
            for file in files:
                if not file.endswith(".md"):
                    continue
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if not content.strip():
                        continue

                    entry = MemoryEntry(
                    role="user",
                    content=content,
                    tags=f"imported, {Path(root).name}",  # ← adds folder name as a tag
                    timestamp=datetime.utcnow()
            )


                    # Commit every 100 files
                    if len(entries) >= 100:
                        db.session.bulk_save_objects(entries)
                        db.session.commit()
                        entries = []
                        print(f"🔁 Committed 100 entries...")

                except Exception as e:
                    print(f"❌ Failed to ingest {file}: {e}")

        # Final commit
        if entries:
            db.session.bulk_save_objects(entries)
            db.session.commit()

        print(f"✅ Finished. Total files ingested: {count}")

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else "uploads"
    ingest_md_files(folder)
