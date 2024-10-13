import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mendefinisikan fungsi
def create_time_total(df):
    time_total_df = df.groupby('time')['cnt'].mean().reset_index()
    return time_total_df

def create_year_perform(df):
    year_perform_df = df.groupby('mnth')['cnt'].sum().reset_index()
    return year_perform_df

# Membaca data utama
main_df = pd.read_csv("dashboard/main_data.csv")

# Mengurutkan dan mengatur format tanggal
datetime_columns = ["dteday"]
main_df.sort_values(by="dteday", inplace=True)
main_df.reset_index(inplace=True)

for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])

min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.shutterstock.com/image-vector/bike-icon-vector-logo-template-600nw-1388480312.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan rentang tanggal yang dipilih
filtered_df = main_df[(main_df["dteday"] >= pd.to_datetime(start_date)) & (main_df["dteday"] <= pd.to_datetime(end_date))]

# Menyiapkan berbagai dataframe dari data yang sudah difilter
time_total_df = create_time_total(filtered_df)
year_perform_df = create_year_perform(filtered_df)

# Nama perusahaan
st.header("Abdee's Bike Sharing")

# Pelanggan berdasarkan waktu
st.subheader("Rata-rata Pelanggan Berdasarkan Waktu")

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(x='time', y='cnt', data=time_total_df)
plt.title('Jumlah Pelanggan dalam Pembagian Waktu')
plt.xlabel('Rentang Waktu')
plt.ylabel('Jumlah Pelanggan')

st.pyplot(fig)

# Performa pelanggan dalam satu tahun
st.subheader("Performa Pelanggan dalam Setahun (2011-2012)")

fig, ax = plt.subplots(figsize=(20, 10))
sns.lineplot(x='mnth', y='cnt', data=year_perform_df)
plt.title('Performa Pelanggan Satu Tahun Terakhir')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pelanggan')
st.pyplot(fig)
