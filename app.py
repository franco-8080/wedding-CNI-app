import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter
from googletrans import Translator

st.set_page_config(page_title="Lake Garda Wedding CNI Pro", layout="wide")

# Initialize the dynamic translator
translator = Translator()

st.title("🇮🇹 Wedding CNI Dynamic Extractor")
st.write("This version uses AI to translate any profession or period into Italian dynamically.")

uploaded_file = st.file_uploader("Upload CNI Document", type=["pdf", "docx", "jpg", "jpeg", "png"])

if uploaded_file:
    st.success("✅ File uploaded!")
    
    col_names = ["Nome e cognome (1)", "Età (2)", "Stato Civile (3)", "Professione (4)", "Luogo di residenza (5)", "Periodo di residenza (6)"]
    
    # Partner 1 Data
    st.subheader("🤵 Partner 1 (Sposo)")
    c1, c2, c3 = st.columns(3)
    with c1:
        n1 = st.text_input("Full Name", "Dominic Jordan ADAMS")
        e1 = st.text_input("Età", "30")
    with c2:
        s1 = st.text_input("Stato Civile (IT)", "Celibe")
        p1_en = st.text_input("Profession (EN)", "Barber")
    with c3:
        l1 = st.text_input("Luogo di residenza", "Stapenhill, UK")
        t1_en = st.text_input("Period of Residence (EN)", "More than a month")

    # Partner 2 Data
    st.subheader("👰 Partner 2 (Sposa)")
    c4, c5, c6 = st.columns(3)
    with c4:
        n2 = st.text_input("Full Name ", "Amy Elizabeth LAMB")
        e2 = st.text_input("Età ", "31")
    with c5:
        s2 = st.text_input("Stato Civile (IT) ", "Nubile")
        p2_en = st.text_input("Profession (EN) ", "Showroom Manager")
    with c6:
        l2 = st.text_input("Luogo di residenza ", "Stapenhill, UK")
        t2_en = st.text_input("Period of Residence (EN) ", "More than a month")

    # DYNAMIC TRANSLATION LOGIC
    # This translates whatever you typed into the boxes above
    p1_it = translator.translate(p1_en, src='en', dest='it').text
    t1_it = translator.translate(t1_en, src='en', dest='it').text
    p2_it = translator.translate(p2_en, src='en', dest='it').text
    t2_it = translator.translate(t2_en, src='en', dest='it').text

    data = [
        [n1, e1, s1, p1_it.capitalize(), l1, t1_it.capitalize()],
        [n2, e2, s2, p2_it.capitalize(), l2, t2_it.capitalize()]
    ]
    
    df = pd.DataFrame(data, columns=col_names)
    
    st.divider()
    st.subheader("📊 Dynamic Translation Table")
    st.table(df)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Traduzione_CNI')
        workbook  = writer.book
        worksheet = writer.sheets['Traduzione_CNI']
        header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_fmt)
            
    st.download_button(
        label="📥 Download Dynamic Excel Translation",
        data=output.getvalue(),
        file_name="Wedding_CNI_Dynamic.xlsx",
        mime="application/vnd.ms-excel"
    )
