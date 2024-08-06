#!/usr/bin/python3
"""
cities endpoint
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route("/cities", methods=['GET'], strict_slashes=False)
def get_cities():
    """get all cities endpoint"""
    data = []
    objs = storage.all(City)
    for key, value in objs.items():
        data.append(value.to_dict())
    return jsonify(data)


@app_views.route(
    "/states/<state_id>/cities",
    methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """get all cities in a specific state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = [city.to_dict() for city in state.cities]
    return jsonify(data)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get specific city by city id endpoint"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete specific city by city id endpoint"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/<state_id>/cities",
    methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """add new city to a specific state endpoint"""
    if request.content_type == "application/json":
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update city object"""
    if request.content_type == "application/json":
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
