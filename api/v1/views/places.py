#!/usr/bin/python3
"""API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve the list of places by city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route("/places", methods=["POST"], strict_slashes=False)
def create_place():
    """Create a new place"""
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Bad request")
    if "name" not in request_data:
        abort(400, "Missing name")
    if "user_id" not in request_data or "city_id" not in request_data:
        abort(400, "Missing user_id or city_id")
    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)
    place = Place(**request_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieve a place by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update a place by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Bad request")
    for key, value in request_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Delete a place by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
