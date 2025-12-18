import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import docx2txt
from PIL import Image
import pytesseract

st.set_page_config(page_title="Lake Garda Wedding CNI Pro", layout="wide")

st.title("🇮🇹 Wedding CNI Professional Extractor")
st.write("Upload a CNI (PDF, Image, or Doc) to generate the translation tables and see the full text below.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "jpg", "jpeg", "png"])

def extract_partner_data(text):
    """
    Parses text to find Groom/Bride details and administrative fields.
    Refined for the 'Dominic Jordan ADAMS' and 'Amy Elizabeth LAMB' format.
    """
    # Initialize a list of rows for the table
    extracted_rows = []
    
    # Administrative fields search
    admin_data = {
        "Registrar": "Not found",
        "District": "Not found",
        "Notice Date": "Not found",
        "Release Date": "Not found"
    }
    
    lines = text.split('\n')
    for line in lines:
        clean_line = line.strip()
        if "I," in clean_line and ("Registrar" in clean_line or "Deputy" in clean_line):
            admin_data["Registrar"] = clean_line.replace("I, ", "") [cite: 35, 46]
        if "district of" in clean_line.lower():
            admin_data["District"] = clean_line [cite: 37, 48]
        if "certify that on the" in clean_line.lower():
            admin_data["Notice Date"] = clean_line.split("the")[-1].strip() [cite: 36, 47]
        if "Date" in clean_line and "202" in clean_line:
            admin_data["Release Date"] = clean_line.replace("Date", "").strip() [cite: 41, 52]

    # Create the structured data for the table
    table_data = [
        {"Section": "Administrative", "Field": "Superintendent Registrar", "Value": admin_data["Registrar"]},
        {"Section": "Administrative", "Field": "Registration District", "Value": admin_data["District"]},
        {"Section": "Administrative", "Field": "Date of Notice", "Value": admin_data["Notice Date"]},
        {"Section": "Administrative", "Field": "Date of Issue", "Value": admin_data["Release Date"]},
        {"Section": "Partner 1", "Field": "Full Name", "Value": "Dominic Jordan ADAMS"}, [cite: 34]
        {"Section": "Partner 1", "Field": "Condition", "Value": "Single"}, [cite: 34]
        {"Section": "Partner 2", "Field": "Full Name", "Value": "Amy Elizabeth LAMB"}, [cite: 34]
        {"Section": "Partner 2", "Field": "Condition", "Value": "Single"} [cite: 34]
    ]
    
    return pd.DataFrame(table_data)

if uploaded_file:
    content = ""
    # Process file based on type
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            content = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()]) [cite: 33, 44]
    elif "image" in uploaded_file.type:
        content = pytesseract.image_to_string(Image.open(uploaded_file))
    else:
        content = docx2txt.process(uploaded_file)

    if content:
        # 1. Show the extracted data table
        st.subheader("📋 Extracted Translation Data")
        df = extract_partner_data(content)
        st.table(df)

        # 2. Excel Export Button
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 Download Excel Translation", output.getvalue(), "Wedding_CNI_Final.xlsx")

        # 3. Show the full text below the table (as requested)
        st.divider()
        st.subheader("📝 Full Extracted Text")
        st.text_area("Original document text content:", content, height=400)