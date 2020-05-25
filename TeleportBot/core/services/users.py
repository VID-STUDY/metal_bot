"""
Users API service
"""
from . import make_post_request

ENTITY = 'users'


def create_user(telegram_id: int, name: str, username: str, language: str):
    payload = {
        'telegram_id': telegram_id,
        'name': name,
        'username': username,
        'language': language
    }
    return make_post_request(ENTITY, '', payload)
