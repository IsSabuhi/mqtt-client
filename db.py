from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine(
        f'postgresql://ism:1qaz2WSX@172.24.230.241:5432/smsiz_test_db',
        pool_size=20,
        max_overflow=10,
        pool_recycle=3600
    )

# Модель для таблицы устройств
class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String, unique=True, nullable=False)  
    firmware_version = Column(String) 
    ubat1 = Column(Float)  
    ubat2 = Column(Float) 
    rssi = Column(Float) 
    snr = Column(Float) 
    logger_temp = Column(Float)  
    
    measurements = relationship("Measurement", back_populates="device")
    inclinometers = relationship("Inclinometer", back_populates="device")

class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False) 
    time = Column(DateTime)  
    quantity = Column(Integer)  
    
    device = relationship("Device", back_populates="measurements")
    sensors = relationship("Sensor", back_populates="measurement")

class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    measurement_id = Column(Integer, ForeignKey('measurements.id'), nullable=False)
    sensor_name = Column(String)  
    value = Column(Float) 
    depth_delta = Column(String) 
    full_depth = Column(String)  
    
    measurement = relationship("Measurement", back_populates="sensors")

class Inclinometer(Base):
    __tablename__ = 'inclinometers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    time = Column(DateTime)
    x = Column(Float)
    y = Column(Float)  
    z = Column(Float)  
    
    device = relationship("Device", back_populates="inclinometers")

    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)