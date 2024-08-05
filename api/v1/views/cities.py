#!/usr/bin/python3
"""
cities endpoint
"""
from api.v1.views import app_views
from flask import request, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/cities", methods=['GET'], strict_slashes=False)
def get_states():
    """get all states endpoint"""
    data = []
    objs = storage.all(City)
    for key, value in objs.items():
        data.append(objs[key].to_dict())
    if data:
        return jsonify(data)
    else:
        abort(404)


@app_views.route(
    "/states/<state_id>/cities",
    methods=['GET'], strict_slashes=False
    )
def get_city_by_states(state_id):
    """get all cities in states"""
    data = []
    try:
        objs = storage.get(State, state_id)
    except KeyError:
        abort(404)
    if objs is None:
        abort(404)
    for city in objs.cities:
        data.append(city.to_dict)
    if data:
        return jsonify(data)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_state(city_id):
    """git specific city by city id endpoint"""
    try:
        obj = storage.get(City, city_id)
    except KeyError:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_state(city_id):
    """delete specific city by city id endpoint"""
    try:
        obj = storage.get(City, city_id)
    except KeyError:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities", methods=['POST'], strict_slashes=False)
def new_state():
    """add new city endpoint"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if data.get('name') is None:
        abort(400, 'Missing name')
    obj = City(**data)
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict())), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state(city_id):
    """update city object"""
    try:
        state = storage.get(City, city_id)
    except KeyError:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            state.key = value
    storage.save()
    return jsonify(state.to_dict()), 200
