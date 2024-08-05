#!/usr/bin/python3
"""
places endpoint
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.place import Place
from models.city import City


@app_views.route(
    "/cities/<city_id>/places",
    methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """get all places in a specific city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = [place.to_dict() for place in city.places]
    return jsonify(data)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get specific city by city id endpoint"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete specific place by city id endpoint"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places",
    methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """add new place to a specific city endpoint"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_city(place_id):
    """update place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
