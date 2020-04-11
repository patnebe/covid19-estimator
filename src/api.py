import os
import sys
import time
from flask import Flask, request, jsonify, abort, Response, g
from marshmallow import Schema, fields, ValidationError
from src.estimator import estimator as impact_estimator
from dicttoxml import dicttoxml
from src.models import setup_db, db, Log_entry


class region_schema(Schema):
    """
    Schema to validate the region object within the input data below
    """
    name = fields.String()
    avgAge = fields.Float()
    avgDailyIncomeInUSD = fields.Float()
    avgDailyIncomePopulation = fields.Float()


class estimation_data_schema(Schema):
    """
    A marshmallow schema which validates the input data for the estimation algorithm
    """
    region = fields.Nested(region_schema)
    periodType = fields.String()
    timeToElapse = fields.Int()
    reportedCases = fields.Int()
    population = fields.Int()
    totalHospitalBeds = fields.Int()


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        status_code = response.status.split()[0]

        latency_ms = int((time.time() - g.start) * 1000)

        new_log_entry = Log_entry(request_method=request.method,
                                  path=request.path, status_code=status_code, latency_ms=latency_ms)

        new_log_entry.insert()

        return response

    @app.route('/')
    @app.route('/index')
    def homepage():
        """
        Homepage.
        """
        response_object = {
            "message": "Welcome to the covid-19 impact estimator API"
        }

        return jsonify(response_object)

    @app.route('/api/v1/on-covid-19/', methods=['POST'])
    @app.route('/api/v1/on-covid-19/<data_format>', methods=['POST'])
    def compute_estimates(data_format=None):
        """
        Returns the covid-19 impact estimate based on the input data provided.
        """

        if data_format not in ['xml', 'json', None]:
            abort(404)

        try:
            request_payload = request.get_json()

            payload_is_valid = estimation_data_schema().load(request_payload)

            response_data = impact_estimator(request_payload)

            if data_format == 'xml':
                # create an xml version of the json data
                xml_data = dicttoxml(response_data)

                return Response(xml_data, mimetype='text/xml')

            elif data_format == 'json':
                return jsonify(response_data)

            return jsonify(response_data)

        except ValidationError:
            abort(400)

        except:
            print(sys.exc_info())
            abort(500)

    @app.route('/api/v1/on-covid-19/logs')
    def get_logs():
        try:
            request_response_logs = Log_entry.query.all()

            log_data = [entry.serialize() for entry in request_response_logs]

            formatted_log_data = ""

            for item in log_data:
                formatted_log_data += item

            return Response(formatted_log_data, mimetype='text/plain')

        except:
            print(sys.exc_info())
            abort(500)

        finally:
            db.session.close()

    @app.errorhandler(400)
    def bad_request(error, message="Bad request"):
        return jsonify({
            "success": False,
            "error": 400,
            "message": message
        }), 400

    @app.errorhandler(404)
    def not_found(error, message="Not found"):
        return jsonify({
            "success": False,
            "error": 404,
            "message": message
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def not_found(error, message="Something went wrong on the server, and we are looking into it. Sorry for the inconvenience."):
        return jsonify({
            "success": False,
            "error": 500,
            "message": message
        }), 500

    return app
