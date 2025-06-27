import sqlite3

conn = sqlite3.connect("C:/Users/scb36/Desktop/VehicleDatabaseProject/Project/mydata.db")
cursor = conn.cursor()

for table in ["Table1", "Table3", "Table5"]:
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    print(f"Columns in {table}:")
    print(columns)
    print()
