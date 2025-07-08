import sqlite3
import os

# Define the path to the database
db_path = os.path.join(os.path.dirname(__file__), "mydata.db")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# --- Delete row where VIN ends with 4392 ---
row_to_delete = cursor.execute(
    "SELECT rowid, * FROM final_cleaned WHERE VIN LIKE ?",
    ('%4392',)
).fetchone()

if row_to_delete:
    print("Deleting row:", row_to_delete)
    cursor.execute("DELETE FROM final_cleaned WHERE rowid = ?", (row_to_delete[0],))
    conn.commit()
    print("✅ Row with VIN ending in 4392 deleted.")
else:
    print("❌ No row with VIN ending in 4392 found.")

# --- Drop the 'index' column if it exists ---
columns = [col[1] for col in cursor.execute("PRAGMA table_info(final_cleaned)").fetchall()]
if "index" in columns:
    cursor.execute("ALTER TABLE final_cleaned DROP COLUMN index;")
    conn.commit()
    print("✅ 'index' column dropped.")
else:
    print("No 'index' column to drop.")

# Close the connection
conn.close()
