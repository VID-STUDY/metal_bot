"""
Users API service
"""
from . import make_post_request, make_get_request
from typing import Optional

ENTITY = 'users'


def create_user(telegram_id: int, name: str, username: str, language: str):
    """
    Create new user
    :param telegram_id: Telegram ID
    :param name: User name
    :param username: Username in Telegram
    :param language: Selected user language
    :return: Response from the API server
    """
    payload = {
        'id': telegram_id,
        'name': name,
        'username': username,
        'language': language
    }
    return make_post_request(ENTITY, '', payload).json()


def user_exists(telegram_id) -> Optional[dict]:
    """
    Check if user already exists
    :param telegram_id: Telegram ID
    :return: Boolean values: True of False
    """
    response = make_get_request(ENTITY, str(telegram_id))
    if response.status_code == 404 or response.status_code == 500:
        return None
    else:
        json = response.json()
        return json
