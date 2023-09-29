#!/usr/bin/env python3
"""Contains app utility functions"""

from typing import Dict, List

class Utils:
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

    def extractErrorMessage(error_message: str):
        """Extracts the useful part of error message"""
        start_index = error_message.find('"')
        end_index = error_message.rfind('"')
        if start_index != -1 and end_index != -1:
            extracted_message = error_message[start_index + 1:end_index]
            return extracted_message
        else:
            return error_message

