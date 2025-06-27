# first cleaning script
"""
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load final_merged table
vins_df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Normalize column names just in case
vins_df.columns = vins_df.columns.str.strip()

# Clean and merge Year columns
vins_df['Year_t1'] = vins_df['Year_t1'].astype(str).str.strip().replace({'nan': pd.NA})
vins_df['Year_t3'] = vins_df['Year_t3'].astype(str).str.strip().replace({'nan': pd.NA})
vins_df['Year'] = vins_df['Year_t1'].fillna(vins_df['Year_t3'])

# Clean and merge Make columns
vins_df['Make_t1'] = vins_df['Make_t1'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Make_t3'] = vins_df['Make_t3'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Make_0'] = vins_df['Make_t1'].fillna(vins_df['Make_t3'])

# Clean and merge Model columns
vins_df['Model_t1'] = vins_df['Model_t1'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Model_t3'] = vins_df['Model_t3'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Model_0'] = vins_df['Model_t1'].fillna(vins_df['Model_t3'])

# Drop the original columns
vins_df.drop(columns=[ 'Year_t1', 'Year_t3', 'Make_t1', 'Make_t3', 'Model_t1', 'Model_t3'], inplace=True)

# Save the cleaned and merged data
vins_df.to_sql("final_merged", conn, if_exists='replace', index=False)

# Close the connection
conn.close()
"""

# second cleaning script
"""import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the updated vins table
vins_df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Normalize column names
vins_df.columns = vins_df.columns.str.strip()

# Normalize values in Model and Model_0
vins_df['Model'] = vins_df['Model'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Model_0'] = vins_df['Model_0'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})

# Merge into final Model column
vins_df['Model'] = vins_df['Model'].fillna(vins_df['Model_0'])

# Drop Model_0
vins_df.drop(columns=['Model_0'], inplace=True)

# Save to database
vins_df.to_sql("final_merged", conn, if_exists='replace', index=False)

# Close connection
conn.close()
# End of second cleaning script
"""
# third cleaning script
"""

import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the updated vins table
vins_df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Normalize column names
vins_df.columns = vins_df.columns.str.strip()

# Normalize values in Make and Make_0
vins_df['Make'] = vins_df['Make'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Make_0'] = vins_df['Make_0'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})

# Merge into final Make column
vins_df['Make'] = vins_df['Make'].fillna(vins_df['Make_0'])

# Drop Make_0
vins_df.drop(columns=['Make_0'], inplace=True)

# Save to database
vins_df.to_sql("final_merged", conn, if_exists='replace', index=False)

# Close connection
conn.close()
# End of third cleaning script
"""
# fourth cleaning script
"""
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the table (replace 'your_table' with the correct table name)
df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Drop the unwanted columns if they exist
df.drop(columns=["Unnamed: 9", "Unnamed: 10"], inplace=True, errors='ignore')

# Optionally save the cleaned DataFrame back to the database
df.to_sql("final_merged", conn, if_exists="replace", index=False)

# Close the connection
conn.close()
# End of fourth cleaning script"""

# fifth cleaning script
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect("mydata.db")

# Load final_merged and table4_part2
final_df = pd.read_sql_query("SELECT * FROM final_merged", conn)
part2_df = pd.read_sql_query("SELECT * FROM table4_part2", conn)

# Normalize the key column name (Vehicle#) in both DataFrames if needed
final_df.columns = final_df.columns.str.strip()
part2_df.columns = part2_df.columns.str.strip()

# Make sure the Vehicle# columns are named the same
# Suppose it's 'Vehicle#' in both
# If needed, rename columns like:
part2_df.rename(columns={"Vehicle": "Vehicle #"}, inplace=True)

# Remove rows in final_df where Vehicle# matches any in part2_df
filtered_final_df = final_df[~final_df['Vehicle #'].isin(part2_df['Vehicle #'])]

# Save back to database (overwrite final_merged)
filtered_final_df.to_sql("final_merged", conn, if_exists="replace", index=False)

conn.close()"""

# sixth cleaning script
"""import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the final_merged table
vins_df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Normalize column names: strip spaces
vins_df.columns = vins_df.columns.str.strip()

# Normalize 'Year' and 'Vehicle Year' columns
vins_df['Year'] = vins_df['Year'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
vins_df['Vehicle Year'] = vins_df['Vehicle Year'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})

# Merge into 'Year' column
vins_df['Year'] = vins_df['Year'].fillna(vins_df['Vehicle Year'])
if 'Vehicle Year' in vins_df.columns:
    vins_df.drop(columns=['Vehicle Year'], inplace=True)

# Normalize 'Vehicle #' and 'Vehicle#' columns (adjust if second col name differs)
if 'Vehicle #' in vins_df.columns and 'Vehicle #' in vins_df.columns:
    vins_df['Vehicle #'] = vins_df['Vehicle #'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
    vins_df['Vehicle #'] = vins_df['Vehicle #'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})

    vins_df['Vehicle #'] = vins_df['Vehicle #'].fillna(vins_df['Vehicle #'])
    vins_df.drop(columns=['Vehicle #'], inplace=True)
elif 'Vehicle #' in vins_df.columns:
    vins_df.rename(columns={'Vehicle #': 'Vehicle #'}, inplace=True)

# Save back to database
vins_df.to_sql("final_merged", conn, if_exists='replace', index=False)

conn.close()"""

# seventh cleaning script
"""# Drop column Vehicle#_t5
import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("mydata.db")

# Load the table
df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Drop the column if it exists
if 'Vehicle #_t5' in df.columns:
    df.drop(columns=['Vehicle #_t5'], inplace=True)

# Save back to database
df.to_sql("final_merged", conn, if_exists='replace', index=False)

conn.close()

print("Script completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))"""

# eighth cleaning script

"""import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the final table
vins_df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Normalize column names: strip whitespace
vins_df.columns = vins_df.columns.str.strip()

# -----------------------------------
# Merge 'veh #' and 'Vehicle #' columns
# -----------------------------------
if 'veh #' in vins_df.columns and 'Vehicle #' in vins_df.columns:
    vins_df['veh #'] = vins_df['veh #'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
    vins_df['Vehicle #'] = vins_df['Vehicle #'].astype(str).str.strip().str.lower().replace({'nan': pd.NA})
    vins_df['Vehicle #'] = vins_df['Vehicle #'].fillna(vins_df['veh #'])
    vins_df.drop(columns=['veh #'], inplace=True)

elif 'veh #' in vins_df.columns:
    vins_df.rename(columns={'veh #': 'Vehicle #'}, inplace=True)

# Save back to the database
vins_df.to_sql("final_merged", conn, if_exists='replace', index=False)

conn.close()

# Print timestamp
print("Merged 'veh #' into 'Vehicle #' at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
"""

#ninth cleaning script
"""import sqlite3
import pandas as pd
from datetime import datetime
# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the final_merged table
df = pd.read_sql_query("SELECT * FROM final_merged", conn)

# Normalize column names
df.columns = df.columns.str.strip()

# Convert Last Service to datetime
df['Last Service'] = pd.to_datetime(df['Last Service'], errors='coerce')

# Sort by VIN and Last Service DESC (so latest service comes first)
df.sort_values(by=['VIN', 'Last Service'], ascending=[True, False], inplace=True)

# Group by VIN and forward-fill missing values
df_filled = df.groupby('VIN', group_keys=False).apply(lambda g: g.ffill().bfill()[df.columns])

# Optional: Save back to the database as cleaned table
df_filled.to_sql("final_merged_cleaned", conn, if_exists="replace", index=False)

# Close the connection
conn.close()

# Done
print("Filled missing values by VIN group. Completed at", datetime.now())"""
"""
#tenth cleaning script
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the data
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Capitalize first letter of every word in 'Driver' column
df['Driver'] = df['Driver'].astype(str).str.strip().str.title()

# Capitalize first letter of every word in 'Depts' column
df['Depts'] = df['Depts'].astype(str).str.strip().str.title()

# Capitalize first letter of every word in 'Make' column
df['Make'] = df['Make'].astype(str).str.strip().str.title()

# Capitalize first letter of every word in 'Model' column
df['Model'] = df['Model'].astype(str).str.strip().str.title()

# Capitalize first letter of every word in 'Calvin #' column
df['Calvin #'] = df['Calvin #'].astype(str).str.strip().str.title()

# Save the updated table
df.to_sql("final_cleaned", conn, if_exists="replace", index=False)

# Print confirmation with timestamp
print(f"'Driver','Depts','Make','Model','Calvin #' column capitalized. Update completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Close the connection
conn.close()"""

# eleventh cleaning script
"""
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the table
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Desired column order (matching what you provided)
desired_columns = [
    "VIN",
    "Vehicle  #",
    "Year",
    "Make",
    "Model",
    "Color",
    "Driver",
    "Depts",
    "Mileage",
    "Current Mileage",
    "Last Service",
    "Service?",
    "Date_of_Service",
    "Calvin #",
    "Title",
    "Notes"
]

# Find any extra columns not listed and append them at the end
extra_columns = [col for col in df.columns if col not in desired_columns]
final_columns = desired_columns + extra_columns

# Reorder
df = df[final_columns]

# Save to new table or overwrite
df.to_sql("final_cleaned", conn, if_exists="replace", index=False)

# Log time
print("Table 'final_cleaned' reordered successfully at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Close connection
conn.close()
"""
# twelfth cleaning script
"""import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the table
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Convert to numeric (errors='coerce' turns non-numeric into NaN)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Add 2000 to values that are clearly truncated
df['Year'] = df['Year'].apply(lambda x: x + 2000 if pd.notnull(x) and x < 100 else x)

# Save back to the database
df.to_sql("final_cleaned", conn, if_exists='replace', index=False)

# Print log
print("Fixed 'Year' values at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Close the connection
conn.close()
"""

"""
# fourteenth cleaning script
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the table
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Remove the word 'white' (case-insensitive) from 'Current Mileage' column
df['Current Mileage'] = df['Current Mileage'].astype(str).str.replace(r'\bwhite\b', '', case=False, regex=True).str.strip()

# Save back to the database
df.to_sql("final_cleaned", conn, if_exists='replace', index=False)

# Log time
print("Removed 'white' from Current Mileage at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Close the connection
conn.close()
"""
# fifteenth cleaning script
"""
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the final_cleaned table
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Normalize the 'Depts' column (optional, but useful for consistency)
df['Depts'] = df['Depts'].astype(str).str.strip().str.title()

# Define your custom order
custom_order = [
    "Facilities", "Grounds", "Building Ser", "Camp Saf", "Mail",
    "Field House", "C-Dining", "Biology", "Bunker", "Slc", "Prison"
]

# Set the 'Depts' column as a Categorical type with the specified order
df['Depts'] = pd.Categorical(df['Depts'], categories=custom_order, ordered=True)

# Sort by the ordered 'Depts'
df = df.sort_values('Depts')

# Save back to database
df.to_sql("final_cleaned", conn, if_exists="replace", index=False)

# Log time
print("Sorted by custom department order at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Close the connection
conn.close()
"""
# sixteenth cleaning script
"""
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the final_cleaned table
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Normalize columns
df.columns = df.columns.str.strip()
df['Depts'] = df['Depts'].astype(str).str.strip().str.title()
df['Vehicle  #'] = df['Vehicle  #'].astype(str).str.strip()

# Define custom department order
custom_order = [
    "Facilities", "Grounds", "Building Ser", "Camp Saf", "Mail",
    "Field House", "C-Dining", "Biology", "Bunker", "Slc", "Prison"
]

# Set 'Depts' as a categorical with custom order
df['Depts'] = pd.Categorical(df['Depts'], categories=custom_order, ordered=True)

# Sort by Depts first, then by Vehicle #
df = df.sort_values(by=['Depts', 'Vehicle  #'])

# Save back to database
df.to_sql("final_cleaned", conn, if_exists="replace", index=False)

# Log time
print("Sorted by Depts and Vehicle # at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Close the connection
conn.close()
"""
# seventeenth cleaning script
"""import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("mydata.db")

# Load the table
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Normalize Model column for consistent comparison
df['Model'] = df['Model'].astype(str).str.strip().str.lower()

# Replace 'silver' with 'Silverado'
df['Model'] = df['Model'].replace('silver', 'Silverado')

# Optional: Fix casing after replacement
df['Model'] = df['Model'].str.title()

# Save back to the database
df.to_sql("final_cleaned", conn, if_exists='replace', index=False)

# Log time
print("Replaced 'silver' with 'Silverado' in Model column at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

conn.close()"""

# eighteenth cleaning script
"""import sqlite3
import pandas as pd
from datetime import datetime

# Define the VIN updates
updates = {
    "1FDWE35L52HB44451": {"Model": "Econoline Box", "Year": 2002, "Driver": "Back Row"},
    "1GCHG35R6W1014222": {"Model": "G3500 EXPRESS", "Year": 1998, "Driver": "Back Row Boom"},
    "1GCCS19X438147215": {"Color": "Maroon", "Model": "Truck", "Year": 2003, "Driver": "Dean/Nick"},
    "1GA2GYDG5A1137501": {"Model": "Express 12 pass", "Year": 2010},
    "1GAGG25K981114271": {"Model": "Express 12 pass", "Year": 2008},
    "1GCOKUEG1GZ122766": {"Color": "Gray", "Model": "2500 W/T", "Year": 2016, "Driver": "Bob"},
    "1GT3KZBG8AF151169": {"Color": "Gray", "Model": "Sierra 2500 SLE", "Year": 2010, "Driver": "Nick"},
    "1GCEK14028Z183571": {"Color": "Plum", "Year": 2008},
    "1GCHC29U04E213020": {"Color": "Gold", "Model": "2500HD", "Year": 2004},
    "1GCOKUEG4FZ506586": {"Color": "Red", "Model": "2500", "Year": 2015},
    "1GC3YSE72LF286037": {"Color": "Blue", "Model": "Silverado 3500", "Year": 2020, "Driver": "Scott M"},
    "1FDNF60H6JVA30777": {"Color": "Red", "Model": "F-600 Dump", "Year": 1988, "Driver": "Back Row"},
    "1FDXK84A6JVA00269": {"Color": "White", "Model": "F-800", "Year": 1988, "Driver": "Back Row"},
    "1FTRE14W85HA43457": {"Model": "E150 Econoline", "Year": 2005, "Driver": "Alton"},
    "1GCHC24U57E102488": {"Color": "White", "Model": "Silverado", "Year": 2007, "Driver": "Back Row"},
    "1GBJC34U87E181831": {"Color": "White", "Model": "Silverado", "Year": 2007, "Driver": "Back Row"},
    "1GC2KUEG6FZ540666": {"Color": "Silver", "Model": "Silverado 2500 W/T", "Year": 2015, "Driver": "Mike"},
    "1GCNKPE07DZ400057": {"Color": "Black", "Model": "Silverado", "Year": 2013},
    "NM0GE9F76E1142148": {"Model": "Transit Connect", "Year": 2016},
}

# Connect to the database
conn = sqlite3.connect("mydata.db")
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Apply the updates
for vin, fields in updates.items():
    for col, val in fields.items():
        df.loc[df['VIN'] == vin, col] = val

# Save the updated table
df.to_sql("final_cleaned", conn, if_exists="replace", index=False)

# Log time
print("VIN-based updates applied at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

conn.close()"""

# thirteenth cleaning script

"""import sqlite3
import pandas as pd
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("mydata.db")

# Load the table
df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)

# Convert to integer (removes '.0' from float values)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')  # Use Int64 to allow for NaN

# Save back to database
df.to_sql("final_cleaned", conn, if_exists='replace', index=False)

# Log time
print("Cleaned '.0' from Year column at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Close the connection
conn.close()"""
