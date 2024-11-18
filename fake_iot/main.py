import paho.mqtt.client as mqtt
import json
import random
import time

# Configurações do MQTT
BROKER = "167.88.33.242"  # Substitua pelo IP do seu servidor MQTT
PORT = 1883
MQTT_USER = "user1"
MQTT_PASSWORD = "@KKxbox1225"
TOPICS = ["iot-gerson-danilo/temperatura", "iot-gerson-danilo/humidade"]

# Configuração de dispositivos simulados
DEVICES = [
    {"id": "sensor1", "type": "temperatura", "unit": "°C", "location": "Sala 101"},
    {"id": "sensor2", "type": "humidade", "unit": "%", "location": "Laboratório 2"},
]

# Conexão ao broker MQTT
def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(BROKER, PORT, keepalive=120)  # Timeout aumentado para 2 minutos
    return client

# Função para gerar dados aleatórios
def generate_data(device):
    if device["type"] == "temperatura":
        value = round(random.uniform(18.0, 30.0), 1) 
    elif device["type"] == "humidade":
        value = round(random.uniform(30.0, 70.0), 1)
    else:
        value = None

    data = {
        "id": f"{device['id']}-{random.randint(1000, 9999)}",
        "timestamp": int(time.time()),
        "sensor": device["type"],
        "value": value,
        "unit": device["unit"],
        "location": device["location"],
        "status": "OK" if value is not None else "ERROR",
        "valid": True if value is not None else False,
    }
    return data

# Publicação de dados
def publish_data(client, device):
    topic = f"iot-gerson-danilo/{device['type']}"
    data = generate_data(device)
    message = json.dumps(data)
    client.publish(topic, message)
    print(f"Publicado no tópico {topic}: {message}")

# Loop principal
def simulate_devices():
    client = connect_mqtt()
    client.loop_start()

    try:
        while True:
            for device in DEVICES:
                publish_data(client, device)
                time.sleep(2) 
            time.sleep(5) 
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    simulate_devices()
