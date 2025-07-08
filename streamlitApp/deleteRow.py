import sqlite3
import os

# Define the path to the database
db_path = os.path.join(os.path.dirname(__file__), "mydata.db")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# --- Delete row #44 (OFFSET 43) ---
row_to_delete = cursor.execute("SELECT rowid, * FROM final_cleaned LIMIT 1 OFFSET 43").fetchone()
if row_to_delete:
    print("Deleting row:", row_to_delete)
    cursor.execute("DELETE FROM final_cleaned WHERE rowid = ?", (row_to_delete[0],))
    conn.commit()
    print("✅ Row 44 deleted.")
else:
    print("❌ Row 44 does not exist.")

# --- Drop the 'index' column if it exists ---
# Check if 'index' column exists
columns = [col[1] for col in cursor.execute("PRAGMA table_info(final_cleaned)").fetchall()]
if "index" in columns:
    cursor.execute("ALTER TABLE final_cleaned DROP COLUMN index;")
    conn.commit()
    print("✅ 'index' column dropped.")
else:
    print("No 'index' column to drop.")

# Close the connection
conn.close()
