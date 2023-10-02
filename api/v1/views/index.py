#!/usr/bin/env python3
"""Index views"""

from api.v1.views import app_views
from flask import jsonify
from flasgger import swag_from


@app_views.route('/status')
def getStatus():
    """
    Returns the status of the server
    responses:
      200:
        description: All systems green!
    """
    return jsonify({
        "status": "success",
        "message": "All systems green!"
    })
