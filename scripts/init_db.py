#!/usr/bin/env python3
"""
Database initialization script
Run this to create all database tables and TimescaleDB hypertables
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.connection import init_db
from src.utils.logger import setup_logging

if __name__ == "__main__":
    setup_logging()
    print("Initializing database...")
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
