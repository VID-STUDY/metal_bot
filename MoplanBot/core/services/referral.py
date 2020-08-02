"""
Service for referral tenders
"""

from . import make_get_request

ENTITY = 'referral'


def get_current_referral_tender():
    response = make_get_request(ENTITY, 'current').json()
    return response


def get_invited_users(user_id, tender_id):
    payload = {'user_id': user_id, 'referral_tender_id': tender_id}
    response = make_get_request(ENTITY, 'invited', payload).json()
    return response


def get_referral_tender_by_id(referral_tender_id):
    response = make_get_request(ENTITY, str(referral_tender_id)).json()
    return response


def get_top_referrals(referral_tender_id):
    response = make_get_request(ENTITY, str(referral_tender_id) + '/top').json()
    return response


def get_latest_tender():
    response = make_get_request(ENTITY, 'latest').json()
    return response
