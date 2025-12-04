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

    # Episode configuration - mapping table names to JSON files
    episodes = {
        'episode1': 'episode1.json',
        'episode2': 'episode2.json',
        'episode3': 'episode3.json',
    }

    try:
        # Read the JSON files
        dataframes = {}
        for table_name, json_file in episodes.items():
            json_path = os.path.join(json_dir, json_file)
            dataframes[table_name] = pd.read_json(json_path, lines=True)

        # Remove existing database if it exists
        if os.path.exists(db_path):
            os.remove(db_path)

        # Connect to the database and write dataframes
        conn = sqlite3.connect(db_path)
        try:
            for table_name, df in dataframes.items():
                df.to_sql(table_name, conn, index=False, if_exists='replace')

            # Verify the tables were created
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tables created: {[t[0] for t in tables]}")

            # Verify data counts using parameterized approach
            for table_name in episodes.keys():
                # Table names are validated against our known list, safe to use
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  {table_name}: {count} rows")
        finally:
            conn.close()

        print(f"\nDatabase created at: {db_path}")

    except (sqlite3.Error, pd.errors.EmptyDataError, FileNotFoundError) as e:
        print(f"Error converting JSON to SQLite: {e}")
        raise


if __name__ == '__main__':
    convert_json_to_sqlite()
