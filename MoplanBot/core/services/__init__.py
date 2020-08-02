"""
Package of data services
"""

import requests
from config import Config

API_BASE = Config.APP_URL + '/api/'


def make_post_request(entity: str, method: str, payload: dict):
    """
    Make POST request to the API
    :param entity: Entity of the system
    :param method: Method for the entity
    :param payload: Data for POST request
    :return: Response from the API
    """
    api_url = API_BASE + entity + '/' + method
    return requests.post(api_url, json=payload)


def make_get_request(entity: str, method: str, payload: dict = None):
    """
    Make GET request to the API
    :param entity: Entity of the system
    :param method: Method for the entity
    :param payload: Params for query
    :return: Response from the API
    """
    api_url = API_BASE + entity + '/' + method
    return requests.get(api_url, params=payload)


def make_put_request(entity: str, method: str, payload: dict):
    """
    Make PUT request to the API
    :param entity: Entity of the system
    :param method: Method for the entity
    :param payload: Data to PUT in the API
    :return: Response from the API
    """
    api_url = API_BASE + entity + '/' + method
    return requests.put(api_url, data=payload)


def make_delete_request(entity: str, method: str):
    """
    Make DELETE request to the API
    :param entity: Entity of the system
    :param method: Method for the entity
    :return: Response from the API
    """
    api_url = API_BASE + entity + '/' + method
    return requests.delete(api_url)
