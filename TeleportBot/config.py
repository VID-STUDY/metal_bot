from dotenv import load_dotenv
import os

load_dotenv('.env')


class Config:
    API_TOKEN = os.getenv('API_TOKEN')
    APP_URL = os.getenv('APP_URL')
    ENVIRONMENT = os.getenv('ENVIRONMENT')
    TELEGRAM_CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL_USERNAME')
    TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK')
    TELEGRAM_SUPPORT_GROUP = os.getenv('TELEGRAM_SUPPORT_GROUP')

    TELEGRAM_PAYME_TOKEN = os.getenv('TELEGRAM_PAYME_TOKEN')
    TELEGRAM_CLICK_TOKEN = os.getenv('TELEGRAM_CLICK_TOKEN')
    TELEGRAM_YANDEX_TOKEN = os.getenv('TELEGRAM_YANDEX_TOKEN')
