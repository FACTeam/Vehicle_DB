# CLean up table2 by converting Vehicle # to integer and removing unwanted characters
    #import sqlite3

    # Connect to your database
    #conn = sqlite3.connect("mydata.db")
    #cursor = conn.cursor()

    # Create a new temporary table with the desired columns and types
    #cursor.execute("""
    #CREATE TABLE table2_cleaned (
    #    [vehicle#] INTEGER,
    #    [Date_of_Service] TEXT,
    #[Notes] TEXT
    #)
    #""")

    # Copy the data, converting Vehicle # to integer
    #cursor.execute("""
    #INSERT INTO table2_cleaned ([vehicle#], [Date_of_Service], [Notes])
    #SELECT CAST([Vehicle #] AS INTEGER), [Date of Service], [Notes]
    #FROM table2
    #""")

    # Drop the old table
    #cursor.execute("DROP TABLE table2")

    # Rename the cleaned table
    #cursor.execute("ALTER TABLE table2_cleaned RENAME TO table2")

    #conn.commit()
    #conn.close()

# Limiting the number of rows for table2
    #import sqlite3
    #import pandas as pd

    # Connect to the SQLite database
    #conn = sqlite3.connect("mydata.db")

    # Load the full table2
    #df = pd.read_sql_query("SELECT * FROM table2", conn)

    # Keep only the first 17 rows
    #df_limited = df.head(17)

    # Save to a new table in the same database
    #df_limited.to_sql("table2_limited", conn, if_exists="replace", index=False)

    #conn.close()
    #print("✅ table2_limited created with first 17 rows of table2.")


 #Rename the column in table2_limited to match vins
    #import sqlite3
    #import pandas as pd
        # Connect to your database
    #conn = sqlite3.connect("mydata.db") 
        # Load the table2_limited
    #table2_df = pd.read_sql_query("SELECT * FROM table2_limited", conn)
    # Rename the column to match the VINs table
    #def rename_columns(df):
        #return df.rename(columns={
         #   'vehicle#': 'Vehicle #',  # Adjust this based on the actual column name in table2_limited
        #})

    #table2_df = rename_columns(table2_df)   
    # Save the modified DataFrame back to the database
    #table2_df.to_sql("table2_limited", conn, if_exists="replace", index=False)
    # Close the connection
    #conn.close()
# Changing the data type for the column 'Vehicle #' in table2_limited to INTEGER    
    #import sqlite3
    #import pandas as pd

    # Connect to SQLite database
#    conn = sqlite3.connect("mydata.db")
#
    # Read the table
 #   df = pd.read_sql_query("SELECT * FROM table2_limited", conn)

    # Print current dtypes (optional for verification)
 #   print("Before conversion:\n", df.dtypes)

    # Convert 'Vehicle #' to string (object)
  #  df['Vehicle #'] = df['Vehicle #'].astype(str)           

    # Print new dtypes for confirmation
   # print("\nAfter conversion:\n", df.dtypes)

    # Save the updated DataFrame back to SQLite (overwrite existing)
    #df.to_sql("table2_limited", conn, if_exists="replace", index=False)

    # Close connection
    #conn.close()
# Normailizing the column names in table2_limited
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("mydata.db")

# Load table2_limited
df = pd.read_sql_query("SELECT * FROM table2_limited", conn)

# Normalize 'Vehicle #' column
df['Vehicle #'] = (
    df['Vehicle #']
    .astype(str)
    .str.replace(r'\.0$', '', regex=True)
)

# Save back to the same table
df.to_sql("table2_limited", conn, if_exists="replace", index=False)

conn.close()