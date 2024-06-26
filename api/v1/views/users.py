#!/usr/bin/python3
"""API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve the list of users"""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new user"""
    request_body = request.get_json(silent=True)
    if not request_body:
        abort(400, "Bad request")
    if "email" not in request_body:
        abort(400, "Missing email")
    if "password" not in request_body:
        abort(400, "Missing password")
    user = User(**request_body)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    request_body = request.get_json(silent=True)
    if not request_body:
        abort(400, "Bad request")
    for key, value in request_body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Delete a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
