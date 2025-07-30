import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image


def dashboard_data():
    # ===============================
    # 🖼️ Logo dan Judul
    # ===============================
    try:
        image = Image.open('images/logo.jpg')
        st.image(image, use_container_width=True)
    except FileNotFoundError:
        st.warning("Logo tidak ditemukan di folder images.")
    st.write("Visualisasi interaktif dari data transaksi penjualan.")

    # ===============================
    # 📥 Load Data
    # ===============================
    try:
        df = pd.read_csv('dataset/cleaned_salesdata.csv')
    except FileNotFoundError:
        st.error("❌ File 'dataset/cleaned_salesdata.csv' tidak ditemukan!")
        st.stop()

    # ===============================
    # 📊 Statistik Ringkas
    # ===============================
    st.subheader("📋 Statistik Ringkasan")

    # Hitung Total Transaksi Cancel dan Non-Cancel
    total_cancel = df[df['TransactionNo'].astype(str).str.contains('C')]['TransactionNo'].nunique()
    total_non_cancel = df[~df['TransactionNo'].astype(str).str.contains('C')]['TransactionNo'].nunique()

    # ======= Baris Atas =======
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="border: 2px solid #ff4d4f; border-radius: 10px; padding: 15px; text-align: center; 
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); background-color:#fff5f5;">
                <h4 style="color:#ff4d4f;">❌ Transaksi Cancel</h4>
                <h2 style="color:#ff4d4f;">{total_cancel:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="border: 2px solid #52c41a; border-radius: 10px; padding: 15px; text-align: center; 
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); background-color:#f6ffed;">
                <h4 style="color:#52c41a;">✅ Transaksi Non-Cancel</h4>
                <h2 style="color:#52c41a;">{total_non_cancel:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ======= Spacer untuk jarak =======
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # ======= Baris Bawah =======
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            f"""
            <div style="border: 1px solid #1890ff; border-radius: 10px; padding: 15px; text-align: center; 
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); background-color:#e6f7ff;">
                <h4 style="color:#1890ff;">👥 Total Customer</h4>
                <h2 style="color:#1890ff;">{df['CustomerNo'].nunique():,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="border: 1px solid #faad14; border-radius: 10px; padding: 15px; text-align: center; 
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); background-color:#fffbe6;">
                <h4 style="color:#faad14;">💰 Total Penjualan (£)</h4>
                <h2 style="color:#faad14;">£{df['SalesTotal'].sum():,.0f}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ===============================
    # 📈 Line Chart (Full Width)
    # ===============================
    st.subheader("📅 Tren Penjualan per Bulan")

    # Konversi kolom Date ke datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)

    # Tandai transaksi Cancel dan Non-Cancel
    df['Status'] = df['TransactionNo'].apply(lambda x: 'Cancel' if 'C' in str(x) else 'Non-Cancel')

    # Group by bulan dan status
    monthly_sales = df.groupby(['Month', 'Status'])['SalesTotal'].sum().reset_index()

    # Buat line chart dengan dua garis
    fig_trend = px.line(
        monthly_sales,
        x='Month',
        y='SalesTotal',
        color='Status',
        markers=True,
        title='📈 Total Penjualan per Bulan: Cancel vs Non-Cancel',
        color_discrete_map={'Non-Cancel': '#77DD77', 'Cancel': '#ff4937'}  # Warna hijau untuk Non-Cancel, merah untuk Cancel
    )

    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("---")

    # ===============================
    # 🥧 Pie Chart & Column Chart (Sebaris)
    # ===============================
    st.subheader("📊 Proporsi & Distribusi Negara")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        country_count = df['Country'].value_counts().reset_index()
        country_count.columns = ['Country', 'Total_Transaksi']

        fig_country = px.bar(
            country_count.head(10),
            x='Country',
            y='Total_Transaksi',
            color='Total_Transaksi',
            color_continuous_scale=['#ff4937','#77DD77'],  
            title='🌍 Top 10 Negara dengan Transaksi Terbanyak'
        )

        st.plotly_chart(fig_country, use_container_width=True)
        
    with col_chart2:
        outlier_count = df['is_outlier'].value_counts().reset_index()
        outlier_count.columns = ['Status', 'Jumlah']
        outlier_count['Status'] = outlier_count['Status'].map({0: 'Normal', 1: 'Outlier'})

        fig_outlier = px.pie(
            outlier_count,
            names='Status',
            values='Jumlah',
            hole=0.4,  
            color='Status',
            color_discrete_map={
                'Normal': '#77DD77',     
                'Outlier': '#ff4937'     
            },
            title='🎯 Proporsi Data Normal & Outlier'
        )
        

        st.plotly_chart(fig_outlier, use_container_width=True)


    st.markdown("---")

    # ===============================
    # 📦 Produk Paling Laris (Full Width)
    # ===============================
    st.subheader("📦 Top 10 Produk Paling Banyak Terjual")
    product_sales = df.groupby('ProductName')['Quantity'].sum().reset_index()
    product_sales = product_sales.sort_values('Quantity', ascending=False).head(10)  # Tetap descending
    fig_product = px.bar(
        product_sales, 
        x='Quantity', 
        y='ProductName',
        orientation='h',
        color='Quantity',
        color_continuous_scale=['#ff4937','#77DD77']
    )
    # Atur supaya kategori diurutkan descending (terbesar di atas)
    fig_product.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig_product, use_container_width=True)


    st.markdown("---")

    # ===============================
    # 🔍 Filter Interaktif & Tabel Data (Full Width)
    # ===============================
    st.subheader("🔍 Filter Data Interaktif")
    country_options = df['Country'].unique().tolist()
    selected_country = st.selectbox('Pilih Negara', ['Semua Negara'] + sorted(country_options))
    
    if selected_country != 'Semua Negara':
        df_filtered = df[df['Country'] == selected_country]
    else:
        df_filtered = df

    st.write(f"📄 Menampilkan **{len(df_filtered):,}** baris data untuk negara: **{selected_country}**")
    st.dataframe(df_filtered, use_container_width=True, height=300)

    # ===============================
    # 📥 Unduh Data
    # ===============================
    st.download_button(
        "⬇️ Unduh Data yang Ditampilkan",
        data=df_filtered.to_csv(index=False),
        file_name="filtered_salesdata.csv",
        mime="text/csv"
    )
