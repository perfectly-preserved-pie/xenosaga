#!/usr/bin/env python3
"""
Script to convert JSON episode data files to SQLite database.

This script reads the JSON files from assets/json/ and creates a SQLite database
at assets/xenosaga.db with three tables: episode1, episode2, and episode3.

Usage:
    python utils/json_to_sqlite.py
"""

import os
import sqlite3
import pandas as pd


def convert_json_to_sqlite():
    """Convert JSON episode files to SQLite database."""
    # Paths
    json_dir = 'assets/json'
    db_path = 'assets/xenosaga.db'

    # Read the JSON files
    ep1_df = pd.read_json(os.path.join(json_dir, 'episode1.json'), lines=True)
    ep2_df = pd.read_json(os.path.join(json_dir, 'episode2.json'), lines=True)
    ep3_df = pd.read_json(os.path.join(json_dir, 'episode3.json'), lines=True)

    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Write dataframes to SQLite
    ep1_df.to_sql('episode1', conn, index=False, if_exists='replace')
    ep2_df.to_sql('episode2', conn, index=False, if_exists='replace')
    ep3_df.to_sql('episode3', conn, index=False, if_exists='replace')

    # Verify the tables were created
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables created: {[t[0] for t in tables]}")

    # Verify data counts
    for table in ['episode1', 'episode2', 'episode3']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} rows")

    conn.close()
    print(f"\nDatabase created at: {db_path}")


if __name__ == '__main__':
    convert_json_to_sqlite()
