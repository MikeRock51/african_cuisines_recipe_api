#!/usr/bin/env python3
"""Index views"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def getStatus():
    """Returns the status of the server"""
    return jsonify({
        "status": "success",
        "message": "All systems green!!!"
    })
