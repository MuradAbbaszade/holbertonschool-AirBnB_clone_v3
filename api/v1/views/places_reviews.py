#!/usr/bin/python3
"""API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route(
    "/places/<place_id>/reviews",
    methods=["GET"],
    strict_slashes=False,
)
def get_reviews_by_place(place_id):
    """
    Retrieves the list of reviews by place
    """
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404)

    review_list = [review.to_dict() for review in place_obj.reviews]
    return jsonify(review_list)


@app_views.route(
    "/places/<place_id>/reviews",
    methods=["POST"],
    strict_slashes=False,
)
def create_review(place_id):
    """
    Creates a new review for a place
    """
    request_body = request.get_json(silent=True)
    if not request_body:
        abort(400, "Bad request")
    if "text" not in request_body:
        abort(400, "Missing text")
    if "user_id" not in request_body:
        abort(400, "Missing user_id")
    place_obj = storage.get(Place, place_id)
    user_obj = storage.get(User, request_body["user_id"])

    if place_obj is None or user_obj is None:
        abort(404)

    new_review = Review(**request_body)
    new_review.place_id = place_id
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_review(review_id):
    """
    Retrieves a review by its ID
    """
    review_obj = storage.get(Review, review_id)

    if review_obj is None:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route(
    "/reviews/<review_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_review(review_id):
    """
    Deletes a review by its ID
    """
    review_obj = storage.get(Review, review_id)

    if review_obj is None:
        abort(404)

    storage.delete(review_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route(
    "/reviews/<review_id>",
    methods=["PUT"],
    strict_slashes=False,
)
def update_review(review_id):
    """
    Updates a review by its ID
    """
    request_body = request.get_json(silent=True)
    review_obj = storage.get(Review, review_id)

    if review_obj is None:
        abort(404)
    elif not request_body:
        abort(400, "Not a JSON")

    for key, value in request_body.items():
        if key not in [
                "id", "user_id", "place_id", "created_at", "updated_at"
        ]:
            setattr(review_obj, key, value)

    storage.save()

    return jsonify(review_obj.to_dict()), 200
