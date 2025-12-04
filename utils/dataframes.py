import pandas as pd
import sqlite3

# Read the data from the SQLite database
_conn = sqlite3.connect('assets/xenosaga.db')
ep1_df = pd.read_sql_query("SELECT * FROM episode1", _conn)
ep2_df = pd.read_sql_query("SELECT * FROM episode2", _conn)
ep3_df = pd.read_sql_query("SELECT * FROM episode3", _conn)
_conn.close()