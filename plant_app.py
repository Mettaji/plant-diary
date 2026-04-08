import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime


from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io



import requests
import base64

def upload_to_imgbb(file):
    api_key = st.secrets["IMGBB_API_KEY"]
    url = "https://api.imgbb.com/1/upload"
    
    # Convert the uploaded file to a format ImgBB understands
    img_data = base64.b64encode(file.read()).decode('utf-8')
    
    payload = {
        "key": api_key,
        "image": img_data,
    }
    
    response = requests.post(url, payload)
    
    if response.status_code == 200:
        return response.json()["data"]["url"]
    else:
        return "Upload Error"

# ==========================================
# 1. PAGE CONFIGURATION & CONNECTION
# ==========================================
st.set_page_config(page_title="WBD Plant Diary", page_icon="🌿", layout="centered")

conn = st.connection("gsheets", type=GSheetsConnection)




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
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Common Name")
        with col2:
            sci_name = st.text_input("Scientific Name")
        

        # --- PHYSICAL DIMENSIONS ---
        col3, col4 = st.columns(2)
        with col3:
            max_h = st.number_input("Mature H (m)", min_value=0.0, step=0.25)
        with col4:
            max_w = st.number_input("Mature W (m)", min_value=0.0, step=0.25)
        

        # --- ENVIRONMENTAL NEEDS ---
        col5, col6 = st.columns(2)
        with col5:
            soil = st.selectbox("Soil Type", ["Sandy", "Clay", "Loam", "Rocky / Shallow", "Rich / Organic"])
        with col6:
            light = st.select_slider("Light", options=["Full Shade", "Mostly shade", "Part shade", "Full sun + shade from afternoon sun", "Full Sun"])
        
        fert = st.text_input("Fertilizer Req.", value="")

        # Create the binary tick box
        low_phos = st.checkbox("Low Phosphorus", value=False)
        

        # --- CHARACTERISTICS ---
        flowering = st.multiselect("Flowering Season(s)", ["Spring", "Summer", "Autumn", "Winter", "Year-round"])
        habit = st.text_input("Growth Habits")
        

        # --- FIELD NOTES ---
        notes = st.text_area("Notes")
        

        # The widget that accepts the file
        uploaded_file = st.file_uploader("Attach Photo", type=["jpg", "jpeg", "png"])
        
        
        # --- SUBMIT LOGIC ---
        if st.form_submit_button("Save to Diary"):

           # 1. Handle the Image Upload FIRST
            if uploaded_file is not None:
               image_link = upload_to_imgbb(uploaded_file)
            else:
               image_link = "No Image"
           
            plant_id = datetime.now().strftime("%Y%m%d%H%M")
            new_row = pd.DataFrame([{
                "ID": plant_id, 
                "Common Name": name, 
                "Scientific Name": sci_name,
                "Max H (m)": max_h, 
                "Max W (m)": max_w, 
                "Soil Type": soil,
                "Light": light, 
                "Low Phosphorous": "✅" if low_phos else "",
                "Fertilizer": fert, 
                "Flowering": ", ".join(flowering), 
                "Notes": notes,
                "Photo Link": image_link  # Now we add the result here

            }])
            
            st.write("Data Preview:", new_row)
            st.success(f"Details for {name} saved to session!")

            

  # Optional: Show a small preview of the image once selected
       # 2. Outside/Below the form (the preview)
            if 'last_upload' in st.session_state and st.session_state['last_upload'] is not None:
                st.write("---")
                st.markdown("**Last Uploaded Preview:**")
                st.image(st.session_state['last_upload'], width=300)


st.write(f"Available keys: {list(st.secrets.keys())}")


# ------------------------------------------
# OPTION: LOG GROWTH UPDATE
# ------------------------------------------
elif choice == "Log Growth Update":
    st.subheader("📸 Progress Photo")
    
    img_file = st.camera_input("Snap a photo of the plant")
    obs = st.text_area("Growth Observations", placeholder="e.g. New leaves appearing")
    
    if img_file and st.button("Save Log"):
        st.success("Progress saved locally!")
