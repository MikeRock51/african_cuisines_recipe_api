#!/usr/bin/env python3
"""Session Authentication module"""

from os import getenv
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')


class SessionAuth():
    """Handles Session Authentication"""

    def __init__(self):
        """Initializes a new redis client"""
        self._client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        print(self._client.get('Mike'))


if __name__ == '__main__':
    SessionAuth()
