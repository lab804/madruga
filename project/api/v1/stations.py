from sqlalchemy import exc
from flask import jsonify, request
from flask_classful import route

from project.api.v1 import V1FlaskView
from project.api.schematics import add_station_schema, station_schema
from project.extensions import db
from project.api.models import Station


class StationsView(V1FlaskView):

    def index(self):
        response_obj = {
                'status': 'fail',
                'message': 'latitude and longitude does not exist.'
        }

        latitude = request.args.get('lat', default=None, type=float)
        longitude = request.args.get('lng', default=None, type=float)

        if latitude is None or longitude is None:
            return jsonify(response_obj), 400

        station = Station.location(latitude, longitude)

        if station is None:
            response_obj['message'] = 'station does not exist.'
            return jsonify(response_obj), 404

        response_obj = {
             'status': 'success',
             'data': station_schema.dump(station).data,
        }

        return jsonify(response_obj), 200

    @route('ping')
    def ping(self):
        return jsonify({
            'status': 'success',
            'message': 'pong!'
        })

    def post(self):
        response_obj = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        json_data = request.get_json()

        if not json_data:
            return jsonify(response_obj), 400

        data, errors = add_station_schema.load(json_data)

        if errors:
            response_obj['errors'] = errors
            return jsonify(response_obj), 422

        try:
            db.session.add(Station(
                name=data['name'], latitude=data['latitude'],
                longitude=data['longitude']))
            db.session.commit()
            response_obj['status'] = 'success'
            response_obj['message'] = f'{data["name"]} was added!'
            return jsonify(response_obj), 201
        except (exc.IntegrityError, ValueError) as e:
            db.session.rollback()
            return jsonify(response_obj), 400
