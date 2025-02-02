import asyncio
import paho.mqtt.client as mqtt
import random
from handlers import handle_message
from logger import log_info, log_error
from config import BROKER, PORT, TOPICS

client_id = f'publish-{random.randint(0, 1000)}'


async def main():
    client = mqtt.Client(
        client_id=client_id,
        clean_session=True
    )

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log_info("Connected to MQTT Broker!")
            for topic in TOPICS:
                client.subscribe((topic, 0))
        else:
            log_error(f"Failed to connect, return code {rc}")

    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        handle_message(msg.topic, payload, msg.qos)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log_info("Disconnected from MQTT Broker.")

if __name__ == "__main__":
    asyncio.run(main())