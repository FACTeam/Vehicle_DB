import pandas as pd
import sqlite3
import os

# === Settings ===
db_path = "mydata.db"  # SQLite DB file
csv_files = ["Maintenance Schedule v2.csv", "ServiceLog.csv","ServiceSchedule.csv","Vehicles - 2.0.csv","Vehicles - VIN - Title.csv"]  # List of your CSV file paths
table_names = ["table1", "table2","table3","table4","table5"]      # Corresponding table names in the DB

# === Connect to SQLite ===
conn = sqlite3.connect("mydata.db")
cursor = conn.cursor()

for csv_file, table_name in zip(csv_files, table_names):
    # Load CSV into DataFrame
    df = pd.read_csv(csv_file)
    
    # Import into SQLite (replace if already exists)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"✅ Imported {csv_file} into table '{table_name}'")

# === Optional: Sample query ===
for table in table_names:
    print(f"\nSample from '{table}':")
    result = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5;", conn)
    print(result)

# === Done ===
conn.close()
