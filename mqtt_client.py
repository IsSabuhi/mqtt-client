import paho.mqtt.client as mqtt
import random
from handlers import handle_message_topic
from logger import log_info, log_error
from db import Session
import asyncio

client_id = f'publish-{random.randint(0, 1000)}'

class MqttClient:
    def __init__(self, broker, port, topics, message_queue):
        self.broker = broker
        self.port = port
        self.topics = topics
        self.message_queue = message_queue 
        self.client_id = client_id
        self.client = None
        self.session = Session()

    async def start(self):
        self.client = mqtt.Client(
            client_id=self.client_id,
            clean_session=True
        )

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                log_info("Connected to MQTT Broker!")
                for topic in self.topics:
                    client.subscribe(topic)
            else:
                log_error(f"Failed to connect, return code {rc}")
                asyncio.create_task(self.reconnect())

        def on_message(client, userdata, msg):
            payload = msg.payload.decode()
            topic = msg.topic
            qos = msg.qos

            message_data = handle_message_topic(topic, payload, qos)
            if message_data:
                log_info(f"Сообщение получено: Тема - {topic}, Payload - {payload}")
                self.message_queue.put((topic, payload, qos))

        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.connect(self.broker, self.port, keepalive=60)

        try:
            self.client.loop_start()
        except Exception as e:
            log_error(f"Error starting MQTT loop: {e}")
            await self.reconnect()

    async def stop(self):
        if self.client is not None:
            self.client.disconnect()
            await self.client.loop_stop()
            self.client = None

    async def reconnect(self):
        """Механизм для повторных попыток подключения к брокеру MQTT."""
        attempt = 0
        while attempt < 5:
            try:
                await self.start()
                log_info("Подключение к MQTT Broker успешно.")
                break
            except Exception as e:
                attempt += 1
                log_error(f"Попытка подключения не удалась ({attempt}): {e}")
                await asyncio.sleep(5) 
        else:
            log_error("Не удалось подключиться к MQTT брокеру после 5 попыток.")