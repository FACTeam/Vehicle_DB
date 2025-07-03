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

# ==== Load data from final_cleaned ====
@st.cache_data
def load_data():
    return pd.read_sql_query("SELECT * FROM final_cleaned", conn)

final_df = load_data()

# === Background image and color ===
st.markdown(
    """
    <style>
    /* --- Global background and text color --- */
    body, .stApp {
        background-color: white !important;
        color: black !important;
    }

    /* --- Target all common text containers and input labels --- */
    .stMarkdown, .stTextInput label, .stSelectbox label, .stNumberInput label,
    .stDateInput label, .stTextArea label, .stCheckbox label,
    .stRadio label, .stExpander, .stDataFrameContainer, .stTable, p, span, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }

    /* --- Buttons: red with no hover color change --- */
    .stButton > button {
        background-color: #C2002F;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #C2002F;
        color: white;
    }

    /* --- Full-width logo banner --- */
    .full-logo-container {
        width: 100%;
        margin-bottom: 1rem;
    }

    .full-logo-container img {
        width: 100%;
        height: auto;
        display: block;
        object-fit: cover;
    }
    </style>

    <!-- Full-width logo banner -->
    <div class="full-logo-container">
        <img src="https://raw.githubusercontent.com/FACTeam/Vehicle_DB/main/logo.png" alt="Company Logo">
    </div>
    """,
    unsafe_allow_html=True
)

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
    st.subheader("Update Existing Vehicle")

    vin_list = sorted(final_df['VIN'].dropna().unique().tolist())
    vin = st.selectbox("Select VIN to update", options=[""] + vin_list)
    existing_record = final_df[final_df['VIN'] == vin] if vin else pd.DataFrame()

    if not existing_record.empty:
        vehicle_num = existing_record['Vehicle  #'].values[0]
        year = int(float(existing_record['Year'].values[0])) if pd.notna(existing_record['Year'].values[0]) else ""
        make = existing_record['Make'].values[0]
        model = existing_record['Model'].values[0]
        color_prefill = existing_record['Color'].values[0]
        driver_prefill = existing_record['Driver'].values[0]
        depts = existing_record['Depts'].values[0]
        mileage_prefill = existing_record['Mileage'].values[0]
        current_mileage = existing_record['Current Mileage'].values[0]
        last_service = existing_record['Last Service'].values[0]
        service_prefill = existing_record['Service?'].values[0]
        date_of_service = existing_record['Date_of_Service'].values[0]
        calvin_num = existing_record['Calvin #'].values[0]
        title = existing_record['Title'].values[0]
        notes_prefill = existing_record['Notes'].values[0]
        vehicle_type = existing_record['Vehicle'].values[0]
        last_lof = existing_record['Last LOF'].values[0]
        tire_condition = existing_record['Tire Condition IN 32nds'].values[0]
        condition = existing_record['Overall condition'].values[0]
        kbb = existing_record['KBB Value'].values[0]
    else:
        vehicle_num = year = make = model = color_prefill = driver_prefill = depts = mileage_prefill = current_mileage = last_service = ""
        service_prefill = date_of_service = calvin_num = title = notes_prefill = vehicle_type = last_lof = tire_condition = condition = kbb = ""

    st.text_input("Vehicle #", value=vehicle_num, disabled=True)
    st.text_input("Year", value=year, disabled=True)
    st.text_input("Make", value=make, disabled=True)
    st.text_input("Model", value=model, disabled=True)
    st.text_input("Depts", value=depts, disabled=True)
    st.text_input("Calvin #", value=calvin_num, disabled=True)
    st.text_input("Title", value=title)
    st.text_input("Driver", value=driver_prefill)
    st.text_input("Color", value=color_prefill)
    st.text_input("Vehicle Type", value=vehicle_type)
    mileage = st.number_input("New Mileage", min_value=0.0)
    last_service_date = st.date_input("Service Date")
    service_status = st.selectbox("Service?", options=["Yes", "No"], index=0 if service_prefill == "Yes" else 1)
    last_lof = st.text_input("Last LOF", value=last_lof)
    tire_condition = st.text_input("Tire Condition IN 32nds", value=tire_condition)
    condition = st.text_input("Overall condition", value=condition)
    kbb = st.text_input("KBB Value", value=kbb)
    notes = st.text_area("Notes", value=notes_prefill)

    if st.button("Submit Update"):
        if vin == "":
            st.warning("VIN is required to submit the update.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            c.execute('''
                UPDATE final_cleaned SET
                    Driver = ?, Mileage = ?, [Current Mileage] = ?, [Last Service] = ?,
                    [Date_of_Service] = ?, [Service?] = ?, Color = ?, Notes = ?,
                    [Title] = ?, [Last LOF] = ?, [Tire Condition IN 32nds] = ?,
                    [Overall condition] = ?, [KBB Value] = ?, Vehicle = ?
                WHERE VIN = ?
            ''', (
                driver_prefill.strip(), mileage_prefill, mileage, last_service,
                str(last_service_date), service_status, color_prefill.strip(), notes.strip(),
                title, last_lof, tire_condition, condition, kbb, vehicle_type, vin
            ))

            c.execute('''
                INSERT INTO survey_log (VIN, Driver, Mileage, Last_Service, Color, Service, Notes, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vin, driver_prefill.strip(), mileage, str(last_service_date), color_prefill.strip(),
                  service_status, notes.strip(), timestamp))

            c.execute('''
                INSERT INTO vin_service_log (VIN, Driver, Mileage, Last_Service, Color, Notes, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (vin, driver_prefill.strip(), mileage, str(last_service_date), color_prefill.strip(),
                  notes.strip(), timestamp))

            conn.commit()
            st.success(f"✅ Update submitted for VIN: {vin}")

# ========== Add New Vehicle Logic ==========
elif st.session_state.action == "add":
    st.subheader("Add New Vehicle")
    new_vin = st.text_input("VIN")
    new_vehicle_num = st.text_input("Vehicle #")
    new_year = st.text_input("Year")
    new_make = st.text_input("Make")
    new_model = st.text_input("Model")
    new_depts = st.text_input("Depts")
    new_calvin = st.text_input("Calvin #")
    new_title = st.text_input("Title")
    new_driver = st.text_input("Driver")
    new_color = st.text_input("Color")
    new_vehicle_type = st.text_input("Vehicle Type")
    new_mileage = st.number_input("Initial Mileage", min_value=0.0, key="new_mileage")
    new_last_service = st.date_input("Initial Service Date", key="new_service")
    new_service = st.selectbox("Service?", options=["Yes", "No"], key="new_service_status")
    new_last_lof = st.text_input("Last LOF")
    new_tire_condition = st.text_input("Tire Condition IN 32nds")
    new_condition = st.text_input("Overall condition")
    new_kbb = st.text_input("KBB Value")
    new_notes = st.text_area("Notes")

    if st.button("Save New Vehicle"):
        try:
            c.execute("""
                INSERT INTO final_cleaned (
                    VIN, [Vehicle  #], Year, Make, Model, Depts, [Calvin #], Title, Driver,
                    Color, Vehicle, [Current Mileage], [Date_of_Service], [Service?],
                    [Last LOF], [Tire Condition IN 32nds], [Overall condition], [KBB Value], Notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_vin, new_vehicle_num, new_year, new_make, new_model, new_depts,
                new_calvin, new_title, new_driver, new_color, new_vehicle_type, new_mileage,
                str(new_last_service), new_service, new_last_lof, new_tire_condition,
                new_condition, new_kbb, new_notes
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
    with st.expander(f"\u25b6 VIN: {vin_item}"):
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

# --- Download Final Cleaned Table ---
st.markdown("### \ud83d\udcc5 Download Vehicle Database")
updated_df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)
csv = updated_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Current Vehicle Data as CSV",
    data=csv,
    file_name="vehicle_database.csv",
    mime="text/csv",
    help="Click to download the full vehicle table"
)

# --- Close DB connection ---
conn.close()