import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = int(os.environ.get('DB_PORT'))
    DB_NAME = os.environ.get('DB_NAME')

BROKER = os.environ.get('BROKER')
PORT = int(os.environ.get('PORT', 1883)) 
TOPICS = [
    os.environ.get('TOPIC_1'),
    os.environ.get('TOPIC_2')
]

