#!/usr/bin/python3
"""API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieve the list of amenities"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    request_body = request.get_json(silent=True)
    if not request_body or "name" not in request_body:
        abort(400, "Bad request")
    amenity = Amenity(**request_body)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["GET"],
    strict_slashes=False
)
def get_single_amenity(amenity_id):
    """Retrieve a single amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_amenity(amenity_id):
    """Update an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    request_body = request.get_json(silent=True)
    if not request_body:
        abort(400, "Bad request")
    for key, value in request_body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_amenity(amenity_id):
    """Delete an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
