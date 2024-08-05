"""
creating view from app_views bluprint
that just return json msg with key status
and value OK
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'])
def status():
    """
    return json msg with key status
    and value OK
    """
    return jsonify({"status": "OK"})
