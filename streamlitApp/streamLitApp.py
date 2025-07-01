import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Set path to database (now inside the same folder as the app)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mydata.db")

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"❌ Database not found at: {DB_PATH}")

print("✅ Connecting to:", DB_PATH)

# Connect to SQLite DB
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
# --- Create necessary tables ---
c.execute('''
    CREATE TABLE IF NOT EXISTS survey_log (
        VIN TEXT,
        Driver TEXT,
        Mileage REAL,
        Last_Service TEXT,
        Color TEXT,
        Service TEXT,
        Notes TEXT,
        Timestamp TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS vin_service_log (
        VIN TEXT,
        Driver TEXT,
        Mileage REAL,
        Last_Service TEXT,
        Color TEXT,
        Notes TEXT,
        Timestamp TEXT
    )
''')

# --- Load data from final_cleaned ---
@st.cache_data
def load_data():
    return pd.read_sql_query("SELECT * FROM final_cleaned", conn)

final_df = load_data()

st.title("Vehicle Update Form")

# --- VIN input & prefill ---
vin = st.text_input("VIN (required)").strip().upper()
existing_record = final_df[final_df['VIN'] == vin] if vin else pd.DataFrame()

if not existing_record.empty:
    vehicle_num = existing_record['Vehicle  #'].values[0]
    year = int(float(existing_record['Year'].values[0])) if pd.notna(existing_record['Year'].values[0]) else ""
    make = existing_record['Make'].values[0]
    model = existing_record['Model'].values[0]
    depts = existing_record['Depts'].values[0]
    calvin_num = existing_record['Calvin #'].values[0]
    driver_prefill = existing_record['Driver'].values[0]
    color_prefill = existing_record['Color'].values[0]
else:
    vehicle_num = year = make = model = depts = calvin_num = driver_prefill = color_prefill = ""

# --- Display readonly autofilled fields ---
st.text_input("Vehicle #", value=vehicle_num, disabled=True)
st.text_input("Year", value=year, disabled=True)
st.text_input("Make", value=make, disabled=True)
st.text_input("Model", value=model, disabled=True)
st.text_input("Depts", value=depts, disabled=True)
st.text_input("Calvin #", value=calvin_num, disabled=True)

# --- Editable input fields ---
driver = st.text_input("Driver", value=driver_prefill)
mileage = st.number_input("Current Mileage", min_value=0.0)
last_service = st.date_input("Last Service Date")
color = st.text_input("Color", value=color_prefill)
service_status = st.selectbox("Service?", options=["Yes", "No"])
Notes = st.text_input("Notes")

# --- Submit Section ---
if st.button("Submit Update"):
    if vin == "":
        st.warning("VIN is required to submit the update.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prev = final_df[final_df['VIN'] == vin]
        prev_current_mileage = prev['Current Mileage'].values[0] if not prev.empty else None
        prev_service_date = prev['Date_of_Service'].values[0] if not prev.empty else None

        # --- Update final_cleaned ---
        c.execute('''
            UPDATE final_cleaned SET
                Driver = ?,
                Mileage = ?,
                [Current Mileage] = ?,
                [Last Service] = ?,
                [Date_of_Service] = ?,
                [Service?] = ?,
                Color = ?,
                Notes = ?
            WHERE VIN = ?
        ''', (
            driver.strip(),
            prev_current_mileage,
            mileage,
            prev_service_date,
            str(last_service),
            service_status,
            color.strip(),
            Notes.strip(),
            vin
        ))

        # --- Log to survey_log ---
        c.execute('''
            INSERT INTO survey_log (VIN, Driver, Mileage, Last_Service, Color, Service, Notes, Timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (vin, driver.strip(), mileage, str(last_service), color.strip(), service_status, Notes.strip(), timestamp))

        # --- Log to vin_service_log ---
        c.execute('''
            INSERT INTO vin_service_log (VIN, Driver, Mileage, Last_Service, Color, Notes, Timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (vin, driver.strip(), mileage, str(last_service), color.strip(), Notes.strip(), timestamp))

        conn.commit()
        st.success(f"✅ Update submitted for VIN: {vin}")

# --- VIN Service History ---
st.markdown("### VIN Service History")

if st.checkbox("Show Survey Log"):
    log_df = pd.read_sql_query("SELECT * FROM survey_log ORDER BY Timestamp DESC", conn)
    st.dataframe(log_df)

vin_list = pd.read_sql_query("SELECT DISTINCT VIN FROM vin_service_log", conn)['VIN'].tolist()

for vin_item in sorted(vin_list):
    with st.expander(f"▶ VIN: {vin_item}"):
        history = pd.read_sql_query("""
            SELECT * FROM vin_service_log
            WHERE VIN = ?
            ORDER BY Timestamp DESC
            LIMIT 2
        """, conn, params=(vin_item,))
        
        if not history.empty:
            st.dataframe(history)
        else:
            st.info("No service records found for this VIN.")

conn.close()
