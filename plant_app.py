import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime


# ==========================================
# 1. PAGE CONFIGURATION & CONNECTION
# ==========================================
st.set_page_config(page_title="WD Plant Diary", page_icon="🌿", layout="centered")

conn = st.connection("gsheets", type=GSheetsConnection)


# ==========================================
# 2. CUSTOM CSS (Mobile UI & Styling)
# ==========================================
st.markdown("""
    <style>
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
    }
    input::placeholder, textarea::placeholder {
        color: #d1d1d1 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #d1d1d1 !important;
    }
    label {
        font-size: 0.85rem !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 3. MAIN APP INTERFACE
# ==========================================
st.title("🌿 Property Plant Diary")
st.write("---")

menu = ["View Collection", "Add New Plant", "Log Growth Update"]
choice = st.sidebar.selectbox("Menu", menu)


# ------------------------------------------
# OPTION: VIEW COLLECTION
# ------------------------------------------
if choice == "View Collection":
    st.subheader("📋 Current Species Collection")
    
    try:
        df = conn.read()
        st.dataframe(df, use_container_width=True)
    except:
        st.info("Diary is empty or connection is pending.")


# ------------------------------------------
# OPTION: ADD NEW PLANT
# ------------------------------------------
elif choice == "Add New Plant":
    st.subheader("📝 Register New Species")
    
    with st.form("new_plant_form", clear_on_submit=True):
        
        # --- IDENTITY & TAXONOMY ---
        st.markdown("**Identity & Taxonomy**")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Common Name", placeholder="e.g. Old Man Banksia")
        with col2:
            sci_name = st.text_input("Scientific Name", placeholder="e.g. Banksia serrata")
        

        # --- PHYSICAL DIMENSIONS ---
        col3, col4 = st.columns(2)
        with col3:
            max_h = st.number_input("Max H (m)", min_value=0.0, step=0.1)
        with col4:
            max_w = st.number_input("Max W (m)", min_value=0.0, step=0.1)
        

        # --- ENVIRONMENTAL NEEDS ---
        col5, col6 = st.columns(2)
        with col5:
            soil = st.selectbox("Soil Type", ["Sandstone/Sandy", "Clay", "Loam", "Rocky/Shallow"])
        with col6:
            light = st.select_slider("Light", options=["Shade", "Part", "Sun"])
        
        fert = st.text_input("Fertilizer", value="Low Phosphorus (Native)")
        

        # --- CHARACTERISTICS ---
        flowering = st.multiselect("Flowering Season(s)", ["Spring", "Summer", "Autumn", "Winter", "Year-round"])
        habit = st.text_area("Growth Habits", placeholder="e.g. Bird attracting, fire-tolerant")
        

        # --- FIELD NOTES ---
        st.markdown("**Field Notes**")
        notes = st.text_area("Initial Planting Notes", placeholder="e.g. Located near the North tank")

        
        # --- SUBMIT LOGIC ---
        if st.form_submit_button("Save to Diary"):
            plant_id = datetime.now().strftime("%Y%m%d%H%M")
            new_row = pd.DataFrame([{
                "ID": plant_id, 
                "Common Name": name, 
                "Scientific Name": sci_name,
                "Max H (m)": max_h, 
                "Max W (m)": max_w, 
                "Soil Type": soil,
                "Light": light, 
                "Fertilizer": fert, 
                "Flowering": ", ".join(flowering), 
                "Notes": notes
            }])
            
            st.write("Data Preview:", new_row)
            st.success(f"Details for {name} saved to session!")


# ------------------------------------------
# OPTION: LOG GROWTH UPDATE
# ------------------------------------------
elif choice == "Log Growth Update":
    st.subheader("📸 Progress Photo")
    
    img_file = st.camera_input("Snap a photo of the plant")
    obs = st.text_area("Growth Observations", placeholder="e.g. New leaves appearing")
    
    if img_file and st.button("Save Log"):
        st.success("Progress saved locally!")
