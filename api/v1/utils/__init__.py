#!/usr/bin/env python3
"""Contains app utility functions"""

from typing import Dict, List
from models.recipe import Recipe
import re

class Utils:
    """Utility class"""
    @staticmethod
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

    @staticmethod
    def extractErrorMessage(error_message: str) -> str:
        """Extracts the useful part of error message"""
        start_index = error_message.find('"')
        end_index = error_message.rfind('"')
        if start_index != -1 and end_index != -1:
            extracted_message = error_message[start_index + 1:end_index]
            return extracted_message
        else:
            return error_message

    @staticmethod
    def getFilterColumns(filterBy: str) -> Dict:
        """Creates a dict of filter columns"""
        filterColumns = {}

        if not filterBy or type(filterBy) != str:
            raise ValueError('Invalid filters')

        try:
            columns = filterBy.split(':')
            for column in columns:
                key, value = column.split()
                try:
                    filterColumns[getattr(Recipe, key)] = int(value)
                except ValueError:
                    filterColumns[getattr(Recipe, key)] = [" ".join(
                        re.split(r'[_-]', col)) for col in value.split(',')]
        except ValueError:
            raise ValueError('Invalid filters')

        return filterColumns

    def successResponse(data: List, detailed: bool = False) -> Dict:
        """Constructs a JSON response based on data"""
        return {
           "status": "success",
            "message": "Sucessfully fetched recipes" if data['data'] != [] else "No match found",
            "data": [recipe.toDict(detailed=detailed) for recipe in data['data']],
            "page": data['page'],
            "page_size": data['page_size'],
            "total_page_items": data['total_items'],
            "total_pages": data['total_pages']
        }
