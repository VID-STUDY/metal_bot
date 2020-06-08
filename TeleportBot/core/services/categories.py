"""
Categories API service
"""
from . import make_get_request
from typing import Optional

ENTITY = 'categories'


def get_parent_categories() -> list:
    response = make_get_request(ENTITY, '').json()
    return response


def get_category(category_id) -> dict:
    response = make_get_request(ENTITY, str(category_id)).json()
    return response


def get_siblings(category_id) -> list:
    response = make_get_request(ENTITY, str(category_id) + '/siblings').json()
    return response
