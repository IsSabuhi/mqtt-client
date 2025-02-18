import tkinter as tk
from tkinter import ttk
from db import Device, Measurement, Sensor, Inclinometer, Session

class DB_TAB:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        label = tk.Label(self.frame, text="Данные с БД")
        label.pack(pady=5)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(pady=5, expand=True, fill='both')

        self.sensor_tab = tk.Frame(self.notebook)
        self.notebook.add(self.sensor_tab, text="Sensors")

        self.device_tab = tk.Frame(self.notebook)
        self.notebook.add(self.device_tab, text="Devices")

        self.measurement_tab = tk.Frame(self.notebook)
        self.notebook.add(self.measurement_tab, text="Measurements")

        self.inclinometer_tab = tk.Frame(self.notebook)
        self.notebook.add(self.inclinometer_tab, text="Inclinometers")

        self.sensor_tree = self.create_table(self.sensor_tab, ["Sensor ID", "Measurement ID", "Sensor Name", "Value", "Depth_delta", "Full_depth"])
        self.device_tree = self.create_table(self.device_tab, ["Device ID", "Serial Number", "Firmware Version", "RSSI", "SNR", "Ubat1", "Ubat2"])
        self.measurement_tree = self.create_table(self.measurement_tab, ["Measurement ID", "Device ID", "Time", "Quantity"])
        self.inclinometer_tree = self.create_table(self.inclinometer_tab, ["Inclinometer ID", "Device ID", "Time", "X", "Y", "Z"])

        self.refresh_button = tk.Button(self.frame, text="Обновить", command=self.refresh_data)
        self.refresh_button.pack(pady=5)

        self.refresh_data()
        
    def create_table(self, parent_frame, columns):
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col, anchor='s')
            tree.column(col, width=100, anchor='center')

        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(expand=True, fill='both')

        return tree 
    
    def refresh_data(self):
        self.update_table(self.sensor_tree, self.get_sensors_data())
        self.update_table(self.device_tree, self.get_devices_data())
        self.update_table(self.measurement_tree, self.get_measurements_data())
        self.update_table(self.inclinometer_tree, self.get_inclinometers_data())

    def update_table(self, tree, data):
        tree.delete(*tree.get_children())
        for row in data:
            tree.insert("", "end", values=row)

    def get_sensors_data(self):
        session = Session()
        sensors = session.query(Sensor).all()
        session.close()
        return [(sensor.id, sensor.measurement_id, sensor.sensor_name, sensor.value, sensor.depth_delta, sensor.full_depth) for sensor in sensors]

    def get_devices_data(self):
        session = Session()
        devices = session.query(Device).all()
        session.close()
        return [(device.id, device.serial_number, device.firmware_version, device.rssi, device.snr, device.ubat1, device.ubat2) for device in devices]

    def get_measurements_data(self):
        session = Session()
        measurements = session.query(Measurement).all()
        session.close()
        return [(measurement.id, measurement.device_id, measurement.time, measurement.quantity) for measurement in measurements]

    def get_inclinometers_data(self):
        session = Session()
        inclinometers = session.query(Inclinometer).all()
        session.close()
        return [(inclinometer.id, inclinometer.device_id, inclinometer.time, inclinometer.x, inclinometer.y, inclinometer.z) for inclinometer in inclinometers]


    