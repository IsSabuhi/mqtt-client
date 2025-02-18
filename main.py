import asyncio
import random
from config import BROKER, PORT, TOPICS
from mqtt_client import MqttClient
import tkinter as tk
from tkinter import ttk
from tabs.mqtt_tab import MQTT_TAB
from tabs.db_tab import DB_TAB
from tabs.queue_tab import QueueTab
from handlers import parse_and_save_data
from logger import log_info, log_error
import threading
import queue
from db import Session

client_id = f'publish-{random.randint(0, 1000)}'
message_queue = queue.Queue()

def process_queue():
    local_session = Session()
    while True:
        try:
            topic, payload, qos = message_queue.get(timeout=1) 
            parse_and_save_data(local_session, topic, payload, qos)
        except queue.Empty:
            continue

queue_thread = threading.Thread(target=process_queue, daemon=True)
queue_thread.start()

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Приложение на Tkinter")
        self.geometry("600x450")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.tab_main = MQTT_TAB(self.notebook)
        self.notebook.add(self.tab_main.frame, text='mqtt')
        
        self.db_tab = DB_TAB(self.notebook)
        self.notebook.add(self.db_tab.frame, text='postgres')
        
        self.queue_tab = QueueTab(self.notebook, message_queue)
        self.notebook.add(self.queue_tab.frame, text='queue')

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mqtt_client = MqttClient(BROKER, PORT, TOPICS, message_queue)
        self.loop = asyncio.new_event_loop()
        self.local_session = Session()
        self.thread = threading.Thread(target=self.run_mqtt_client, args=(self.mqtt_client,))
        self.thread.daemon = True
        self.thread.start()
        
        self.check_queue()
        
    def run_mqtt_client(self, mqtt_client):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(mqtt_client.start())
            
    def check_queue(self):
        try:
            while True:
                topic, payload, qos = message_queue.get_nowait()
                
                log_info(f"Получено сообщение от темы {topic}, QoS: {qos}")
                
                message_data = parse_and_save_data(self.local_session, topic, payload, qos)
                print('!message_date', message_data)
                self.update_tab_main(message_data)
                
                
        except queue.Empty:
            log_info("Очередь сообщений пуста, повторная проверка...")
        except Exception as e:
            log_error(f"Ошибка при обработке очереди: {str(e)}")
        
        self.after(50000, self.check_queue)

    def on_closing(self):
        self.local_session.close()
        self.destroy()
        

    def run(self):
        self.mainloop()

    def close(self):
        self.on_closing()

    def update_tab_main(self, data):
        print('data',data)
        self.tab_main.update_received_data(data)
        pass
        
if __name__ == "__main__":
    app = MainApplication()
    app.run()