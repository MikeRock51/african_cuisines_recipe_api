#!/usr/bin/env python3
"""Contains app utility functions"""

from typing import Dict, List
from models.recipe import Recipe
import re
from flask import abort
import json
from json.decoder import JSONDecodeError
import os
from sqlalchemy.sql.sqltypes import JSON


def allowedFile(filename, allowedExt):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowedExt


def getFileExtension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


class Utils:
    """Utility class"""
    # def __init__():
    #     """Constructor"""
    #     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def getReqJSON(request, requiredFields: List = None) -> Dict:
        """Extracts JSON data from request"""
        if request:
            data = request.get_json()
            if not data:
                abort(400, description="Requires JSON object!")

            if requiredFields:
                for field in requiredFields:
                    if field not in data:
                        abort(400, description=f'Missing required {field}')
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
    def getFilterColumnsFromStr(filterBy: str) -> Dict:
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

    @staticmethod
    def getFilterColumns(filterBy: str) -> Dict:
        """Creates a dict of filter columns"""
        filterColumns = {}

        if not filterBy or type(filterBy) != str:
            raise ValueError('Invalid filters')

        try:
            filterBy = json.loads(filterBy)
            for key, value in filterBy.items():
                filterColumns[getattr(Recipe, key)] = value
                print(type(getattr(Recipe, key).type))
                if isinstance(getattr(Recipe, key).type, JSON):
                    print(f'{key} is a list')
        except AttributeError as e:
            raise ValueError(str(e))
        except (ValueError, JSONDecodeError):
            raise ValueError('Invalid filters')
        

        return filterColumns

    def successResponse(data: List, detailed: bool = False, objName='') -> Dict:
        """Constructs a JSON response based on data"""
        return {
            "status": "success",
            "message": f"Successfully fetched {objName}" if data['data'] != [] else "No match found",
            "page": data['page'],
            "page_size": data['page_size'],
            "total_page_items": data['total_items'],
            "total_pages": data['total_pages'],
            "data": [recipe.toDict(detailed=detailed) for recipe in data['data']]
        }

    def uploadFile(request, uploadFolder, ALLOWED_EXTENSIONS):
        """Extracts file from the request object and uploads it to the given upload folder"""
        from werkzeug.utils import secure_filename

        file = request.files['file']
        if file.filename == '':
            abort(400, description="No file selected")
        if file and not allowedFile(file.filename, ALLOWED_EXTENSIONS):
            abort(
                400, description=f"Invalid file format! Supported Formats: {(', ').join(ALLOWED_EXTENSIONS)}")
        if not os.path.exists(uploadFolder):
            os.makedirs(uploadFolder)

        filename = secure_filename(file.filename)
        file.save(os.path.join(uploadFolder, filename))

        return filename
    
    def deleteFile(filePath: str) -> None:
        """Deletes the files at filePath if it exists"""
        try:
            os.remove(filePath)
        except FileNotFoundError:
            print("File not found! Moving on...")
            pass


class VError(ValueError):
    """A custom value error"""

    def __init__(self, message, statusCode):
        super().__init__(message)
        self.statusCode = statusCode
