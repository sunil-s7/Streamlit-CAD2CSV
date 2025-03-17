import streamlit as st
from PIL import Image
import requests

st.title("CAD Data Extractor")

uploaded_file = st.file_uploader("Upload CAD Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("Processing..."):
        # Show preview
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)  # Updated parameter
        
        # Process
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://localhost:8000/process-image/", files=files)
        
        if response.status_code == 200:
            st.success("Processing complete!")
            st.download_button(
                "Download CSV",
                data=response.content,
                file_name="cad_data.csv",
                mime="text/csv"
            )
        else:
            st.error(f"Processing failed: {response.text}")