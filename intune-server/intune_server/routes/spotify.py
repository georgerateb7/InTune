from flask import Blueprint, session, make_response
import spotipy
import json

spotify_blueprint = Blueprint('spotify_blueprint', __name__)


@spotify_blueprint.route("/user_info", methods=['GET'])
def handle_get_user_info():
    sp = spotipy.Spotify(session["token"])
    results = sp.current_user()
    return make_response(results)


@spotify_blueprint.route("/user_data", methods=['GET'])
def handle_get_user_data():
    sp = spotipy.Spotify(session["token"])
    return json.dumps({
        "current_user": sp.current_user(),
        "top_tracks": sp.current_user_top_tracks(limit=100)["items"],
        "top_artists": sp.current_user_top_artists(limit=100)["items"],
    })


@spotify_blueprint.route("/top_tracks", methods=['GET'])
def handle_get_top_tracks():
    sp = spotipy.Spotify(session["token"])
    results = sp.current_user_top_tracks(limit=100)
    return make_response(results)
