#!/usr/bin/python3
"""
reviews endpoint
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
    "/places/<place_id>/reviews",
    methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """get all reviews in a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = [review.to_dict() for review in place.reviews]
    return jsonify(data)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get specific review by review id endpoint"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<review_id>",
    methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete specific review by review id endpoint"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews",
    methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """add new review to a specific place endpoint"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    check = [
        'id', 'place_id', 'user_id',
        'created_at', 'updated_at', 'state_id']
    for key, value in data.items():
        if key not in check:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
