import sqlite3
import pandas as pd

conn = sqlite3.connect('mydata.db')

df1 = pd.read_sql_query("SELECT * FROM table1;", conn)
df3 = pd.read_sql_query("SELECT * FROM table3;", conn)
df5 = pd.read_sql_query("SELECT * FROM table5;", conn)

# Strip spaces from column names
df1.columns = df1.columns.str.strip()
df3.columns = df3.columns.str.strip()
df5.columns = df5.columns.str.strip()

# Merge on 'VIN' with outer joins
merged = pd.merge(df1, df3, on='VIN', how='outer', suffixes=('_t1', '_t3'))
merged = pd.merge(merged, df5, on='VIN', how='outer', suffixes=('', '_t5'))

# Save merged dataframe back to SQLite as 'vins' table
merged.to_sql('vins', conn, if_exists='replace', index=False)

conn.close()
