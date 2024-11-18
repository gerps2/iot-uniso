import paho.mqtt.client as mqtt
import sqlite3
import json
import os

# Configurações do MQTT
BROKER = "167.88.33.242"  # Substitua pelo IP público do seu servidor MQTT
PORT = 1883
MQTT_USER = "user1"
MQTT_PASSWORD = "@KKxbox1225"
TOPICS = [("iot-gerson-danilo/temperatura", 0), ("iot-gerson-danilo/humidade", 0)]

# Verificar se o arquivo do banco existe
if not os.path.exists("database.db"):
    print("O arquivo do banco de dados não foi encontrado!")
    exit(1)

# Função para salvar dados no SQLite
def save_to_db(sensor, data):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sensor_data (id, sensor, value, unit, timestamp, location, status, valid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"], sensor, data["value"], data["unit"],
            data["timestamp"], data["location"], data["status"], data["valid"]
        ))
        conn.commit()
        print(f"Dados salvos no banco de dados: {data}")
    except sqlite3.Error as e:
        print(f"Erro ao salvar no banco de dados: {e}")
    finally:
        conn.close()

# Callback para conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        for topic, qos in TOPICS:
            client.subscribe(topic)
            print(f"Inscrito no tópico: {topic}")
    else:
        print(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")

# Callback para mensagens
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        sensor = msg.topic.split("/")[-1]
        print(f"Mensagem recebida no tópico {msg.topic}: {payload}")
        save_to_db(sensor, payload)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

print("Conectando ao broker MQTT...")
try:
    client.connect(BROKER, PORT, 120)
    print("Conexão com o broker MQTT bem-sucedida.")
except Exception as e:
    print(f"Erro ao conectar ao broker MQTT: {e}")
    exit(1)

# Loop infinito
print("Aguardando mensagens...")
client.loop_forever()
