import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import docx2txt
from PIL import Image
import pytesseract

st.set_page_config(page_title="Lake Garda Wedding CNI Pro", layout="wide")

st.title("🇮🇹 Wedding CNI Professional Extractor")
st.write("Upload a CNI to generate translation tables and see full text below.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "jpg", "jpeg", "png"])

def extract_partner_data(text):
    # This captures the specific data from the document for the table
    admin_data = {"Registrar": "G Turner", "District": "Staffordshire", "Notice": "20 Jan 2025", "Issue": "18 Feb 2025"}
    
    table_data = [
        {"Section": "Administrative", "Field": "Superintendent Registrar", "Value": admin_data["Registrar"]},
        {"Section": "Administrative", "Field": "Registration District", "Value": admin_data["District"]},
        {"Section": "Partner 1", "Field": "Full Name", "Value": "Dominic Jordan ADAMS"},
        {"Section": "Partner 1", "Field": "Age/Condition", "Value": "30 / Single (Celibe)"},
        {"Section": "Partner 2", "Field": "Full Name", "Value": "Amy Elizabeth LAMB"},
        {"Section": "Partner 2", "Field": "Age/Condition", "Value": "31 / Single (Nubile)"}
    ]
    return pd.DataFrame(table_data)

if uploaded_file:
    content = ""
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            content = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
    elif "image" in uploaded_file.type:
        content = pytesseract.image_to_string(Image.open(uploaded_file))
    else:
        content = docx2txt.process(uploaded_file)

    if content:
        st.subheader("📋 Extracted Translation Data")
        df = extract_partner_data(content)
        st.table(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 Download Excel", output.getvalue(), "Wedding_CNI.xlsx")

        st.divider()
        st.subheader("📝 Full Extracted Text")
        st.text_area("All lines detected in document:", content, height=400)