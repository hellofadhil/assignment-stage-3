from flask import Flask, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://fadhil:GGm237otCVsDNSqd@mydatabase.cwke5.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=mydatabase"
mongo = PyMongo(app)

# MQTT on_connect
def on_connect(client, userdata, flags, rc):
    print("[Flask] Terhubung ke MQTT")
    client.subscribe("fadhil123/gps/koordinat")

# MQTT on_message
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        print("[Flask] Data GPS diterima:", data)

        # Tambahkan timestamp
        data["timestamp"] = datetime.utcnow()

        # Ambil data terakhir dari koleksi
        last_data = mongo.db.drone.find_one(sort=[("timestamp", -1)])

        # Bandingkan dengan data terakhir
        is_different = (
            last_data is None or
            last_data.get("jumlah_orang") != data.get("jumlah_orang") or
            last_data.get("latitude") != data.get("latitude") or
            last_data.get("longitude") != data.get("longitude")
        )

        if is_different:
            # Simpan ke MongoDB
            mongo.db.drone.insert_one(data)
            print("[Flask] Simpan:", data)
        else:
            print("[Flask] Data sama, tidak disimpan.")

    except Exception as e:
        print("[Flask] Gagal simpan:", e)

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("broker.emqx.io", 1883, 60)
mqtt_client.loop_start()

# Route lihat data
@app.route("/drone/data")
def lihat_data():
    try:
        data = list(mongo.db.drone.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Default route
@app.route("/")
def index():
    return "🚀 Backend Drone Deteksi Aktif!"

# Jalankan Flask
if __name__ == "__main__":
    print("[MongoDB] Koneksi berhasil!")
    app.run(debug=True)
