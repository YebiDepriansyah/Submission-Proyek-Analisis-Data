Dashboard Analisis Kualitas Udara ✨

Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

Setup Environment - Shell/Terminal
python -m venv main-ds
source main-ds/bin/activate # For Linux/Mac
.\main-ds\Scripts\activate # For Windows
pip install -r requirements.txt

Run Streamlit App
cd dashboard
streamlit run dashboard.py
