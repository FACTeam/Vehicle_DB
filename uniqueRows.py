import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect("mydata.db")

# Load the table
df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Normalize column names
df.columns = df.columns.str.strip()

# Fill missing values within each VIN group
df = (
    df.groupby('VIN', group_keys=False)
      .apply(lambda g: g.ffill().bfill())
)

# Drop duplicate rows — keep the first complete one per VIN
df_unique = df.drop_duplicates(subset='VIN', keep='first')

# Save cleaned data back to the database
df_unique.to_sql("final_cleaned", conn, if_exists='replace', index=False)

# Optional: show how many duplicates were dropped
print(f"Original rows: {len(df)}, After deduplication: {len(df_unique)}")

# Close the connection
conn.close()
