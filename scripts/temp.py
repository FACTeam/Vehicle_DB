import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect("mydata.db")

# Run a temporary query to view mileage order
query = """
SELECT VIN, Driver, Mileage, [Last Service]
FROM final_cleaned
WHERE Mileage IS NOT NULL
ORDER BY CAST(Mileage AS INTEGER) DESC
LIMIT 45;
"""

# Execute the query and display results
preview_df = pd.read_sql_query(query, conn)
print(preview_df)

# Close connection
conn.close()
