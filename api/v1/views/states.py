#!/usr/bin/python3
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """get all states endpoint"""
    data = []
    objs = storage.all(State)
    for key, value in objs.items():
        data.append(objs[key].to_dict())
    if data:
        return jsonify(data)
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """git specific state by state id endpoint"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)
