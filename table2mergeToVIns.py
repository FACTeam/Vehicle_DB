import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect("mydata.db")

# Load tables
vins_df = pd.read_sql_query("SELECT * FROM vins", conn)
table2_df = pd.read_sql_query("SELECT * FROM table2_limited", conn)

# Inspect columns
print("VINS COLUMNS:", vins_df.columns.tolist())
print("TABLE2 COLUMNS BEFORE RENAME:", table2_df.columns.tolist())

# Rename to match exactly (adjust the left-hand side based on the print result)
vins_df.rename(columns={"Vehicle#": "Vehicle #"}, inplace=True)
table2_df.rename(columns={"Vehicle  #": "Vehicle #"}, inplace=True)  # Adjust if needed

# Merge
merged_df = pd.merge(vins_df, table2_df, on="Vehicle #", how="left")

# Save
merged_df.to_sql("vins_merged", conn, if_exists="replace", index=False)

conn.close()
