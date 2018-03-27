from flask import jsonify
from project.api.v1 import V1FlaskView


class StationsView(V1FlaskView):

    def index(self):
        return jsonify({'message': 'ok'})
