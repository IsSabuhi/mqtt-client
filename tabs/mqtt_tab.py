import tkinter as tk
from tkinter import ttk

class MQTT_TAB:
    def __init__(self, parent, received_data_callback=None):
        self.frame = tk.Frame(parent)
        self.received_data_callback = received_data_callback

        # Таблица для данных с TOPIC_1 (TK)
        self.tk_data_label = ttk.Label(self.frame, text="Данные с TOPIC_1 (TK):")
        self.tk_data_label.pack(pady=5)

        self.tk_tree_frame = tk.Frame(self.frame)
        self.tk_tree_frame.pack(pady=5)

        self.tk_tree = ttk.Treeview(
            self.tk_tree_frame,
            columns=("Name", "Value", "Delta", "Full"),
            show="headings"
        )
        
        self.tk_tree.heading("Name", text="Name")
        self.tk_tree.heading("Value", text="Value")
        self.tk_tree.heading("Delta", text="Delta")
        self.tk_tree.heading("Full", text="Full")
        
        self.tk_tree.column("Name", width=100)
        self.tk_tree.column("Value", width=100)
        self.tk_tree.column("Delta", width=100)
        self.tk_tree.column("Full", width=100)
        
        # Добавим полосу прокрутки
        self.scrollbar = ttk.Scrollbar(self.tk_tree_frame, orient="vertical", command=self.tk_tree.yview)
        self.tk_tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.tk_tree.pack(pady=5)

        # Таблица для данных с TOPIC_2 (INC)
        self.inc_data_label = ttk.Label(self.frame, text="Данные с TOPIC_2 (INC):")
        self.inc_data_label.pack(pady=5)

        self.inc_tree_frame = tk.Frame(self.frame)
        self.inc_tree_frame.pack(pady=5)

        self.inc_tree = ttk.Treeview(
            self.inc_tree_frame,
            columns=("X", "Y", "Z"),
            show="headings"
        )
        
        self.inc_tree.heading("X", text="X")
        self.inc_tree.heading("Y", text="Y")
        self.inc_tree.heading("Z", text="Z")
        
        self.inc_tree.column("X", width=100)
        self.inc_tree.column("Y", width=100)
        self.inc_tree.column("Z", width=100)

        # Добавим полосу прокрутки
        self.inc_scrollbar = ttk.Scrollbar(self.inc_tree_frame, orient="vertical", command=self.inc_tree.yview)
        self.inc_tree.configure(yscrollcommand=self.inc_scrollbar.set)
        self.inc_scrollbar.pack(side="right", fill="y")

        self.inc_tree.pack(pady=5)

    def update_received_data(self, data):
        if data["type"] == "TK":
            for sensor, value in data["sensors"].items():
                value_parts = value.split("; ")
                sensor_value = value_parts[0]
                delta_full = value_parts[1] if len(value_parts) > 1 else ""
                delta = delta_full.split(", ")[0].replace("Depth delta=", "") if delta_full else ""
                full = delta_full.split(", ")[1].replace("full=", "") if delta_full else ""

                # Добавляем данные в таблицу без удаления старых
                self.tk_tree.insert("", "end", values=(sensor, sensor_value, delta, full))

        elif data["type"] == "INC":
            # Добавляем данные в таблицу без удаления старых
            self.inc_tree.insert("", "end", values=(data["x"], data["y"], data["z"]))
