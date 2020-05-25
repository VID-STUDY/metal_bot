from dotenv import load_dotenv
import os

load_dotenv('.env')


class Config:
    API_TOKEN = os.getenv('API_TOKEN')
