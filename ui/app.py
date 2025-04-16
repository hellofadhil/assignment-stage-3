import streamlit as st
from utils.api import fetch_drone_data
from maps.map_view import render_map
from tables.history_table import show_history

st.set_page_config(page_title="Drone Monitor", layout="wide", page_icon="🚁")

# Tambahkan header yang lebih menarik
st.markdown("""
# 🚁 **Drone Data Visualization** 
Pantau data lokasi drone dengan visualisasi peta dan riwayat data.
""", unsafe_allow_html=True)

# Fetch data sekali untuk semua
data = fetch_drone_data()

# Bagi layout menjadi dua kolom, dengan margin dan padding untuk jarak lebih
col1, col2 = st.columns([2, 1])

# Kolom pertama - Peta
with col1:
    st.markdown("<h2 style='text-align: center;'>📍 Drone Map</h2>", unsafe_allow_html=True)
    render_map()

# Kolom kedua - Tabel Riwayat
with col2:
    st.markdown("<h2 style='text-align: center;'>📋 Data Riwayat</h2>", unsafe_allow_html=True)
    if data:
        st.markdown("""
        Berikut adalah riwayat data drone berdasarkan lokasi dan jumlah orang yang terdeteksi.
        """, unsafe_allow_html=True)
    show_history(data)

# Tambahkan footer dengan informasi aplikasi
st.markdown("""
---
Made with ❤️ by Team Dile Comunity
""", unsafe_allow_html=True)
