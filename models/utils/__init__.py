#!/usr/bin/env python3
"""Defines Utiliy methods for models"""

from typing import Dict, List


class Utils:
    """Utils class"""
    @staticmethod
    def sortDictKeys(obj: Dict, order: List) -> Dict:
        """Returns obj with keys sorted in the provided order"""
        def customSort(key):
            """Sorts the position of a dict key"""
            if key in order:
                return (order.index(key), key)
            return(len(order), key)

        sortedKeys = sorted(obj.keys(), key=customSort)
        return {key: obj[key] for key in sortedKeys}
