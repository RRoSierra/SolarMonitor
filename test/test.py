import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Obtener directorio del script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuraciones
TOPIC = "usm/casa_central/ldr_sensor"
BROKER = "broker.hivemq.com"
FILE_NAME = os.path.join(SCRIPT_DIR, "historico_voltaje.csv")

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Conectado al broker MQTT correctamente!")
        client.subscribe(TOPIC)
        print(f"📡 Suscrito al topic: {TOPIC}")
        print(f"💾 Los datos se guardarán en: {FILE_NAME}")
        print("-" * 50)
        print("Esperando datos del ESP32... (Ctrl+C para salir)")
    else:
        print(f"❌ Error de conexión. Código: {rc}")

def on_disconnect(client, userdata, rc, properties=None, reason=None):
    print(f"⚠️  Desconectado del broker (código: {rc})")

def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        now = datetime.now()
        
        # Estructura del dato
        new_data = {
            "timestamp": now,
            "hora": now.strftime("%H:%M:%S"),
            "fecha": now.strftime("%Y-%m-%d"),
            "v33": payload["v33"],
            "v55": payload["v55"]
        }
        
        # Guardar en CSV inmediatamente para no perder datos por cortes
        df = pd.DataFrame([new_data])
        df.to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False)
        
        print(f"[{new_data['hora']}] V_Real: {payload['v33']}V | V_Equiv: {payload['v55']}V")
        
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

# Configurar Cliente MQTT (API v2)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print(f"🔌 Conectando a {BROKER}:1883...")
client.connect(BROKER, 1883)
client.loop_forever()