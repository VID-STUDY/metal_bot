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
