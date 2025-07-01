import sqlite3
import os

# Define the path to the database
db_path = os.path.join(os.path.dirname(__file__), "mydata.db")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Preview the 47th row to confirm it's the correct one
row_to_delete = cursor.execute("SELECT rowid, * FROM final_cleaned LIMIT 1 OFFSET 46").fetchone()
if row_to_delete:
    print("Deleting row:", row_to_delete)

    # Delete the row using its rowid
    cursor.execute("DELETE FROM final_cleaned WHERE rowid = ?", (row_to_delete[0],))
    conn.commit()
    print("✅ Row deleted.")
else:
    print("❌ Row 47 does not exist.")

# Close the connection
conn.close()
