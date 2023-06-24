from flask import session
import spotipy


def get_spotify_username():
    sp = spotipy.Spotify(session["token"])
    return sp.current_user()["display_name"]
