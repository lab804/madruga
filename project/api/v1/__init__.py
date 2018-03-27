from flask_classful import FlaskView


class V1FlaskView(FlaskView):
    route_prefix = '/v1/'
    trailing_slash = False
