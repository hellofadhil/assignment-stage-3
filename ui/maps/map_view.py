import folium
from streamlit_folium import st_folium
from utils.api import fetch_drone_data

def render_map():
    data = fetch_drone_data()
    default_location = [-6.2, 106.816666]
    m = folium.Map(location=default_location, zoom_start=12, control_scale=True)

    if data:
        for i, item in enumerate(data):
            lat = item.get("latitude")
            lon = item.get("longitude")
            jumlah = item.get("jumlah_orang")
            waktu = item.get("timestamp", {}).get("$date", "")

            # 📍 Menambahkan Marker dengan ikon kustom dan warna yang menarik
            folium.Marker(
                location=[lat, lon],
                tooltip="Klik untuk melihat detail",
                popup=f"""
                <b>Jumlah Orang:</b> {jumlah}<br>
                <b>Lokasi:</b> ({lat}, {lon})<br>
                <b>Waktu:</b> {waktu}
                """,
                icon=folium.Icon(
                    color="darkblue",  # Mengganti warna ikon
                    icon="cloud",      # Mengganti ikon
                    prefix="fa"        # Menggunakan font-awesome untuk ikon
                )
            ).add_to(m)

            # 🔵 CircleMarker untuk visualisasi jumlah orang dengan transparansi
            folium.CircleMarker(
                location=[lat, lon],
                radius=min(jumlah * 2, 30),  # Membatasi ukuran maksimum untuk radius
                color="cyan",
                fill=True,
                fill_color="cyan",
                fill_opacity=0.6,
                popup=f"{jumlah} orang",
                weight=2  # Menambahkan garis tepi lebih tebal
            ).add_to(m)

            # Menambahkan gradient warna untuk representasi jumlah orang yang lebih visual
            folium.CircleMarker(
                location=[lat, lon],
                radius=min(jumlah * 2, 30),  # Membatasi radius maksimum
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.5,
                popup=f"Jumlah Orang: {jumlah}",
            ).add_to(m)

        # Fokuskan peta pada data terakhir atau default jika tidak ada data
        m.location = [data[-1]["latitude"], data[-1]["longitude"]] if data else default_location

    else:
        folium.Marker(
            default_location, 
            tooltip="Tidak ada data",
            icon=folium.Icon(color="gray", icon="ban", prefix="fa")  # Menambahkan ikon untuk "no data"
        ).add_to(m)

    st_folium(m, width=700, height=500)
