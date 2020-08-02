"""
Settings API service
"""
from . import make_get_request

ENTITY = 'settings'


def get_settings() -> dict:
    response = make_get_request(ENTITY, '').json()
    return response
