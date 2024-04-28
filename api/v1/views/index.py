#!/usr/bin/python3
"""API"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Status function"""
    return jsonify({"status": "OK"})
