import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("mydata.db", check_same_thread=False)
c = conn.cursor()

# Load existing data from final_merged to enable auto-fill
@st.cache_data

def load_data():
    return pd.read_sql_query("SELECT * FROM final_cleaned", conn)

final_df = load_data()

st.title("Vehicle Update Form")

# --- Input VIN and auto-fill fields if found ---
vin = st.text_input("VIN (required)").strip().upper()
existing_record = final_df[final_df['VIN'] == vin] if vin else pd.DataFrame()

if not existing_record.empty:
    vehicle_num = existing_record['Vehicle  #'].values[0]
    year = int(float(existing_record['Year'].values[0])) if pd.notna(existing_record['Year'].values[0]) else ""
    make = existing_record['Make'].values[0]
    model = existing_record['Model'].values[0]
    depts = existing_record['Depts'].values[0]
    calvin_num = existing_record['Calvin #'].values[0]
else:
    vehicle_num = ""
    year = ""
    make = ""
    model = ""
    depts = ""
    calvin_num = ""

# --- Input fields ---
st.text_input("Vehicle #", value=vehicle_num, disabled=True)
st.text_input("Year", value=year, disabled=True)
st.text_input("Make", value=make, disabled=True)
st.text_input("Model", value=model, disabled=True)
st.text_input("Depts", value=depts, disabled=True)
st.text_input("Calvin #", value=calvin_num, disabled=True)

driver = st.text_input("Driver")
mileage = st.number_input("Current Mileage", min_value=0.0)
last_service = st.date_input("Last Service Date")
color = st.text_input("Color")
service_status = st.selectbox("Service?", options=["Yes", "No"])
Notes = st.text_input("Notes")

# --- Submit section ---
if st.button("Submit Update"):
    if vin == "":
        st.warning("VIN is required to submit the update.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fetch current values to shift down
        prev = final_df[final_df['VIN'] == vin]
        if not prev.empty:
            prev_current_mileage = prev['Current Mileage'].values[0]
            prev_service_date = prev['Date_of_Service'].values[0]
        else:
            prev_current_mileage = None
            prev_service_date = None

        # Update final_merged: shift old current values to base fields
        c.execute('''
            UPDATE final_merged SET
                Driver = ?,
                Mileage = ?,
                [Current Mileage] = ?,
                [Last Service] = ?,
                [Date_of_Service] = ?,
                [Service?] = ?,
                Color = ?
            WHERE VIN = ?
        ''', (
            driver.strip(),
            prev_current_mileage,
            mileage,
            prev_service_date,
            str(last_service),
            service_status,
            color.strip(),
            vin
        ))

        # Log to survey_log
        c.execute('''
            CREATE TABLE IF NOT EXISTS survey_log (
                VIN TEXT,
                Driver TEXT,
                Mileage REAL,
                Last_Service TEXT,
                Color TEXT,
                Service TEXT,
                Timestamp TEXT
            )
        ''')
        c.execute('''
            INSERT INTO survey_log (VIN, Driver, Mileage, Last_Service, Color, Service, Timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (vin, driver.strip(), mileage, str(last_service), color.strip(), service_status, timestamp))

        conn.commit()
        st.success(f"✅ Update submitted for VIN: {vin}")

# --- Optional: View latest survey log ---
if st.checkbox("Show Survey Log"):
    log_df = pd.read_sql_query("SELECT * FROM survey_log ORDER BY Timestamp DESC", conn)
    st.dataframe(log_df)

conn.close()
