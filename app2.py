import streamlit as st
import pandas as pd
from logic import *

# Load CSV
df = pd.read_csv('Sales Transaction v.4a.csv')

# Siapkan list produk dan negara
produk_list = df['ProductName'].dropna().unique().tolist()
produk_list.insert(0, 'Pilih produk...')

produk_dict = df.dropna(subset=['ProductName', 'Price']) \
                .drop_duplicates(subset=['ProductName']) \
                .set_index('ProductName')['Price'].to_dict()

negara_list = sorted(df['Country'].dropna().unique().tolist())
negara_list.insert(0, 'Pilih negara...')

# Judul aplikasi
st.title('📦 Aplikasi Prediksi Outlier Pembelian Produk')
st.write("Aplikasi ini memprediksi apakah transaksi tergolong outlier berdasarkan negara, produk, dan jumlah pembelian.")

st.header('📝 Masukkan Data Transaksi')

# Input pengguna
selected_country = st.selectbox('Negara', negara_list)
selected_product = st.selectbox('Nama Produk', produk_list)

# Tampilkan harga produk
harga_produk = produk_dict.get(selected_product, 0)
if selected_product != 'Pilih produk...':
    st.write(f"💰 Harga per item: **${harga_produk:,.0f}**")

quantity = st.number_input('Jumlah Produk', min_value=0) 
# Hitung total harga
total_harga = harga_produk * quantity if isinstance(harga_produk, (int, float)) else 0
st.write(f"🧾 Total harga: **${total_harga:,.0f}**")

# Tombol prediksi
if st.button('Prediksi Transaksi'):
    if selected_country == 'Pilih negara...':
        st.warning("⚠️ Silakan pilih negara terlebih dahulu.")
    elif selected_product == 'Pilih produk...':
        st.warning("⚠️ Silakan pilih produk terlebih dahulu.")
    else:
        try:
            # Encode manual (lebih baik gunakan encoder yang sama saat training)
            country_encoded = hash(selected_country) % 1000
            product_encoded = hash(selected_product) % 1000

            input_data = {
                'country': selected_country,
                'productname': selected_product,
                'quantity': quantity,
                'country_encoded': country_encoded,
                'product_encoded': product_encoded,
                'price': harga_produk
            }

            prediction, probability, _ = predict_purchase(input_data)

            st.header('📈 Hasil Prediksi')
            if prediction == 1:
                st.success('✅ Transaksi DIPREDIKSI NORMAL')
            else:
                st.error('⚠️ Transaksi DIPREDIKSI OUTLIER')

            st.write(f"🎯 Probabilitas termasuk data normal: {probability:.2f}")

            # Simpan ke database jika normal
            if prediction == 1:
                save_to_database(input_data)
                st.info("✅ Data transaksi disimpan ke database.")
            else:
                st.warning("❌ Data tidak disimpan karena termasuk outlier.")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# Menampilkan data dari database
st.markdown("---")
st.subheader("📋 Riwayat Transaksi Tersimpan")
if st.button("Tampilkan Data dari Database"):
    try:
        df_show = fetch_all_predictions()
        if df_show.empty:
            st.info("📭 Belum ada data tersimpan.")
        else:
            st.dataframe(df_show)
    except Exception as e:
        st.error(f"Gagal menampilkan data: {e}")
