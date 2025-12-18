import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import xlsxwriter

st.set_page_config(page_title="Lake Garda Wedding CNI Pro", layout="wide")

st.title("🇮🇹 Wedding CNI Professional Extractor")
st.write("Upload a CNI to generate translation tables. You can edit the values below manually if needed.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "jpg", "jpeg", "png"])

# Pre-set data for Dominic & Amy as a fallback
default_data = {
    "name1": "Dominic Jordan ADAMS",
    "age1": "30 / Celibe",
    "name2": "Amy Elizabeth LAMB",
    "age2": "31 / Nubile",
    "registrar": "G Turner",
    "district": "Staffordshire"
}

if uploaded_file:
    content = ""
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                content = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        
        st.success("✅ File uploaded!")
        
        # Manual Editor colums
        st.subheader("📋 Verify & Edit Translation Data")
        col1, col2 = st.columns(2)
        with col1:
            n1 = st.text_input("Groom Name", default_data["name1"])
            a1 = st.text_input("Groom Age/Status", default_data["age1"])
        with col2:
            n2 = st.text_input("Bride Name", default_data["name2"])
            a2 = st.text_input("Bride Age/Status", default_data["age2"])
        
        reg = st.text_input("Registrar", default_data["registrar"])
        dist = st.text_input("District", default_data["district"])

        # Create DataFrame for Excel
        df = pd.DataFrame([
            {"Campo": "Sposo", "Valore": n1, "Dettaglio": a1},
            {"Campo": "Sposa", "Valore": n2, "Dettaglio": a2},
            {"Campo": "Ufficiale", "Valore": reg, "Dettaglio": dist}
        ])
        st.table(df)

        # Excel Export
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 Download Excel Translation",
            data=output.getvalue(),
            file_name="CNI_Translation.xlsx",
            mime="application/vnd.ms-excel"
        )

        if content:
            st.divider()
            st.subheader("📝 Raw Text Found")
            st.text_area("Document Content:", content, height=200)
        else:
            st.warning("⚠️ Text could not be read automatically. Please use the manual boxes above.")

    except Exception as e:
        st.error(f"Error: {e}")
