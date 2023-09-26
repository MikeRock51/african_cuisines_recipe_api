#!/usr/bin/env python3
"""Contains app utility functions"""

from typing import Dict, List

class Utilities:
    """Utility class"""
    def getReqJSON(request, requiredFields: List = None) -> Dict:
        """Extracts JSON data from request"""
        if request:
            data = request.get_json()
            if not data:
                abort(400)

            if requiredFields:
                for field in requiredFields:
                    if field not in data:
                        raise ValueError(f'Missing required {field}')

            return data
