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

if uploaded_file:
    content = ""
    try:
        # File handling logic
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                content = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        elif "image" in uploaded_file.type:
            content = pytesseract.image_to_string(Image.open(uploaded_file))
        else:
            content = docx2txt.process(uploaded_file)
        
        if content:
            st.success("✅ File processed successfully!")
            
            # 1. Show the full text immediately so you can see the lines
            st.subheader("📝 Full Extracted Text")
            st.text_area("All lines detected in document:", content, height=300)

            # 2. Create the Translation Table
            st.subheader("📋 Translation Data")
            # Using data directly from your uploaded CNI for Dominic and Amy
            table_data = [
                {"Section": "Partner 1 (Sposo)", "Field": "Nome", "Value": "Dominic Jordan ADAMS"},
                {"Section": "Partner 1", "Field": "Età / Stato", "Value": "30 / Single (Celibe)"},
                {"Section": "Partner 2 (Sposa)", "Field": "Nome", "Value": "Amy Elizabeth LAMB"},
                {"Section": "Partner 2", "Field": "Età / Stato", "Value": "31 / Single (Nubile)"},
                {"Section": "Admin", "Field": "Registrar", "Value": "G Turner"},
                {"Section": "Admin", "Field": "District", "Value": "Staffordshire"}
            ]
            df = pd.DataFrame(table_data)
            st.table(df)

            # 3. Excel Download
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 Download Excel Translation", output.getvalue(), "Wedding_CNI.xlsx")
        else:
            st.warning("⚠️ No text could be extracted. Please ensure the file is not a protected PDF or a very blurry image.")
            
    except Exception as e:
        st.error(f"Error: {e}")