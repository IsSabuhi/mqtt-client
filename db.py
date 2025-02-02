from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
# Настройка подключения к базе данных
engine = create_engine(f'postgresql://ism:1qaz2WSX@172.24.230.241:5432/smsiz_test_db')
Session = sessionmaker(bind=engine)


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    device = Column(String(30))
    sensors = relationship('Sensor', back_populates='measurement')

class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    sensor_name = Column(String(30), nullable=False)
    value = Column(Float, nullable=False)
    depth_delta = Column(String, nullable=False)
    full_depth = Column(String, nullable=False)
    measurement_id = Column(Integer, ForeignKey('measurements.id'), nullable=False)
    measurement = relationship('Measurement', back_populates='sensors')

class InclinometerReading(Base):
    __tablename__ = 'inclinometer_readings'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    device = Column(String(30))
    
Base.metadata.create_all(engine)