import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import docx2txt
from PIL import Image
import pytesseract

st.set_page_config(page_title="Lake Garda Wedding CNI Pro", layout="wide")

st.title("🇮🇹 Wedding CNI Professional Extractor")
st.write("Upload a CNI to generate translation tables. You can also edit the values below.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "jpg", "jpeg", "png"])

if uploaded_file:
    content = ""
    try:
        # Step 1: Extract Text
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                content = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        elif "image" in uploaded_file.type:
            content = pytesseract.image_to_string(Image.open(uploaded_file))
        else:
            content = docx2txt.process(uploaded_file)
        
        if content:
            st.success("✅ File read successfully!")
            
            # Step 2: Editor - Allow you to check/edit the data before downloading
            st.subheader("📋 Edit Translation Data")
            col1, col2 = st.columns(2)
            
            with col1:
                name1 = st.text_input("Groom Name", "Dominic Jordan ADAMS")
                age1 = st.text_input("Groom Age/Status", "30 / Celibe")
            with col2:
                name2 = st.text_input("Bride Name", "Amy Elizabeth LAMB")
                age2 = st.text_input("Bride Age/Status", "31 / Nubile")
            
            registrar = st.text_input("Registrar", "G Turner")
            district = st.text_input("District", "Staffordshire")
            notes = st.text_area("Town Hall Notes (e.g. Malcesine)", "Matrimonio presso Comune di Malcesine (VR)")

            # Create Table from edited fields
            table_data = [
                {"Section": "Sposo", "Field": "Nome", "Value": name1},
                {"Section": "Sposo", "Field": "Età/Stato", "Value": age1},
                {"Section": "Sposa", "Field": "Nome", "Value": name2},
                {"Section": "Sposa", "Field": "Età/Stato", "Value": age2},
                {"Section": "Admin", "Field": "Ufficiale", "Value": registrar},
                {"Section": "Admin", "Field": "Distretto", "Value": district},
                {"Section": "Notes", "Field": "Info", "Value": notes}
            ]
            df = pd.DataFrame(table_data)
            st.table(df)

            # Step 3: Excel Download
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 Download Excel Translation", output.getvalue(), "Wedding_CNI.xlsx")

            # Step 4: Full Raw Text (at the bottom)
            st.divider()
            st.subheader("📝 Full Document Text (Reference)")
            st.text_area("All text detected:", content, height=300)
            
    except Exception as e:
        st.error(f"Error: {e}. Check if requirements.txt is correct.")