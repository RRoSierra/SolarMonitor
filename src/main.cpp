#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

// --- Configuración de Red ---
const char* ssid = "MOVISTAR-WIFI6-F020";
const char* password = "A8q9EoQr2dLSfuNoEdg4";
const char* mqtt_server = "broker.hivemq.com"; // Broker público gratuito

// --- Configuración de Hardware ---
const int ldrPin = 34; // Pin ADC (GPIO34)
const float factor_conversion = 5.5 / 3.3; // Para escalar de 3.3V a 5.5V

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.begin(115200);
  Serial.print("\nConectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado - IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conexión MQTT...");
    // ID de cliente único para evitar desconexiones en la USM
    String clientId = "ESP32LDR-USM-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("conectado");
    } else {
      Serial.print("falló, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

void setup() {
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  analogSetAttenuation(ADC_11db); // Permite leer hasta 3.3V
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Leer ADC (0 a 4095)
  int rawADC = analogRead(ldrPin);
  
  // Convertir a voltaje real (3.3V)
  // El ADC del ESP32 no es 100% lineal, esto es una aproximación estándar
  float volt33 = (rawADC * 3.3) / 4095.0;
  
  // Calcular aproximado a 5.5V
  float volt55 = volt33 * factor_conversion;

  // Crear mensaje JSON
  String payload = "{\"v33\":" + String(volt33, 2) + ",\"v55\":" + String(volt55, 2) + "}";
  
  Serial.print("Enviando: ");
  Serial.println(payload);
  
  // Publicar en un tópico único (Cámbialo si quieres privacidad)
  client.publish("usm/casa_central/ldr_sensor", payload.c_str());

  delay(10000); // Envía datos cada 10 segundos
}