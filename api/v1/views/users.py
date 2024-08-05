#!/usr/bin/python3
"""users endpoint that do crud operation"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Get all users endpoint"""
    objs = storage.all(User)
    data = [obj.to_dict() for obj in objs.values()]
    return jsonify(data)


@app_views.route(
    "/users/<user_id>",
    methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get specific user by user id endpoint"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete specific user by user id endpoint"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/users", methods=['POST'],
    strict_slashes=False)
def create_user():
    """Add new user endpoint"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = User(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update user object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
