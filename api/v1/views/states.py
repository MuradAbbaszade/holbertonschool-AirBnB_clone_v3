#!/usr/bin/python3
"""API"""
from models import storage
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route(
    "/states/<state_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_state(state_id):
    """Delete state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_data = request.get_json(silent=True)
    if not state_data:
        abort(400, "Not a JSON")
    for key, value in state_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Get states"""
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create state"""
    state_data = request.get_json(silent=True)
    if not state_data:
        abort(400, "Not a JSON")
    elif "name" not in state_data:
        abort(400, "Missing name")
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route(
    "/states/<state_id>",
    methods=["GET"],
    strict_slashes=False
)
def get_state(state_id):
    """get state by id"""
    if request.method == "GET":
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())
