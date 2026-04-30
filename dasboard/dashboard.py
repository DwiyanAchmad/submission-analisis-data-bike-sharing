import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman agar tampil penuh
st.set_page_config(page_title="Bike Sharing Analytics", layout="wide")

# Gaya Visualisasi
sns.set(style='whitegrid')

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Menggunakan path relatif agar Streamlit bisa menemukan file di dalam folder yang sama
    import os
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "main_data.csv")
    
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df
main_df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚲 Bike Rental Control")
    st.markdown("Filter di bawah ini akan mengubah seluruh tampilan grafik secara otomatis.")
    
    # Filter Musim (Lebih stabil untuk analisis)
    all_seasons = main_df["season"].unique()
    selected_season = st.multiselect(
        "Pilih Musim yang Ingin Ditampilkan:", 
        options=all_seasons, 
        default=all_seasons
    )

# Logic Filter
filtered_df = main_df[main_df["season"].isin(selected_season)]

# --- MAIN PAGE ---
st.title('Bike Sharing Analytics Dashboard 🚲')
st.markdown(f"**Analisis Data oleh: Dwiyan Achmad Assidiqie**")

# --- RINGKASAN DATA (METRICS) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan Harian", value=f"{round(filtered_df['cnt'].mean(), 2):,}")
with col3:
    st.metric("Puncak Penyewa per Jam", value=f"{filtered_df['cnt'].max():,}")

st.divider()

# --- ANALISIS PERTANYAAN 1: MUSIM ---
st.header("1. Perbandingan Penyewaan Antar Musim")
st.info("**Pertanyaan Bisnis:** Bagaimana perbedaan rata-rata jumlah penyewaan sepeda (per hari) antara musim gugur (Fall) dan musim dingin (Winter) selama rentang waktu tahun 2011 hingga 2012?")

col_plot1, col_text1 = st.columns([2, 1])

with col_plot1:
    # Menghitung rata-rata penyewaan per musim
    seasonal_usage = filtered_df.groupby("season")["cnt"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"] # Memberi highlight pada bar tertentu
    sns.barplot(x="season", y="cnt", data=seasonal_usage, palette="coolwarm", ax=ax)
    
    ax.set_title("Rata-rata Penyewaan per Musim", fontsize=15)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewa")
    st.pyplot(fig)

with col_text1:
    st.markdown("**Keterangan Diagram:**")
    st.write("Diagram batang ini memvisualisasikan performa penyewaan di setiap musim. Bar yang lebih tinggi menunjukkan minat masyarakat yang lebih besar untuk bersepeda pada periode tersebut.")
    st.markdown("**Kesimpulan:**")
    st.success("Musim Gugur (Fall) adalah periode tersibuk. Hal ini kemungkinan dipengaruhi oleh suhu udara yang nyaman bagi pesepeda dibandingkan Musim Dingin (Winter).")

# --- ANALISIS PERTANYAAN 2: JAM SIBUK ---
st.header("2. Analisis Jam Puncak (Peak Hours)")
st.info("**Pertanyaan Bisnis:** Pada jam berapakah puncak (peak hour) penyewaan sepeda terjadi pada hari kerja (working day) dibandingkan dengan hari libur (holiday) selama periode tahun 2011-2012?")

col_plot2, col_text2 = st.columns([2, 1])

with col_plot2:
    # Menghitung tren jam
    hourly_usage = filtered_df.groupby(["workingday", "hr"])["cnt"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=hourly_usage, 
        x="hr", 
        y="cnt", 
        hue="workingday", 
        palette={0: "#E74C3C", 1: "#2E86C1"}, 
        marker="o", 
        ax=ax
    )
    
    ax.set_title("Tren Penyewaan: Hari Kerja (Biru) vs Hari Libur (Merah)", fontsize=15)
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Jam (00:00 - 23:00)")
    ax.set_ylabel("Rata-rata Penyewa")
    ax.legend(title="Tipe Hari", labels=["Hari Libur/Akhir Pekan", "Hari Kerja"])
    st.pyplot(fig)

with col_text2:
    st.markdown("**Keterangan Diagram:**")
    st.write("Garis biru menunjukkan pola penggunaan sepeda sebagai alat transportasi utama (komuter). Garis merah menunjukkan pola penggunaan untuk rekreasi.")
    st.markdown("**Kesimpulan:**")
    st.success("Puncak terjadi pada jam 08.00 dan 17.00 di hari kerja. Di hari libur, penyewaan lebih merata di siang hari.")

st.divider()

# --- REKOMENDASI STRATEGIS ---
st.header("💡 Rekomendasi Action Item")
st.markdown("""
*   **Optimalisasi Stok:** Pastikan jumlah sepeda tersedia maksimal di titik-titik transportasi umum pada pukul 07.30 pagi setiap hari kerja.
*   **Perawatan Rutin:** Jadwalkan pemeliharaan unit besar-besaran pada Musim Dingin (saat permintaan rendah) agar armada siap total menyambut Musim Gugur.
*   **Paket Wisata:** Buat promo khusus hari libur antara pukul 10.00 hingga 14.00 untuk menarik lebih banyak penyewa rekreasi.
""")

st.caption('Copyright (c) 2026 - Bike Sharing Analysis Dashboard')
