import os
import requests
from requests.auth import HTTPBasicAuth
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BEARER_B64_STRING = HTTPBasicAuth(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

"""
Requests an access token from the Spotify API. Only called if no refresh token for the
current user exists.
Returns: either [access token, refresh token, expiration time] or None if request failed
"""
def get_auth_token(code):
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'code': code,
        'redirect_uri': os.getenv("REDIRECT_URI"),
        'grant_type': 'authorization_code'
    }
    post_response = requests.post(token_url,
                                  auth=BEARER_B64_STRING,
                                  headers=headers,
                                  data=body)
    # 200 code indicates access token was properly granted
    if post_response.status_code == 200:
        json = post_response.json()
        logger.info("Got access token")
        return json['access_token'], json['refresh_token'], json['expires_in']
    else:
        logger.error('getToken:' + str(post_response.status_code))
        return None


"""
Determines whether new access token has to be requested because time has expired on the 
old token. If the access token has expired, the token refresh function is called. 
Returns: None if error occurred or 'Success' string if access token is okay
"""
def check_token_status(session):
    if time.time() > session['token_expiration']:
        payload = get_new_token(session['refresh_token'])
        if payload is None:
            logger.error("Error refreshing token")
            return False
        session['token'] = payload[0]
        session['token_expiration'] = time.time() + payload[1]

    return True


"""Requests an access token from the Spotify API with a refresh token.
Only called if an accesstoken and refresh token were previously acquired.
Returns: either [access token, expiration time] or None if request failed
"""
def get_new_token(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'refresh_token': refresh_token,
            'grant_type': 'refresh_token'}
    post_response = requests.post(token_url,
                                  auth=BEARER_B64_STRING,
                                  headers=headers,
                                  data=body)

    # 200 code indicates access token was properly granted
    if post_response.status_code == 200:
        return post_response.json()['access_token'], post_response.json()['expires_in']
    else:
        logger.error('refreshToken:' + str(post_response.status_code))
        return None
