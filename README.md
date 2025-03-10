# **DASHBOARD ANALISIS KUALITAS UDARA** ✨

## **Setup Environment - Anaconda**
1. Buat environment baru dengan Anaconda:
    ```bash
    conda create --name main-ds python=3.9
    conda activate main-ds
    pip install -r requirements.txt
    ```

## **Setup Environment - Shell/Terminal**
1. Buat environment baru dengan venv (untuk Shell/Terminal):
    ```bash
    python -m venv main-ds
    source main-ds/bin/activate  # For Linux/Mac
    .\main-ds\Scripts\activate   # For Windows
    pip install -r requirements.txt
    ```

## **Run Streamlit App**
Setelah environment diaktifkan, jalankan aplikasi Streamlit:
    ```bash
    cd dashboard
    streamlit run dashboard.py
    ```
