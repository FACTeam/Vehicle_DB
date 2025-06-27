import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load vins_merged table
vins_df = pd.read_sql_query("SELECT * FROM vins_merged", conn)

# Normalize column names just in case
vins_df.columns = vins_df.columns.str.strip()

# Normalize Dept_t1 and Dept_t3: strip whitespace, lowercase, and convert 'nan' strings to pd.NA
vins_df['Dept_t1'] = vins_df['Dept_t1'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Dept_t3'] = vins_df['Dept_t3'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})

# Merge Dept_t1 and Dept_t3 into a new column 'Depts' (use Dept_t1 unless missing, then Dept_t3)
vins_df['Depts'] = vins_df['Dept_t1'].fillna(vins_df['Dept_t3'])

# Drop original Dept_t1 and Dept_t3 columns
vins_df.drop(columns=['Dept_t1', 'Dept_t3'], inplace=True)

# Save the modified DataFrame back to the database in a new table
vins_df.to_sql("vins_merged_updated", conn, if_exists='replace', index=False)

# Close the connection
conn.close()
