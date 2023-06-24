from flask import (
    Blueprint,
    make_response,
    redirect,
    request,
    session
)

import os
import time
import json
import logging

logger = logging.getLogger('app')
logger.setLevel(logging.NOTSET)

from ..services.authorization import get_auth_token, check_token_status

authorization_blueprint = Blueprint('authorization_blueprint', __name__)
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/en/authorize"


@authorization_blueprint.route("/authorize")
def authorize():
    auth_url = (
        SPOTIFY_AUTH_URL
        + "?response_type=code"
        + f"&client_id={os.getenv('CLIENT_ID')}"
        + f"&redirect_uri={os.getenv('REDIRECT_URI')}"
        + f"&scope={os.getenv('SCOPE')}"
    )

    return make_response(redirect(auth_url))


@authorization_blueprint.route("/token_status")
def token_status():
    if session.get("refresh_token") is None:
        logging.error("Refresh token not set in session.")
        return json.dumps(False)

    return json.dumps(check_token_status(session))


@authorization_blueprint.route("/callback")
def callback():
    code = request.args.get("code")
    payload = get_auth_token(code)
    if payload is not None:
        logger.info("Setting access token in session:")
        logger.info(payload[0])
        session['token'] = payload[0]
        session['refresh_token'] = payload[1]
        session['token_expiration'] = time.time() + payload[2]

        # resp = make_response("done")
        # return resp
        return make_response(redirect("http://localhost:3000"))


    logger.error("Did not receive token on callback")
    return "Login failure."

