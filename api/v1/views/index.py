#!/usr/bin/python3
"""
creating view from app_views bluprint
that just return json msg with key status
and value OK
"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage

classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"}


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    return json msg with key status
    and value OK
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """return number of all obbjects of all types"""
    dic = {}
    for key, value in classes.items():
        dic[key] = storage.count(value)
    if dic:
        return jsonify(dic)
    else:
        abort(404)
