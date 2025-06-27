import sqlite3
import pandas as pd

# 1. Connect to SQLite database
conn = sqlite3.connect('path_to_your_database.db')

# 2. Load tables into pandas DataFrames
Table1 = pd.read_sql_query("SELECT * FROM Table1;", conn)
Table3 = pd.read_sql_query("SELECT * FROM Table3;", conn)
Table5 = pd.read_sql_query("SELECT * FROM Table5;", conn)

# 3. Clean column names function
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.lower()
        .str.replace(r'[^a-z0-9_]', '', regex=True)
    )
    return df

# Apply cleaning
Table1 = clean_columns(Table1)
Table3 = clean_columns(Table3)
Table5 = clean_columns(Table5)

# Now Table1, Table3, Table5 have consistent column names, ready for merging

# Don't forget to close the connection when done
conn.close()
