"""
Vacations API service
"""

from . import make_get_request, make_post_request, make_put_request, make_delete_request

ENTITY = 'vacations'


def create_vacation(data: dict):
    payload = {
        'title': data['title'], 'salary': data['salary'], 'category': data['category'],
        'description': data['description'], 'contacts': data['contacts'], 'location': data['location']['full_name'],
        'user_id': data['user_id'], 'categories': [category['id'] for category in data['categories']]
    }
    response = make_post_request(ENTITY, '', payload).json()
    return response


def get_vacation(vacation_id):
    response = make_get_request(ENTITY, str(vacation_id)).json()
    return response


def update_vacation(vacation_id, data: dict) -> dict:
    response = make_put_request(ENTITY, str(vacation_id), data).json()
    return response


def delete_vacation(vacation_id):
    make_delete_request(ENTITY, str(vacation_id))
