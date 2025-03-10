# **DASHBOARD ANALISIS KUALITAS UDARA** ✨

## **Setup Environment - Anaconda**
1. Buat environment baru dengan Anaconda:
    ```bash
    conda create --name air-quality python=3.9
    conda activate air-quality
    pip install numpy pandas matplotlib seaborn streamlit babel pathlib
    ```

## **Setup Environment - Shell/Terminal**
1. Buat environment baru dengan venv (untuk Shell/Terminal):
    ```bash
    python -m venv air-quality
    source air-quality/bin/activate  # For Linux/Mac
    .\air-quality\Scripts\activate   # For Windows
    pip install numpy pandas matplotlib seaborn streamlit babel pathlib
    ```

## **Run Streamlit App**
Setelah environment diaktifkan, jalankan aplikasi Streamlit:
    ```bash
    python -m streamlit run dashboard/dashboard.py
    ```

## **Fitur Dashboard**
- Tren Polutan Harian: Visualisasi PM2.5, PM10, dan NO2
- Analisis per Stasiun: Perbandingan 12 stasiun pemantauan
- Analisis Cuaca: Hubungan polutan dengan parameter cuaca
- Pola Harian: Analisis 24 jam dan perbandingan siang-malam
- Korelasi: Hubungan antar polutan dan faktor cuaca
