import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS MergedVehicles;")
cursor.execute("DROP TABLE IF EXISTS merged_vins;")

conn.commit()
conn.close()
