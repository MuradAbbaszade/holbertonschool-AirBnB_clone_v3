#!/usr/bin/python3
"""API"""
from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close storage function"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Not found exception handler"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
