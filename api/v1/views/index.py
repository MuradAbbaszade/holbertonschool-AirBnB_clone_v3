#!/usr/bin/python3
"""API"""
from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Status function"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """Stats function"""

    return jsonify(
        {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User),
        }
    )
