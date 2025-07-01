import sqlite3

# Replace with your absolute path
db_path = r"C:\Users\scb36\Desktop\VehicleDatabaseProject\Vehicle_DB\mydata.db"

# Connect to the database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get and print all table names
tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Close connection
conn.close()
