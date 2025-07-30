import streamlit as st
from dashboard_data import *

# ✅ Set page config SEKALI SAJA
st.set_page_config(
    page_title="Aplikasi Outlier",
    layout="wide"
)

# ===============================
# 🎛️ Sidebar Aplikasi
# ===============================
st.sidebar.header('⚙️ Navigasi Aplikasi')
st.sidebar.write("""
**Selamat datang di Aplikasi Prediksi Transaksi! ✨**  
""")
menu = st.sidebar.radio('**Menu**', ['Dashboard Data','Input Prediksi', 'Dashboard Input'])
st.caption('presented by Dini Septiana & Selma Nabila R')

# ===============================
# Routing Halaman
# ===============================
if menu == 'Dashboard Data':
    dashboard_data()
elif menu == 'Input Prediksi':
    st.write("""**Fitur ini belum tersedia di deploy/masih local. Silakan gunakan fitur lain.**  
"""             "Fitur ini akan segera hadir! 🚀")
elif menu == 'Dashboard Input':
    st.write("""**Fitur ini belum tersedia di deploy/masih local. Silakan gunakan fitur lain.**  
"""             "Fitur ini akan segera hadir! 🚀")
