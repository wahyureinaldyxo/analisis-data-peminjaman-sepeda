import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')
#D:\Bike-sharing-dataset\day.csv

# Preprocessing
day_df['workingday_label'] = day_df['workingday'].map({0: 'Weekend/Holiday', 1: 'Working Day'})
day_df['weathersit_label'] = day_df['weathersit'].map({1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'})


# Streamlit layout
st.title('Bike Sharing Exploratory Data Analysis 🚲')
st.write('Analisis peminjaman sepeda berdasarkan waktu, cuaca, dan hari')

# Show dataset preview
st.subheader('Preview Dataset')
st.dataframe(day_df.head())

# 1. Rata-rata peminjaman berdasarkan Workingday
st.subheader('Rata-rata Peminjaman Berdasarkan Workingday')
fig1, ax1 = plt.subplots()
sns.barplot(x='workingday_label', y='cnt', data=day_df, ci=None, ax=ax1)
ax1.set_xlabel('Tipe Hari')
ax1.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig1)

# 2. Rata-rata peminjaman berdasarkan Cuaca
st.subheader('Rata-rata Peminjaman Berdasarkan Cuaca')
fig2, ax2 = plt.subplots()
sns.barplot(x='weathersit_label', y='cnt', data=day_df, ci=None, ax=ax2)
ax2.set_xlabel('Tipe Cuaca')
ax2.set_ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot(fig2)

# Insight box
st.subheader('Insight Utama 🧐')
st.markdown("""
- **Working Day** cenderung memiliki peminjaman lebih banyak dibandingkan weekend/holiday.
- **Cuaca cerah (Clear)** berkontribusi pada jumlah peminjaman tertinggi.""")

