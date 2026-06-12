"""
Migration script to add missing AI verification columns to verification_status table.
Run: python migrate_verification.py
"""
import os
import sys

# Add backend dir to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import text, inspect
from app import create_app
from api.models import db


COLUMNS_TO_ADD = [
    ("ai_confidence", "FLOAT"),
    ("ai_reasoning", "TEXT"),
    ("is_consistent", "BOOLEAN"),
    ("detected_objects", "JSON"),
    ("mismatch_flags", "JSON"),
]


def get_existing_columns(engine, table_name):
    inspector = inspect(engine)
    return {col["name"] for col in inspector.get_columns(table_name)}


def run_migration():
    app = create_app()

    with app.app_context():
        engine = db.engine
        existing = get_existing_columns(engine, "verification_status")

        added = []
        for col_name, col_type in COLUMNS_TO_ADD:
            if col_name not in existing:
                sql = text(f"ALTER TABLE verification_status ADD COLUMN {col_name} {col_type}")
                db.session.execute(sql)
                added.append(col_name)
            else:
                print(f"  [OK] Column '{col_name}' already exists")

        if added:
            db.session.commit()
            print(f"\n  [DONE] Added {len(added)} column(s): {', '.join(added)}")
        else:
            print("\n  [DONE] All columns already present, no changes needed")


if __name__ == "__main__":
    print("------ Migration: Add AI columns to verification_status ------\n")
    try:
        run_migration()
    except Exception as e:
        print(f"\n  [ERROR] {e}")
        db.session.rollback()
        sys.exit(1)
