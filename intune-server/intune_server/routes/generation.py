from flask import Blueprint, request, make_response, send_file, Response
from ..services.generation import execute_generate_job, get_all_jobs
from bson import json_util
import json


generation_blueprint = Blueprint('generation_blueprint', __name__)


@generation_blueprint.route("/generate_song", methods=['POST'])
def handle_generate_song():
    data = request.get_json()
    output, error = execute_generate_job(sample_length_in_seconds=data["sampleLength"],
                                         meta_list=data["metas"],
                                         levels=data["levels"])
    resp = json.dumps({
        "output": output,
        "error": error
    })
    print(resp)
    return resp


# document = dict(
#     spotify_username=get_spotify_username(),
#     mode=mode,
#     metas=metas_json,
#     sample_length_in_seconds=sample_length_in_seconds,
#     track=track,
#     slurm_job_id=""
# )


@generation_blueprint.route("/jobs", methods=["GET"])
def handle_jobs():
    return json.dumps({"jobs": get_all_jobs()}, default=json_util.default)


@generation_blueprint.route("/songs/<wav_path>")
def handle_song(wav_path):
    return send_file(
        f"static/{wav_path}",
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename=wav_path)
# @generation_blueprint.route("/songs/<wav_path>")
# def handle_song(wav_path):
#     def generate():
#         with open("static/CantinaBand60.wav", "rb") as fwav:
#             data = fwav.read(1024)
#             while data:
#                 yield data
#                 data = fwav.read(1024)
#
#     return Response(generate(), mimetype="audio/x-wav")
