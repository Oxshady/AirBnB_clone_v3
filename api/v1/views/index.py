#!/usr/bin/python3
"""
creating view from app_views bluprint
that just return json msg with key status
and value OK
"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
classes = ["Amenity", "City", "Place", "Review", "State", "User"]


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
    for cls in classes:
        dic[cls.lower()] = storage.count(cls)
    if dic:
        return jsonify(dic)
    else:
        abort(404)
