import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
from PIL import Image
import pytesseract
import docx2txt

st.set_page_config(page_title="Lake Garda Wedding - CNI Multi-Tool", layout="wide")

st.title("🇮🇹 Wedding Document Data Extractor")
st.write("Upload a CNI in any format (PDF, Word, Image, or Text) to generate a translation.")

# File uploader for multiple formats
uploaded_file = st.file_uploader("Upload document", type=["pdf", "docx", "jpg", "jpeg", "png", "txt"])

def extract_data(file_content):
    # This is a placeholder for your specific extraction logic
    # In a production version, we would use LLM prompts or Regex to map to your Excel columns
    return {
        "Nome e cognome (1)": ["Dominic Jordan ADAMS", "Amy Elizabeth LAMB"],
        "Età (2)": ["30", "31"],
        "Stato Civile (3)": ["Celibe", "Nubile"],
        "Professione (4)": ["Barber", "Showroom Manager"],
        "Luogo di residenza (5)": ["Stapenhill, UK", "Stapenhill, UK"],
        "Periodo di residenza (6)": ["More than a month", "More than a month"]
    }

if uploaded_file is not None:
    file_type = uploaded_file.type
    text_content = ""

    try:
        # 1. Handle PDF
        if file_type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text_content = "\n".join([page.extract_text() for page in pdf.pages])
        
        # 2. Handle DOCX
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text_content = docx2txt.process(uploaded_file)
            
        # 3. Handle Images (OCR)
        elif "image" in file_type:
            img = Image.open(uploaded_file)
            text_content = pytesseract.image_to_string(img)
            
        # 4. Handle Text
        else:
            text_content = uploaded_file.read().decode("utf-8")

        if text_content:
            st.success(f"Successfully read {uploaded_file.name}")
            
            # Process and Display Data
            extracted_data = extract_data(text_content)
            df = pd.DataFrame(extracted_data)
            st.dataframe(df)

            # Export to Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Translation')
            
            st.download_button(
                label="Download Excel Translation",
                data=output.getvalue(),
                file_name=f"Translation_{uploaded_file.name.split('.')[0]}.xlsx",
                mime="application/vnd.ms-excel"
            )
    except Exception as e:
        st.error(f"Error processing file: {e}")