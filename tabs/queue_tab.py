import tkinter as tk
from tkinter import ttk

class QueueTab:
    def __init__(self, parent, queue_data):
        self.frame = tk.Frame(parent)
        self.queue_data = queue_data

        label = ttk.Label(self.frame, text="Данные в очереди")
        label.pack(pady=5)

        self.queue_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.queue_listbox.pack(pady=10)

        update_button = tk.Button(self.frame, text="Обновить очередь", command=self.update_queue_display)
        update_button.pack(pady=5)

        self.update_queue_display() 

    def update_queue_display(self):
        """Обновление отображения данных в очереди"""
        self.queue_listbox.delete(0, tk.END)  


        queue_items = list(self.queue_data.queue) 
        for item in queue_items:
            self.queue_listbox.insert(tk.END, str(item)) 
    def add_to_queue(self, data):
        """Добавление данных в очередь"""
        self.queue_data.put(data)
        self.update_queue_display() 