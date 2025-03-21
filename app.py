import streamlit as st
from PIL import Image
import requests
import json

st.title("CAD Data Extractor")

# Initialize session state
if 'csv_data' not in st.session_state:
    st.session_state.csv_data = None
if 'diamonds' not in st.session_state:
    st.session_state.diamonds = None
if 'diamond_rates' not in st.session_state:
    st.session_state.diamond_rates = {}

with st.form("data_form"):
    # Metal finding inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        finding_14kt_str = st.text_input(
            "Finding For Gold 14KT",
            placeholder="Enter finding for 14KT"
        )
        try:
            finding_14kt = float(finding_14kt_str) if finding_14kt_str else 0.0
            if finding_14kt < 0:
                st.error("Please enter a non-negative number for 14KT finding")
                finding_14kt = 0.0
        except ValueError:
            st.error("Please enter a valid number for 14KT finding")
            finding_14kt = 0.0
            
    with col2:
        finding_18kt_str = st.text_input(
            "Finding For Gold 18KT",
            placeholder="Enter finding for 18KT"
        )
        try:
            finding_18kt = float(finding_18kt_str) if finding_18kt_str else 0.0
            if finding_18kt < 0:
                st.error("Please enter a non-negative number for 18KT finding")
                finding_18kt = 0.0
        except ValueError:
            st.error("Please enter a valid number for 18KT finding")
            finding_18kt = 0.0
            
    with col3:
        finding_plt_str = st.text_input(
            "Finding for Plt.",
            placeholder="Enter finding for Plt"
        )
        try:
            finding_plt = float(finding_plt_str) if finding_plt_str else 0.0
            if finding_plt < 0:
                st.error("Please enter a non-negative number for Plt finding")
                finding_plt = 0.0
        except ValueError:
            st.error("Please enter a valid number for Plt finding")
            finding_plt = 0.0

    uploaded_file = st.file_uploader("Upload CAD Image", type=["png", "jpg", "jpeg"])
    submit_image = st.form_submit_button("Extract Data")

if submit_image and uploaded_file:
    with st.spinner("Processing image..."):
        # Show preview
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Get diamond data first
        files = {"file": uploaded_file.getvalue()}
        try:
            response = requests.post(
                "https://utkarsh134-fastapi-img2csv.hf.space/extract-diamonds/",
                files=files
            )
            
            if response.status_code == 200:
                st.session_state.diamonds = response.json()['diamonds']
                st.success("Diamond data extracted successfully!")
            else:
                st.error(f"Failed to extract diamond data: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please ensure the FastAPI server is running.")

if st.session_state.diamonds:
    st.subheader("Enter Diamond Rates")
    
    with st.form("diamond_rates_form"):
        for idx, diamond in enumerate(st.session_state.diamonds):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"Diamond: {diamond['Dia Qlty']} ({diamond['MM Size']})")
            with col2:
                # Using text_input instead of number_input
                rate_str = st.text_input(
                    f"Rate for {diamond['Dia Qlty']}",
                    key=f"rate_{idx}",
                    placeholder="Enter rate"
                )
                # Validate and convert input to float
                try:
                    rate = float(rate_str) if rate_str else 0.0
                    if rate < 0:
                        st.error("Please enter a non-negative number")
                        rate = 0.0
                except ValueError:
                    st.error("Please enter a valid number")
                    rate = 0.0
                st.session_state.diamond_rates[idx] = rate
        
        process_button = st.form_submit_button("Process with Diamond Rates")
        
        if process_button:
            with st.spinner("Processing final data..."):
                files = {"file": uploaded_file.getvalue()}
                data = {
                    "finding_14kt": finding_14kt,
                    "finding_18kt": finding_18kt,
                    "finding_plt": finding_plt,
                    "diamond_rates": json.dumps(st.session_state.diamond_rates)
                }
                
                try:
                    response = requests.post(
                        "https://utkarsh134-fastapi-img2csv.hf.space/process-image/",
                        files=files,
                        data=data
                    )
                    
                    if response.status_code == 200:
                        st.success("Processing complete!")
                        st.session_state.csv_data = response.content
                    else:
                        st.error(f"Processing failed: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the server. Please ensure the FastAPI server is running.")

# Display download button if we have CSV data
if st.session_state.csv_data is not None:
    st.download_button(
        "Download CSV",
        data=st.session_state.csv_data,
        file_name="cad_data.csv",
        mime="text/csv"
    )
