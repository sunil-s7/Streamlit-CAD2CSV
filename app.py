import streamlit as st
from PIL import Image
import requests

st.title("CAD Data Extractor")

if 'csv_data' not in st.session_state:
    st.session_state.csv_data = None

with st.form("data_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        finding_14kt = st.number_input("Finding For Gold 14KT", min_value=0.0, format="%.2f")
    with col2:
        finding_18kt = st.number_input("Finding For Gold 18KT", min_value=0.0, format="%.2f")
    with col3:
        finding_plt = st.number_input("Finding for Plt.", min_value=0.0, format="%.2f")

    uploaded_file = st.file_uploader("Upload CAD Image", type=["png", "jpg", "jpeg"])
    
    # Submit button
    submit_button = st.form_submit_button("SUBMIT")

if submit_button:
    if uploaded_file is None:
        st.error("Please upload an image first!")
    else:
        with st.spinner("Processing..."):
            # Show preview
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Process with finding values
            files = {
                "file": uploaded_file.getvalue()
            }
            data = {
                "finding_14kt": finding_14kt,
                "finding_18kt": finding_18kt,
                "finding_plt": finding_plt
            }
            
            try:
                response = requests.post(
                    "https://utkarsh134-fastapi-img2csv.hf.space/process-image/",
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    st.success("Processing complete!")
                    # Store response content in session state
                    st.session_state.csv_data = response.content
                else:
                    st.error(f"Processing failed: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the server. Please ensure the FastAPI server is running.")

# Display download button outside the form if we have CSV data
if st.session_state.csv_data is not None:
    st.download_button(
        "Download CSV",
        data=st.session_state.csv_data,
        file_name="cad_data.csv",
        mime="text/csv"
    )
