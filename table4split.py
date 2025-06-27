import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect("mydata.db")

# Load the full table4
table4 = pd.read_sql_query("SELECT * FROM table4", conn)

# Split into two logical parts
table4_part1 = table4.iloc[:48].copy()
table4_part2 = table4.iloc[48:81].copy()  # Adjust if your second table goes further

# Optionally: reset index (not necessary but nice for clarity)
table4_part1.reset_index(drop=True, inplace=True)
table4_part2.reset_index(drop=True, inplace=True)

# Save each part as its own table in the database
table4_part1.to_sql("table4_part1", conn, if_exists="replace", index=False)
table4_part2.to_sql("table4_part2", conn, if_exists="replace", index=False)

# Close the connection
conn.close()

print("Split completed: table4_part1 and table4_part2 saved.")

"""import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the part2 table
df = pd.read_sql_query("SELECT * FROM table4_part2", conn)

# Rename columns
df.rename(columns={
    "Vehicle": "Vehicle#",
    "Veh #": "Dept.",
    "Driver": "YR",
    "Current Mileage": "Make",
    "Last LOF": "VIN-last 4",
    "Tire Condition IN 32nds": "Notes"
}, inplace=True)

# Drop unwanted columns
columns_to_drop = ['Overall condition', 'KBB Value']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Drop the first row
df = df.drop(df.index[0])

# Save the cleaned table
df.to_sql("table4_part2_final", conn, if_exists="replace", index=False)

conn.close()

print("✅ table4_part2_final has been cleaned and saved.")"""

