import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load data
day_df = pd.read_csv('day_clean.csv')

# Pastikan kolom date ada dan bertipe datetime
day_df['date'] = pd.to_datetime(day_df['dteday'])

# Label kategorikal
day_df['workingday_label'] = day_df['workingday'].map({0: 'Weekend/Holiday', 1: 'Working Day'})
day_df['weathersit_label'] = day_df['weathersit'].map({
    1: 'Clear',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Snow'
})
day_df['season_label'] = day_df['season'].map({
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
})

# Layout dashboard
st.title('🚲 Bike Sharing Exploratory Data Analysis')
st.write('Analisis peminjaman sepeda berdasarkan waktu, cuaca, dan hari')

# Sidebar - Filter
st.sidebar.header('Filter Data')

# Filter musim
selected_season = st.sidebar.multiselect(
    'Pilih Musim:',
    options=day_df['season_label'].unique(),
    default=day_df['season_label'].unique()
)

# Filter cuaca
selected_weather = st.sidebar.multiselect(
    'Pilih Cuaca:',
    options=day_df['weathersit_label'].unique(),
    default=day_df['weathersit_label'].unique()
)

# Filter working day
selected_workingday = st.sidebar.multiselect(
    'Pilih Tipe Hari:',
    options=day_df['workingday_label'].unique(),
    default=day_df['workingday_label'].unique()
)

# Filter tanggal
min_date = day_df['date'].min().date()
max_date = day_df['date'].max().date()
date_range = st.sidebar.date_input(
    "Rentang Tanggal:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Cek hasil date_range
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

# Terapkan filter ke dataframe
filtered_df = day_df[
    (day_df['season_label'].isin(selected_season)) &
    (day_df['weathersit_label'].isin(selected_weather)) &
    (day_df['workingday_label'].isin(selected_workingday)) &
    (day_df['date'].dt.date >= start_date) &
    (day_df['date'].dt.date <= end_date)
]

# Tampilkan data setelah difilter
st.subheader('🔍 Preview Data yang Difilter')
st.dataframe(filtered_df.head())

# Plot 1: Rata-rata peminjaman berdasarkan Working Day
st.subheader('📊 Rata-rata Peminjaman Berdasarkan Working Day')
fig1, ax1 = plt.subplots()
sns.barplot(x='workingday_label', y='cnt', data=filtered_df, ci=None, ax=ax1)
ax1.set_xlabel('Tipe Hari')
ax1.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig1)

# Plot 2: Rata-rata peminjaman berdasarkan Cuaca
st.subheader('📊 Rata-rata Peminjaman Berdasarkan Cuaca')
fig2, ax2 = plt.subplots()
sns.barplot(x='weathersit_label', y='cnt', data=filtered_df, ci=None, ax=ax2)
ax2.set_xlabel('Tipe Cuaca')
ax2.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig2)

# Insight
st.subheader('🧐 Insight Utama')
st.markdown("""
- **Working Day** cenderung memiliki peminjaman lebih banyak dibandingkan Weekend/Holiday.
- **Working Day** peminjaman banyak dilakukan oleh pekerja dan anak sekolah
- **Holiday** Peminjaman banyak dilakukan oleh orang yang ingin berekreasi, berwisata, dan berjalan santai
- **Cuaca cerah (Clear)** mendorong peminjaman sepeda yang lebih tinggi.
- Anda dapat memfilter data untuk melihat tren per musim dan rentang waktu tertentu.
""")

# Kesimpulan
st.subheader('Conlusion')
st.markdown("""
- **Working Day** Armada sepeda harus difokuskan pada area permukiman dan pusat bisnis pada jam sibuk pagi dan sore.
- **Holiday** Perlu distribusi sepeda yang lebih merata ke area rekreasi, taman, dan pusat wisata.
- **Strategi Promosi** Lakukan promosi aktif saat cuaca cerah atau prakiraan cuaca mendukung, seperti diskon atau bundling perjalanan.
- **Penyesuaian Tarif** Bisa diberlakukan tarif insentif saat cuaca mendung atau kurang ideal untuk mendorong pemakaian.
- **Operasional** Optimalkan distribusi sepeda saat cuaca baik, dan siapkan pengurangan armada atau penjadwalan ulang saat cuaca buruk diperkirakan.
""")
