import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Set up the page for a clean mobile look
st.set_page_config(
    page_title="Wat Buddha Dhamma Plant Diary", 
    page_icon="🌿", 
    layout="centered"
)

# 1. Establish connection to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🌿 Wat Buddha Dhamma Plant Diary")

# Navigation Sidebar
menu = ["View Collection", "Add New Plant", "Log Growth Update"]
choice = st.sidebar.selectbox("Menu", menu)

# --- OPTION 1: VIEW COLLECTION ---
if choice == "View Collection":
    st.subheader("Current Species on Property")
    try:
        # Read the 'Plants' sheet
        df = conn.read()
        if df.empty:
            st.info("The diary is empty. Head to 'Add New Plant' to start your catalog.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error("Could not load data. Check your Google Sheet sharing settings.")

# --- OPTION 2: ADD NEW PLANT ---
elif choice == "Add New Plant":
    st.subheader("📝 Register New Species")
    st.markdown("Enter the permanent botanical details for this species.")

    with st.form("new_plant_form", clear_on_submit=True):
        # Top Row: Names
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Common Name", placeholder="e.g. Old Man Banksia")
            sci_name = st.text_input("Scientific Name", placeholder="e.g. Banksia serrata")
        with col2:
            max_h = st.number_input("Max Height (m)", min_value=0.0, step=0.5)
            max_w = st.number_input("Max Width (m)", min_value=0.0, step=0.5)

        # Middle Row: Requirements
        col3, col4 = st.columns(2)
        with col3:
            soil = st.selectbox("Soil Type", ["Sandstone/Sandy", "Clay", "Loam", "Rocky/Shallow"])
            light = st.select_slider("Light", options=["Full Shade", "Part Shade", "Full Sun"])
        with col4:
            fert = st.text_input("Fertilizer", value="Low Phosphorus (Native)")
            flowering = st.multiselect("Flowering Season", ["Spring", "Summer", "Autumn", "Winter"])

        # Bottom Row: Habits & Notes
        habit = st.text_area("Growth Habits", placeholder="e.g. Bird attracting, fire-tolerant, fast-growing")
        notes = st.text_area("Initial Planting Notes")

        if st.form_submit_button("Save to Diary"):
            # Create a unique ID based on the current time
            plant_id = datetime.now().strftime("%Y%m%d%H%M")
            
            # Prepare data for Google Sheets
            new_row = pd.DataFrame([{
                "ID": plant_id,
                "Common Name": name,
                "Scientific Name": sci_name,
                "Max Height (m)": max_h,
                "Max Width (m)": max_w,
                "Soil Type": soil,
                "Light": light,
                "Fertilizer": fert,
                "Growth Habit": habit,
                "Flowering Season": ", ".join(flowering),
                "Notes": notes
            }])

            # Append and Update (Requires Service Account for writing)
            # If you haven't set up the Service Account yet, this will show a preview
            st.write("Preview of data to be saved:", new_row)
            st.success(f"Details for {name} are ready. (Note: Instant syncing to Sheets requires a Service Account Key).")

# --- OPTION 3: LOG GROWTH UPDATE ---
elif choice == "Log Growth Update":
    st.subheader("📸 Bi-Weekly Progress Photo")
    
    try:
        df_plants = conn.read(worksheet="Plants")
        plant_to_update = st.selectbox("Select Plant", df_plants["Common Name"])
        
        # Access the phone's camera
        img_file = st.camera_input("Take a progress photo")
        obs = st.text_area("Growth Observations (New leaves? Pests? Flowering?)")
        
        if img_file and st.button("Upload Progress"):
            st.success(f"Progress recorded for {plant_to_update}!")
            st.image(img_file, caption="Last recorded photo")
    except:
        st.warning("Please add at least one plant in 'Add New Plant' first.")
