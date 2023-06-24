import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from .routes import authorization_blueprint, generation_blueprint, recommendation_blueprint, spotify_blueprint
from flask_apscheduler import APScheduler
from intune_server.services.downloader import download_songs


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(authorization_blueprint)
app.register_blueprint(generation_blueprint)
app.register_blueprint(recommendation_blueprint)
app.register_blueprint(spotify_blueprint)

app.config["SCHEDULER_API_ENABLED"] = True
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config["SESSION_COOKIE_SECURE"] = "True"
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True
server_session = Session(app)

# initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


CORS(app, supports_credentials=True)


@scheduler.task('interval', id='do_job_1', seconds=300, misfire_grace_time=300)
def job1():
    download_songs()


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0")
