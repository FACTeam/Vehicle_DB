import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the tables
vins_df = pd.read_sql_query("SELECT * FROM vins_merged_updated", conn)
table4_df = pd.read_sql_query("SELECT * FROM table4", conn)

# Normalize column names (strip spaces)
vins_df.columns = vins_df.columns.str.strip()
table4_df.columns = table4_df.columns.str.strip()

# Normalize 'Driver' columns to lowercase and strip whitespace
vins_df['Driver'] = vins_df['Driver'].astype(str).str.strip().str.lower()
table4_df['Driver'] = table4_df['Driver'].astype(str).str.strip().str.lower()

# Merge on Driver only
merged_df = pd.merge(
    vins_df,
    table4_df,
    on='Driver',
    how='left',
    suffixes=('_vins', '_table4')
)

# Save merged DataFrame back to database
merged_df.to_sql("final_merged", conn, if_exists="replace", index=False)

conn.close()
