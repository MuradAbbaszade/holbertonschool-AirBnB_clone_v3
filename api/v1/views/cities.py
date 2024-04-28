#!/usr/bin/python3
"""API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET"],
    strict_slashes=False
)
def get_cities_by_state(state_id):
    """Retrieve the list of cities by state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route(
    "/states/<state_id>/cities",
    methods=["POST"],
    strict_slashes=False
)
def create_city(state_id):
    """Create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_body = request.get_json(silent=True)
    if not request_body or "name" not in request_body:
        abort(400, "Bad request")
    city = City(**request_body)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieve a city by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Update a city by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_body = request.get_json(silent=True)
    if not request_body:
        abort(400, "Bad request")
    for key, value in request_body.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Delete a city by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
