import sqlite3

# Connect to your database
conn = sqlite3.connect("C:/Users/scb36/Desktop/VehicleDatabaseProject/Project/mydata.db")
cursor = conn.cursor()

# Example: run a SQL query
query = """
SELECT * FROM table1 LIMIT 10;
"""

try:
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as e:
    print("Error:", e)

conn.close()
