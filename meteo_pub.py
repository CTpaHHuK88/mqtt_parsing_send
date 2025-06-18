import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
from check_host import CheckHost
from config import ConfigPub

# Кастомный JSON-encoder для обработки datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def sendMessage():
    #------
    #Проверяем доступность хоста
    host = CheckHost(ConfigPub.CH_HOST) 
    status_host = host.check()

    with open('meteo.json', 'r') as file:
        data = json.load(file) # Сообщение   
        # Проверяем тип данных  и формируем двнные для добавления
    if isinstance(data, list):
        new_item = {
            "datestamp": datetime.now().strftime("%d.%m.%Y"),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "status_host": status_host
        }
        data.append(new_item)
    elif isinstance(data, dict):
        data["new_item"] = {
            "datestamp": datetime.now().strftime("%d.%m.%Y"),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "status_host": status_host
        }
    MQTT_MESSAGE = json.dumps(data, cls=DateTimeEncoder)  # Преобразуем в строку
    return MQTT_MESSAGE
#------

# Callback при успешном подключении к брокеру
def on_connect(client, userdata, flags, rc):
    #Подключаемся
    if rc == 0:
        # Публикуем сообщение после подключения        
        client.publish(ConfigPub.MQTT_TOPIC, sendMessage())

# Создаем клиента MQTT
client = mqtt.Client()
# Назначаем callback для подключения
client.on_connect = on_connect

while True:
    client.connect(ConfigPub.MQTT_BROKER, ConfigPub.MQTT_PORT, 60)
    # Запускаем сетевой цикл (обработка сообщений)
    client.loop_start()
    sendMessage()
    # Ждем 2 секунды, чтобы сообщение успело отправиться
    time.sleep(2)

    # Отключаемся
    client.disconnect()
    client.loop_stop()
    print("🔴 Отключено от брокера.")
    time.sleep(5)