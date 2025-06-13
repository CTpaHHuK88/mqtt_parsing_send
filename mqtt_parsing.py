# Работаем с библиотекой, получаем данные из MQTT pip install paho-mqtt
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from config import ConfigSub
import os

FILE_PATH = 'meteo.json'

if os.path.exists(FILE_PATH):
    pass
else:
    with open(FILE_PATH, 'w') as f:
        pass  


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))  # Декодируем байты и парсим JSON
    
        #Сохраняем в JSON
        with open('meteo.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except AttributeError:
        print("Message payload is empty or invalid")

client = mqtt.Client()
client.on_message = on_message
# Устанавливаем логин и пароль
#client.username_pw_set(username="ваш_логин", password="ваш_пароль")
# Подключаемся к брокеру
client.connect(ConfigSub.MQTT_BROKER, ConfigSub.MQTT_PORT)
client.subscribe(ConfigSub.MQTT_TOPIC)
# Запускаем цикл обработки сообщений
client.loop_forever()