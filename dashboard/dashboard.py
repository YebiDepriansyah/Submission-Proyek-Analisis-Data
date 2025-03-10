import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from pathlib import Path
import numpy as np
sns.set(style='dark')

# Load dataset
@st.cache_data
def load_data():
    current_dir = Path(__file__).parent
    file_path = current_dir / "all_data.csv"
    df = pd.read_csv(file_path)
    
    # Membuat kolom datetime dari year, month, day, hour
    df['date'] = pd.to_datetime(dict(year=df['year'], 
                                   month=df['month'], 
                                   day=df['day'], 
                                   hour=df['hour']))
    return df

df = load_data()

# Helper function: Agregasi rata-rata polusi harian
def create_daily_pollution_df(df):
    daily_pollution_df = df.resample('D', on='date').agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "NO2": "mean"
    }).reset_index()
    return daily_pollution_df

# Helper function: Konsentrasi polutan berdasarkan stasiun
def create_station_pollution_df(df):
    station_pollution_df = df.groupby("No")[["PM2.5", "PM10", "NO2"]].agg({
        'PM2.5': ['mean', 'min', 'max'],
        'PM10': ['mean', 'min', 'max'],
        'NO2': ['mean', 'min', 'max']
    }).reset_index()
    
    # Merapikan nama kolom
    station_pollution_df.columns = ['station', 
                                  'PM2.5_mean', 'PM2.5_min', 'PM2.5_max',
                                  'PM10_mean', 'PM10_min', 'PM10_max',
                                  'NO2_mean', 'NO2_min', 'NO2_max']
    return station_pollution_df

# Helper function: Analisis bulanan
def create_monthly_pollution_df(df):
    df['month_year'] = df['date'].dt.strftime('%Y-%m')
    monthly_pollution = df.groupby('month_year').agg({
        'PM2.5': ['mean', 'min', 'max'],
        'PM10': ['mean', 'min', 'max'],
        'NO2': ['mean', 'min', 'max']
    }).reset_index()
    
    monthly_pollution.columns = ['month_year', 
                               'PM2.5_mean', 'PM2.5_min', 'PM2.5_max',
                               'PM10_mean', 'PM10_min', 'PM10_max',
                               'NO2_mean', 'NO2_min', 'NO2_max']
    return monthly_pollution

# Helper function: Variasi polutan berdasarkan waktu (siang vs malam)
def create_daynight_pollution_df(df):
    df["hour"] = pd.to_datetime(df["date"]).dt.hour
    df["time_of_day"] = df["hour"].apply(lambda x: "Day" if 6 <= x < 18 else "Night")
    daynight_pollution_df = df.groupby("time_of_day")[["PM2.5", "PM10", "NO2"]].mean().reset_index()
    return daynight_pollution_df

# Helper function: Korelasi polutan & cuaca
def create_weather_correlation_df(df):
    weather_corr_df = df[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", 
                         "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]].corr()
    return weather_corr_df

# Menentukan rentang tanggal minimum & maksimum dari dataset
min_date = df["date"].min()
max_date = df["date"].max()

# Sidebar untuk filter
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")  # Logo (bisa diganti)
    
    # Widget filter rentang tanggal
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter dataset berdasarkan tanggal yang dipilih
main_df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]

# Membuat DataFrame baru berdasarkan filter
daily_pollution_df = create_daily_pollution_df(main_df)
station_pollution_df = create_station_pollution_df(main_df)
daynight_pollution_df = create_daynight_pollution_df(main_df)
weather_correlation_df = create_weather_correlation_df(main_df)

# Membuat layout dashboard
st.header('Dashboard Analisis Kualitas Udara 🌍')

# Tab untuk berbagai visualisasi
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    'Tren Polutan Harian', 
    'Analisis per Stasiun', 
    'Analisis Cuaca', 
    'Pola Harian', 
    'Korelasi'
])

# Tab 1: Tren Polutan Harian
with tab1:
    st.subheader('Tren Polutan Harian')
    
    # Line plot untuk tren harian
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_pollution_df['date'], daily_pollution_df['PM2.5'], label='PM2.5')
    ax.plot(daily_pollution_df['date'], daily_pollution_df['PM10'], label='PM10')
    ax.plot(daily_pollution_df['date'], daily_pollution_df['NO2'], label='NO2')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Konsentrasi (µg/m³)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Menambahkan statistik ringkas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rata-rata PM2.5", f"{main_df['PM2.5'].mean():.2f} µg/m³")
    with col2:
        st.metric("Rata-rata PM10", f"{main_df['PM10'].mean():.2f} µg/m³")
    with col3:
        st.metric("Rata-rata NO2", f"{main_df['NO2'].mean():.2f} µg/m³")

# Tab 2: Analisis per Stasiun
with tab2:
    st.subheader('Analisis Kualitas Udara per Stasiun')
    
    # Hitung statistik per stasiun
    station_stats = main_df.groupby('station')[['PM2.5', 'PM10', 'NO2']].agg(['mean', 'min', 'max'])
    
    # Bar plot untuk perbandingan stasiun
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(station_stats.index))
    width = 0.25
    
    ax.bar(x - width, station_stats['PM2.5']['mean'], width, label='PM2.5')
    ax.bar(x, station_stats['PM10']['mean'], width, label='PM10')
    ax.bar(x + width, station_stats['NO2']['mean'], width, label='NO2')
    
    ax.set_ylabel('Konsentrasi Rata-rata (µg/m³)')
    ax.set_xlabel('Stasiun')
    ax.set_xticks(x)
    ax.set_xticklabels(station_stats.index, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Tampilkan stasiun dengan polusi tertinggi
    st.write("### Stasiun dengan Tingkat Polusi Tertinggi")
    col1, col2, col3 = st.columns(3)
    with col1:
        max_pm25 = station_stats['PM2.5']['mean'].idxmax()
        st.metric("PM2.5 Tertinggi", 
                 f"{max_pm25}\n({station_stats['PM2.5']['mean'].max():.2f} µg/m³)")
    with col2:
        max_pm10 = station_stats['PM10']['mean'].idxmax()
        st.metric("PM10 Tertinggi", 
                 f"{max_pm10}\n({station_stats['PM10']['mean'].max():.2f} µg/m³)")
    with col3:
        max_no2 = station_stats['NO2']['mean'].idxmax()
        st.metric("NO2 Tertinggi", 
                 f"{max_no2}\n({station_stats['NO2']['mean'].max():.2f} µg/m³)")

    # Tampilkan stasiun dengan polusi terendah
    st.write("### Stasiun dengan Tingkat Polusi Terendah")
    col1, col2, col3 = st.columns(3)
    with col1:
        min_pm25 = station_stats['PM2.5']['mean'].idxmin()
        st.metric("PM2.5 Terendah", 
                 f"{min_pm25}\n({station_stats['PM2.5']['mean'].min():.2f} µg/m³)")
    with col2:
        min_pm10 = station_stats['PM10']['mean'].idxmin()
        st.metric("PM10 Terendah", 
                 f"{min_pm10}\n({station_stats['PM10']['mean'].min():.2f} µg/m³)")
    with col3:
        min_no2 = station_stats['NO2']['mean'].idxmin()
        st.metric("NO2 Terendah", 
                 f"{min_no2}\n({station_stats['NO2']['mean'].min():.2f} µg/m³)")

    # Tambahkan ringkasan analisis
    st.write("### Ringkasan Analisis")
    st.write(f"""
    - Stasiun {max_pm25} memiliki tingkat PM2.5 tertinggi, sementara {min_pm25} memiliki tingkat terendah
    - Stasiun {max_pm10} memiliki tingkat PM10 tertinggi, sementara {min_pm10} memiliki tingkat terendah
    - Stasiun {max_no2} memiliki tingkat NO2 tertinggi, sementara {min_no2} memiliki tingkat terendah
    """)

# Tab 3: Analisis Cuaca
with tab3:
    st.subheader('Analisis Hubungan Polutan dengan Cuaca')
    
    # Scatter plot untuk hubungan polutan dengan suhu
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Hubungan Polutan dengan Suhu")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(main_df['TEMP'], main_df['PM2.5'], alpha=0.5, label='PM2.5')
        ax.scatter(main_df['TEMP'], main_df['PM10'], alpha=0.5, label='PM10')
        ax.set_xlabel('Temperatur (°C)')
        ax.set_ylabel('Konsentrasi (µg/m³)')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.write("### Hubungan Polutan dengan Curah Hujan")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(main_df['RAIN'], main_df['PM2.5'], alpha=0.5, label='PM2.5')
        ax.scatter(main_df['RAIN'], main_df['PM10'], alpha=0.5, label='PM10')
        ax.set_xlabel('Curah Hujan (mm)')
        ax.set_ylabel('Konsentrasi (µg/m³)')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Statistik cuaca
    st.write("### Statistik Cuaca")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rata-rata Suhu", f"{main_df['TEMP'].mean():.1f}°C")
    with col2:
        st.metric("Rata-rata Kelembaban", f"{main_df['DEWP'].mean():.1f}°C")
    with col3:
        st.metric("Rata-rata Tekanan", f"{main_df['PRES'].mean():.1f} hPa")
    with col4:
        st.metric("Rata-rata Kecepatan Angin", f"{main_df['WSPM'].mean():.1f} m/s")

# Tab 4: Pola Harian
with tab4:
    st.subheader('Pola Harian Polutan')
    
    # Analisis per jam
    hourly_stats = main_df.groupby(main_df['date'].dt.hour)[['PM2.5', 'PM10', 'NO2']].mean()
    
    # Line plot untuk pola 24 jam
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hourly_stats.index, hourly_stats['PM2.5'], marker='o', label='PM2.5')
    ax.plot(hourly_stats.index, hourly_stats['PM10'], marker='o', label='PM10')
    ax.plot(hourly_stats.index, hourly_stats['NO2'], marker='o', label='NO2')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Konsentrasi Rata-rata (µg/m³)')
    ax.set_xticks(range(0, 24))
    ax.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Perbandingan siang vs malam
    st.write("### Perbandingan Siang vs Malam")
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(daynight_pollution_df['time_of_day']))
    width = 0.25
    
    ax.bar([i - width for i in x], daynight_pollution_df['PM2.5'], width, label='PM2.5')
    ax.bar(x, daynight_pollution_df['PM10'], width, label='PM10')
    ax.bar([i + width for i in x], daynight_pollution_df['NO2'], width, label='NO2')
    
    ax.set_ylabel('Konsentrasi Rata-rata (µg/m³)')
    ax.set_xticks(x)
    ax.set_xticklabels(daynight_pollution_df['time_of_day'])
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Tab 5: Korelasi
with tab5:
    st.subheader('Analisis Korelasi antar Variabel')
    
    # Heatmap korelasi
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(weather_correlation_df, 
                annot=True, 
                cmap='coolwarm', 
                center=0,
                fmt='.2f',
                ax=ax)
    plt.title('Korelasi antara Polutan dan Faktor Cuaca')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Interpretasi korelasi
    st.write("### Interpretasi Korelasi Utama")
    
    # Mencari korelasi tertinggi
    corr_values = weather_correlation_df.unstack()
    corr_values = corr_values[corr_values != 1.0]  # Menghilangkan korelasi dengan diri sendiri
    top_corr = corr_values.abs().sort_values(ascending=False)[:5]
    
    for idx, corr in zip(top_corr.index, top_corr.values):
        var1, var2 = idx
        st.write(f"- Korelasi antara {var1} dan {var2}: {corr:.3f}")

