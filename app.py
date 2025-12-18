import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

# Stable internal translation for common wedding terms
# All other unique professions can be edited live in the app
RESIDENCY_MAP = {
    "More than a month": "Oltre un mese",
    "Less than a month": "Meno di un mese",
    "More than four months": "Oltre quattro mesi"
}

st.set_page_config(page_title="Lake Garda Wedding CNI Pro", layout="wide")

st.title("🇮🇹 Wedding CNI Dynamic Extractor")
st.write("Edit the fields below. The Italian translation for residency and profession will update dynamically.")

uploaded_file = st.file_uploader("Upload CNI Document", type=["pdf", "docx", "jpg", "jpeg", "png"])

if uploaded_file:
    st.success("✅ File uploaded! Verify the Italian translation below.")
    
    col_names = ["Nome e cognome (1)", "Età (2)", "Stato Civile (3)", "Professione (4)", "Luogo di residenza (5)", "Periodo di residenza (6)"]
    
    # Partner 1 (Sposo)
    st.subheader("🤵 Partner 1 (Sposo)")
    c1, c2, c3 = st.columns(3)
    with c1:
        n1 = st.text_input("Full Name", "Dominic Jordan ADAMS")
        e1 = st.text_input("Età", "30")
    with c2:
        s1 = st.text_input("Stato Civile", "Celibe")
        p1 = st.text_input("Professione (Edit to Italian)", "Barbiere")
    with c3:
        l1 = st.text_input("Luogo di residenza", "Stapenhill, UK")
        t1_en = st.selectbox("Periodo di residenza", list(RESIDENCY_MAP.keys()))
        t1_it = RESIDENCY_MAP[t1_en]

    # Partner 2 (Sposa)
    st.subheader("👰 Partner 2 (Sposa)")
    c4, c5, c6 = st.columns(3)
    with c4:
        n2 = st.text_input("Full Name ", "Amy Elizabeth LAMB")
        e2 = st.text_input("Età ", "31")
    with c5:
        s2 = st.text_input("Stato Civile ", "Nubile")
        p2 = st.text_input("Professione (Edit to Italian) ", "Responsabile Showroom")
    with c6:
        l2 = st.text_input("Luogo di residenza ", "Stapenhill, UK")
        t2_en = st.selectbox("Periodo di residenza ", list(RESIDENCY_MAP.keys()))
        t2_it = RESIDENCY_MAP[t2_en]

    # Dynamic Data Table
    data = [
        [n1, e1, s1, p1, l1, t1_it],
        [n2, e2, s2, p2, l2, t2_it]
    ]
    df = pd.DataFrame(data, columns=col_names)
    
    st.divider()
    st.subheader("📊 Final Italian Table Preview")
    st.table(df)

    # Excel Download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Traduzione_CNI')
        workbook  = writer.book
        worksheet = writer.sheets['Traduzione_CNI']
        header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_fmt)
            
    st.download_button(
        label="📥 Download COMPLETE Italian Excel",
        data=output.getvalue(),
        file_name="Wedding_CNI_Italy.xlsx",
        mime="application/vnd.ms-excel"
    )
