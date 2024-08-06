#!/usr/bin/python3
"""amenities endpoint"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """Get all amenities endpoint"""
    objs = storage.all(Amenity)
    data = [obj.to_dict() for obj in objs.values()]
    return jsonify(data)


@app_views.route(
    "/amenities/<amenity_id>",
    methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get specific amenity by amenity id endpoint"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete specific amenity by amenity id endpoint"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/amenities", methods=['POST'],
    strict_slashes=False)
def create_amenity():
    """Add new amenity endpoint"""
    if request.content_type == "application/json":
        data = request.get_json()
    elif request.content_type == "application/x-www-form-urlencoded":
        data = request.form
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = Amenity(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
