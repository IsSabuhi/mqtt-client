import json
from datetime import datetime
from db import Session, Sensor, Inclinometer, Device, Measurement
from datetime import datetime
import pytz

session = Session()

def convert_timestamp_to_datetime(ts, tz='UTC'):
    timestamp = ts
    timezone = pytz.timezone(tz)
    dt_object = datetime.fromtimestamp(timestamp, tz=timezone)
    return f"{dt_object.date()} {dt_object.time()}"


def parse_and_save_data(session, topic, payload, qos):
    data = json.loads(payload)
    # print(f"Received data: {data}")  

    parts = topic.split('/')
    device_serial = parts[2]
    
    try:
        device = session.query(Device).filter_by(serial_number=device_serial).first()
        print(f"Device found: {device}")

        if not device:
            print(f"Device with serial number {device_serial} not found. Inserting...")
            device = Device(serial_number=device_serial)
            session.add(device)
            session.flush() 
            session.commit()

        # print(f"Device after insert: {device}")

        update_data = {
            'firmware_version': data.get('FirmwareVersion'),
            'ubat1': data.get('Ubat1'),
            'ubat2': data.get('Ubat2'),
            'rssi': data.get('RSSI'),
            'snr': data.get('SNR'),
            'logger_temp': data.get('LoggerTemp'),
            'cpu_temp': data.get('CpuTemp')
        }

        for key, value in update_data.items():
            if value is not None:
                setattr(device, key, value)

        session.commit()

        if "INC" in topic:
            time = convert_timestamp_to_datetime(data['Time'])
            inclinometer = Inclinometer(
                time=time,
                x=data['X'],
                y=data['Y'],
                z=data['Z'],
                device_id=device.serial_number 
            )
            session.add(inclinometer)
            session.commit()

        else: 
            time = convert_timestamp_to_datetime(data['Time'])
            quantity = data.get('Quantity')
            
            measurement = Measurement(
                time=time,
                quantity=quantity,
                device_id=device.serial_number 
            )

            for key in [k for k in data.keys() if k.startswith('Sensor')]:
                if key in data:
                    sensor_value, _, depth_info = data[key].partition('; ')
                    depth_delta, _, full_depth = depth_info.partition(', ')
                    sensor = Sensor(
                        sensor_name=key,
                        value=float(sensor_value),
                        depth_delta=depth_delta.split('=')[1] if depth_delta else None,
                        full_depth=full_depth.split('=')[1] if full_depth else None,
                        measurement=measurement
                    )
                    measurement.sensors.append(sensor)
            
            session.add(measurement)
            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")

    print(f"{datetime.now()} Received message {payload} on topic '{topic}' with QoS {qos}")
    

def handle_message_topic(topic, payload, qos):
    try:
        data = json.loads(payload)
        if "RusGeo/TK" in topic:  
            return {
                "type": "TK",
                "time": data.get("Time"),
                "sensors": {f"Sensor{i}": data.get(f"Sensor{i}") for i in range(1, 23)}
            }
        elif "RusGeo/INC" in topic: 
            return {
                "type": "INC",
                "time": data.get("Time"),
                "x": data.get("X"),
                "y": data.get("Y"),
                "z": data.get("Z")
            }
        elif "RusGeo/STATUS" in topic: 
            return handle_status_data(data, topic)
        else:
            print(f"Неизвестный топик: {topic}")
            return None

    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
    return None



def handle_status_data(data, topic):
    device_type = topic.split("/")[1]  
    return {
        "type": "STATUS",
        "device_type": device_type,
        "serial_number": data.get("SerialNumber"),
        "firmware_version": data.get("FirmwareVersion"),
        "ubat1": data.get("Ubat1"),
        "ubat2": data.get("Ubat2"),
        "rssi": data.get("RSSI"),
        "snr": data.get("SNR"),
        "logger_temp": data.get("LoggerTemp")
    }
    