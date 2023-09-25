#!/usr/bin/env python3
"""Session Authentication module"""

from os import getenv
import redis
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')


class SessionAuth():
    """Handles Session Authentication"""

    def __init__(self):
        """Initializes a new redis client"""
        self._client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def createSession(self, request=None):
        """Creates and stores a new session token"""

if __name__ == '__main__':
    session = SessionAuth()
    session.createSession()
