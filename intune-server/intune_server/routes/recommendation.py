from flask import Blueprint, request
from ..services.recommendation import recommend

recommendation_blueprint = Blueprint('recommendation_blueprint', __name__)


@recommendation_blueprint.route("/recommend_playlist", methods=['POST'])
def handle_recommend_playlist():
    data = request.get_json()
    return recommend(data)