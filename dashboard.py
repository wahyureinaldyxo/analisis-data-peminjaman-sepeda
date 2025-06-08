import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 


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
st.write('Analisis peminjaman sepeda berdasarkan cuaca dan hari')

# Sidebar - Filter
st.sidebar.header('Filter Data')


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
    (day_df['date'].dt.date >= start_date) &
    (day_df['date'].dt.date <= end_date)
]


# Plot 1: Rata-rata peminjaman berdasarkan Working Day
st.subheader('Rata-rata Peminjaman Berdasarkan Workingday')
fig1, ax1 = plt.subplots()
sns.barplot(x='workingday_label', y='cnt', data=filtered_df, ci=None, ax=ax1)
ax1.set_xlabel('Tipe Hari')
ax1.set_ylabel('Rata-rata Jumlah Peminjaman')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)}'))
st.pyplot(fig1)

# Plot 2: Rata-rata peminjaman berdasarkan Cuaca
st.subheader('Rata-rata Peminjaman Berdasarkan Cuaca')
fig2, ax2 = plt.subplots()
sns.barplot(x='weathersit_label', y='cnt', data=filtered_df, order=['Clear', 'Mist/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Snow'], ci=None, ax=ax2)
ax2.set_xlabel('Kondisi Cuaca')
ax2.set_ylabel('Rata-rata Jumlah Peminjaman')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)}'))
st.pyplot(fig2)

# Insight
st.subheader('Insight 1')
st.markdown("""
 Berdasarkan data, hari kerja (Working Day) memiliki rata-rata jumlah peminjaman yang lebih tinggi, dibandingkan dengan hari libur/akhir pekan (Weekend/Holiday). Puncak aktivitas kemungkinan terjadi pada jam sibuk, yakni pagi dan sore, menunjukkan bahwa banyak pengguna memanfaatkan sepeda sebagai  transportasi untuk bekerja atau sekolah.
""")

st.subheader('Rekomendasi Insight 1')
st.markdown("""
- Fokuskan distribusi armada di area permukiman dan pusat bisnis pada hari kerja, terutama di jam sibuk pagi dan sore.
- Terapkan rotasi armada pada siang hari (waktu off-peak) ke lokasi yang lebih membutuhkan, guna meningkatkan efisiensi penggunaan unit sepeda.
-  Hari libur/akhir pekan: distribusikan sepeda ke area rekreasi, taman, dan kawasan wisata karena tren peminjaman bergeser ke aktivitas santai.
- Jadwalkan perawatan/maintenance sepeda di waktu pagi atau malam saat jumlah peminjaman menurun, agar tidak mengganggu layanan operasional utama.
""")

st.subheader('Insight 2')
st.markdown("""
 Cuaca memiliki dampak yang signifikan terhadap tingkat peminjaman. Pada cuaca Clear (cerah), jumlah peminjaman melonjak tinggi. Sebaliknya, pada cuaca Light Snow/Rain (Hujan ringan/Salju/gerimis), jumlah peminjaman menurun drastis. Kondisi Mist/Cloudy (Berkabut/Berawan) masih relatif tinggi tapi menurun sedikit dibanding ketika cuaca cerah, menunjukkan bahwa Light Snow/Rain (Hujan ringan/Salju/gerimis) memiliki dampak penurunan yang paling tajam. Sedangkan ketika cuaca di kondisi paling buruk yaitu Heavy rain/Snow (Hujan Badai) hampir tidak ada orang yang meminjam sepeda
""")

st.subheader('Rekomendasi Insight 2')
st.markdown("""
- Luncurkan promosi khusus seperti diskon, bundling perjalanan, atau poin reward saat cuaca cerah atau prakiraan cuaca mendukung, untuk memaksimalkan pendapatan.
- Terapkan tarif insentif (diskon) saat kondisi cuaca kurang ideal (gerimis) untuk mendorong pengguna tetap menyewa dan menjaga pendapatan tetap stabil.
-  Gunakan data prakiraan cuaca harian untuk mengoptimalkan distribusi armada, serta siapkan strategi penyesuaian armada saat cuaca buruk (misalnya pengurangan unit aktif atau penyimpanan aman di shelter).
""")

# Kesimpulan
st.subheader('Conlusion')
st.markdown("""
- Meningkatkan efisiensi operasional melalui penjadwalan armada yang lebih cerdas.
- Meningkatkan kepuasan pelanggan dengan ketersediaan sepeda yang tepat waktu dan di lokasi strategis.
- Meningkatkan potensi pendapatan dengan strategi tarif dan promosi berbasis data cuaca dan waktu.
""")
