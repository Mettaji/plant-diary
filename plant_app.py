import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Establish the connection FIRST
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Define your headers
headers = [
    "ID", "Common Name", "Scientific Name", "Max Height (m)", 
    "Max Width (m)", "Soil Type", "Light", "Fertilizer", 
    "Growth Habit", "Flowering Season", "Notes"
]

# 3. Sidebar tool to fix the sheet
if st.sidebar.button("🔨 Initialize Sheet Headers"):
    # Create an empty row with these headers
    df_headers = pd.DataFrame(columns=headers)
    
    # In this library, we use .update() with the data directly
    conn.update(worksheet="Plants", data=df_headers)
    st.sidebar.success("Headers updated! Check your Google Sheet.")

st.title("🌿 Wat Buddha Dhamma Plant Diary")

menu = ["View Diary", "Add New Plant", "Log Growth"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Add New Plant":
    st.subheader("Register a New Species")
    with st.form("new_plant"):
        name = st.text_input("Common Name (e.g., Old Man Banksia)")
        sci_name = st.text_input("Scientific Name")
        loc = st.selectbox("Location", ["Gully", "Ridge", "Water Tanks", "Entrance"])
        notes = st.text_area("Initial Notes")
        
        if st.form_submit_button("Add Plant"):
            # Logic to append row to Google Sheet
            st.success(f"Registered {name}!")

elif choice == "Log Growth":
    st.subheader("Bi-Weekly Photo Update")
    # Pull plant list from Sheets
    df = conn.read(worksheet="Plants")
    plant_choice = st.selectbox("Select Plant", df["Common Name"])
    
    # The Magic Camera Button
    img_file = st.camera_input("Snap a progress photo")
    obs = st.text_area("Growth Observations")
    
    if img_file and st.button("Save Log"):
        # Upload photo to a cloud host (like Cloudinary) 
        # then save the URL and observations to the 'Logs' sheet
        st.success("Progress recorded!")

elif choice == "View Diary":
    st.subheader("Your Collection")
    data = conn.read()
    st.dataframe(data)
