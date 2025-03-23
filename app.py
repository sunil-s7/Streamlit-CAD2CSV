import streamlit as st
from PIL import Image
import requests
import json

st.title("CAD Data Extractor")

# Add sidebar with instructions
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    ### Steps to Use:
    1. **Upload Image**
        * Upload your CAD image
        * Click on "Extract Data"
    
    2. **Fill Values**
        * Each field needs to be filled individually
        * Click on each input field and enter the required value
        * Ensure all fields are properly filled
    
    3. **Process Data**
        * After filling all fields
        * Click on "Process with Diamond Rates"
    
    4. **Download Results**
        * Once processing is complete
        * Click on "Download CSV" to get your file
    
    ### Important Notes:
    * All fields must be filled before submission
    * Values should be numeric
    * Wait for each step to complete before proceeding
    """)

if 'csv_data' not in st.session_state:
    st.session_state.csv_data = None
if 'diamonds' not in st.session_state:
    st.session_state.diamonds = None
if 'diamond_rates' not in st.session_state:
    st.session_state.diamond_rates = {}
if 'finding_14kt' not in st.session_state:
    st.session_state.finding_14kt = 0.0
if 'finding_18kt' not in st.session_state:
    st.session_state.finding_18kt = 0.0
if 'finding_plt' not in st.session_state:
    st.session_state.finding_plt = 0.0

# Initialize markup state variables
if 'gold_markup_type' not in st.session_state:
    st.session_state.gold_markup_type = "percentage"
if 'gold_markup_value' not in st.session_state:
    st.session_state.gold_markup_value = 0.0
if 'platinum_markup_type' not in st.session_state:
    st.session_state.platinum_markup_type = "percentage"
if 'platinum_markup_value' not in st.session_state:
    st.session_state.platinum_markup_value = 0.0
if 'diamond_markup_type' not in st.session_state:
    st.session_state.diamond_markup_type = "percentage"
if 'diamond_markup_value' not in st.session_state:
    st.session_state.diamond_markup_value = 0.0
if 'finding_markup_type' not in st.session_state:
    st.session_state.finding_markup_type = "percentage"
if 'finding_markup_value' not in st.session_state:
    st.session_state.finding_markup_value = 0.0

# Add these callback functions at the start of the file, after the imports
def update_gold_markup_type():
    st.session_state.gold_markup_value = 0.0
    st.session_state.gold_markup_value_input = ""

def update_platinum_markup_type():
    st.session_state.platinum_markup_value = 0.0
    st.session_state.platinum_markup_value_input = ""

def update_diamond_markup_type():
    st.session_state.diamond_markup_value = 0.0
    st.session_state.diamond_markup_value_input = ""

def update_finding_markup_type():
    st.session_state.finding_markup_value = 0.0
    st.session_state.finding_markup_value_input = ""

def update_markup_value(markup_type, value_str):
    try:
        value = float(value_str) if value_str else 0.0
        if value < 0:
            st.error(f"Please enter a non-negative number for {markup_type} markup")
            value = 0.0
        return value
    except ValueError:
        st.error(f"Please enter a valid number for {markup_type} markup")
        return 0.0

# Initial form - only for image upload
with st.form("data_form"):
    uploaded_file = st.file_uploader("Upload CAD Image", type=["png", "jpg", "jpeg"])
    submit_image = st.form_submit_button("Extract Data")

if submit_image and uploaded_file:
    with st.spinner("Processing image..."):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        files = {"file": uploaded_file.getvalue()}
        try:
            response = requests.post(
                "http://localhost:8000/extract-diamonds/",
                files=files
            )
            
            if response.status_code == 200:
                st.session_state.diamonds = response.json()['diamonds']
                st.success("Diamond data extracted successfully!")
            else:
                st.error(f"Failed to extract diamond data: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please ensure the FastAPI server is running.")

# First display markup settings
st.subheader("Markup Settings")

# Gold Markup
col1, col2 = st.columns(2)
with col1:
    gold_markup_type = st.radio(
        "Gold Markup Type",
        ["percentage", "fixed"],
        horizontal=True,
        index=0 if st.session_state.gold_markup_type == "percentage" else 1,
        key="gold_markup_type_radio",
        on_change=update_gold_markup_type
    )
    st.session_state.gold_markup_type = gold_markup_type

with col2:
    gold_markup_value_str = st.text_input(
        f"Gold Markup Value ({'+%' if gold_markup_type == 'percentage' else '+$'})",
        key="gold_markup_value_input"
    )
    st.session_state.gold_markup_value = update_markup_value("gold", gold_markup_value_str)

# Platinum Markup
col1, col2 = st.columns(2)
with col1:
    platinum_markup_type = st.radio(
        "Platinum Markup Type",
        ["percentage", "fixed"],
        horizontal=True,
        index=0 if st.session_state.platinum_markup_type == "percentage" else 1,
        key="platinum_markup_type_radio",
        on_change=update_platinum_markup_type
    )
    st.session_state.platinum_markup_type = platinum_markup_type

with col2:
    platinum_markup_value_str = st.text_input(
        f"Platinum Markup Value ({'+%' if platinum_markup_type == 'percentage' else '+$'})",
        key="platinum_markup_value_input"
    )
    st.session_state.platinum_markup_value = update_markup_value("platinum", platinum_markup_value_str)

# Diamond Markup
col1, col2 = st.columns(2)
with col1:
    diamond_markup_type = st.radio(
        "Diamond Markup Type",
        ["percentage", "fixed"],
        horizontal=True,
        index=0 if st.session_state.diamond_markup_type == "percentage" else 1,
        key="diamond_markup_type_radio",
        on_change=update_diamond_markup_type
    )
    st.session_state.diamond_markup_type = diamond_markup_type

with col2:
    diamond_markup_value_str = st.text_input(
        f"Diamond Markup Value ({'+%' if diamond_markup_type == 'percentage' else '+$'})",
        key="diamond_markup_value_input"
    )
    st.session_state.diamond_markup_value = update_markup_value("diamond", diamond_markup_value_str)

# Finding Markup
col1, col2 = st.columns(2)
with col1:
    finding_markup_type = st.radio(
        "Finding Markup Type",
        ["percentage", "fixed"],
        horizontal=True,
        index=0 if st.session_state.finding_markup_type == "percentage" else 1,
        key="finding_markup_type_radio",
        on_change=update_finding_markup_type
    )
    st.session_state.finding_markup_type = finding_markup_type

with col2:
    finding_markup_value_str = st.text_input(
        f"Finding Markup Value ({'+%' if finding_markup_type == 'percentage' else '+$'})",
        key="finding_markup_value_input"
    )
    st.session_state.finding_markup_value = update_markup_value("finding", finding_markup_value_str)

# Then display diamond rates section
if st.session_state.diamonds:
    st.subheader("Enter Diamond Rates and Finding Values")
    
    with st.form("diamond_rates_form"):
        # Add finding values section
        st.subheader("Finding Values")
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
        
        st.subheader("Diamond Rates")
        for idx, diamond in enumerate(st.session_state.diamonds):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"Diamond: {diamond['Dia Qlty']} ({diamond['MM Size']})")
            with col2:
                rate_str = st.text_input(
                    f"Rate for {diamond['Dia Qlty']}",
                    key=f"rate_{idx}",
                    placeholder="Enter rate"
                )
                try:
                    rate = float(rate_str) if rate_str else 0.0
                    if rate < 0:
                        st.error("Please enter a non-negative number")
                        rate = 0.0
                except ValueError:
                    st.error("Please enter a valid number")
                    rate = 0.0
                st.session_state.diamond_rates[str(idx)] = rate
        
        process_button = st.form_submit_button("Process with Diamond Rates")
        
        if process_button and 'diamonds' in st.session_state and st.session_state.diamonds:
            # Store the finding values in session state
            st.session_state.finding_14kt = finding_14kt
            st.session_state.finding_18kt = finding_18kt
            st.session_state.finding_plt = finding_plt
            
            with st.spinner("Processing final data..."):
                # Use the uploaded file from earlier
                if 'uploaded_file' in locals() and uploaded_file:
                    files = {"file": uploaded_file.getvalue()}
                    
                    data = {
                        "finding_14kt": finding_14kt,
                        "finding_18kt": finding_18kt,
                        "finding_plt": finding_plt,
                        "diamond_rates": json.dumps(st.session_state.diamond_rates),
                        "gold_markup_type": st.session_state.gold_markup_type,
                        "gold_markup_value": st.session_state.gold_markup_value,
                        "platinum_markup_type": st.session_state.platinum_markup_type,
                        "platinum_markup_value": st.session_state.platinum_markup_value,
                        "diamond_markup_type": st.session_state.diamond_markup_type,
                        "diamond_markup_value": st.session_state.diamond_markup_value,
                        "finding_markup_type": st.session_state.finding_markup_type,
                        "finding_markup_value": st.session_state.finding_markup_value
                    }
                    
                    try:
                        response = requests.post(
                            "http://localhost:8000/process-image/",
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

if st.session_state.csv_data is not None:
    st.download_button(
        "Download CSV",
        data=st.session_state.csv_data,
        file_name="cad_data.csv",
        mime="text/csv"
    )
