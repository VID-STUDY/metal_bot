"""
Users API service
"""
from . import make_post_request, make_get_request, make_put_request, referral
from typing import Optional

ENTITY = 'users'


def create_user(telegram_id: int, name: str, username: str, language: str, referral_from_id=None):
    """
    Create new user
    :param referral_from_id:
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
        'language': language,
        'referral_from_id': referral_from_id
    }
    response = make_post_request(ENTITY, '', payload).json()
    return response


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
        data = response.json()
        return data


def set_user_role(telegram_id: int, user_role: str):
    """
    Change or set new user role
    :param telegram_id: Telegram ID
    :param user_role: user role value
    :return: Updated user
    """
    payload = {
        'user_role': user_role
    }
    response = make_put_request(ENTITY, str(telegram_id), payload).json()
    return response


def get_user_resumes(telegram_id):
    """
    Getting user resumes
    :param telegram_id: Telegram ID
    :return: List of resumes
    """
    response = make_get_request(ENTITY, str(telegram_id) + '/resumes').json()
    return response


def get_user_vacations(telegram_id):
    response = make_get_request(ENTITY, str(telegram_id) + '/vacations').json()
    return response
