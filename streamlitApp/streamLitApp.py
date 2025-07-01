import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# --- Set up dynamic path to database ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "mydata.db"))  # Database now inside app folder

# --- Check if database file exists ---
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"❌ Database not found at: {DB_PATH}")

print("✅ Connecting to:", DB_PATH)

# --- Connect to database ---
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

# --- Action buttons ---
if "action" not in st.session_state:
    st.session_state.action = "update"

col1, col2 = st.columns(2)
with col1:
    if st.button("Update Existing Vehicle"):
        st.session_state.action = "update"
with col2:
    if st.button("Add New Vehicle"):
        st.session_state.action = "add"

st.divider()

# ========== Update Existing Vehicle Logic ==========
if st.session_state.action == "update":
    st.subheader("🔧 Update Existing Vehicle")

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
        notes_prefill = existing_record['Notes'].values[0]
        service_prefill = existing_record['Service?'].values[0]
    else:
        vehicle_num = year = make = model = depts = calvin_num = driver_prefill = color_prefill = notes_prefill = service_prefill = ""

    st.text_input("Vehicle #", value=vehicle_num, disabled=True)
    st.text_input("Year", value=year, disabled=True)
    st.text_input("Make", value=make, disabled=True)
    st.text_input("Model", value=model, disabled=True)
    st.text_input("Depts", value=depts, disabled=True)
    st.text_input("Calvin #", value=calvin_num, disabled=True)

    driver = st.text_input("Driver", value=driver_prefill)
    mileage = st.number_input("Current Mileage", min_value=0.0)
    last_service = st.date_input("Last Service Date")
    color = st.text_input("Color", value=color_prefill)
    service_status = st.selectbox("Service?", options=["Yes", "No"], index=0 if service_prefill == "Yes" else 1)
    Notes = st.text_input("Notes", value=notes_prefill)

    if st.button("Submit Update"):
        if vin == "":
            st.warning("VIN is required to submit the update.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prev = final_df[final_df['VIN'] == vin]
            prev_current_mileage = prev['Current Mileage'].values[0] if not prev.empty else None
            prev_service_date = prev['Date_of_Service'].values[0] if not prev.empty else None

            c.execute('''
                UPDATE final_cleaned SET
                    Driver = ?, Mileage = ?, [Current Mileage] = ?, [Last Service] = ?,
                    [Date_of_Service] = ?, [Service?] = ?, Color = ?, Notes = ?
                WHERE VIN = ?
            ''', (
                driver.strip(), prev_current_mileage, mileage, prev_service_date,
                str(last_service), service_status, color.strip(), Notes.strip(), vin
            ))

            c.execute('''
                INSERT INTO survey_log (VIN, Driver, Mileage, Last_Service, Color, Service, Notes, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vin, driver.strip(), mileage, str(last_service), color.strip(),
                  service_status, Notes.strip(), timestamp))

            c.execute('''
                INSERT INTO vin_service_log (VIN, Driver, Mileage, Last_Service, Color, Notes, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (vin, driver.strip(), mileage, str(last_service), color.strip(),
                  Notes.strip(), timestamp))

            conn.commit()
            st.success(f"✅ Update submitted for VIN: {vin}")

# ========== Add New Vehicle Logic ==========
elif st.session_state.action == "add":
    st.subheader("🚗 Add New Vehicle")
    new_vin = st.text_input("VIN")
    new_vehicle_num = st.text_input("Vehicle #")
    new_year = st.text_input("Year")
    new_make = st.text_input("Make")
    new_model = st.text_input("Model")
    new_depts = st.text_input("Depts")
    new_calvin = st.text_input("Calvin #")
    new_driver = st.text_input("Driver")
    new_mileage = st.number_input("Initial Mileage", min_value=0.0, key="new_mileage")
    new_last_service = st.date_input("Initial Service Date", key="new_service")
    new_color = st.text_input("Color")
    new_service = st.selectbox("Service?", options=["Yes", "No"], key="new_service_status")
    new_notes = st.text_area("Notes")

    if st.button("Save New Vehicle"):
        try:
            c.execute("""
                INSERT INTO final_cleaned (
                    VIN, [Vehicle  #], Year, Make, Model, Depts, [Calvin #], Driver,
                    [Current Mileage], [Date_of_Service], [Service?], Color, Notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_vin, new_vehicle_num, new_year, new_make, new_model, new_depts,
                new_calvin, new_driver, new_mileage, str(new_last_service), new_service,
                new_color, new_notes
            ))
            conn.commit()
            st.success(f"✅ New vehicle with VIN {new_vin} added.")
        except Exception as e:
            st.error(f"Error adding vehicle: {e}")

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