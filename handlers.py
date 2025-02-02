import json
from datetime import datetime as dt
from db import Session, Measurement, Sensor, InclinometerReading
from datetime import datetime

session = Session()

def write_to_json_file(data, filename='messages.json'):
    # Преобразуем дату в строку
    if isinstance(data["timestamp"], dt):
        data["timestamp"] = data["timestamp"].isoformat()
    
    data_json = json.dumps(data, indent=4)
    with open(filename, 'a') as file:
        file.write(data_json + '\n')
        
        
def parse_and_save_data(session, topic, payload, qos):
    data = json.loads(payload)
    
    device_id = topic.split('/')[2]
    if topic.startswith('RusGeo/TK/'):
        time = datetime.fromtimestamp(data['Time'])
        
        # Получаем количество датчиков, если оно присутствует
        quantity = data.get('Quantity')
        
        # Создаем запись измерения только если есть количество датчиков
        if quantity is not None:
            measurement = Measurement(time=time, quantity=quantity, device=device_id)
            
            for key in [k for k in data.keys() if k.startswith('Sensor')]:
                sensor_value, _, depth_info = data[key].partition('; ')
                depth_delta, _, full_depth = depth_info.partition(', ')
                
                depth_delta = str(depth_delta.split('=')[1])
                full_depth = str(full_depth.split('=')[1])    
                
                sensor = Sensor(sensor_name=key, value=float(sensor_value), depth_delta=depth_delta, full_depth=full_depth)
                measurement.sensors.append(sensor)
            
            session.add(measurement)
            session.commit()
    
    elif topic.startswith('RusGeo/INC/'):
        time = datetime.fromtimestamp(data['Time'])
        
        inclinometer_reading = InclinometerReading(time=time, x=data['X'], y=data['Y'], z=data['Z'], device=device_id)
        
        session.add(inclinometer_reading)
        session.commit()
    
    # print(f"{datetime.now()} Received message {payload} on topic '{topic}' with QoS {qos}")

def handle_message(topic, payload, qos):
    parse_and_save_data(session, topic, payload, qos)
    message_data = {
        "timestamp": dt.now(),
        "topic": topic,
        "qos": qos,
        "message": payload
    }
    # write_to_json_file(message_data, filename=f'{topic.replace("/", "_")}_messages.json')
    print(f"{dt.now()} Received message {payload} on topic '{topic}' with QoS {qos}")