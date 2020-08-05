"""
Resumes API service
"""

from . import make_post_request, make_get_request, make_put_request, make_delete_request

ENTITY = 'resumes'


def create_resume(data: dict) -> dict:
    payload = {'title': data['title'], 'price': data['price'], 'name': data['name'], 'contacts': data['contacts'],
               'location': data['location']['code'], 'user_id': data['user_id'],
               'categories': [category['id'] for category in data['categories']]}
    response = make_post_request(ENTITY, '', payload).json()
    return response


def get_resume(resume_id) -> dict:
    response = make_get_request(ENTITY, str(resume_id)).json()
    return response


def update_resume(resume_id, data: dict) -> dict:
    response = make_put_request(ENTITY, str(resume_id), data).json()
    return response


def delete_resume(resume_id):
    make_delete_request(ENTITY, str(resume_id))


def get_vacations_for_resume(resume_id):
    response = make_get_request(ENTITY, str(resume_id) + '/vacations').json()
    return response
