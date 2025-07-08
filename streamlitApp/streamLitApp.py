import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from io import StringIO
import base64
import os

# === Set up dynamic path to database ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "mydata.db"))

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"❌ Database not found at: {DB_PATH}")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# === Create missing columns if not already in the table ===
def ensure_column(name, dtype):
    """Ensure a column exists in the final_cleaned table."""
    existing_cols = [col[1] for col in c.execute("PRAGMA table_info(final_cleaned)").fetchall()]
    if name not in existing_cols:
        allowed_types = {"TEXT", "INTEGER", "REAL", "BLOB"}
        if not name.replace("_", "").replace(" ", "").isalnum():
            raise ValueError(f"Invalid column name: {name}")
        if dtype.upper() not in allowed_types:
            raise ValueError(f"Invalid column type: {dtype}")
        c.execute(f"ALTER TABLE final_cleaned ADD COLUMN \"{name}\" {dtype.upper()};")

ensure_column("Tires Changed?", "TEXT")
ensure_column("Tire Change Date", "TEXT")

@st.cache_data
def load_data():
    """Load all data from the final_cleaned table."""
    return pd.read_sql_query("SELECT * FROM final_cleaned", conn)

final_df = load_data()

# === UI Styling ===
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: white !important;
        color: black !important;
    }
    .stMarkdown, .stTextInput label, .stSelectbox label, .stNumberInput label,
    .stDateInput label, .stTextArea label, .stCheckbox label,
    .stRadio label, .stExpander, .stDataFrameContainer, .stTable, p, span, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }
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
    /* Make the expander header/button red */
    .streamlit-expanderHeader {
        background-color: #C2002F !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold;
        padding: 0.5rem 1rem !important;
    }
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
    <div class="full-logo-container">
        <img src="https://raw.githubusercontent.com/FACTeam/Vehicle_DB/main/logo.png" alt="Company Logo">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Vehicle Form")

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

def get_value_or_prompt(field, df):
    """
    Get a value from df or prompt for input.
    Editable if value is missing/null/empty.
    """
    if (
        df.empty
        or field not in df.columns
        or not pd.notna(df[field].values[0])
        or str(df[field].values[0]).strip() == ""
    ):
        val = ""
        editable = True
    else:
        val = df[field].values[0]
        editable = False
    return st.text_input(field, value=val, disabled=not editable, key=f"{field}_update")

if st.session_state.action == "update":
    st.subheader("Update Existing Vehicle")

    # Combine Vehicle #, VIN, and Driver for search
    final_df["search_label"] = (
        "Vehicle#: " + final_df["Vehicle  #"].astype(str) +
        " | VIN: " + final_df["VIN"].astype(str) +
        " | Driver: " + final_df["Driver"].astype(str)
    )

    search_query = st.text_input(
        "Search by Vehicle #, VIN, or Driver",
        key="vehicle_search"
    )

    # Filter rows that contain the search query (case-insensitive)
    if search_query:
        filtered = final_df[
            final_df["Vehicle  #"].astype(str).str.contains(search_query, case=False, na=False) |
            final_df["VIN"].astype(str).str.contains(search_query, case=False, na=False) |
            final_df["Driver"].astype(str).str.contains(search_query, case=False, na=False)
        ]
else:
    filtered = final_df

# Let user pick from filtered results
vin = st.selectbox(
    "Select Vehicle to update",
    options=[""] + filtered["VIN"].dropna().unique().tolist(),
    key="select_vin_update"
)
existing_record = final_df[final_df['VIN'] == vin] if vin else pd.DataFrame()

if not existing_record.empty:
    st.markdown("**Is the vehicle being serviced?**")
    service_status = st.selectbox(
        "Service Status", options=["No", "Yes"], key="service_status_update", label_visibility="collapsed"
    )

    if service_status == "Yes":
        get_value_or_prompt("Vehicle  #", existing_record)
        get_value_or_prompt("Year", existing_record)
        get_value_or_prompt("Make", existing_record)
        get_value_or_prompt("Model", existing_record)
        get_value_or_prompt("Color", existing_record)
        get_value_or_prompt("Vehicle", existing_record)
        get_value_or_prompt("Title", existing_record)
        get_value_or_prompt("Driver", existing_record)
        get_value_or_prompt("Depts", existing_record)
        get_value_or_prompt("Calvin #", existing_record)

    mileage = st.number_input("Current Mileage", min_value=0.0, key="current_mileage_update")
    last_service = st.date_input("Date Serviced (New)", key="date_serviced_update")

    st.markdown("**Were tires changed?**")
    tires_changed = st.selectbox(
        "Tires Changed?", options=["No", "Yes"], key="tires_changed_update", label_visibility="collapsed"
    )
    tire_change_date = st.date_input("Tire Change Date", key="tire_change_date_update") if tires_changed == "Yes" else ""

    st.markdown("**Was oil changed?**")
    oil_changed = st.selectbox(
        "Oil Changed?", options=["No", "Yes"], key="oil_changed_update", label_visibility="collapsed"
    )
    oil_change_date = st.date_input("Oil Change Date", key="oil_change_date_update") if oil_changed == "Yes" else ""

    st.markdown("**Notes**")
    notes = st.text_area(
        "Notes",
        value=existing_record['Notes'].values[0] if pd.notna(existing_record['Notes'].values[0]) else "",
        key="notes_update"
    )

    if st.button("Submit Update", key="submit_update_btn"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prev_service = existing_record['Date_of_Service'].values[0] if 'Date_of_Service' in existing_record.columns else ""
        last_mileage = existing_record['Current Mileage'].values[0] if 'Current Mileage' in existing_record.columns else ""
        previous_lof = existing_record['Last LOF'].values[0] if 'Last LOF' in existing_record.columns else ""

        # Set last_mileage to the previous value and mileage to the new input
        c.execute('''
            UPDATE final_cleaned SET
                [Last Mileage] = ?, [Current Mileage] = ?, Mileage = ?,
                [Previous LOF] = ?, [Last LOF] = ?,
                [Last Service] = ?, [Date_of_Service] = ?, [Service?] = ?,
                [Tires Changed?] = ?, [Tire Change Date] = ?,
                [Oil Changed?] = ?, [Oil Change Date] = ?, Notes = ?
            WHERE VIN = ?
        ''', (
            last_mileage, mileage, mileage,
            previous_lof, previous_lof,
            prev_service, str(last_service), service_status,
            tires_changed, str(tire_change_date) if tires_changed == "Yes" else None,
            oil_changed, str(oil_change_date) if oil_changed == "Yes" else None,
            notes, vin
        ))

        c.execute('''
            INSERT INTO survey_log (VIN, Driver, Mileage, Last_Service, Color, Service, Notes, Timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vin, existing_record['Driver'].values[0], mileage if service_status == "Yes" else None,
            str(last_service) if service_status == "Yes" else None,
            existing_record['Color'].values[0], service_status, notes.strip(), timestamp
        ))

        conn.commit()
        st.success(f"✅ Update submitted for VIN: {vin}")
        # Refresh data and show updated record
        final_df = load_data()
        st.write("Updated record:")
        st.dataframe(final_df[final_df['VIN'] == vin])

elif st.session_state.action == "add":
    st.subheader("Add New Vehicle")
    known_makes = ["Toyota", "Ford", "Honda", "Chevrolet", "Other"]
    known_colors = ["White", "Black", "Red", "Blue", "Silver", "Other"]
    with st.form("add_vehicle_form"):
        responses = {}
        responses["VIN"] = st.text_input("VIN", key="vin_add")
        responses["Vehicle  #"] = st.text_input("Vehicle  #", key="vehicle_num_add")
        responses["Year"] = st.text_input("Year", key="year_add")
        responses["Make"] = st.selectbox("Make", options=known_makes, key="make_add")
        responses["Model"] = st.text_input("Model", key="model_add")
        responses["Color"] = st.selectbox("Color", options=known_colors, key="color_add")
        responses["Vehicle"] = st.text_input("Vehicle", key="vehicle_add")
        responses["Title"] = st.text_input("Title", key="title_add")
        responses["Driver"] = st.text_input("Driver", key="driver_add")
        responses["Depts"] = st.text_input("Depts", key="depts_add")
        responses["Calvin #"] = st.text_input("Calvin #", key="calvin_add")
        responses["Last LOF"] = st.text_input("Last LOF", key="last_lof_add")
        responses["Tire Condition IN 32nds"] = st.text_input("Tire Condition IN 32nds", key="tire_condition_add")
        responses["Overall condition"] = st.text_input("Overall condition", key="overall_condition_add")
        responses["KBB Value"] = st.text_input("KBB Value", key="kbb_value_add")
        responses["Notes"] = st.text_area("Notes", key="notes_add")
        mileage = st.number_input("Initial Mileage", min_value=0.0, key="initial_mileage_add")
        last_service = st.date_input("Initial Service Date", key="initial_service_date_add")
        service_status = st.selectbox("Service?", options=["Yes", "No"], key="service_status_add")
        submitted = st.form_submit_button("Submit New Vehicle")  # <-- Removed key argument
        if submitted:
            # Input validation
            if not responses["VIN"]:
                st.error("VIN is required.")
            elif final_df['VIN'].eq(responses["VIN"]).any():
                st.error("A vehicle with this VIN already exists.")
            else:
                try:
                    c.execute('''
                        INSERT INTO final_cleaned (
                            VIN, [Vehicle  #], Year, Make, Model, Color, [Vehicle], Title,
                            Driver, Depts, [Calvin #], [Current Mileage], Mileage,
                            [Date_of_Service], [Last Service], [Service?], [Last LOF],
                            [Tire Condition IN 32nds], [Overall condition], [KBB Value], Notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        responses["VIN"], responses["Vehicle  #"], responses["Year"], responses["Make"], responses["Model"],
                        responses["Color"], responses["Vehicle"], responses["Title"], responses["Driver"], responses["Depts"],
                        responses["Calvin #"], mileage, mileage, str(last_service), str(last_service), service_status,
                        responses["Last LOF"], responses["Tire Condition IN 32nds"], responses["Overall condition"],
                        responses["KBB Value"], responses["Notes"]
                    ))
                    conn.commit()
                    st.success(f"✅ New vehicle with VIN {responses['VIN']} added.")
                    # Refresh data
                    final_df = load_data()
                except Exception as e:
                    st.error(f"Error adding vehicle: {e}")

st.markdown("---")

# Initialize session state for table visibility
if "show_db" not in st.session_state:
    st.session_state.show_db = False

# Always show the same button text
if st.button("Show Full Database", key="show_db_btn"):
    st.session_state.show_db = not st.session_state.show_db

if st.session_state.show_db:
    st.markdown("### Full Vehicle Database")
    # Always reload the latest data
    final_df = load_data()
    if "index" in final_df.columns:
        st.dataframe(final_df.drop(columns=["index"]))
    else:
        st.dataframe(final_df)

# ========== Download Most Recent Data ==========
st.markdown("### Download Final Table")
export_df = pd.read_sql_query("SELECT * FROM final_cleaned", conn)
buffer = StringIO()
export_df.to_csv(buffer, index=False, encoding='utf-8')
buffer.seek(0)
b64 = base64.b64encode(buffer.getvalue().encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="vehicle_data.csv">📅 Download CSV</a>'
st.markdown(href, unsafe_allow_html=True)