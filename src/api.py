import os
import sys
from flask import Flask, request, jsonify, abort
from marshmallow import Schema, fields

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def homepage():
    # do stuff
    pass


@app.route('/api/v1/on-covid-19')
@app.route('/api/v1/on-covid-19/json')
def compute_estimates():
    pass


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
