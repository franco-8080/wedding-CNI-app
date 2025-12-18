import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import xlsxwriter

st.set_page_config(page_title="Lake Garda Wedding CNI Pro", layout="wide")

st.title("🇮🇹 Wedding CNI Professional Extractor")
st.write("Complete the translation details below for the Lake Garda Town Hall.")

uploaded_file = st.file_uploader("Upload CNI Document", type=["pdf", "docx", "jpg", "jpeg", "png"])

if uploaded_file:
    st.success("✅ File uploaded! Please verify the details for the Excel export.")
    
    # Define the 6 columns required by your wedding business template
    col_names = ["Nome e cognome (1)", "Età (2)", "Stato Civile (3)", "Professione (4)", "Luogo di residenza (5)", "Periodo di residenza (6)"]
    
    # Partner 1 Data (Sposo)
    st.subheader("🤵 Partner 1 (Sposo)")
    c1, c2, c3 = st.columns(3)
    with c1:
        n1 = st.text_input("Full Name", "Dominic Jordan ADAMS")
        e1 = st.text_input("Age", "30")
    with c2:
        s1 = st.text_input("Civil Status", "Celibe")
        p1 = st.text_input("Profession", "Barber")
    with c3:
        l1 = st.text_input("Residence", "Stapenhill, UK")
        t1 = st.text_input("Period", "More than a month")

    # Partner 2 Data (Sposa)
    st.subheader("👰 Partner 2 (Sposa)")
    c4, c5, c6 = st.columns(3)
    with c4:
        n2 = st.text_input("Full Name ", "Amy Elizabeth LAMB")
        e2 = st.text_input("Age ", "31")
    with c5:
        s2 = st.text_input("Civil Status ", "Nubile")
        p2 = st.text_input("Profession ", "Showroom Manager")
    with c6:
        l2 = st.text_input("Residence ", "Stapenhill, UK")
        t2 = st.text_input("Period ", "More than a month")

    # Create the complete DataFrame
    data = [
        [n1, e1, s1, p1, l1, t1],
        [n2, e2, s2, p2, l2, t2]
    ]
    df = pd.DataFrame(data, columns=col_names)
    
    st.divider()
    st.subheader("📊 Final Translation Table")
    st.table(df)

    # Excel Export with formatting
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='CNI_Translation')
        # Simple formatting to make headers bold
        workbook  = writer.book
        worksheet = writer.sheets['CNI_Translation']
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
    st.download_button(
        label="📥 Download COMPLETE Excel Translation",
        data=output.getvalue(),
        file_name="Wedding_CNI_Complete.xlsx",
        mime="application/vnd.ms-excel"
    )
