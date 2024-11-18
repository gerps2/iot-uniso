import network
import time
from machine import Pin
import dht
import ujson
import ubinascii
import machine
from umqtt.simple import MQTTClient

MQTT_CLIENT_ID = "iot-sensor-humidade"
BROKER = "167.88.33.242"
PORT = 1883
MQTT_USER = "user1"
MQTT_PASSWORD = "@KKxbox1225"
MQTT_TOPIC = "iot-gerson-danilo/humidade"

sensor = dht.DHT22(Pin(15))

print("Conectando ao WiFi...", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("\nConectado ao WiFi!")

print("Conectando ao broker MQTT...", end="")
client = MQTTClient(MQTT_CLIENT_ID, BROKER, PORT, MQTT_USER, MQTT_PASSWORD)
client.connect()
print("Conectado ao broker MQTT!")

def generate_id():
    return ubinascii.hexlify(machine.unique_id()).decode() + "-" + str(time.ticks_ms())

while True:
    try:
        sensor.measure()
        humidity = sensor.humidity()
        data = {
            "id": generate_id(),
            "timestamp": time.time(),
            "sensor": "humidade",
            "value": humidity,
            "unit": "%",
            "location": "Laboratório 2",
            "status": "OK",
            "valid": True if 0 <= humidity <= 100 else False,
        }
        message = ujson.dumps(data)
        client.publish(MQTT_TOPIC, message)
        print(f"Publicado no tópico {MQTT_TOPIC}: {message}")
        time.sleep(5)
    except Exception as e:
        print("Erro ao publicar dados:", e)
        time.sleep(5)
