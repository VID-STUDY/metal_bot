"""
Resumes API service
"""

from . import make_post_request

ENTITY = 'resumes'


def create_resume(data: dict):
    payload = {'title': data['title'], 'description': data['description'], 'contacts': data['contacts'],
               'location': data['location']['full_name'], 'user_id': data['user_id'],
               'categories': [category['id'] for category in data['categories']]}
    response = make_post_request(ENTITY, '', payload).json()
    return response
