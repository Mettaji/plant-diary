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
    
    # Forced CSS for Placeholder Color (Light Grey)
    st.markdown("""
        <style>
        /* This targets the internal Streamlit input styling more aggressively */
        input::placeholder, textarea::placeholder {
            color: #d1d1d1 !important; 
            opacity: 1 !important;
            -webkit-text-fill-color: #d1d1d1 !important;
        }
        /* Tighten padding so columns fit better on mobile */
        [data-testid="column"] {
            width: 50% !important;
            flex: 1 1 50% !important;
            min-width: 50% !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.form("new_plant_form", clear_on_submit=True):
        # Row 1: Names
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Common Name", placeholder="e.g. Old Man Banksia")
        with col_b:
            sci_name = st.text_input("Scientific Name", placeholder="e.g. Banksia serrata")

        # Row 2: Dimensions - Using a smaller gap to encourage side-by-side
        col_c, col_d = st.columns(2, gap="small")
        with col_c:
            # We use value=0.0 to initialize it as a number
            max_h = st.number_input("Max H (m)", min_value=0.0, step=0.1)
        with col_d:
            max_w = st.number_input("Max W (m)", min_value=0.0, step=0.1)
            
        # ... Rest of your form ...
        
        if st.form_submit_button("Save to Diary"):
            st.success("Entry recorded and form cleared!")


# --- OPTION 3: LOG GROWTH UPDATE ---
elif choice == "Log Growth Update":
    st.subheader("📸 Monthly Progress Photo")
    
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
