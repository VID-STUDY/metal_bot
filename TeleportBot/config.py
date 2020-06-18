from dotenv import load_dotenv
import os

load_dotenv('.env')


class Config:
    API_TOKEN = os.getenv('API_TOKEN')
    APP_URL = os.getenv('APP_URL')
    ENVIRONMENT = os.getenv('ENVIRONMENT')
    TELEGRAM_CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL_USERNAME')
    TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK')
