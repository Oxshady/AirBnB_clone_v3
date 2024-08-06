#!/usr/bin/python3
"""
state endpoint
"""
from api.v1.views import app_views
from flask import request, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """get all states endpoint"""
    data = []
    objs = storage.all(State)
    for key, value in objs.items():
        data.append(objs[key].to_dict())
    if data:
        return jsonify(data)
    else:
        return []


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """git specific state by state id endpoint"""
    try:
        obj = storage.get(State, state_id)
    except KeyError:
        abort(404)
    if obj is not None:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_state(state_id):
    """delete specific state by state id endpoint"""
    try:
        obj = storage.get(State, state_id)
    except KeyError:
        abort(404)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def new_state():
    """add new state endpoint"""
    if request.content_type == "application/json":
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')
    if data is None:
        abort(400, 'Not a JSON')
    if data.get('name') is None:
        abort(400, 'Missing name')
    obj = State(**data)
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict())), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update state object"""
    if request.content_type == "application/json":
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')
    try:
        state = storage.get(State, state_id)
    except KeyError:
        abort(404)
    if state is None:
        abort(404)
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
