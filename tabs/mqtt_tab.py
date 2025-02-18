import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import Device, Measurement, Session

class MQTT_TAB:
    def __init__(self, parent, received_data_callback=None):
        self.frame = tk.Frame(parent)
        self.received_data_callback = received_data_callback

        # Таблица для данных с TOPIC_1 (TK)
        self.tk_data_label = ttk.Label(self.frame, text="Данные с TOPIC_1 (TK):")
        self.tk_data_label.pack(pady=5)

        self.tk_tree_frame = tk.Frame(self.frame)
        self.tk_tree_frame.pack(pady=10)

        self.tk_tree = ttk.Treeview(
            self.tk_tree_frame,
            columns=("Name", "Value", "Delta", "Full"),
            show="headings"
        )
        
        self.tk_tree.heading("Name", text="Name")
        self.tk_tree.heading("Value", text="Value")
        self.tk_tree.heading("Delta", text="Delta")
        self.tk_tree.heading("Full", text="Full")
        
        self.tk_tree.column("Name", width=50, anchor='s')
        self.tk_tree.column("Value", width=50, anchor='s')
        self.tk_tree.column("Delta", width=50, anchor='s')
        self.tk_tree.column("Full", width=50, anchor='s')
        
        # Добавим полосу прокрутки
        self.scrollbar = ttk.Scrollbar(self.tk_tree_frame, orient="vertical", command=self.tk_tree.yview)
        self.tk_tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.tk_tree.pack(pady=10)

        # Таблица для данных с TOPIC_2 (INC)
        self.inc_data_label = ttk.Label(self.frame, text="Данные с TOPIC_2 (INC):")
        self.inc_data_label.pack(pady=10)

        self.inc_tree_frame = tk.Frame(self.frame)
        self.inc_tree_frame.pack(pady=10)

        self.inc_tree = ttk.Treeview(
            self.inc_tree_frame,
            columns=("X", "Y", "Z"),
            show="headings"
        )
        
        self.inc_tree.heading("X", text="X", anchor='s')
        self.inc_tree.heading("Y", text="Y", anchor='s')
        self.inc_tree.heading("Z", text="Z", anchor='s')
        
        self.inc_tree.column("X", width=50, anchor='s')
        self.inc_tree.column("Y", width=50, anchor='s')
        self.inc_tree.column("Z", width=50, anchor='s')

        # Добавим полосу прокрутки
        self.inc_scrollbar = ttk.Scrollbar(self.inc_tree_frame, orient="vertical", command=self.inc_tree.yview)
        self.inc_tree.configure(yscrollcommand=self.inc_scrollbar.set)
        self.inc_scrollbar.pack(side="right", fill="y")

        self.inc_tree.pack(pady=5)
        
         # Выпадающий список устройств
        self.device_list = ttk.Combobox(self.frame, state="readonly")
        self.device_list.pack(pady=5)
        self.device_list.bind("<<ComboboxSelected>>", self.plot_device_data)  # При выборе строить график

        # График
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

        self.refresh_device_list()  # Загрузка списка устройств

    def refresh_device_list(self):
        """Обновляет список устройств"""
        session = Session()
        devices = session.query(Device).all()
        session.close()

        device_names = [f"{device.id} - {device.serial_number}" for device in devices]

        self.device_list["values"] = device_names  # Заполняем список
        if device_names:
            self.device_list.current(0)  # Выбираем первый элемент

    def plot_device_data(self, event):
        """Построение графика для выбранного устройства"""
        selected = self.device_list.get()
        if not selected:
            return

        device_id = int(selected.split(" - ")[0])  # Получаем ID устройства
        session = Session()
        measurements = session.query(Measurement).filter_by(device_id=device_id).all()
        session.close()

        if not measurements:
            return

        times = [m.time for m in measurements]  # Временные метки
        values = [m.quantity for m in measurements]  # Значения

        self.ax.clear()
        self.ax.plot(times, values, marker="o", linestyle="-", color="b", label="Измерения")
        self.ax.set_xlabel("Время")
        self.ax.set_ylabel("Значение")
        self.ax.set_title(f"График данных для {selected}")
        self.ax.legend()
        self.canvas.draw()

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