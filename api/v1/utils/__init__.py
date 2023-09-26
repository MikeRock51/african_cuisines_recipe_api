#!/usr/bin/env python3
"""Handles error parsing/extraction"""

def extractErrorMessage(error_message: str):
    """Extracts the useful part of error message"""
    start_index = error_message.find('"')
    end_index = error_message.rfind('"')
    if start_index != -1 and end_index != -1:
        extracted_message = error_message[start_index + 1:end_index]
        return extracted_message
    else:
        return error_message
