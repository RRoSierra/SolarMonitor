# 🌞 SolarMonitor

Monitor de voltaje solar usando ESP32, MQTT y Python.

## 📁 Estructura

```
├── src/main.cpp          # Código del ESP32
├── platformio.ini        # Configuración PlatformIO
├── test/
│   ├── test.py           # Receptor MQTT (guarda datos)
│   └── visualizar.py     # Genera gráficos
└── requirements.txt      # Dependencias Python
```

## 🚀 Instalación

### ESP32 (PlatformIO)
1. Abrir el proyecto en VS Code con PlatformIO
2. Modificar WiFi en `src/main.cpp`:
   ```cpp
   const char* ssid = "TU_WIFI";
   const char* password = "TU_PASSWORD";
   ```
3. Compilar y subir al ESP32

### Python (Receptor de datos)
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📡 Uso

1. **Recopilar datos** (dejar corriendo):
   ```bash
   python test/test.py
   ```

2. **Visualizar datos** (después de recopilar):
   ```bash
   python test/visualizar.py
   ```

## ⚙️ Configuración MQTT

| Variable | Valor |
|----------|-------|
| Broker | broker.hivemq.com |
| Puerto | 1883 |
| Topic | usm/casa_central/ldr_sensor |

## 📊 Datos

Los datos se guardan en `test/historico_voltaje.csv` con el formato:
- timestamp, hora, fecha, v33, v55
