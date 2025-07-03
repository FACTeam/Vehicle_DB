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

st.title("Vehicle Form")

# --- Action Buttons ---
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

# --- Helper Function ---
def get_value_or_prompt(field, df, editable=False):
    val = df[field].values[0] if field in df.columns and pd.notna(df[field].values[0]) else ""
    if editable or val == "":
        return st.text_input(field, value=val)
    else:
        return st.text_input(field, value=val, disabled=True)

# ========== Update Existing Vehicle ==========
if st.session_state.action == "update":
    st.subheader("Update Existing Vehicle")
    vin_list = sorted(final_df['VIN'].dropna().unique().tolist())
    vin = st.selectbox("Select VIN to update", options=[""] + vin_list)
    existing_record = final_df[final_df['VIN'] == vin] if vin else pd.DataFrame()

    if not existing_record.empty:
        vehicle_num = get_value_or_prompt("Vehicle  #", existing_record)
        year = get_value_or_prompt("Year", existing_record)
        make = get_value_or_prompt("Make", existing_record)
        model = get_value_or_prompt("Model", existing_record)
        color = get_value_or_prompt("Color", existing_record)
        vehicle_type = get_value_or_prompt("Vehicle", existing_record)
        title = get_value_or_prompt("Title", existing_record)
        driver = get_value_or_prompt("Driver", existing_record)
        depts = get_value_or_prompt("Depts", existing_record)
        mileage = st.number_input("Current Mileage", min_value=0.0)
        lof = get_value_or_prompt("Last LOF", existing_record)
        tire = get_value_or_prompt("Tire Condition IN 32nds", existing_record)
        condition = get_value_or_prompt("Overall condition", existing_record)
        kbb = get_value_or_prompt("KBB Value", existing_record)
        notes = st.text_area("Notes", value=existing_record['Notes'].values[0] if pd.notna(existing_record['Notes'].values[0]) else "")
        last_service = st.date_input("Last Service Date")
        service_status = st.selectbox("Service?", options=["Yes", "No"])

        if st.button("Submit Update"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prev = final_df[final_df['VIN'] == vin]
            prev_service_date = prev['Date_of_Service'].values[0] if not prev.empty else None

            c.execute('''
                UPDATE final_cleaned SET
                    [Vehicle  #] = ?, Year = ?, Make = ?, Model = ?, Color = ?, [Vehicle] = ?, [Title] = ?,
                    Driver = ?, Depts = ?, [Current Mileage] = ?, [Last LOF] = ?, [Tire Condition IN 32nds] = ?,
                    [Overall condition] = ?, [KBB Value] = ?, Notes = ?, [Date_of_Service] = ?, [Service?] = ?
                WHERE VIN = ?
            ''', (
                vehicle_num, year, make, model, color, vehicle_type, title,
                driver, depts, mileage, lof, tire, condition, kbb, notes,
                str(last_service), service_status, vin
            ))

            c.execute('''
                INSERT INTO survey_log (VIN, Driver, Mileage, Last_Service, Color, Service, Notes, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vin, driver.strip(), mileage, str(last_service), color.strip(), service_status, notes.strip(), timestamp))

            c.execute('''
                INSERT INTO vin_service_log (VIN, Driver, Mileage, Last_Service, Color, Notes, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (vin, driver.strip(), mileage, str(last_service), color.strip(), notes.strip(), timestamp))

            conn.commit()
            st.success(f"✅ Update submitted for VIN: {vin}")

# ========== Add New Vehicle ==========
elif st.session_state.action == "add":
    st.subheader("Add New Vehicle")
    fields = {
        "VIN": "",
        "Vehicle  #": "",
        "Year": "",
        "Make": "",
        "Model": "",
        "Color": "",
        "Vehicle": "",
        "Title": "",
        "Driver": "",
        "Depts": "",
        "Calvin #": "",
        "Last LOF": "",
        "Tire Condition IN 32nds": "",
        "Overall condition": "",
        "KBB Value": "",
        "Notes": ""
    }
    responses = {k: st.text_input(k) for k in fields}
    mileage = st.number_input("Initial Mileage", min_value=0.0)
    last_service = st.date_input("Initial Service Date")
    service_status = st.selectbox("Service?", options=["Yes", "No"])

    if st.button("Save New Vehicle"):
        try:
            c.execute('''
                INSERT INTO final_cleaned (
                    VIN, [Vehicle  #], Year, Make, Model, Color, [Vehicle], Title,
                    Driver, Depts, [Calvin #], [Current Mileage], [Date_of_Service],
                    [Service?], [Last LOF], [Tire Condition IN 32nds],
                    [Overall condition], [KBB Value], Notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                responses["VIN"], responses["Vehicle  #"], responses["Year"], responses["Make"], responses["Model"],
                responses["Color"], responses["Vehicle"], responses["Title"], responses["Driver"], responses["Depts"],
                responses["Calvin #"], mileage, str(last_service), service_status, responses["Last LOF"],
                responses["Tire Condition IN 32nds"], responses["Overall condition"], responses["KBB Value"],
                responses["Notes"]
            ))
            conn.commit()
            st.success(f"✅ New vehicle with VIN {responses['VIN']} added.")
        except Exception as e:
            st.error(f"Error adding vehicle: {e}")

# ========== Download Most Recent Data ==========
st.markdown("### Download Final Table")
export_df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)
buffer = StringIO()
export_df.to_csv(buffer, index=False, encoding='utf-8')
buffer.seek(0)
b64 = base64.b64encode(buffer.read().encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="vehicle_data.csv">📥 Download CSV</a>'
st.markdown(href, unsafe_allow_html=True)

conn.close()
